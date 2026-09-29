from ..core.model import datamodel
from ..core.types import PresentModelField, ScurrypyStr, ScurrypyInt

from .base_event import Event

@datamodel
class SessionStartLimit(Event):
    """Represents the Session Start Limit object."""

    total: PresentModelField[ScurrypyInt]
    """Total remaining shards."""

    remaining: PresentModelField[ScurrypyInt]
    """Shards left to connect."""

    reset_after: PresentModelField[ScurrypyInt]
    """When `remaining` resets from now (in ms)."""

    max_concurrency: PresentModelField[ScurrypyInt]
    """How many shards can be started at once."""

@datamodel
class GatewayEvent(Event):
    """Represents the Gateway Event object."""

    url: PresentModelField[ScurrypyStr] 
    """Gateway URL to connect."""

    shards: PresentModelField[ScurrypyInt]
    """Recommended shard count for the aaplication."""

    session_start_limit: PresentModelField[SessionStartLimit]
    """Session start info."""
