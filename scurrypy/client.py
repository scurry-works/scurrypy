import asyncio
import inspect

from .core.intents import Intents
from .core.http import HTTPClient
from .core.gateway import GatewayClient
from .core.error import DiscordError
from .parts.command import SlashCommand, UserCommand, MessageCommand

from .events.gateway_events import GatewayEvent

import logging

logger = logging.getLogger(__name__)

class Client:
    """Main entry point for Discord bots.
        Ties together the moving parts: gateway, HTTP and event dispatching.
    """

    token: str
    """Bot's token."""

    intents: int
    """Bot intents for listening to events."""

    _http: HTTPClient
    """HTTP session for requests."""

    shards: list[GatewayClient]
    """Shards as a list of gateways."""

    events: dict[str: list[callable]]
    """Events for the client to listen to."""

    startup_hooks: list[callable]
    """Handlers to call once before the bot starts."""

    shutdown_hooks: list[callable]
    """Handlers to call once after the bot shuts down."""

    def __init__(self, 
        *,
        token: str,
        intents: int = Intents.DEFAULT
    ):
        """
        Args:
            token (str): the bot's token
            intents (int, optional): gateway intents. Defaults to `Intents.DEFAULT`.
        """
        if not isinstance(intents, int):
            raise ValueError("Intents must be an integer.")
        
        self.token = token
        self.intents = intents
        
        self._http = HTTPClient()

        self.shards: list[GatewayClient] = []

        self.events = {}
        self.startup_hooks = []
        self.shutdown_hooks = []

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
        from .resources.application import Application

        return Application(self._http, id=application_id, context=None)
    
    def bot_emoji(self, application_id: int):
        """Creates an interactable bot emoji resource.

        Args:
            application_id (int): ID of target application

        Returns:
            (BotEmojis): the BotEmoji resource
        """
        from .resources.bot_emoji import BotEmoji

        return BotEmoji(self._http, None, application_id)
    
    def guild_emoji(self, guild_id: int):
        """Creates an interactable emoji resource.

        Args:
            guild_id (int): guild ID of target emojis

        Returns:
            (GuildEmoji): the GuildEmoji resource
        """
        from .resources.guild_emoji import GuildEmoji

        return GuildEmoji(self._http, None, guild_id)

    def guild(self, guild_id: int, *, context = None):
        """Creates an interactable guild resource.

        Args:
            guild_id (int): ID of target guild
            context (Any, optional): optional associated data 

        Returns:
            (Guild): the Guild resource
        """
        from .resources.guild import Guild

        return Guild(self._http, context, guild_id)

    def channel(self, channel_id: int, *, context = None):
        """Creates an interactable channel resource.

        Args:
            channel_id (int): ID of target channel
            context (Any, optional): optional associated data

        Returns:
            (Channel): the Channel resource
        """
        from .resources.channel import Channel

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
        from .resources.message import Message

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
        from .resources.interaction import Interaction

        return Interaction(self._http, context, id, token)
    
    def user(self, user_id: int, *, context = None):
        """Creates an interactable user resource.

        Args:
            user_id (int): ID of target user
            context (Any, optional): optional associated data

        Returns:
            (User): the User resource
        """
        from .resources.user import User

        return User(self._http, context, user_id)
    
    async def register_guild_commands(self, application_id: int, commands: list[SlashCommand | UserCommand | MessageCommand], guild_id: int):
        """Registers commands at the guild level.

        Args:
            application_id (int): bot's user ID
            commands (list[SlashCommand  |  UserCommand  |  MessageCommand]): commands to register
            guild_id (int): ID of guild in which to register command
        """
        if not isinstance(commands, list):
            commands = [commands]

        await self._http.request(
            'PUT', 
            f"applications/{application_id}/guilds/{guild_id}/commands", 
            data=[command.to_dict() for command in commands]
        )
    
    async def register_global_commands(self, application_id: int, commands: list[SlashCommand | UserCommand | MessageCommand]):
        """Registers a command at the global/bot level. (ALL GUILDS)

        Args:
            application_id (int): bot's user ID
            commands (list[SlashCommand  |  UserCommand  |  MessageCommand]): commands to register
        """
        if not isinstance(commands, list):
            commands = [commands]

        await self._http.request(
            'PUT', 
            f"applications/{application_id}/commands", 
            data=[command.to_dict() for command in commands]
        )

    async def listen_shard(self, shard: GatewayClient):
        """Consume a GatewayClient's event queue.

        Args:
            shard (GatewayClient): gateway to listen on
        """

        from .core.events import EVENTS

        while True:
            try:
                dispatch_type, event_data = await shard.event_queue.get()

                if dispatch_type not in self.events.keys():
                    logger.debug(f"SHARD ID {shard.shard_id} DISPATCH -> {dispatch_type}")
                else:
                    logger.info(f"SHARD ID {shard.shard_id} DISPATCH -> {dispatch_type}")

                event_model = EVENTS.get(dispatch_type)
                if not event_model:
                    logger.warning(f"Event {dispatch_type} is not implemented.")
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
                        logger.error(e)
                        continue

            except Exception:
                # catastrophic errors (network, shard death, unexpected OP code)
                logger.exception(f"SHARD ID {shard.shard_id}: Dispatcher error")
                continue

    async def _start_shards(self, gateway: GatewayEvent):
        """Starts all shards batching by max_concurrency."""

        # pull important values for easier access
        total_shards = gateway.shards
        batch_size = gateway.session_start_limit.max_concurrency

        tasks = []
        
        for batch_start in range(0, total_shards, batch_size):
            batch_end = min(batch_start + batch_size, total_shards)

            logger.debug(f"Starting shards {batch_start}-{batch_end} of {total_shards}")

            for shard_id in range(batch_start, batch_end):
                shard = GatewayClient(gateway.url, shard_id, total_shards)
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

            data = await self._http.request('GET', '/gateway/bot')

            if not data:
                return

            gateway = GatewayEvent.from_dict(data)

            for hook in self.startup_hooks:
                try:
                    result = hook()
                    if inspect.isawaitable(result):
                        await result
                except Exception:
                    logger.exception("Error in shartup hook")

            tasks = await asyncio.create_task(self._start_shards(gateway))

            # end all ongoing tasks
            await asyncio.gather(*tasks)
            
        except asyncio.CancelledError:
            logger.info("Connection cancelled via KeyboardInterrupt.")
        except Exception:
            logger.error(f"Unhandled client start exception.")
        finally:
            await self._close()

    async def _close(self):
        """Gracefully close HTTP session, websocket connections, and run shutdown logic."""  

        for hook in self.shutdown_hooks:
            try:
                result = hook()
                if inspect.isawaitable(result):
                    await result
            except Exception:
                logger.exception("Error in shutdown hook")
                
        logger.info("Closing HTTP session...")
        await self._http.close()

        # close each connection or shard
        await asyncio.gather(*[shard.close_ws() for shard in self.shards])
    
    def run(self):
        """User-facing entry point for starting the client."""  

        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.error(f"{type(e).__name__} {e}")
        finally:
            logger.info("Bot shutting down.")
