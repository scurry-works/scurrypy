from typing import TypedDict
from ..core.snowflake import Snowflake
from ..core.timestamp import Timestamp

from ..enums.guild_scheduled_event import (
    GuildScheduledEventPrivacyLevel, 
    GuildScheduledEventEntityType, 
    GuildScheduledEventStatus
)

from ..api import ImageDataPart, RecurrenceRulePart

class GuildScheduledEventParams(TypedDict, total=False):
    """Represents fields for editing a scheduled event."""

    channel_id: Snowflake | None
    """Channel ID of the scheduled event.
    
    !!! note
        Set to `None` if changing `entity_type` to `EXTERNAL`.
    """
    
    name: str
    """Name of the scheduled event."""
    
    privacy_level: GuildScheduledEventPrivacyLevel
    """Privacy level of the scheduled event."""
    
    scheduled_start_time: Timestamp
    """When the scheduled event is to be scheduled."""
    
    scheduled_end_time: Timestamp
    """When the scheduled event is scheduled to end."""
    
    description: str | None
    """Description of the scheduled event."""
    
    entity_type: GuildScheduledEventEntityType
    """Entity type of the scheduled event."""
    
    status: GuildScheduledEventStatus
    """Status of the scheduled event."""
    
    image: ImageDataPart
    """Cover image of the scheduled event."""
    
    recurrence_rule: RecurrenceRulePart
    """How often the event should recur."""
