from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

@dataclass
class HelloEvent(Event, DataModel):
    """Heartbeat interval event."""

    heartbeat_interval: int
    """Heartbeat interval in milliseconds."""
