import asyncio
import inspect

from .intents import Intents
from .core.http import HttpClient
from .core.gateway import GatewayClient
from .core.error import DiscordError
from .core.snowflake import Snowflake
from .core.exceptions import MissingIntents, InvalidCallbackSignature
from .core.json_query import JsonQuery

from .enums.events import EventType

from .resources.application import Application
from .resources.audit_log import AuditLog
from .resources.automod import AutoModeration
from .resources.emoji import ApplicationEmoji, GuildEmoji
from .resources.channel import Channel
from .resources.command import GlobalCommand, GuildCommand
from .resources.guild_scheduled_event import GuildScheduledEvent
from .resources.guild_template import GuildTemplate
from .resources.guild import Guild
from .resources.interaction import Interaction
from .resources.invite import Invite
from .resources.message import Message
from .resources.poll import Poll
from .resources.sticker import Sticker
from .resources.user import User
from .resources.webhook import Webhook

import logging

logger = logging.getLogger("scurrypy.client")
logger.addHandler(logging.NullHandler())

from collections.abc import Callable, Awaitable

type CoreHandler = Callable[[JsonQuery], Awaitable[None]]
type HookHandler = Callable[[], Awaitable[None] | None]

class Client:
    """Main entry point for Discord bots.
        Ties together the moving parts: gateway, HTTP and event dispatching.
    """

    token: str
    """Bot's token."""

    intents: Intents
    """Bot intents for listening to events."""

    http: HttpClient
    """Public HTTP session for requests."""

    shards: list[GatewayClient]
    """Shards as a list of gateways."""

    events: dict[EventType | str, list[CoreHandler]]
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
        shard_count: int = 0
    ):
        """
        Args:
            token (str): the bot's token
            intents (Intents, optional): gateway intents. Defaults to `Intents.DEFAULT`.
            shard_count (int, optional): number of shards to spawn. Defaults to `0` or recommended shard count.
        """
        if not isinstance(intents, Intents):
            raise MissingIntents("Invalid intents type.")
        
        self.token = token
        self.intents = intents
        self.shard_count = shard_count
        
        self.http: HttpClient = HttpClient()

        self.shards: list[GatewayClient] = []

        self.events = {}
        self.startup_hooks = []
        self.shutdown_hooks = []

    def add_event_listener(self, event: EventType | str, handler: CoreHandler) -> None:
        """Helper function to register listener functions.

        Args:
            event (EventType | str): name of the event to listen
            handler (CoreHandler): listener function
        """
        if not inspect.iscoroutinefunction(handler):
            raise InvalidCallbackSignature(f"{handler.__name__} must be async")
        
        sig = inspect.signature(handler)
        params = list(sig.parameters.values())

        if len(params) != 1:
            raise InvalidCallbackSignature(f"{handler.__name__} must accept exactly 1 parameter (event: JsonQuery)")

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

        Args:
            application_id (Snowflake): ID of target application

        Returns:
            (Application): the Application resource
        """
        return Application(self.http, application_id)

    def audit_log(self) -> AuditLog:
        """Creates an interactable application resource.

        Returns:
            (AuditLog): the AuditLog resource
        """
        return AuditLog(self.http)
    
    def application_emoji(self, application_id: Snowflake) -> ApplicationEmoji:
        """Creates an interactable application emoji resource.

        Args:
            application_id (Snowflake): ID of target application

        Returns:
            (ApplicationEmoji): the ApplicationEmoji resource
        """
        return ApplicationEmoji(self.http, application_id)

    def auto_moderation(self, guild_id: Snowflake) -> AutoModeration:
        """Creates an interactable application auto moderation resource.

        Args:
            guild_id (Snowflake): guild ID of target automod rules

        Returns:
            (AutoModeration): the AutoModeration resource
        """
        return AutoModeration(self.http, guild_id)

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
            guild_id (Snowflake): ID of guild in which the command belongs

        Returns:
            (GuildCommand): the GuildCommand resource
        """
        return GuildCommand(self.http, application_id, guild_id)

    def guild_emoji(self, guild_id: Snowflake) -> GuildEmoji:
        """Creates an interactable guild emoji resource.

        Args:
            guild_id (Snowflake): guild ID of target emojis

        Returns:
            (GuildEmoji): the GuildEmoji resource
        """
        return GuildEmoji(self.http, guild_id)

    def guild_scheduled_event(self, guild_id: Snowflake) -> GuildScheduledEvent:
        """Creates an interactable guild scheduled event resource.

        Args:
            guild_id (Snowflake): ID of target guild

        Returns:
            (GuildScheduledEvent): the GuildScheduledEvent resource
        """
        return GuildScheduledEvent(self.http, guild_id)

    def guild_template(self) -> GuildTemplate:
        """Creates an interactable guild template resource.

        Returns:
            (GuildTemplate): the GuildTemplate resource
        """
        return GuildTemplate(self.http)

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

        Returns:
            (Invite): the Invite resource
        """
        return Invite(self.http, code)

    def message(self, channel_id: Snowflake, message_id: Snowflake) -> Message:
        """Creates an interactable message resource.

        Args:
            channel_id (Snowflake): channel ID of target message
            message_id (Snowflake): ID of target message

        Returns:
            (Message): the Message resource
        """
        return Message(self.http, message_id, channel_id)

    def poll(self, channel_id: Snowflake, message_id: Snowflake) -> Poll:
        """Creates an interactable poll resource

        Args:
            channel_id (Snowflake): ID of target message
            message_id (Snowflake): channel ID of target message

        Returns:
            (Poll): the Poll resource
        """
        return Poll(self.http, channel_id, message_id)

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

    def webhook(self) -> Webhook:
        """Creates an interactable webhook resource.

        Returns:
            (Webhook): the Webhook resource
        """
        return Webhook(self.http)

    def get_shard_from_guild_id(self, guild_id: Snowflake) -> GatewayClient:
        """Fetch the shard in which the guild belongs.

        Args:
            guild_id (Snowflake): ID of the guild

        Returns:
            (GatewayClient): shard of the guild
        """
        return self.shards[(guild_id >> 22) % self.shard_count]

    def get_shard_id_from_guild_id(self, guild_id: Snowflake) -> int:
        """Fetch the shard ID in which the guild belongs.

        Args:
            guild_id (Snowflake): ID of the guild

        Returns:
            (int): shard ID of the guild
        """
        return (guild_id >> 22) % self.shard_count

    async def listen_shard(self, shard: GatewayClient) -> None:
        """Consume a gateway client's event queue.

        Args:
            shard (GatewayClient): gateway to listen on
        """
        while True:
            try:
                dispatch_type, event_data = await shard.event_queue.get()

                logger.info(f"SHARD ID {shard.shard_id} RECV -> {dispatch_type}")

                if dispatch_type in self.events.keys():
                    logger.info(f"SHARD ID {shard.shard_id} DISPATCH -> {dispatch_type}")

                handlers = self.events.get(dispatch_type, [])
                for handler in handlers:
                    try:
                        event_data['dispatch_name'] = dispatch_type
                        await handler(JsonQuery(event_data))
                    except DiscordError as e:
                        logger.error(e)
                        continue

            except Exception:
                # catastrophic errors (network, shard death, unexpected OP code)
                logger.exception(f"SHARD ID {shard.shard_id}: Dispatcher error")
                continue

    async def start_shards(self, gateway: JsonQuery) -> list[asyncio.Task[None]]:
        """Starts all shards batching by max_concurrency.

        Args:
            gateway (JsonQuery): gatewway info event data

        Returns:
            list[asyncio.Task]: list of gateway connection tasks
        """

        # pull important values for easier access
        total_shards: int = self.shard_count or gateway.get('shards', t=int).value
        self.shard_count = total_shards
        batch_size: int = gateway.get('session_start_limit.max_concurrency', t=int).value

        tasks = []
        
        for batch_start in range(0, total_shards, batch_size):
            batch_end = min(batch_start + batch_size, total_shards)

            logger.debug(f"Starting shards {batch_start}-{batch_end} of {total_shards}")

            for shard_id in range(batch_start, batch_end):
                shard = GatewayClient()
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

            gateway = await self.http.request_json('GET', '/gateway/bot')

            if not gateway:
                return

            # run startup hooks while shards are starting
            asyncio.create_task(self.run_startup_hooks())

            tasks = await self.start_shards(JsonQuery(gateway))

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
