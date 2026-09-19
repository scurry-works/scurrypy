import logging

logger = logging.getLogger('scurrypy')

from scurrypy import Client
from scurrypy.bases import Addon
from scurrypy.enums import EventType
from scurrypy.core import DiscordError, InvalidCallbackSignature, DataModelTypeError
from scurrypy.api.interactions import MessageComponentDataModel, ModalDataModel
from scurrypy.events import InteractionEvent

from .ctx import MessageComponentContext, ComponentModalContext, ComponentContext

from collections.abc import Callable, Awaitable

type AddonHandler = Callable[[ComponentContext], Awaitable[None]]

type AddonDecorator = Callable[[AddonHandler], AddonHandler]

def _check_func_params(func: AddonHandler) -> None:
    """Inspect a user-defined function callback for component interactions.

    Args:
        func (AddonHandler): function callback

    Raises:
        (InvalidCallbackSignature): invalid signature
    """
    import inspect

    if not inspect.iscoroutinefunction(func):
        raise InvalidCallbackSignature(f"Component handler '{func.__name__}' must be async.")
    
    params_len = len(inspect.signature(func).parameters)

    if params_len != 1:
        raise InvalidCallbackSignature(f"Component handler '{func.__name__}' must accept exactly one parameter (ctx).")

class ComponentsAddon(Addon):
    """Addon that implements automatic registering and decorating component interactions."""

    def __init__(self, client: Client):
        """
        Args:
            client (Client): the bot client object
        """
        self.bot = client

        self.component_handlers: dict[str, AddonHandler] = {}
        """Mapping of component custom IDs to handler."""

        client.add_startup_hook(self.on_startup) # wait until start to register commands

    def on_startup(self) -> None:
        """Sets up the addon with the client."""

        self.bot.add_event_listener(EventType.INTERACTION_CREATE, self.dispatch)

    def component(self, custom_id: str, *, handler: AddonHandler | None = None) -> AddonDecorator | None:
        """Common function for registering components.

        Args:
            custom_id (str): custom ID of component
            handler (AddonHandler, optional): callback for component (if not a decorator)
        """
        if handler is None:
            def decorator(func: AddonHandler) -> AddonHandler:
                _check_func_params(func)
                self.component_handlers[custom_id] = func
                return func
            return decorator
        
        _check_func_params(handler)
        self.component_handlers[custom_id] = handler
        return None
    
    # helpers purly for ergonomics
    def button(self, custom_id: str, *, handler: AddonHandler | None = None) -> AddonDecorator | None:
        """Register and route button interactions.

        Args:
            custom_id (str): custom ID of button
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
            handler (AddonHandler, optional): callback for the command (if not a decorator)
        """
        return self.component(custom_id, handler=handler)

    def select(self, custom_id: str, *, handler: AddonHandler | None = None) -> AddonDecorator | None:
        """Register and route select menu interactions.

        Args:
            custom_id (str): custom ID of select menu
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
            handler (AddonHandler, optional): callback for the command (if not a decorator)
        """
        return self.component(custom_id, handler=handler)

    def modal(self, custom_id: str, *, handler: AddonHandler | None = None) -> AddonDecorator | None:
        """Register and route modal interactions.

        Args:
            custom_id (str): custom ID of modal
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
            handler (AddonHandler, optional): callback for the command (if not a decorator)
        """
        return self.component(custom_id, handler=handler)

    def _get_handler(self, name: str) -> AddonHandler | None:
        """Helper function for fetching a handler by `fnmatch`.

        Args:
            name (str): handler name
        """

        import fnmatch
        for k, v in self.component_handlers.items():
            if fnmatch.fnmatch(name, k):
                return v
        return None

    async def dispatch(self, event: InteractionEvent) -> None:
        """Dispatch a response to an `INTERACTION_CREATE` event

        Raises:
            (DataModelTypeError): no component context

        Args:
            event (InteractionEvent): interaction event object
        """
        # only respond to component interactions
        data = event.data

        if not isinstance(data, (MessageComponentDataModel, ModalDataModel)):
            return # ignore non-component interactions

        name = data.custom_id
        handler = self._get_handler(name)

        if handler is None:
            logger.warning(f"No handler registered for interaction '{name}'")
            return
        
        ctx: ComponentContext
        
        if isinstance(data, MessageComponentDataModel):
            ctx = MessageComponentContext(self.bot, event)
        
        elif isinstance(data, ModalDataModel):
            ctx = ComponentModalContext(self.bot, event)

        else:
            raise DataModelTypeError("Component context could not be resolved.")

        try:
            await handler(ctx)
            logger.info(f"Interaction '{name}' Acknowledged.")
        except DiscordError as e:
            logger.error(f"Error in interaction '{name}': {e}")
        except Exception as e:
            logger.exception(f"Unhandled error in interaction '{name}': {e}")
