from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import RequiredPartField, OptionalPartField, OptionalNullablePartField, PresentModelField, OmittableModelField, OmittableNullableModelField

from ...enums.channel import ChannelType, AutoArchiveDurationType

from ..user import GuildMemberModel

from .channel import ChannelModel

@dataclass
class ThreadFromMessagePart(DataModel):
    """Parameters for creating a thread attached to a message."""

    name: RequiredPartField[str] = None
    """Name of the thread."""

    auto_archive_duration: OptionalPartField[AutoArchiveDurationType] = None
    """Duration in minutes threads will be hidden after period of inactivity."""

    rate_limit_per_user: OptionalNullablePartField[int] = None
    """Seconds user must wait between sending messages in the channel."""

@dataclass
class ThreadWithoutMessagePart(DataModel):
    """Parameters for creating a thread without a message."""

    name: RequiredPartField[str] = None
    """Name of the thread."""

    auto_archive_duration: OptionalPartField[AutoArchiveDurationType] = None
    """Duration in minutes threads will be hidden after period of inactivity."""

    type: OptionalPartField[ChannelType] = None
    """Type of thread to create. If omitted, Discord defaults to `ChannelType.PRIVATE_THREAD`."""

    invitable: OptionalPartField[bool] = None
    """Whether non-moderators can add other non-moderators to the thread (private threads only)."""

    rate_limit_per_user: OptionalNullablePartField[int] = None
    """Seconds user must wait between sending messages in the channel."""

@dataclass
class ThreadMetadataModel(DataModel):
    """Represents the thread metadata object."""

    archived: PresentModelField[bool]
    """Whether the thread is archived."""

    auto_archive_duration: PresentModelField[int]
    """How long to wait until the thread is hidden (in minutes)."""

    archive_timestamp: PresentModelField[str]
    """ISO8601 timestamp of when the thread's archive status was last changed."""

    locked: PresentModelField[bool]
    """Whether the thread is locked.
    
    !!! note
        Only users with `MANAGE_THREADS` can unarchive the thread.
    """

    invitable: OmittableModelField[bool]
    """Whether non-moderators can add other non-moderators to the thread (private threads only)."""

    create_timestamp: OmittableNullableModelField[str]
    """ISO8601 timestamp of thread creation (field only exists after Jan 09, 2022)."""

@dataclass
class ThreadMemberModel(DataModel):
    """Represents a user that has joined a thread."""

    id: OmittableModelField[Snowflake]
    """ID of the thread."""

    user_id: OmittableModelField[Snowflake]
    """ID of the user."""

    join_timestamp: PresentModelField[str]
    """ISO8601 timestamp of when the user last joined the thread."""

    member: OmittableModelField[GuildMemberModel]
    """Additional information about the user.
    
    !!! note
        Only present when `with_member` is toggled on request.
    """

@dataclass
class ArchivedThreadsModel(DataModel):
    """Response body for fetching archived threads."""

    threads: PresentModelField[list[ChannelModel]]
    """The archived threads."""

    members: PresentModelField[list[ThreadMemberModel]]
    """Thread member for each returned thread the bot has joined."""

    has_more: PresentModelField[bool]
    """Whether there are additional threads to be returned with subsequent calls."""

@dataclass
class ActiveThreadsModel(DataModel):
    """Response body for fetching active guild threads."""

    threads: PresentModelField[list[ChannelModel]]
    """The arctive threads."""

    members: PresentModelField[list[ThreadMemberModel]]
    """Thread member for each returned thread the bot has joined."""

@dataclass
class ThreadChannelModel(ChannelModel):
    """Represents the thread channel."""

    owner_id: OmittableModelField[Snowflake]
    """ID of the creator of the thread."""

    application_id: OmittableNullableModelField[Snowflake]
    """ID of the application that created thread."""

    thread_metadata: OmittableModelField[ThreadMetadataModel]
    """Thread-specific fields not needed by other channels."""

    member: OmittableModelField[ThreadMemberModel]
    """Thread member object for the current user if they have joined the thread."""

    default_auto_archive_duration: OmittableModelField[AutoArchiveDurationType]
    """Default duration in minutes threads will be hidden after period of inactivity."""
