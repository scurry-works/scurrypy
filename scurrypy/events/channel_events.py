from ..core.model import datamodel
from ..core.snowflake import Snowflake
from ..core.timestamp import Timestamp
from ..core.types import (
    PresentModelField, 
    OmittableModelField, 
    OmittableNullableModelField, 
    ScurrypyStr
)

from .base_event import Event

from ..enums.events import EventType

from ..api.channels import ChannelModel

@datamodel
class ChannelCreateEvent(Event, ChannelModel):
    """Received when a guild channel has been created."""
    
    dispatch_name = EventType.CHANNEL_CREATE

@datamodel
class ChannelUpdateEvent(Event, ChannelModel):
    """Received when a guild channel has been updated.

    !!! note
        Not send when `last_message_id` is changed.
    """

    dispatch_name = EventType.CHANNEL_UPDATE

@datamodel
class ChannelDeleteEvent(Event, ChannelModel):
    """Received when a guild channel has been deleted."""

    dispatch_name = EventType.CHANNEL_DELETE

@datamodel
class ChannelPinsUpdateEvent(Event):
    """Pin update event."""

    dispatch_name = EventType.CHANNEL_PINS_UPDATE
    
    channel_id: PresentModelField[Snowflake]
    """ID of channel where the pins were updated."""

    guild_id: OmittableModelField[Snowflake]
    """ID of the guild where the pins were updated."""

    last_pin_timestamp: OmittableNullableModelField[Timestamp]
    """ISO8601 formatted timestamp of the last pinned message in the channel."""

@datamodel
class WebhooksUpdateEvent(Event):
    """Received when a guild's channel webhook is created, updated, or deleted."""

    dispatch_name = EventType.WEBHOOKS_UPDATE

    guild_id: PresentModelField[Snowflake]
    """ID of the guild."""

    channel_id: PresentModelField[Snowflake]
    """ID of the channel."""
