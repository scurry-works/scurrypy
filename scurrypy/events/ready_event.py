from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from ..models.user import UserModel
from ..models.guild import ReadyGuildModel
from ..models.application import ApplicationModel

@dataclass
class ReadyEvent(Event, DataModel):
    """Received when bot goes online."""

    v: int
    """API version number."""

    user: UserModel
    """Information about the user."""

    guilds: list[ReadyGuildModel]
    """List of guilds bot is in."""

    session_id: str
    """Used for resuming connections."""

    resume_gateway_url: str
    """Gateway URL for resuming connections."""

    shard: list[int]
    """Shard information associated with this session."""

    application: ApplicationModel
    """Partial application object. Contains ID and flags."""
