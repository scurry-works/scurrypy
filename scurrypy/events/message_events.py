from ..core.model import datamodel
from ..core.snowflake import Snowflake
from ..core.types import PresentModelField, OmittableModelField

from .base_event import Event

from ..enums.events import EventType

from ..api.messages import MessageModel
from ..api.user import UserModel, GuildMemberModel
from ..api.channels import ChannelType

@datamodel
class MessageCreateEvent(Event, MessageModel):
    """Received when a message is created.
    
    !!! note
        `member` may be missing on `MESSAGE_CREATE` and `MESSAGE_UPDATE`. Use `author` when you need the user.
    """

    dispatch_name = EventType.MESSAGE_CREATE

    guild_id: OmittableModelField[Snowflake]
    """Guild ID of the updated message (if in a guild channel)."""

    member: OmittableModelField[GuildMemberModel]
    """Partial Member object of the author of the message."""

    mentions: PresentModelField[list[UserModel]]
    """Users specifically mentioned in the message."""

    channel_type: OmittableModelField[ChannelType]
    """Type of channel in which the message was sent."""

@datamodel
class MessageUpdateEvent(Event, MessageModel):
    """Received when a message is updated."""

    dispatch_name = EventType.MESSAGE_UPDATE

    guild_id: OmittableModelField[Snowflake]
    """Guild ID of the updated message (if in a guild channel)."""

    member: OmittableModelField[GuildMemberModel]
    """Partial Member object of the author of the message."""

    mentions: PresentModelField[list[UserModel]]
    """Users specifically mentioned in the message."""

    channel_type: OmittableModelField[ChannelType]
    """Type of channel in which the message was sent."""

@datamodel
class MessageDeleteEvent(Event):
    """Received when a message is deleted."""

    dispatch_name = EventType.MESSAGE_DELETE

    id: PresentModelField[Snowflake]
    """ID of the deleted message."""

    channel_id: PresentModelField[Snowflake]
    """Channel ID of the deleted message."""

    guild_id: OmittableModelField[Snowflake]
    """Guild ID of the deleted message (if in a guild channel)."""

@datamodel
class BulkMessageDeleteEvent(Event):
    """Received when bulk deleting messages."""

    dispatch_name = EventType.BULK_MESSAGE_DELETE

    ids: PresentModelField[list[Snowflake]]
    """IDs of the messages that were deleted."""

    channel_id: PresentModelField[Snowflake]
    """ID of the channel."""

    guild_id: OmittableModelField[Snowflake]
    """ID of the guild."""
