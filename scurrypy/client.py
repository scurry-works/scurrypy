import asyncio
import inspect

from .intents import Intents
from .core.http import HTTPClient, HTTPClientProtocol
from .core.gateway import GatewayClient, GatewayClientProtocol
from .core.error import DiscordError
from .core.snowflake import Snowflake
from .core.exceptions import MissingIntents, InvalidCallbackSignature
from .core.events import EVENTS

from .enums.events import EventType

from .events.gateway_events import GatewayEvent

from .resources.application import Application
from .resources.emoji import ApplicationEmoji, GuildEmoji
from .resources.channel import Channel
from .resources.command import GlobalCommand, GuildCommand
from .resources.guild import Guild
from .resources.interaction import Interaction
from .resources.invite import Invite
from .resources.message import Message
from .resources.sticker import Sticker
from .resources.user import User

import logging

logger = logging.getLogger("scurrypy.client")
logger.addHandler(logging.NullHandler())

from typing import Any
from collections.abc import Callable, Awaitable

# The event parameter is intentionally Any: the concrete event instance
# is determined by EventType at dispatch time, not by the handler annotation.
type CoreHandler = Callable[[Any], Awaitable[None]]
type HookHandler = Callable[[], Awaitable[None] | None]

class Client:
    """Main entry point for Discord bots.
        Ties together the moving parts: gateway, HTTP and event dispatching.
    """

    token: str
    """Bot's token."""

    intents: Intents
    """Bot intents for listening to events."""

    http: HTTPClientProtocol
    """Public HTTP session for requests."""

    shards: list[GatewayClientProtocol]
    """Shards as a list of gateways."""

    events: dict[EventType, list[CoreHandler]]
    """Events for the client to listen to."""

    startup_hooks: list[HookHandler]
    """Handlers to call once before the bot starts."""

    shutdown_hooks: list[HookHandler]
    """Handlers to call once after the bot shuts down."""

    def __init__(
        self,
        *,
        token: str,
        intents: Intents = Intents.DEFAULT,
        shard_count: int = 0,
        http: HTTPClientProtocol | None = None,
        gateway_impl: type[GatewayClientProtocol] | None = None,
    ):
        """
        Args:
            token (str): the bot's token
            intents (Intents, optional): gateway intents. Defaults to `Intents.DEFAULT`.
            shard_count (int, optional): number of shards to spawn. Defaults to `0` or recommended shard count.
            http (HTTPClientProtocol, optional): HTTP protocol implementation. Leave blank for default client.
            gateway_impl (GatewayClientProtocol, optional): Gateway protocol implementation. Leave blank for default client.
        """
        if not isinstance(intents, Intents):
            raise MissingIntents("Invalid intents type.")
        
        self.token = token
        self.intents = intents
        self.shard_count = shard_count
        
        self.http: HTTPClientProtocol = http or HTTPClient()

        self.shards: list[GatewayClientProtocol] = []
        self.shard_type = gateway_impl or GatewayClient

        self.events = {}
        self.startup_hooks = []
        self.shutdown_hooks = []

    def add_event_listener(self, event: EventType, handler: CoreHandler) -> None:
        """Helper function to register listener functions.

        Args:
            event (EventType): name of the event to listen
            handler (CoreHandler): listener function
        """
        if not inspect.iscoroutinefunction(handler):
            raise InvalidCallbackSignature(f"{handler.__name__} must be async")
        
        sig = inspect.signature(handler)
        params = list(sig.parameters.values())

        if len(params) != 1:
            raise InvalidCallbackSignature(f"{handler.__name__} must accept exactly 1 parameter (event: {EVENTS[event].__name__})")

        self.events.setdefault(event, []).append(handler)

    def _check_hook_signature(self, handler: HookHandler) -> None:
        """Helper function for checking hook signatures.

        Args:
            handler (HookHandler): hook callback

        Raises:
            (InvalidCallbackSignature): invalid signature
        """
        sig = inspect.signature(handler)
        params = list(sig.parameters.values())

        if len(params) != 0:
            raise InvalidCallbackSignature(f"{handler.__name__} must accept exactly no parameters")

    def add_startup_hook(self, handler: HookHandler) -> None:
        """Register a startup function.
            Runs once on startup BEFORE READY event.

        Raises:
            (InvalidCallbackSignature): invalid signature

        Args:
            handler (HookHandler): startup function
        """
        self._check_hook_signature(handler)
        self.startup_hooks.append(handler)

    def add_shutdown_hook(self, handler: HookHandler) -> None:
        """Register a shutdown function.
            Runs once on shutdown.

        Raises:
            (InvalidCallbackSignature): invalid signature

        Args:
            handler (HookHandler): shutdown function
        """
        self._check_hook_signature(handler)
        self.shutdown_hooks.append(handler)

    def application(self, application_id: Snowflake) -> Application:
        """Creates an interactable application resource.

        Raises:
            (InvalidCallbackSignature): invalid signature

        Args:
            application_id (Snowflake): ID of target application

        Returns:
            (Application): the Application resource
        """
        return Application(self.http, application_id)
    
    def application_emoji(self, application_id: Snowflake) -> ApplicationEmoji:
        """Creates an interactable application emoji resource.

        Args:
            application_id (Snowflake): ID of target application

        Returns:
            (ApplicationEmoji): the ApplicationEmoji resource
        """
        return ApplicationEmoji(self.http, application_id)

    def channel(self, channel_id: Snowflake) -> Channel:
        """Creates an interactable channel resource.

        Args:
            channel_id (Snowflake): ID of target channel

        Returns:
            (Channel): the Channel resource
        """
        return Channel(self.http, channel_id)

    def global_command(self, application_id: Snowflake) -> GlobalCommand:
        """Creates an interactable command resource.

        Args:
            application_id (Snowflake): bot's user ID

        Returns:
            (GlobalCommand): the GlobalCommand resource
        """
        return GlobalCommand(self.http, application_id)
    
    def guild_command(self, application_id: Snowflake, guild_id: Snowflake) -> GuildCommand:
        """Creates an interactable command resource.

        Args:
            application_id (Snowflake): bot's user ID
            guild_id (Snowflake, optional): ID of guild if command is in guild scope

        Returns:
            (GuildCommand): the GuildCommand resource
        """
        return GuildCommand(self.http, application_id, guild_id)

    def guild_emoji(self, guild_id: Snowflake) -> GuildEmoji:
        """Creates an interactable emoji resource.

        Args:
            guild_id (Snowflake): guild ID of target emojis

        Returns:
            (GuildEmoji): the GuildEmoji resource
        """
        return GuildEmoji(self.http, guild_id)

    def guild(self, guild_id: Snowflake) -> Guild:
        """Creates an interactable guild resource.

        Args:
            guild_id (Snowflake): ID of target guild

        Returns:
            (Guild): the Guild resource
        """
        return Guild(self.http, guild_id)

    def interaction(self, id: Snowflake, token: str) -> Interaction:
        """Creates an interactable interaction resource.

        Args:
            id (Snowflake): ID of the interaction
            token (str): interaction token

        Returns:
            (Interaction): the Interaction resource
        """
        return Interaction(self.http, id, token)

    def invite(self, code: str) -> Invite:
        """Creates an interactable invite resource.

        Args:
            code (str): unique invite code
        """
        return Invite(self.http, code)

    def message(self, channel_id: Snowflake, message_id: Snowflake) -> Message:
        """Creates an interactable message resource.

        Args:
            message_id (Snowflake): ID of target message
            channel_id (Snowflake): channel ID of target message

        Returns:
            (Message): the Message resource
        """
        return Message(self.http, message_id, channel_id)

    def sticker(self) -> Sticker:
        """Creates an interactable sticker resource

        Returns:
            (Sticker): the Sticker resource
        """
        return Sticker(self.http)
    
    def user(self) -> User:
        """Creates an interactable user resource.

        Returns:
            (User): the User resource
        """
        return User(self.http)

    async def listen_shard(self, shard: GatewayClientProtocol) -> None:
        """Consume a gateway client's event queue.

        Args:
            shard (GatewayClientProtocol): gateway to listen on
        """

        while True:
            try:
                dispatch_type, event_data = await shard.event_queue.get()

                event_type = EventType.from_dict(str(dispatch_type))

                if event_type not in self.events.keys():
                    logger.debug(f"SHARD ID {shard.shard_id} DISPATCH -> {dispatch_type}")
                else:
                    logger.info(f"SHARD ID {shard.shard_id} DISPATCH -> {dispatch_type}")

                event_model = EVENTS.get(event_type)
                if not event_model:
                    logger.warning(f"Event {dispatch_type} is not implemented.")
                    continue

                obj = event_model.from_dict(event_data)
                obj.raw = event_data

                handlers = self.events.get(event_type, [])
                for handler in handlers:
                    try:
                        await handler(obj)
                    except DiscordError as e:
                        logger.error(e)
                        continue

            except Exception:
                # catastrophic errors (network, shard death, unexpected OP code)
                logger.exception(f"SHARD ID {shard.shard_id}: Dispatcher error")
                continue

    async def start_shards(self, gateway: GatewayEvent) -> list[asyncio.Task[None]]:
        """Starts all shards batching by max_concurrency.

        Args:
            gateway (GatewayEvent): gatewway info event data

        Returns:
            list[asyncio.Task]: list of gateway connection tasks
        """

        # pull important values for easier access
        total_shards = self.shard_count or gateway.shards
        batch_size = gateway.session_start_limit.max_concurrency

        tasks = []
        
        for batch_start in range(0, total_shards, batch_size):
            batch_end = min(batch_start + batch_size, total_shards)

            logger.debug(f"Starting shards {batch_start}-{batch_end} of {total_shards}")

            for shard_id in range(batch_start, batch_end):
                shard = self.shard_type()
                self.shards.append(shard)

                # fire and forget
                tasks.append(asyncio.create_task(shard.start(self.token, self.intents, shard_id, total_shards)))
                tasks.append(asyncio.create_task(self.listen_shard(shard)))

            # wait before next batch to respect identify rate limit
            await asyncio.sleep(5)

        return tasks

    async def start(self) -> None:
        """Starts the HTTP/Websocket client, run startup logic, and registers commands."""
        try:
            await self.http.start(self.token)

            data = await self.http.request('GET', '/gateway/bot')

            if not data:
                return

            gateway = GatewayEvent.from_dict(data)

            await self.run_startup_hooks()

            tasks = await self.start_shards(gateway)

            await asyncio.gather(*tasks)
            
        except asyncio.CancelledError:
            logger.info("Connection cancelled via KeyboardInterrupt.")
        except DiscordError as e:
            logger.error(e)
        except Exception:
            logger.exception(f"Unhandled client start exception.")
        finally:
            await self.close()

    async def run_startup_hooks(self) -> None:
        """Runs registered startup hooks."""

        for hook in self.startup_hooks:
            try:
                logger.debug(f"Running hook {hook}...")
                result = hook()
                if result is not None:
                    await asyncio.wait_for(result, timeout=60)
            except Exception:
                logger.exception("Error in shartup hook")

    async def run_shutdown_hooks(self) -> None:
        """Runs registered shutdown hooks."""

        for hook in self.shutdown_hooks:
            try:
                logger.debug(f"Running hook {hook}...")
                result = hook()
                if result is not None:
                    await asyncio.wait_for(result, timeout=60)
            except Exception:
                logger.exception("Error in shutdown hook")

    async def close(self) -> None:
        """Gracefully close HTTP session, websocket connections, and run shutdown logic."""  

        await self.run_shutdown_hooks()

        # close each connection or shard BEFORE HTTP
        await asyncio.gather(
            *(shard.close_ws() for shard in self.shards),
            return_exceptions=True
        )

        logger.info("Closing HTTP session...")
        await self.http.close()
    
    def run(self) -> None:
        """User-facing entry point for starting the client."""
        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.exception(f"{type(e).__name__} {e}")
        finally:
            logger.info("Bot shutting down.")
