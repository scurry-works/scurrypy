from ..client import Client
from ..core.intents import Intents
from ..core.logger import Logger
from ..core.error import DiscordError

from ..parts.command import CommandOption

from typing import TypedDict, Unpack

class CacheConfig(TypedDict, total=False):
    """Types of objects to cache."""
    roles: bool
    channels: bool
    bot_emojis: bool
    guild_emojis: bool

from .cache import *

class EasyBot(Client):
    """Prepackaged interaction, prefix, and event convenience for most of your needs!"""

    def __init__(self, *, 
        token: str, 
        application_id: int, 
        intents = Intents.DEFAULT, 
        prefix = None, 
        sync_commands = True, 
        debug_mode = False,
        **cache_config: Unpack[CacheConfig]
    ):
        """
        Args:
            token (str): the bot's token
            application_id (int): the bot's user ID
            intents (int, optional): gateway intents. Defaults to `Intents.DEFAULT`.
            prefix (str, optional): prefix if using prefix commands
            sync_commands (bool, optional): Whether commands should be synced with changes. Defaults to `True`.
            debug_mode (bool, optional): Whether error trace should be printed. Defaults to `False`.
            **cache_config (Unpack[CacheConfig], optional): what objects should be cached
        """

        # THEN init client
        super().__init__(
            token=token, 
            application_id=application_id, 
            intents=intents,
            logger=Logger(debug_mode=debug_mode)
        )

        # init addons
        self.channel_cache = GuildChannelCacheAddon(self) if cache_config.get('channels') else None
        self.role_cache = RoleCacheAddon(self) if cache_config.get('roles') else None
        self.bot_emoji_cache = BotEmojisCacheAddon(self) if cache_config.get('bot_emojis') else None
        self.guild_emoji_cache = GuildEmojiCacheAddon(self) if cache_config.get('guild_emojis') else None

        from scurrypy.addons.prefix import PrefixAddon
        self.prefixes = PrefixAddon(self, prefix) if prefix else None

        from scurrypy.addons.interaction import InteractionAddon
        self.commands = InteractionAddon(self, sync_commands)

        from scurrypy.addons.events import EventsAddon
        self.bot_events = EventsAddon(self)

        self._startup_hooks = []
        self._shutdown_hooks = []

        self.add_startup_hook(self.run_startup_hooks)
        self.add_shutdown_hook(self.run_shutdown_hooks)
        
    async def get_channel(self, channel_id: int):
        """Fetch a guild channel. If not found, request and store it.

        Args:
            channel_id (int): ID of channel

        Returns:
            (ChannelModel | None): hydrated channel object or None if fetch failed
        """
        channel = self.channel_cache.get_channel(channel_id)
        if channel:
            return channel

        try:
            channel = await self.channel(channel_id).fetch()
        except DiscordError:
            return None

        self.channel_cache.put(channel)
        return channel
    
    async def get_role(self, guild_id: int, role_id: int):
        """Fetch a guild role. If not found, request and store it.

        Args:
            guild_id (int): guild ID of role
            role_id (int): role ID of guild

        Returns:
            (RoleModel | None): hydrated role object or None if fetch failed
        """
        role = self.role_cache.get_role(role_id)
        if role:
            return role
        
        try:
            role = await self.guild(guild_id).fetch_guild_role(role_id)
        except DiscordError:
            return None
        
        self.role_cache.put(guild_id, role)
        return role
    
    def get_guild_emoji(self, emoji_id: int):
        """Get a guild emoji by ID.

        Args:
            emoji_id (int): emoji ID

        Returns:
            (EmojiModel | None): the queried emoji object if in cache else None
        """
        return self.guild_emoji_cache.get_emoji(emoji_id)
    
    def get_bot_emoji(self, emoji_name: str):
        """Get a bot emoji by ID.

        Args:
            emoji_name (str): name of emoji

        Returns:
            (EmojiModel | None): the queried emoji object if in cache else None
        """
        return self.bot_emoji_cache.get_emoji(emoji_name)

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
        if not self.prefixes:
            raise AttributeError("Prefixes Addon is not set. Consider setting a prefix.")

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
        """
        return self.commands.button(custom_id)
    
    def select(self, custom_id: str):
        """Decorator to route select menu interactions using InteractionAddon.

        Args:
            custom_id (str): custom ID of select menu
        """
        return self.commands.select(custom_id)
    
    def modal(self, custom_id: str):
        """Decorator to route modal interactions using InteractionAddon.

        Args:
            custom_id (str): custom ID of modal
        """
        return self.commands.modal(custom_id)
