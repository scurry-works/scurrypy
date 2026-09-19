import logging

logger = logging.getLogger('scurrypy')

from scurrypy import Client
from scurrypy.bases import Addon
from scurrypy.enums import EventType, InteractionDataType
from scurrypy.core import DiscordError, Snowflake, InvalidCallbackSignature, DataModelTypeError
from scurrypy.api.commands import (
    SlashCommandPart, 
    UserCommandPart, 
    MessageCommandPart, 
    CommandOptionPart
)
from scurrypy.api.interactions import (
    ApplicationCommandDataModel, 
    AutocompleteApplicationCommandDataModel
)

from scurrypy.events import InteractionEvent

from .ctx import CommandContext, ApplicationCommandContext, AutocompleteApplicationCommandContext

from collections.abc import Callable, Awaitable

type AddonHandler = Callable[[CommandContext], Awaitable[None]]

type AddonDecorator = Callable[[AddonHandler], AddonHandler]

def _check_func_params(func: AddonHandler) -> None:
    """Inspect a user-defined function callback for command interactions.

    Args:
        func (AddonHandler): function callback

    Raises:
        (InvalidCallbackSignature): invalid signature
    """
    import inspect

    if not inspect.iscoroutinefunction(func):
        raise InvalidCallbackSignature(f"Command handler '{func.__name__}' must be async.")
    
    params_len = len(inspect.signature(func).parameters)

    if params_len != 1:
        raise InvalidCallbackSignature(f"Command handler '{func.__name__}' must accept exactly one parameter (ctx).")

class CommandsAddon(Addon):
    """Addon that implements automatic registering and decorating command interactions."""

    def __init__(self, client: Client, application_id: Snowflake, sync_commands: bool = True):
        """
        Args:
            client (Client): the bot client object
            sync_commands (bool): whether to sync commands. Defaults to `True`.
        """
        self.bot = client

        self.application_id = application_id

        self.sync_commands = sync_commands

        self._global_commands: list[SlashCommandPart | MessageCommandPart | UserCommandPart] = []
        """List of all Global commands."""

        self._guild_commands: dict[Snowflake, list[SlashCommandPart | MessageCommandPart | UserCommandPart]] = {}
        """Guild commands mapped by guild ID."""

        self.slash_handlers: dict[str, AddonHandler] = {}
        """Mapping of command names to handler."""

        self.message_handlers: dict[str, AddonHandler] = {}
        """Mapping of message command names to handler."""

        self.user_handlers: dict[str, AddonHandler] = {}
        """Mapping of user command names to handler."""

        self.autocomplete_handlers: dict[str, AddonHandler] = {}
        """Mapping of autocomplete keys to handler."""

        client.add_startup_hook(self.on_startup) # wait until start to register commands

    def on_startup(self) -> None:
        """Sets up the addon with the client."""

        self.bot.add_event_listener(EventType.INTERACTION_CREATE, self.dispatch)
        if self.sync_commands:
            self.bot.add_startup_hook(self._register_commands)

    def slash_command(self, 
        name: str, 
        description: str, 
        *, 
        handler: AddonHandler | None = None,
        options: list[CommandOptionPart] | None = None, 
        guild_ids: list[Snowflake] | None = None
    ) -> AddonDecorator | None:
        """Register and route a slash command.

        Args:
            name (str): command name
            description (str): command description
            handler (AddonHandler, optional): callback for the command (if not a decorator)
            options (list[CommandOptionPart], optional): list of command options
            guild_ids (list[Snowflake], optional): list of guild IDs for guild commands or omit for global
        """
        self._queue_command(SlashCommandPart(name, description, options), guild_ids)

        if handler is None:
            def decorator(func: AddonHandler) -> AddonHandler:
                _check_func_params(func)
                self.slash_handlers[name] = func
                logger.info(f"Slash command '/{name}' registered.")
                return func
            return decorator
        
        _check_func_params(handler)
        self.slash_handlers[name] = handler
        logger.info(f"Slash command '/{name}' registered.")
        return None
    
    def user_command(self, 
        name: str, 
        *, 
        handler: AddonHandler | None = None, 
        guild_ids: list[Snowflake] | None = None
    ) -> AddonDecorator | None:
        """Register and route a user command.

        Args:
            name (str): command name
            handler (AddonHandler, optional): callback for the command (if not a decorator)
            guild_ids (list[Snowflake], optional): list of guild IDs for guild commands or omit for global
        """
        self._queue_command(UserCommandPart(name), guild_ids)

        if handler is None:
            def decorator(func: AddonHandler) -> AddonHandler:
                _check_func_params(func)
                self.user_handlers[name] = func
                logger.info(f"User command '{name}' registered.")
                return func
            return decorator
        
        _check_func_params(handler)
        self.user_handlers[name] = handler
        logger.info(f"User command '{name}' registered.")
        return None

    def message_command(self, 
        name: str, 
        *, 
        handler: AddonHandler | None = None, 
        guild_ids: list[Snowflake] | None = None
    ) -> AddonDecorator | None:
        """Register and route a message command.

        Args:
            name (str): command name
            handler (AddonHandler, optional): callback for the command (if not a decorator)
            guild_ids (list[Snowflake], optional): list of guild IDs for guild commands or omit for global
        """
        self._queue_command(MessageCommandPart(name), guild_ids)

        if handler is None:
            def decorator(func: AddonHandler) -> AddonHandler:
                _check_func_params(func)
                self.message_handlers[name] = func
                logger.info(f"Message command '{name}' registered.")
                return func
            return decorator
        
        _check_func_params(handler)
        self.message_handlers[name] = handler
        logger.info(f"Message command '{name}' registered.")
        return None

    def autocomplete(self, 
        command_name: str, 
        option_name: str, 
        *, 
        handler: AddonHandler | None = None
    ) -> AddonDecorator | None:
        """Register and route an autocomplete interaction.

        Args:
            command_name (str): name of command to autocomplete
            option_name (str): name of option to autocomplete
            handler (AddonHandler, optional): callback for the command (if not a decorator)
        """
        key = f"{command_name}:{option_name}"

        if handler is None:
            def decorator(func: AddonHandler) -> AddonHandler:
                _check_func_params(func)
                self.autocomplete_handlers[key] = func
                logger.info(f"Autocomplete '{key}' registered.")
                return func
            return decorator
        
        _check_func_params(handler)
        self.autocomplete_handlers[key] = handler
        logger.info(f"Autocomplete '{key}' registered.")
        return None

    async def _register_commands(self) -> None:
        """Register both guild and global commands to the client."""

        # global registry
        _global_commands = self.bot.global_command(self.application_id)
        global_commands = await _global_commands.fetch_all()

        for g_cmd in global_commands:
            await _global_commands.delete(g_cmd.id)

        for cmd in self._global_commands:
            await _global_commands.create(cmd)

        # guild registry (only guilds in the registry are updated)
        for guild_id, cmds in self._guild_commands.items():
            _guild_commands = self.bot.guild_command(self.application_id, guild_id)
            commands_ = await _guild_commands.fetch_all()

            for delete_cmd in commands_:
                await _guild_commands.delete(delete_cmd.id)

            for create_cmd in cmds:
                await _guild_commands.create(create_cmd)
    
    def _queue_command(self, 
        command: SlashCommandPart | MessageCommandPart | UserCommandPart, 
        guild_ids: list[Snowflake] | None = None
    ) -> None:
        """Queue a decorated command to be registered on startup.

        Args:
            command (SlashCommandPart | MessageCommandPart | UserCommandPart): the command object
            guild_ids (list[Snowflake], optional): list of guild IDs for guild commands or omit for global
        """
        if guild_ids:
            gids = [guild_ids] if not isinstance(guild_ids, list) else guild_ids

            for gid in gids:
                self._guild_commands.setdefault(gid, []).append(command)
        
        else:
            self._global_commands.append(command)

    def clear_commands(self, guild_ids: list[Snowflake] | None = None) -> None:
        """Clear a guild's or global commands (slash, message, and user).

        Args:
            guild_ids (list[Snowflake], optional): list of guild IDs for guild commands or omit for global
        """
        if guild_ids is None:
            self._global_commands.clear()
            logger.info("Global commands have been cleared.")
        else:
            gids = [guild_ids] if isinstance(guild_ids, (Snowflake, int)) else guild_ids
            for gid in gids:
                removed = self._guild_commands.pop(gid, None)
                if removed is None:
                    logger.warning(f"Guild ID {gid} not found; skipping...")
                else:
                    logger.info(f"Guild commands for ID {gid} have been cleared.")

    async def dispatch(self, event: InteractionEvent) -> None:
        """Dispatch a response to an `INTERACTION_CREATE` event.

        Raises:
            (DataModelTypeError): no command context

        Args:
            event (InteractionEvent): interaction event object
        """
        if not isinstance(event.data, (ApplicationCommandDataModel, AutocompleteApplicationCommandDataModel)):
            return # ignore non-command interactions
        
        handler = None
        name = None

        data = event.data
        name = data.name # name is present in CommandDataModel

        ctx: CommandContext

        if isinstance(data, ApplicationCommandDataModel): # command types are NOT structurally identical
            match data.type:
                case InteractionDataType.SLASH_COMMAND: # command data types are structurally identical
                    handler = self.slash_handlers.get(name)
                case InteractionDataType.USER_COMMAND:
                    handler = self.user_handlers.get(name)
                case InteractionDataType.MESSAGE_COMMAND:
                    handler = self.message_handlers.get(name)

            ctx = ApplicationCommandContext(self.bot, event)

        elif isinstance(data, AutocompleteApplicationCommandDataModel):
            # Extract option being autocompleted

            focused = next((opt for opt in data.options or [] if opt.focused), None)

            if not focused:
                logger.error("No focused option found for autocomplete!")
                return

            name = f"{event.data.name}:{focused.name}"
            handler = self.autocomplete_handlers.get(name)

            ctx = AutocompleteApplicationCommandContext(self.bot, event)

        else:
            raise DataModelTypeError("Command context could not be resolved.")
        
        if not handler:
            logger.warning(f"No handler registered for interaction '{name}'")
            return

        try:
            await handler(ctx)
            logger.info(f"Interaction '{name}' Acknowledged.")
        except DiscordError as e:
            logger.error(f"Error in interaction '{name}': {e}")
        except Exception as e:
            logger.exception(f"Unhandled error in interaction '{name}': {e}")
