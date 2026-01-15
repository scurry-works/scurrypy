import asyncio
import json
import websockets

import logging

logger = logging.getLogger(__name__)

MIN_BACKOFF = 5

class GatewayClient:
    def __init__(self, gateway_url: str, shard_id: int, total_shards: int):
        """Initialize this websocket.

        Args:
            gateway_url (str): gateway URL provided by GET /gateway/bot endpoint
            shard_id (int): assigned shard ID
            total_shards (int): total shard count provided by GET /gateway/bot endpoint
        """
        self.shard_id = shard_id
        self.total_shards = total_shards
        self.ws = None
        self.seq = None
        self.session_id = None
        self.allow_resume = False # default: assume IDENTIFY
        self.backoff = MIN_BACKOFF
        self.heartbeat_task = None
        self.heartbeat_interval = None
        self.event_queue = asyncio.Queue()

        self.base_url = gateway_url
        self.url_params = "?v=10&encoding=json"

    async def wait_reconnect(self):
        """Sleep for exponentially increasing time between reconnects."""

        self.backoff = min(self.backoff * 2, 60)
        
        logger.warning(f"SHARD ID {self.shard_id}: Disconnected, reconnecting in {self.backoff}s...")
        await asyncio.sleep(self.backoff)

    async def start(self, token: str, intents: int):
        """Start this websocket's connection.

        Args:
            token (str): the bot's token
            intents (int): the bot's intents
        """
        while True:
            try:
                await self.connect_ws()

                if self.allow_resume and self.session_id:
                    logger.debug(f"SHARD ID {self.shard_id}: Attempting to resume...")
                    await self.resume(token)
                else:
                    logger.debug(f"SHARD ID {self.shard_id}: Attempting to identify...")
                    await self.identify(token, intents)

                await self._listen()  # blocks until disconnect

            except websockets.exceptions.ConnectionClosedOK:
                logger.info(f"SHARD ID {self.shard_id}: Connection closed properly.")
                break

            except (ConnectionError, websockets.exceptions.ConnectionClosedError) as e:
                logger.error(f"SHARD ID {self.shard_id}: {e}")
                await self.close_ws()

                await self.wait_reconnect()

            except Exception:
                logger.exception(f"SHARD ID {self.shard_id}: Unexpected error")
                await self.close_ws()
                
                await self.wait_reconnect()

    async def connect_ws(self):
        """Connect to Discord's Gateway (websocket)."""

        # connect to websocket
        self.ws = await websockets.connect(self.base_url + self.url_params)
        logger.info(f"SHARD ID {self.shard_id}: Connected to Discord!")

        # wait to recv HELLO
        hello = await self.receive()

        # extra info from recv'd HELLO
        self.heartbeat_interval = hello["d"]["heartbeat_interval"] / 1000
        self.seq = hello.get('s')

        # start heartbeat in background
        self.heartbeat_task = asyncio.create_task(self.heartbeat())

    async def send(self, data: dict):
        """Send data through the websocket.

        Args:
            data (dict): data to send
        """
        await self.ws.send(json.dumps(data))

    async def receive(self):
        """Receive data through the websocket.

        Returns:
            (dict): websocket data
        """
        return json.loads(await self.ws.recv())

    async def heartbeat(self):
        """Heartbeat task to keep connection alive."""

        # add jitter only on before the first heartbeat
        import random
        jitter = random.uniform(0, 1)
        await asyncio.sleep(self.heartbeat_interval * jitter)

        while self.ws:
            await self.send({"op": 1, "d": self.seq})
            logger.debug(f"SHARD ID {self.shard_id}: Heartbeat sent")
            await asyncio.sleep(self.heartbeat_interval)

    async def identify(self, token: str, intents: int):
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
                'properties': {
                    'os': 'my_os',
                    'browser': 'my_browser',
                    'device': 'my_device'
                },
                'shards': [self.shard_id, self.total_shards]
            }
        })
        logger.info(f"SHARD ID {self.shard_id}: IDENIFY Sent.")

    async def resume(self, token: str):
        """Send a RESUME payload to resume a connection.

        Args:
            token (str): the bot's token
        """

        await self.send({
            'op': 6,
            'd': {
                'token': f"Bot {token}",
                'session_id': self.session_id,
                'seq': self.seq or 0
            }
        })
        logger.info(f"SHARD ID {self.shard_id}: Resume Sent.")

    async def _listen(self):
        """Listen for events and queue them to be consumed by Client.

        Raises:
            (ConnectionError): an error occurred
        """

        while self.ws:
            data = await self.receive()
            op_code = data.get("op")

            match op_code:
                case 0:  # DISPATCH
                    self.seq = data.get("s") or self.seq
                    event_data = data.get('d')
                    dispatcher_type = data.get("t")

                    if dispatcher_type == "READY":
                        self.session_id = event_data.get("session_id")
                        self.base_url = event_data.get("resume_gateway_url", self.base_url)

                        # this is a stable connection so reset backoff
                        self.backoff = MIN_BACKOFF

                    await self.event_queue.put((dispatcher_type, event_data))

                case 7:  # RECONNECT
                    self.allow_resume = True
                    logger.debug(f"SHARD ID {self.shard_id}: Reconnect requested by server.")
                    raise ConnectionError("Reconnect requested by server.")

                case 9:
                    resumable = bool(data.get("d"))
                    self.allow_resume = resumable

                    if resumable:
                        logger.debug(f"SHARD ID {self.shard_id}: Invalid session (resumable).")
                    else:
                        self.session_id = self.seq = None
                        logger.debug(f"SHARD ID {self.shard_id}: Invalid session (not resumable).")

                    raise ConnectionError("Invalid session.")

                case 11:  # HEARTBEAT_ACK
                    logger.debug(f"SHARD ID {self.shard_id}: Heartbeat ACK")

    async def close_ws(self):
        """Close the websocket connection if one is still open and cancels heartbeat."""

        logger.info(f"Shard ID {self.shard_id}: Closing connection...")
        if self.ws:
            if self.heartbeat_task:
                self.heartbeat_task.cancel()
                try:
                    await self.heartbeat_task
                except asyncio.CancelledError:
                    pass
            await self.ws.close()

        self.ws = None
