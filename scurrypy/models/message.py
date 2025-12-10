from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from .user import UserModel

@dataclass
class MessageModel(DataModel):
    """A Discord message."""

    id: int
    """ID of the message."""

    channel_id: int
    """Channel ID of the message."""

    author: UserModel
    """User data of author of the message."""
    
    content: str
    """Content of the message."""

    pinned: bool
    """If the message is pinned."""

    type: int
    """Type of message."""

    webhook_id: Optional[int]
    """ID of the webhook if the message is a webhook."""
