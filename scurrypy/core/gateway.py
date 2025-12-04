import asyncio
import json
import websockets

from .logger import LoggerLike

class GatewayClient:
    def __init__(self, gateway_url: str, shard_id: int, total_shards: int, logger: LoggerLike):
        """Initialize this websocket.

        Args:
            gateway_url (str): gateway URL provided by GET /gateway/bot endpoint
            shard_id (int): assigned shard ID
            total_shards (int): total shard count provided by GET /gateway/bot endpoint
            logger (LoggerLike): logger instance for logging events
        """
        self.logger = logger
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

    async def connect_ws(self):
        """Connect to Discord's Gateway (websocket)."""

        try:
            # connect to websocket
            self.ws = await websockets.connect(self.base_url + self.url_params)
            self.logger.log_high_priority(f"SHARD ID {self.shard_id}: Connected to Discord!")

            # wait to recv HELLO
            hello = await self.receive()

            # extra info from recv'd HELLO
            self.heartbeat_interval = hello["d"]["heartbeat_interval"] / 1000
            self.seq = hello.get('s')

            # start heartbeat in background
            self.heartbeat_task = asyncio.create_task(self.heartbeat())

        except Exception as e:
            self.logger.log_error(f"SHARD ID {self.shard_id}: Connection Error - {e}")

    async def start(self, token, intents):
        """Starts the websocket and handles reconnections."""

        backoff = 1
        while True:
            try:
                await self.connect_ws()
                
                if self.allow_resume and self.session_id and self.seq:
                    await self.resume(token)
                else:
                    await self.identify(token, intents)
                
                await self._listen()  # blocks until disconnect

            except (ConnectionError, websockets.exceptions.ConnectionClosedError) as e:
                self.logger.log_error(f"SHARD ID {self.shard_id}: Disconnected: {e}, reconnecting in {backoff}s...")
                await self.close_ws()
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 30)
            except asyncio.CancelledError:
                # only break; don't close here — let Client handle shutdown
                break
            except Exception as e:
                self.logger.log_error(f"SHARD ID {self.shard_id}: Unhandled error - {e}")
                await self.close_ws()
                await asyncio.sleep(backoff)

    async def send(self, data: dict):
        """Send data through the websocket."""

        try:
            await self.ws.send(json.dumps(data))
        except Exception:
            raise

    async def receive(self):
        """Receive data through the websocket."""

        try:
            return json.loads(await self.ws.recv())
        except Exception:
            raise
    
    async def heartbeat(self):
        """Heartbeat task to keep connection alive."""
        while self.ws:
            await asyncio.sleep(self.heartbeat_interval)
            await self.send({"op": 1, "d": self.seq})
            self.logger.log_info(f"SHARD ID {self.shard_id} Heartbeat sent")

    async def identify(self, token, intents):
        """Send an IDENTIFY payload to handshake for bot."""

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
        self.logger.log_info(f"SHARD ID {self.shard_id}: IDENIFY Sent.")

    async def resume(self, token):
        """Send a RESUME payload to resume a connection."""

        await self.send({
            'op': 6,
            'd': {
                'token': f"Bot {token}",
                'session_id': self.session_id,
                'seq': self.seq
            }
        })
        self.logger.log_info("Resume Sent.")

    async def _listen(self):
        """Listen for events and queue them to be picked up by Client."""

        while self.ws:
            try:
                data = await self.receive()

                op_code = data.get('op')
                
                match op_code:
                    case 0:
                        dispatcher_type = data.get('t')
                        self.logger.log_info(f"SHARD ID {self.shard_id} DISPATCH -> {dispatcher_type}")
                        event_data = data.get('d')
                        self.seq = data.get('s') or self.seq

                        if dispatcher_type == 'READY':
                            self.session_id = event_data.get('session_id')
                            self.base_url = event_data.get('resume_gateway_url') or self.base_url

                        await self.event_queue.put((dispatcher_type, event_data))
                    case 7:
                        self.allow_resume = True
                        raise ConnectionError("Reconnect requested by server.")
                    case 9:
                        self.session_id = self.seq = None
                        self.allow_resume = False
                        raise ConnectionError("Invalid session.")
                    case 11:
                        self.logger.log_info(f"SHARD ID {self.shard_id}: Heartbeat ACK")

            except websockets.exceptions.ConnectionClosed as e:
                if e.code in (4009, 4011):
                    self.allow_resume = True
                else:
                    self.session_id = self.seq = None
                    self.allow_resume = False
                break

            except Exception as e:
                self.logger.log_error(f"SHARD ID {self.shard_id}: Listen Error - {e}")
                break
    
    async def close_ws(self):
        """Close the websocket connection if one is still open."""

        self.logger.log_high_priority(f"Closing Shard ID {self.shard_id}...")
        if self.ws:
            if self.heartbeat_task:
                self.heartbeat_task.cancel()
                try:
                    await self.heartbeat_task
                except asyncio.CancelledError:
                    pass
            await self.ws.close()

        self.ws = None
