from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from typing import Optional

@dataclass
class GuildChannelEvent(Event, DataModel):
    """Base guild channel event."""

    id: int
    """ID of the guild channel."""

    type: int
    """Type of channel."""

    guild_id: Optional[int]
    """Guild ID of the channel."""

    position: Optional[int]
    """Position of the channel within a category."""

    name: Optional[str]
    """Name of the channel."""

    topic: Optional[str]
    """Topic of the channel."""

    nsfw: Optional[bool]
    """If this channel is flagged NSFW."""

    last_message_id: Optional[int]
    """ID of the last message sent in the channel."""

    parent_id: Optional[int]
    """Category ID of the channel."""

class GuildChannelCreateEvent(GuildChannelEvent):
    """Received when a guild channel has been created."""
    pass

class GuildChannelUpdateEvent(GuildChannelEvent):
    """Received when a guild channel has been updated."""
    pass

class GuildChannelDeleteEvent(GuildChannelEvent):
    """Received when a guild channel has been deleted."""
    pass

@dataclass
class ChannelPinsUpdateEvent(Event, DataModel):
    """Pin update event."""
    
    channel_id: int
    """ID of channel where the pins were updated."""

    guild_id: Optional[int]
    """ID of the guild where the pins were updated."""

    last_pin_timestamp: Optional[str]  # ISO8601 timestamp of last pinned message
    """ISO8601 formatted timestamp of the last pinned message in the channel."""
