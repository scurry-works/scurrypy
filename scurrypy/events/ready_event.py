from ..core.model import datamodel
from ..core.types import (
    PresentModelField, 
    OmittableModelField, 
    ScurrypyStr, 
    ScurrypyInt
)

from .base_event import Event

from ..enums.events import EventType

from ..api.guilds import UnavailableGuildModel

from ..api.user import UserModel
from ..api.application import ApplicationModel

@datamodel
class ReadyEvent(Event):
    """Received when bot goes online."""

    dispatch_name = EventType.READY

    v: PresentModelField[ScurrypyInt]
    """API version number."""

    user: PresentModelField[UserModel]
    """Information about the user."""

    guilds: PresentModelField[list[UnavailableGuildModel]]
    """List of guilds bot is in."""

    session_id: PresentModelField[ScurrypyStr]
    """Used for resuming connections."""

    resume_gateway_url: PresentModelField[ScurrypyStr]
    """Gateway URL for resuming connections."""

    shard: OmittableModelField[list[ScurrypyInt]]
    """Shard information associated with this session."""

    application: PresentModelField[ApplicationModel]
    """Partial application object. Contains ID and flags."""
