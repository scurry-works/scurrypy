import inspect
from ..core.base_client import BaseClient
from .addon import Addon

class AddonManager:
    """Defines constraits for custom addons."""

    def __init__(self, client: BaseClient):
        self.client = client

    # --- validation ---

    def _check_event(self, handler):
        """Inspects the addon's event handler.

        Args:
            handler (callable): addon's handler

        Raises:
            TypeError: invalid parameters
        """
        sig = inspect.signature(handler)
        if len(sig.parameters) != 1:
            raise TypeError(
                f"Addon listener '{handler.__name__}' must accept exactly one arg (event)."
            )

    def _check_hook(self, handler):
        """Inspects the addon's hook handler.

        Args:
            handler (callable): addon's handler

        Raises:
            TypeError: invalid parameters
        """
        sig = inspect.signature(handler)
        if len(sig.parameters) != 0:
            raise TypeError(
                f"Addon hook '{handler.__name__}' must accept no parameters."
            )

    # --- registration ---

    def add(self, addon: Addon):
        """Helper function to auto-register an addon on instantiation.

        Args:
            addon (Addon): the addon object
        """
        addon.setup()

    def add_event_listener(self, event_name: str, handler):
        """Register an addon's handler to an event name to receive the event.

        Args:
            event_name (str): name of event to receive
            handler (callable): addon's handler
        """
        self._check_event(handler)
        self.client.add_event_listener(event_name, handler)

    def add_startup_hook(self, handler):
        """Register an addon's handler to run on startup.

        Args:
            handler (callable): addon's handler
        """
        self._check_hook(handler)
        self.client.add_startup_hook(handler)

    def add_shutdown_hook(self, handler):
        """Register an addon's handler to run on shutdown.

        Args:
            handler (callable): addon's handler
        """
        self._check_hook(handler)
        self.client.add_shutdown_hook(handler)
