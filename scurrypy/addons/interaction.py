from .addon import Addon
from ..core.error import DiscordError
from ..client import Client

from ..parts.command import SlashCommand, UserCommand, MessageCommand, CommandOption

from ..events.interaction_events import InteractionEvent
from ..models.interaction import InteractionDataTypes, InteractionTypes

class InteractionAddon(Addon):
    """Addon that implements automatic registering and decorating interactions."""

    def __init__(self, client: Client, sync_commands: bool = True):
        """
        Args:
            client (Client): the bot client object
            sync_commands (bool): whether to sync commands. Defaults to `True`.
        """
        self.bot = client

        self.logger = client.logger

        self.sync_commands = sync_commands

        self._global_commands = []
        """List of all Global commands."""

        self._guild_commands = {}
        """Guild commands mapped by guild ID."""

        self.component_handlers = {}
        """Mapping of component custom IDs to handler."""

        self.slash_handlers = {}
        """Mapping of command names to handler."""

        self.message_handlers = {}
        """Mapping of message command names to handler."""

        self.user_handlers = {}
        """Mapping of user command names to handler."""

        self.autocomplete_handlers = {}
        """Mapping of autocomplete keys to handler."""

        client.addons.add(self)

    def setup(self):
        """Sets up the addon with the client."""

        self.bot.add_event_listener('INTERACTION_CREATE', self.dispatch)
        if self.sync_commands:
            self.bot.add_startup_hook(self.register_commands)

    def _component(self, custom_id: str):
        def decorator(func):
            self.component_handlers[custom_id] = func
        return decorator
    
    # helpers purly for ergonomics
    def button(self, custom_id: str):
        """Decorator to route button interactions.

        Args:
            custom_id (str): custom ID of button
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
        """
        return self._component(custom_id)

    def select(self, custom_id: str):
        """Decorator to route select menu interactions.

        Args:
            custom_id (str): custom ID of select menu
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
        """
        return self._component(custom_id)

    def modal(self, custom_id: str):
        """Decorator to route modal interactions.

        Args:
            custom_id (str): custom ID of modal
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
        """
        return self._component(custom_id)

    def slash_command(self, name: str, description: str, *, options: list[CommandOption] = None, guild_ids: list[int] = None):
        """Register and route a slash command.

        Args:
            name (str): command name
            description (str): command description
            options (list[CommandOption], optional): list of command options
            guild_ids (list[int], optional): list of guild IDs for guild commands or omit for global
        """
        self._queue_command(SlashCommand(name, description, options), guild_ids)

        def decorator(func):
            self.slash_handlers[name] = func
        return decorator
    
    def user_command(self, name: str, *, guild_ids: list[int] = None):
        """Register and route a user command.

        Args:
            name (str): command name
            guild_ids (list[int], optional): list of guild IDs for guild commands or omit for global
        """
        self._queue_command(UserCommand(name), guild_ids)

        def decorator(func):
            self.user_handlers[name] = func
        return decorator

    def message_command(self, name: str, *, guild_ids: list[int] = None):
        """Register and route a message command.

        Args:
            name (str): command name
            guild_ids (list[int], optional): list of guild IDs for guild commands or omit for global
        """
        self._queue_command(MessageCommand(name), guild_ids)

        def decorator(func):
            self.message_handlers[name] = func
        return decorator
    
    def autocomplete(self, command_name: str, option_name: str):
        """Register and route an autocomplete interaction.

        Args:
            command_name (str): name of command to autocomplete
            option_name (str): name of option to autocomplete
        """
        key = f"{command_name}:{option_name}"

        def decorator(func):
            self.autocomplete_handlers[key] = func
        return decorator
    
    async def register_commands(self):
        """Register both guild and global commands to the client."""

        if self._global_commands:
            await self.bot.register_global_commands(self._global_commands)

        for guild_id, cmds in self._guild_commands.items():
            await self.bot.register_guild_commands(cmds, guild_id)

        self.logger.log_info("Commands set!")
    
    def _queue_command(self, command: SlashCommand | MessageCommand | UserCommand, guild_ids: list[int] = None):
        """Queue a decorated command to be registered on startup.

        Args:
            command (SlashCommand | MessageCommand | UserCommand): the command object
            guild_ids (list[int], optional): list of guild IDs for guild commands or omit for global
        """
        if guild_ids:
            gids = [guild_ids] if not isinstance(guild_ids, list) else guild_ids

            for gid in gids:
                self._guild_commands.setdefault(gid, []).append(command)
        
        else:
            self._global_commands.append(command)

    def clear_commands(self, guild_ids: list[int] = None):
        """Clear a guild's or global commands (all types).

        Args:
            guild_ids (list[int], optional): list of guild IDs for guild commands or omit for global
        """
        if guild_ids:
            gids = [guild_ids] if isinstance(guild_ids, int) else guild_ids
            for gid in gids:
                removed = self._guild_commands.pop(gid, None)
                if removed is None:
                    self.logger.log_warn(f"Guild ID {gid} not found; skipping...")
        else:
            self._global_commands.clear()

    def _get_handler(self, name: str):
        """Helper function for fetching a handler by `fnmatch`."""

        import fnmatch
        for k, v in self.component_handlers.items():
            if fnmatch.fnmatch(name, k):
                return v
        return False

    async def dispatch(self, event: InteractionEvent):
        """Dispatch a response to an `INTERACTION_CREATE` event

        Args:
            event (InteractionEvent): interaction event object
        """
        handler = None
        name = None

        match event.type:
            case InteractionTypes.APPLICATION_COMMAND:
                name = event.data.name
                match event.data.type:
                    case InteractionDataTypes.SLASH_COMMAND:
                        handler = self.slash_handlers.get(name)
                    case InteractionDataTypes.USER_COMMAND:
                        handler = self.user_handlers.get(name)
                    case InteractionDataTypes.MESSAGE_COMMAND:
                        handler = self.message_handlers.get(name)

            # BOTH modals and message components have custom IDs!
            case InteractionTypes.MESSAGE_COMPONENT | InteractionTypes.MODAL_SUBMIT:
                name = event.data.custom_id
                handler = self._get_handler(name)

            case InteractionTypes.APPLICATION_COMMAND_AUTOCOMPLETE:
                # Extract option being autocompleted

                focused = next((opt for opt in event.data.options if opt.focused), None)

                if not focused:
                    self.logger.log_error("No focused option found for autocomplete!")
                    return

                name = f"{event.data.name}:{focused.name}"
                handler = self.autocomplete_handlers.get(name)

        if not handler:
            self.logger.log_warn(f"No handler registered for interaction '{name}'")
            return

        try:
            res = self.bot.interaction(event.id, event.token, context=event)
            await handler(self.bot, res)
            self.logger.log_info(f"Interaction '{name}' Acknowledged.")
        except DiscordError as e:
            self.logger.log_error(f"Error in interaction '{name}': {e}")
        except Exception as e:
            self.logger.log_error(f"Unhandled error in interaction '{name}': {e}")
