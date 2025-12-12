import asyncio

from .core.intents import Intents
from .core.base_client import BaseClient
from .core.gateway import GatewayClient

from .core.logger import Logger, LoggerLike
from .core.http import HTTPClient

class Client(BaseClient):
    """Main entry point for Discord bots.
        Ties together the moving parts: gateway, HTTP and event dispatching.
    """
    def __init__(self, 
        *,
        token: str,
        application_id: int,
        intents: int = Intents.DEFAULT,
        logger: LoggerLike = None
    ):
        """
        Args:
            token (str): the bot's token
            application_id (int): the bot's user ID
            intents (int, optional): gateway intents. Defaults to `Intents.DEFAULT`.
            logger (LoggerLike, optional): logger interface for logging events
        """
        if not token:
            raise ValueError("Token is required.")
        if not application_id:
            raise ValueError("Application ID is required.")

        self.token = token
        self.intents = intents
        self.application_id = application_id

        self.logger = logger or Logger()
        
        self._http = HTTPClient(self.logger)

        self.shards: list[GatewayClient] = []

        self.events = {}
        self.startup_hooks = []
        self.shutdown_hooks = []
    
    def run(self):
        """User-facing entry point for starting the client."""  

        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            self.logger.log_info("Shutdown requested via KeyboardInterrupt.")
        except Exception as e:
            self.logger.log_error(f"{type(e).__name__} {e}")
        finally:
            self.logger.log_high_priority("Bot shutting down.")
            self.logger.close()
