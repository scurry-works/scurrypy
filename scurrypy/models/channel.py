from dataclasses import dataclass
from ..core.model import DataModel
from ..core.permissions import Permissions

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

    type: int
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

    permissions: Optional[int]
    """Permissions for the invoking user in this channel.
        Includes role and overwrite calculations. [`INT_LIMIT`]
    """

    def user_can(self, permission_bit: int):
        """Checks `permissions` to see if permission bit is toggled.

        !!! warning
            If `permission` field is `None`, this function always returns `False`.

        Args:
            permission_bit (int): permission bit. See [Permissions][scurrypy.core.permissions.Permissions].

        Returns:
            (bool): whether the user has this permission
        """
        if not self.permissions:
            return False
        return Permissions.has(self.permissions, permission_bit)
