from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

@dataclass
class SessionStartLimit(Event, DataModel):
    """Represents the Session Start Limit object."""

    total: int
    """Total remaining shards."""

    remaining: int
    """Shards left to connect."""

    reset_after: int
    """When `remaining` resets from now (in ms)."""

    max_concurrency: int
    """How many shards can be started at once."""

@dataclass
class GatewayEvent(Event, DataModel):
    """Represents the Gateway Event object."""

    url: str 
    """Gateway URL to connect."""

    shards: int
    """Recommended shard count for the aaplication."""

    session_start_limit: SessionStartLimit
    """Session start info."""
