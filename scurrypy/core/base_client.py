import asyncio
import inspect
from typing import Protocol

from .http import HTTPClient
from .gateway import GatewayClient
from .logger import LoggerLike
from .error import DiscordError
from .addon import Addon
from ..parts.command import SlashCommand, UserCommand, MessageCommand

from ..events import *

EVENTS = {
    # startup events
    'READY': ReadyEvent,

    # channel events
    'CHANNEL_CREATE': GuildChannelCreateEvent,
    'CHANNEL_UPDATE': GuildChannelDeleteEvent,
    'CHANNEL_DELETE': GuildChannelDeleteEvent,
    'CHANNEL_PINS_UPDATE': ChannelPinsUpdateEvent,

    # guild events
    'GUILD_CREATE': GuildCreateEvent,
    'GUILD_UPDATE': GuildDeleteEvent,
    'GUILD_DELETE': GuildDeleteEvent,
    'GUILD_MEMBER_ADD': GuildMemberAddEvent,
    'GUILD_MEMBER_UPDATE': GuildMemberUpdateEvent,
    'GUILD_MEMBER_REMOVE': GuildMemberRemoveEvent,
    'GUILD_EMOJIS_UPDATE': GuildEmojisUpdateEvent,

    # interaction events
    'INTERACTION_CREATE': InteractionEvent,

    # message events
    'MESSAGE_CREATE': MessageCreateEvent,
    'MESSAGE_UPDATE': MessageUpdateEvent,
    'MESSAGE_DELETE': MessageDeleteEvent,

    # reaction events
    'MESSAGE_REACTION_ADD': ReactionAddEvent,
    'MESSAGE_REACTION_REMOVE': ReactionRemoveEvent,
    'MESSAGE_REACTION_REMOVE_ALL': ReactionRemoveAllEvent,
    'MESSAGE_REACTION_REMOVE_EMOJI': ReactionRemoveEmojiEvent,

    'ROLE_CREATE': RoleCreateEvent,
    'ROLE_UPDATE': RoleUpdateEvent,
    'ROLE_DELETE': RoleDeleteEvent
}

class BaseClient(Protocol):
    """Exposes a common interface for [`Client`][scurrypy.client.Client]."""

    token: str
    """Bot's token."""

    application_id: int
    """Bot's application ID."""

    intents: int
    """Bot intents for listening to events."""

    _http: HTTPClient
    """HTTP session for requests."""

    shards: list[GatewayClient]
    """Shards as a list of gateways."""

    logger: LoggerLike
    """Logger instance to log events."""

    events: dict[str: list[callable]]
    """Events for the client to listen to."""

    startup_hooks: list[callable]
    """Handlers to call once before the bot starts."""

    shutdown_hooks: list[callable]
    """Handlers to call once after the bot shuts down."""

    def add_event_listener(self, event: str, handler):
        """Helper function to register listener functions.

        Args:
            event (str): name of the event to listen
            handler (callable): listener function
        """
        params_len = len(inspect.signature(handler).parameters)

        if params_len != 1:
            raise TypeError(
                f"Event listener '{handler.__name__}' must accept exactly one parameter (event)."
            )
    
        self.events.setdefault(event, []).append(handler)

    def add_startup_hook(self, handler):
        """Helper function to register startup functions.
            Runs once on startup BEFORE READY event.

        Args:
            handler (callable): startup function
        """
        params_len = len(inspect.signature(handler).parameters)

        if params_len != 0:
            raise TypeError(
                f"Startup hook '{handler.__name__}' must accept no parameters."
            )
        
        self.startup_hooks.append(handler)

    def add_shutdown_hook(self, handler):
        """Helper function to register shutdown functions.
            Runs once on shutdown.

        Args:
            handler (callable): shutdown function
        """
        params_len = len(inspect.signature(handler).parameters)

        if params_len != 0:
            raise TypeError(
                f"Shutdown hook '{handler.__name__}' must accept no parameters."
            )

        self.shutdown_hooks.append(handler)

    def application(self, application_id: int):
        """Creates an interactable application resource.

        Args:
            application_id (int): ID of target application

        Returns:
            (Application): the Application resource
        """
        from ..resources.application import Application

        return Application(self._http, None, application_id)
    
    def bot_emoji(self):
        """Creates an interactable bot emoji resource.

        Returns:
            (BotEmojis): the BotEmoji resource
        """
        from ..resources.bot_emoji import BotEmoji

        return BotEmoji(self._http, None, self.application_id)
    
    def guild_emoji(self, guild_id: int):
        """Creates an interactable emoji resource.

        Args:
            guild_id (int): guild ID of target emojis

        Returns:
            (GuildEmoji): the GuildEmoji resource
        """
        from ..resources.guild_emoji import GuildEmoji

        return GuildEmoji(self._http, None, guild_id)

    def guild(self, guild_id: int, *, context = None):
        """Creates an interactable guild resource.

        Args:
            guild_id (int): ID of target guild
            context (Any, optional): optional associated data 

        Returns:
            (Guild): the Guild resource
        """
        from ..resources.guild import Guild

        return Guild(self._http, context, guild_id)

    def channel(self, channel_id: int, *, context = None):
        """Creates an interactable channel resource.

        Args:
            channel_id (int): ID of target channel
            context (Any, optional): optional associated data

        Returns:
            (Channel): the Channel resource
        """
        from ..resources.channel import Channel

        return Channel(self._http, context, channel_id)

    def message(self, channel_id: int, message_id: int, *, context = None):
        """Creates an interactable message resource.

        Args:
            message_id (int): ID of target message
            channel_id (int): channel ID of target message
            context (Any, optional): optional associated data

        Returns:
            (Message): the Message resource
        """
        from ..resources.message import Message

        return Message(self._http, context, message_id, channel_id)
    
    def interaction(self, id: int, token: str, *, context = None):
        """Creates an interactable interaction resource.

        Args:
            id (int): ID of the interaction
            token (str): interaction token
            context (Any, optional): optional associated data

        Returns:
            (Interaction): the Interaction resource
        """
        from ..resources.interaction import Interaction

        return Interaction(self._http, context, id, token)
    
    def user(self, user_id: int, *, context = None):
        """Creates an interactable user resource.

        Args:
            user_id (int): ID of target user
            context (Any, optional): optional associated data

        Returns:
            (User): the User resource
        """
        from ..resources.user import User

        return User(self._http, context, user_id)

    async def listen_shard(self, shard: GatewayClient):
        while True:
            try:
                dispatch_type, event_data = await shard.event_queue.get()

                event_model = EVENTS.get(dispatch_type)
                if not event_model:
                    self.logger.log_warn(f"Event {dispatch_type} is not implemented.")
                    continue

                obj = event_model.from_dict(event_data)
                obj.name = dispatch_type
                obj.raw = event_data

                handlers = self.events.get(dispatch_type, [])
                for handler in handlers:
                    try:
                        result = handler(obj)
                        if inspect.isawaitable(result):
                            await result
                    except DiscordError as e:
                        self.logger.log_error(
                            f"Error in handler '{handler.__name__}' for event '{dispatch_type}': {e}"
                        )
                        continue

            except Exception as e:
                # catastrophic errors (network, shard death, unexpected OP code)
                self.logger.log_error(f"Dispatcher error: {e}")
                continue

    async def register_guild_commands(self, commands: list[SlashCommand | UserCommand | MessageCommand], guild_id: int):
        """Registers commands at the guild level.

        Args:
            commands (list[SlashCommand  |  UserCommand  |  MessageCommand]): commands to register
            guild_id (int): ID of guild in which to register command
        """
        if not isinstance(commands, list):
            commands = [commands]

        await self._http.request(
            'PUT', 
            f"applications/{self.application_id}/guilds/{guild_id}/commands", 
            data=[command.to_dict() for command in commands]
        )
    
    async def register_global_commands(self, commands: list[SlashCommand | UserCommand | MessageCommand]):
        """Registers a command at the global/bot level. (ALL GUILDS)

        Args:
            commands (list[SlashCommand  |  UserCommand  |  MessageCommand]): commands to register
        """
        if not isinstance(commands, list):
            commands = [commands]

        await self._http.request(
            'PUT', 
            f"applications/{self.application_id}/commands", 
            data=[command.to_dict() for command in commands]
        )

    async def _start_shards(self):
        """Starts all shards batching by max_concurrency."""

        from ..events.gateway_events import GatewayEvent

        data = await self._http.request('GET', '/gateway/bot')

        gateway = GatewayEvent.from_dict(data)

        # pull important values for easier access
        total_shards = gateway.shards
        batch_size = gateway.session_start_limit.max_concurrency

        tasks = []
        
        for batch_start in range(0, total_shards, batch_size):
            batch_end = min(batch_start + batch_size, total_shards)

            self.logger.log_info(f"Starting shards {batch_start}-{batch_end - 1} of {total_shards}")

            for shard_id in range(batch_start, batch_end):
                shard = GatewayClient(gateway.url, shard_id, total_shards, self.logger)
                self.shards.append(shard)

                # fire and forget
                tasks.append(asyncio.create_task(shard.start(self.token, self.intents)))
                tasks.append(asyncio.create_task(self.listen_shard(shard)))

            # wait before next batch to respect identify rate limit
            await asyncio.sleep(5)

        return tasks
    
    async def start(self):
        """Starts the HTTP/Websocket client, run startup logic, and registers commands."""
        
        try:
            await self._http.start(self.token)

            for hook in self.startup_hooks:
                result = hook()
                if inspect.isawaitable(result):
                    await result

            tasks = await asyncio.create_task(self._start_shards())

            # end all ongoing tasks
            await asyncio.gather(*tasks)
            
        except asyncio.CancelledError:
            self.logger.log_high_priority("Connection cancelled via KeyboardInterrupt.")
        except Exception as e:
            self.logger.log_error(f"{type(e).__name__} - {e}")
        finally:
            await self._close()

    async def _close(self):
        """Gracefully close HTTP session, websocket connections, and run shutdown logic."""  

        for hook in self.shutdown_hooks:
            result = hook()
            if inspect.isawaitable(result):
                await result

        self.logger.log_info("Closing HTTP session...")
        await self._http.close()

        # close each connection or shard
        for shard in self.shards:
            await shard.close_ws()
