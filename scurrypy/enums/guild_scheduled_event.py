from .enum_types import DiscordTypes

class GuildScheduledEventPrivacyLevel(DiscordTypes):
    """Represents how public the scheduled event is."""

    GUILD_ONLY = 2
    """Only visible to guild members."""

class GuildScheduledEventEntityType(DiscordTypes):
    """Represents types of schedule events."""

    EXTERNAL = 3
    """Takes place outside of Discord."""

class GuildScheduledEventStatus(DiscordTypes):
    """Represents statuses aa scheduled event can have."""

    SCHEDULED = 1
    """The event is scheduled."""

    ACTIVE = 2
    """The event is active."""

    COMPLETED = 3
    """The event has completed."""

    CANCELED = 4
    """The event was cancelled."""

class GuildScheduledEventRecurrenceRuleFrequencyType(DiscordTypes):
    """Represents how often a scheduled event should occur."""

    YEARLY = 0
    """The event occurs once a year."""

    MONTHLY = 1
    """The event occurs once a month."""

    WEEKLY = 2
    """The event occurs once a week."""

    DAILY = 3
    """The event occurs once a day."""

class GuildScheduledEventRecurrenceRuleWeekdayType(DiscordTypes):
    """Represents what days of the week an event will occur."""

    MONDAY = 0
    """The event occurs on a Monday."""

    TUESDAY = 1
    """The event occurs on a Tuesday."""
    
    WEDNESDAY = 2
    """The event occurs on a Wednesday."""

    THURSDAY = 3
    """The event occurs on a Thursday."""

    FRIDAY = 4
    """The event occurs on a Friday."""

    SATURDAY = 5
    """The event occurs on a Saturday."""

    SUNDAY = 6
    """The event occurs on a Sunday."""

class GuildScheduledEventRecurrenceRuleMonthType(DiscordTypes):
    """Represents what months of the year an event will occur."""

    JANUARY = 1
    """The event occurs in January."""

    FEBRUARY = 2
    """The event occurs in February."""

    MARCH = 3
    """The event occurs in March."""

    APRIL = 4
    """The event occurs in April."""

    MAY = 5
    """The event occurs in May."""

    JUNE = 6
    """The event occurs in June."""

    JULY = 7
    """The event occurs in July."""

    AUGUST = 8
    """The event occurs in August."""

    SEPTEMBER = 9
    """The event occurs in September."""

    OCTOBER = 10
    """The event occurs in October."""

    NOVEMBER = 11
    """The event occurs in November."""

    DECEMBER = 12
    """The event occurs in December."""
