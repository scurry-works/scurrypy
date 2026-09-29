from ..core.model import datamodel
from ..core.snowflake import Snowflake
from ..core.types import (
    PresentModelField, 
    OmittableModelField, 
    ScurrypyInt, 
    ScurrypyBool
)

from .base_event import Event

from ..enums.channel import ChannelType
from ..enums.events import EventType

from ..api.channels import ChannelModel
from ..api.channels import ThreadMemberModel

@datamodel
class ThreadCreateEvent(Event, ChannelModel):
    """Received when a thread is created."""

    dispatch_name = EventType.THREAD_CREATE

    newly_created: PresentModelField[ScurrypyBool]
    """Whether the thread has just been created."""

@datamodel
class ThreadUpdateEvent(Event, ChannelModel):
    """Received when a thread is updated.
    
    !!! note
        Not send when `last_message_id` is changed.
    """

    dispatch_name = EventType.THREAD_UPDATE

@datamodel
class ThreadDeleteEvent(Event):
    """Received when a thread is deleted."""

    dispatch_name = EventType.THREAD_DELETE

    id: PresentModelField[Snowflake]
    """ID of the thread."""
    
    guild_id: OmittableModelField[Snowflake]
    """Guild ID of the thread."""
    
    parent_id: OmittableModelField[Snowflake]
    """ID of the parent channel."""
    
    type: PresentModelField[ChannelType]
    """Type of thread."""

@datamodel
class ThreadMemberUpdateEvent(Event, ThreadMemberModel):
    """Received when a thread member for the bot is updated."""

    dispatch_name = EventType.THREAD_MEMBER_UPDATE

    guild_id: PresentModelField[Snowflake]
    """ID of the guild."""

@datamodel
class ThreadMembersUpdateEvent(Event):
    """Received when someone is added or removed from a thread.
    
    !!! important
        Without the `GUILD_MEMBERS` privileged intent, this event only fires if the 
        bot was added or removed from a thread.
    """

    dispatch_name = EventType.THREAD_MEMBERS_UPDATE

    id: PresentModelField[Snowflake]
    """ID of the thread."""

    guild_id: PresentModelField[Snowflake]
    """ID of the guild."""

    member_count: PresentModelField[ScurrypyInt]
    """Approximate number of members in the thread (max `50`)."""

    added_members: OmittableModelField[list[ThreadMemberModel]]
    """Users who were added to the thread"""

    removed_member_ids: OmittableModelField[list[Snowflake]]
    """ID of the users who were removed from the thread."""

@datamodel
class ThreadListSyncEvent(Event):
    """Received when the bot gains access to a channel."""

    dispatch_name = EventType.THREAD_LIST_SYNC

    guild_id: PresentModelField[Snowflake]
    """ID of the guild."""

    channel_ids: OmittableModelField[list[Snowflake]]
    """Parent channel IDs of the threads being synced."""

    threads: PresentModelField[list[ChannelModel]]
    """Active threads in the given channel that the bot can access."""

    members: PresentModelField[list[ThreadMemberModel]]
    """Thread members from the synced threads that the bot an access."""
