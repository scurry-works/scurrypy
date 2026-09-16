import logging

logger = logging.getLogger('scurrypy')

from scurrypy import Client
from scurrypy.bases import Addon
from scurrypy.enums import EventType
from scurrypy.core import DiscordError, InvalidCallbackSignature
from scurrypy.events import Event

from collections.abc import Callable, Awaitable
from typing import Any

type _AddonHandler[C: Event] = Callable[[Client, C], Awaitable[None]]

AddonHandler = _AddonHandler[Any]

type AddonDecorator = Callable[[AddonHandler], AddonHandler]

def _check_func_params(handler: AddonHandler) -> None:
    import inspect

    if not inspect.iscoroutinefunction(handler):
        raise InvalidCallbackSignature(f"Event handler '{handler.__name__}' must be async.")
    
    params_len = len(inspect.signature(handler).parameters)

    if params_len != 2:
        raise InvalidCallbackSignature(f"Event handler '{handler.__name__}' must accept exactly two parameters (bot, event).")

class EventsAddon(Addon):
    """Addon that implements automatic registering and decorating events."""

    def __init__(self, client: Client):
        """
        Args:
            client (Client): the Client object
        """
        self.bot = client

        self._events: dict[EventType, list[AddonHandler]] = {}
        """Maps EVENT_NAME to handlers."""

        client.add_startup_hook(self.on_startup)

    def on_startup(self) -> None:
        """Adds registered events to client's event listener."""

        # lead all registered events to this dispatch
        for dispatch_type in self._events.keys():
            self.bot.add_event_listener(dispatch_type, self.dispatch)

    def listen(self, event_name: EventType, *, handler: AddonHandler | None = None) -> AddonDecorator | None:
        """Register and route an event with params (bot, event).

        Raises:
            (InvalidCallbackSignature): invalid signature

        Args:
            event_name (str): event name
            handler (AddonHandler, optional): callback for the event (if not a decorator)
        """

        if handler is None:
            def decorator(func: AddonHandler) -> AddonHandler:
                _check_func_params(func)
                self._events.setdefault(event_name, []).append(func)
                return func
            return decorator

        _check_func_params(handler)
        self._events.setdefault(event_name, []).append(handler)
        return None

    async def dispatch(self, event: Event) -> None:
        """Addon's entry point.

        Args:
            event (Event): event data object
        """
        handlers = self._events.get(event.dispatch_name)

        if not handlers:
            return
        
        for handler in handlers:
            try:
                await handler(self.bot, event)
            except DiscordError as e:
                logger.error(f"Error in event '{handler}': {e}")
            except Exception as e:
                logger.exception(f"Unhandled error in event '{handler.__name__}': {e}")
