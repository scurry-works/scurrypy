import asyncio
import json
import websockets

import logging

logger = logging.getLogger(__name__)

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
        self.heartbeat_task = None
        self.heartbeat_interval = None
        self.event_queue = asyncio.Queue()

        self.base_url = gateway_url
        self.url_params = "?v=10&encoding=json"

    async def wait_reconnect(self, backoff: float):
        import random

        backoff = min(backoff * 2, 60)
        backoff *= random.uniform(0.8, 1.2)
        
        logger.warning(f"SHARD ID {self.shard_id}: Disconnected, reconnecting in {backoff}s...")
        await asyncio.sleep(backoff)

        return backoff

    async def start(self, token, intents):
        backoff = 5

        while True:
            try:
                await self.connect_ws()

                if self.allow_resume and self.session_id and self.seq:
                    await self.resume(token)
                else:
                    await self.identify(token, intents)

                await self._listen()  # blocks until disconnect
                backoff = 5  # reset after successful connection

            except websockets.exceptions.ConnectionClosedOK:
                logger.info(f"SHARD ID {self.shard_id}: Connection closed properly.")
                break

            except (ConnectionError, websockets.exceptions.ConnectionClosedError) as e:
                logger.error(f"SHARD ID {self.shard_id}: {e}")
                await self.close_ws()

                backoff = await self.wait_reconnect(backoff)

            except Exception:
                logger.exception(f"SHARD ID {self.shard_id}: Unexpected error")
                await self.close_ws()
                
                backoff = await self.wait_reconnect(backoff)

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
        """Send data through the websocket."""
        await self.ws.send(json.dumps(data))

    async def receive(self):
        """Receive data through the websocket."""
        return json.loads(await self.ws.recv())

    async def heartbeat(self):
        """Heartbeat task to keep connection alive."""
        
        import random
        jitter = random.uniform(0.5, 1.0)

        while self.ws:
            await asyncio.sleep(self.heartbeat_interval * jitter)
            await self.send({"op": 1, "d": self.seq})
            logger.info(f"SHARD ID {self.shard_id}: Heartbeat sent")

    async def identify(self, token: str, intents: int):
        """Send an IDENTIFY payload to handshake for bot."""

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
        """Send a RESUME payload to resume a connection."""

        await self.send({
            'op': 6,
            'd': {
                'token': f"Bot {token}",
                'session_id': self.session_id,
                'seq': self.seq
            }
        })
        logger.info(f"SHARD ID {self.shard_id}: Resume Sent.")

    async def _listen(self):
        """Listen for events and queue them to be picked up by Client."""

        while self.ws:
            data = await self.receive()
            op_code = data.get("op")

            match op_code:
                case 0:  # DISPATCH
                    self.seq = data.get("s") or self.seq
                    dispatcher_type = data.get("t")

                    if dispatcher_type == "READY":
                        self.session_id = data["d"].get("session_id")
                        self.base_url = data["d"].get("resume_gateway_url", self.base_url)

                    await self.event_queue.put((dispatcher_type, data["d"]))

                case 7:  # RECONNECT
                    self.allow_resume = True
                    raise ConnectionError("Reconnect requested by server")

                case 9:  # INVALID_SESSION
                    resumable = data.get("d", False)
                    self.allow_resume = resumable
                    if not resumable:
                        self.session_id = self.seq = None
                    raise ConnectionError("Invalid session")

                case 11:  # HEARTBEAT_ACK
                    logger.info(f"SHARD ID {self.shard_id}: Heartbeat ACK")

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
