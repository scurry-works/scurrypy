import asyncio
import json
import websockets

import logging

logger = logging.getLogger("scurrypy.gateway")
logger.addHandler(logging.NullHandler())

from ..config import GATEWAY_PROPERTIES

from .exceptions import NoSession

MIN_BACKOFF = 5

from dataclasses import dataclass
import time
from typing import Protocol

from .types import JSON

@dataclass
class GatewayMetrics:
    _last_heartbeat_sent: float
    heartbeat_rrt: float

class EventQueueProtocol(Protocol):
    """Internal contract for the GatewayClient's event queue used by the Client. Meant for testing."""
    async def put(self, item: tuple[str, JSON]) -> None: ...
    async def get(self) -> tuple[str, JSON]: ...

class GatewayClientProtocol(Protocol):
    """Internal contract for the GatewayClient used by the Client. Meant for testing."""
    event_queue: EventQueueProtocol
    shard_id: int
    total_shards: int

    async def start(self, token: str, intents: int, shard_id: int, total_shards: int) -> None: ...
    async def close_ws(self) -> None: ...

class GatewayClient(GatewayClientProtocol):
    def __init__(self) -> None:
        self.shard_id: int = 0
        self.total_shards: int = 0
        self._ws: websockets.ClientConnection | None = None
        self.seq: int | None = None
        self.session_id: str | None = None
        self.allow_resume: bool = False # default: assume IDENTIFY
        self.reconnect_immediately: bool = False
        self._ws_closed: bool = False
        self.backoff: int = MIN_BACKOFF
        self.metrics: GatewayMetrics = GatewayMetrics(0.0, 0.0)
        self.heartbeat_task: asyncio.Task[None] | None = None # if Task is set, it returns None (GatewayClient.heartbeat)
        self.heartbeat_interval: int = 0
        self.event_queue: asyncio.Queue[tuple[str, JSON]] = asyncio.Queue()

        self.base_url = "wss://gateway.discord.gg"
        self.url_params = "?v=10&encoding=json"

    @property
    def ws(self) -> websockets.ClientConnection:
        if not self._ws:
            raise NoSession("Websocket session not started.")
        return self._ws

    async def wait_reconnect(self) -> None:
        """Sleep for exponentially increasing time between reconnects."""

        logger.warning(f"SHARD ID {self.shard_id}: Disconnected, reconnecting in {self.backoff}s...")
        await asyncio.sleep(self.backoff)

        self.backoff = min(self.backoff * 2, 60)

    async def start(self, token: str, intents: int, shard_id: int, total_shards: int) -> None:
        """Start this websocket's connection.

        Args:
            token (str): the bot's token
            intents (int): the bot's intents
        """
        self.shard_id = shard_id
        self.total_shards = total_shards

        while True:
            try:
                await self.connect_ws()

                if self.allow_resume and self.session_id and self.seq is not None:
                    logger.debug(f"SHARD ID {self.shard_id}: Attempting to resume...")
                    await self.resume(token)
                else:
                    logger.debug(f"SHARD ID {self.shard_id}: Attempting to identify...")
                    await self.identify(token, intents)

                await self._listen()  # blocks until disconnect

            except (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosed):
                logger.info(f"SHARD ID {self.shard_id}: Connection closed properly.")
                
                if not self._ws_closed:
                    await self.close_ws()

                if self.reconnect_immediately:
                    await self.wait_reconnect()
                    self.reconnect_immediately = False

            except (ConnectionError, websockets.exceptions.ConnectionClosedError) as e:
                logger.warning(f"SHARD ID {self.shard_id}: {e}")

                await self.close_ws()

                if self.reconnect_immediately:
                    await self.wait_reconnect()
                    self.reconnect_immediately = False

            except Exception:
                logger.exception(f"SHARD ID {self.shard_id}: Unexpected error")
                
                await self.close_ws()

                if self.reconnect_immediately:
                    await self.wait_reconnect()
                    self.reconnect_immediately = False

    async def connect_ws(self) -> None:
        """Connect to Discord's Gateway (websocket)."""

        self._ws_closed = False

        # connect to websocket
        self._ws = await websockets.connect(self.base_url + self.url_params)
        logger.info(f"SHARD ID {self.shard_id}: Connected to Discord!")

        # wait to recv HELLO
        hello = await self.receive()

        # extra info from recv'd HELLO
        self.heartbeat_interval = hello["d"]["heartbeat_interval"] / 1000

        # start heartbeat in background
        self.heartbeat_task = asyncio.create_task(self.heartbeat())

    async def send(self, data: JSON) -> None:
        """Send data through the websocket.

        Args:
            data (dict): data to send
        """
        await self.ws.send(json.dumps(data))

    async def receive(self) -> JSON:
        """Receive data through the websocket.

        Returns:
            (dict): websocket data
        """
        return dict(json.loads(await self.ws.recv()))

    async def heartbeat(self) -> None:
        """Heartbeat task to keep connection alive."""

        # add jitter only on before the first heartbeat
        import random
        jitter = random.uniform(0, 1)
        await asyncio.sleep(self.heartbeat_interval * jitter)

        while self.ws:
            self.metrics._last_heartbeat_sent = time.monotonic()
            await self.send({"op": 1, "d": self.seq})
            logger.debug(f"SHARD ID {self.shard_id}: Heartbeat sent")
            await asyncio.sleep(self.heartbeat_interval)

    async def identify(self, token: str, intents: int) -> None:
        """Send an IDENTIFY payload to handshake for bot.

        Args:
            token (str): the bot's token
            intents (int): the bot's intents

        Raises:
            (ConnectionError): invalid intents
        """

        if not isinstance(intents, int):
            raise ConnectionError("Invalid intents.")

        await self.send({
            'op': 2,
            'd': {
                'token': f"Bot {token}",
                'intents': intents,
                'properties': GATEWAY_PROPERTIES,
                'shards': [self.shard_id, self.total_shards]
            }
        })
        logger.info(f"SHARD ID {self.shard_id}: IDENIFY Sent.")

    async def resume(self, token: str) -> None:
        """Send a RESUME payload to resume a connection.

        Args:
            token (str): the bot's token
        """

        await self.send({
            'op': 6,
            'd': {
                'token': f"Bot {token}",
                'session_id': self.session_id,
                'seq': self.seq
            }
        })
        logger.info(f"SHARD ID {self.shard_id}: Resume Sent.")

    async def _listen(self) -> None:
        """Listen for events and queue them to be consumed by Client.

        Raises:
            (ConnectionError): an error occurred
        """

        while self.ws:
            data = await self.receive()
            op_code = data.get("op")

            match op_code:
                case 0:  # DISPATCH
                    if data.get('s') is not None:
                        self.seq = data['s']

                    event_data: JSON = data['d']
                    dispatcher_type: str = data['t']

                    if dispatcher_type == "READY":
                        self.session_id = event_data.get("session_id")
                        self.base_url = event_data.get("resume_gateway_url", self.base_url)
                        self.backoff = MIN_BACKOFF
                        
                    elif dispatcher_type == "RESUMED":
                        self.backoff = MIN_BACKOFF

                    await self.event_queue.put((dispatcher_type, event_data))

                case 7:  # RECONNECT
                    self.allow_resume = True
                    self.reconnect_immediately = True
                    logger.debug(f"SHARD ID {self.shard_id}: Reconnect requested by server.")

                    raise ConnectionError("Reconnect requested by server.")

                case 9:  # INVALID_SESSION
                    resumable = bool(data.get("d"))
                    self.allow_resume = resumable

                    if resumable:
                        logger.debug(f"SHARD ID {self.shard_id}: Invalid session (resumable).")
                    else:
                        self.session_id = self.seq = None
                        logger.debug(f"SHARD ID {self.shard_id}: Invalid session (not resumable).")

                    self.reconnect_immediately = True
                    raise ConnectionError("Invalid session.")

                case 11:  # HEARTBEAT_ACK
                    now = time.monotonic()

                    self.metrics.heartbeat_rrt = now - self.metrics._last_heartbeat_sent

                    logger.debug(f"SHARD ID {self.shard_id}: Heartbeat ACK ({round(self.metrics.heartbeat_rrt *1000)}ms)")

    async def close_ws(self) -> None:
        """Close the websocket connection if one is still open and cancels heartbeat."""

        if self._ws_closed or not self.ws:
            logger.debug(f"Shard ID {self.shard_id}: Connection already closed!")
            return
    
        self._ws_closed = True
        logger.info(f"Shard ID {self.shard_id}: Closing connection...")

        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
            self.heartbeat_task = None
        await self.ws.close()

        self._ws = None
