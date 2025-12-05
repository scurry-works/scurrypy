from .addon import Addon
from ..client import Client
from ..core.error import DiscordError
from ..events.base_event import Event

class EventsAddon(Addon):
    """Addon that implements automatic registering and decorating events."""

    def __init__(self, client: Client):
        """
        Args:
            client (Client): the Client object
        """
        self.bot = client

        self.logger = client.logger

        self._events = {}
        """Maps EVENT_NAME to handlers."""

        client.addons.add(self)

    def setup(self):
        """Sets up the addon with the client."""
        self.bot.add_startup_hook(self.on_startup)

    def on_startup(self):
        """Adds registered events to client's event listener."""

        # lead all registered events to this dispatch
        for dispatch_type in self._events.keys():
            self.bot.add_event_listener(dispatch_type, self.dispatch)
        
    def event(self, event_name: str):
        """Register an event in which to listen.

        Args:
            event_name (str): event name
        """
        def decorator(func):
            self._events.setdefault(event_name, []).append(func)
        return decorator

    async def dispatch(self, event: Event):
        """Addon's entry point.

        Args:
            event (Event): event data object
        """
        handlers = self._events.get(event.name)

        if not handlers:
            return
        try:
            for handler in handlers:
                await handler(self.bot, event)
        except DiscordError as e:
            self.logger.log_error(f"Error in event '{handler}': {e}")
        except Exception as e:
            self.logger.log_error(f"Unhandled error in event '{handler.__name__}': {e}")
