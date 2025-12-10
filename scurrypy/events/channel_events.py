from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from typing import Optional

from ..models.channel import ChannelModel

class GuildChannelCreateEvent(Event, ChannelModel):
    """Received when a guild channel has been created."""
    pass

class GuildChannelUpdateEvent(Event, ChannelModel):
    """Received when a guild channel has been updated."""
    pass

class GuildChannelDeleteEvent(Event, ChannelModel):
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
