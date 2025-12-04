from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from .message import MessageModel

@dataclass
class PinnedMessageModel(DataModel):
    """Pinned message data."""

    message: MessageModel
    """Message resource of the pinned message."""

    pinned_at: Optional[str]
    """ISO8601 timestamp of when the message was pinned."""

@dataclass
class ChannelModel(DataModel):
    """Represents a Discord guild channel."""

    id: int
    """ID of the channel."""

    type: Optional[int]
    """Type of channel."""

    guild_id: Optional[int]
    """Guild ID of the channel."""

    parent_id: Optional[int]
    """Category ID of the channel."""

    position: Optional[int]
    """Position of the channel."""

    name: Optional[str]
    """Name of the channel."""

    topic: Optional[str]
    """Topic of the channel."""

    nsfw: Optional[bool]
    """If the channel is flagged NSFW."""

    last_message_id: Optional[int]
    """ID of the last message sent in the channel."""

    last_pin_timestamp: Optional[str]
    """ISO8601 timestamp of the last pinned messsage in the channel."""

    rate_limit_per_user: Optional[int]
    """Seconds user must wait between sending messages in the channel."""
