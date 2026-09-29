from ..core.model import datamodel
from ..core.snowflake import Snowflake
from ..core.timestamp import Timestamp
from ..core.types import (
    PresentModelField, 
    OmittableModelField, 
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool
)

from .base_event import Event

from ..enums.events import EventType

from ..api.user import UserModel

@datamodel
class InviteCreateEvent(Event):
    """Received when an invite is created."""

    dispatch_name = EventType.INVITE_CREATE

    channel_id: PresentModelField[Snowflake]
    """Channel ID in which the invite belongs."""

    code: PresentModelField[ScurrypyStr]
    """Invite code (unique ID)."""

    guild_id: OmittableModelField[Snowflake]
    """Guild ID in which the invite belongs."""

    inviter: OmittableModelField[UserModel]
    """User who created invite."""

    uses: PresentModelField[ScurrypyInt]
    """Number of times this invite was used."""

    max_uses: PresentModelField[ScurrypyInt]
    """Max number of times this invite can be used."""

    max_age: PresentModelField[ScurrypyInt]
    """Duration (in seconds) after which this invite expires."""

    temporary: PresentModelField[ScurrypyBool]
    """Whether this invite only grants temporary membership."""

    created_at: PresentModelField[Timestamp]
    """ISO8601 timestamp for when this invite was created."""


@datamodel
class InviteDeleteEvent(Event):
    """Received when an invite is deleted."""

    dispatch_name = EventType.INVITE_DELETE

    channel_id: PresentModelField[Snowflake]
    """Channel ID in which the invite belongs."""

    guild_id: OmittableModelField[Snowflake]
    """Guild ID in which the invite belongs."""

    code: PresentModelField[ScurrypyStr]
    """Unique invite code."""
