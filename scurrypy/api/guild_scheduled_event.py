from dataclasses import dataclass

from ..core.part import Part
from ..core.snowflake import Snowflake
from ..core.timestamp import Timestamp
from ..core.types import (
    RequiredPartField,
    RequiredNullablePartField,
    OptionalPartField
)

from ..enums.guild_scheduled_event import (
    GuildScheduledEventRecurrenceRuleWeekdayType,
    GuildScheduledEventRecurrenceRuleFrequencyType,
    GuildScheduledEventRecurrenceRuleMonthType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventEntityType
)

from .image_data import ImageDataPart

@dataclass
class RecurrenceRulePart(Part):
    """Represents fields for creating a scheduled event recurrence rule."""
    
    start: RequiredPartField[Timestamp] = None
    """Starting time of the recurrence interval."""
    
    end: RequiredNullablePartField[Timestamp] = None
    """Ending time of the recurrence interval."""
    
    frequency: RequiredPartField[GuildScheduledEventRecurrenceRuleFrequencyType] = None
    """How often the event occurs."""
    
    interval: RequiredPartField[int] = None
    """Spacing between the events as defined by frequency."""
    
    by_weekday: RequiredNullablePartField[list[GuildScheduledEventRecurrenceRuleWeekdayType]] = None
    """Set of specific days within a week for the event to recur."""
    
    # by_n_weekday: RequiredNullablePartField[list[GuildScheduledEventRecurrenceRuleNthWeekdayPart]] = None TODO: Add part!
    """List of specific days within a specific week (1-5) to recur."""
    
    by_month: RequiredNullablePartField[list[GuildScheduledEventRecurrenceRuleMonthType]] = None
    """Set of specific months to recur."""
    
    by_month_day: RequiredNullablePartField[list[int]] = None
    """Set of specific dates within a month to recur."""
    
    by_year_day: RequiredNullablePartField[list[int]] = None
    """Set of days within a year to recur."""
    
    count: RequiredNullablePartField[int] = None
    """Total amount of times that the event is allowed to recur before stopping."""

@dataclass
class GuildScheduledEventPart(Part):
    """Represents fields for creating a scheduled event."""
    
    channel_id: OptionalPartField[Snowflake] = None
    """Channel ID of the scheduled event."""
    
    name: RequiredPartField[str] = None
    """Name of the scheduled event."""
    
    privacy_level: RequiredPartField[GuildScheduledEventPrivacyLevel] = None
    """Privacy level of the scheduled event."""
    
    scheduled_start_time: RequiredPartField[Timestamp] = None
    """When the scheduled event is to be scheduled."""

    scheduled_end_time: OptionalPartField[Timestamp] = None
    """When the scheduled event is scheduled to end."""

    description: OptionalPartField[str] = None
    """Description of the scheduled event."""
    
    entity_type: RequiredPartField[GuildScheduledEventEntityType] = None
    """Entity type of the scheduled event."""
    
    image: OptionalPartField[ImageDataPart] = None
    """Cover image of the scheduled event."""
    
    recurrence_rule: OptionalPartField[RecurrenceRulePart] = None
    """How often the event should recur."""
