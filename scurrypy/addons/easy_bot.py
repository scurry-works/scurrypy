from ..client import Client
from ..core.intents import Intents
from ..core.logger import Logger

from ..parts.command import CommandOption

class EasyBot(Client):
    """Prepackaged interaction, prefix, and event convenience for most of your needs!"""

    def __init__(self, *, 
        token: str, 
        application_id: int, 
        intents = Intents.DEFAULT, 
        prefix = None, 
        sync_commands = True, 
        load_bot_emojis = False, 
        debug_mode = False
    ):
        """
        Args:
            token (str): the bot's token
            application_id (int): the bot's user ID
            intents (int, optional): gateway intents. Defaults to `Intents.DEFAULT`.
            prefix (str, optional): prefix if using prefix commands.
            sync_commands (bool, optional): Whether commands should be synced with changes. Defaults to `True`.
            load_bot_emojis (bool, optional): Whether bot emojis should be loaded on startup. Defaults to `True`.
            debug_mode (bool, optional): Whether error trace should be printed. Defaults to `False`.
        """

        # THEN init client
        super().__init__(
            token=token, 
            application_id=application_id, 
            intents=intents,
            logger=Logger(debug_mode=debug_mode)
        )

        # init addons
        from scurrypy.addons.prefix import PrefixAddon
        self.prefixes = PrefixAddon(self, prefix)

        from scurrypy.addons.interaction import InteractionAddon
        self.commands = InteractionAddon(self, sync_commands)

        from scurrypy.addons.events import EventsAddon
        self.bot_events = EventsAddon(self)

        self.emojis = self.bot_emojis()

        self._startup_hooks = []
        self._shutdown_hooks = []

        self.add_startup_hook(self.run_startup_hooks)
        self.add_shutdown_hook(self.run_shutdown_hooks)

        if load_bot_emojis:
            self.add_startup_hook(self.load_emojis)

    async def load_emojis(self):
        """Loads bot emojis on startup if `load_bot_emojis` is toggled."""
        await self.emojis.fetch_all()

    async def get_emoji(self, name: str):
        """Get an emoji from bot emoji cache.

        Args:
            name (str): emoji name

        Returns:
            (str): formatted emoji (if it exists)
        """
        emoji = self.emojis.get_emoji(name)

        return emoji.mention if emoji else None

    async def run_startup_hooks(self):
        """Wrapper for running user defined start hooks."""
        for hook in self._startup_hooks:
            await hook(self)

    async def run_shutdown_hooks(self):
        """Wrapper for running user defined end hooks."""
        for hook in self._shutdown_hooks:
            await hook(self)

    def start_hook(self, func):
        """Decorator to register a startup hook."""
        self._startup_hooks.append(func)
        return func
    
    def end_hook(self, func):
        """Decorator to register a shutdown hook."""
        self._shutdown_hooks.append(func)
        return func

    def prefix(self, name: str):
        """Register a prefix command using PrefixAddon.

        Args:
            name (str): name of the command
                !!! warning "Important"
                    Prefix commands are CASE-INSENSITIVE.
        """
        return self.prefixes.register(name)
    
    def event(self, event_name: str):
        """Register an event in which to listen using EventsAddon.

        Args:
            event_name (str): event name
        """
        return self.bot_events.event(event_name.upper())
    
    def slash_command(self, name: str, description: str, *, options: list[CommandOption] = None, guild_ids: list[int] = None):
        """Register and route a slash command using InteractionAddon.

        Args:
            name (str): command name
            description (str): command description
            options (list[CommandOption], optional): list of command options
            guild_ids (list[int], optional): list of guild IDs for guild commands or omit for global
        """
        return self.commands.slash_command(name, description, options=options, guild_ids=guild_ids)
    
    def user_command(self, name: str, guild_ids: list[int] = None):
        """Register and route a user command using InteractionAddon.

        Args:
            name (str): command name
            guild_ids (list[int], optional): list of guild IDs for guild commands or omit for global
        """
        return self.commands.user_command(name, guild_ids=guild_ids)
    
    def message_command(self, name: str, guild_ids: list[int] = None):
        """Register and route a message command using InteractionAddon.

        Args:
            name (str): command name
            guild_ids (list[int], optional): list of guild IDs for guild commands or omit for global
        """
        return self.commands.message_command(name, guild_ids=guild_ids)
    
    def autocomplete(self, command_name: str, option_name: str):
        """Register and route an autocomplete interaction using InteractionAddon.

        Args:
            command_name (str): name of command to autocomplete
            option_name (str): name of option to autocomplete
        """
        return self.commands.autocomplete(command_name, option_name)

    def button(self, custom_id: str):
        """Decorator to route button interactions using InteractionAddon.

        Args:
            custom_id (str): custom ID of button
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
        """
        return self.commands.button(custom_id)
    
    def select(self, custom_id: str):
        """Decorator to route select menu interactions using InteractionAddon.

        Args:
            custom_id (str): custom ID of select menu
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
        """
        return self.commands.select(custom_id)
    
    def modal(self, custom_id: str):
        """Decorator to route modal interactions using InteractionAddon.

        Args:
            custom_id (str): custom ID of modal
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
        """
        return self.commands.modal(custom_id)
