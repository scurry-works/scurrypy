from dataclasses import dataclass

from ..core.model import DataModel

from .base_event import Event

from ..enums.events import EventType

from ..api.guilds.guild import UnavailableGuildModel

from ..api.user import UserModel
from ..api.application import ApplicationModel

@dataclass
class ReadyEvent(Event, DataModel):
    """Received when bot goes online."""

    dispatch_name = EventType.READY

    v: int
    """API version number."""

    user: UserModel
    """Information about the user."""

    guilds: list[UnavailableGuildModel]
    """List of guilds bot is in."""

    session_id: str
    """Used for resuming connections."""

    resume_gateway_url: str
    """Gateway URL for resuming connections."""

    shard: list[int]
    """Shard information associated with this session."""

    application: ApplicationModel
    """Partial application object. Contains ID and flags."""
