from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

class ChannelTypes:
    """
        Constants for channel types.

        !!! note
            Only supported Channel Types listed here
    """

    GUILD_TEXT = 0
    """Text channel within a server."""

    GUILD_CATEGORY = 4
    """Organizational category that contains up to 50 channels."""

    GUILD_ANNOUNCEMENT = 5
    """Channel that users can follow and crosspost into their own server (formerly news channels)."""

@dataclass
class GuildChannel(DataModel):
    """Parameters for creating/editing a guild channel."""

    name: Optional[str] = None
    """Name of the channel."""

    type: Optional[int] = None
    """Type of channel. See [`ChannelTypes`][scurrypy.parts.channel.ChannelTypes]."""

    topic: Optional[str] = None
    """Topic of channel."""

    position: Optional[int] = None
    """Sorting position of the channel (channels with the same position are sorted by id)."""

    parent_id: Optional[int] = None
    """ID of the parent category for a channel."""

    nsfw: Optional[bool] = None
    """Whether the channel is NSFW."""
