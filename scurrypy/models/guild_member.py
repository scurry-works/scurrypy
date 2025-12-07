from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from .user import UserModel

@dataclass
class GuildMemberModel(DataModel):
    """Represents a guild member."""

    roles: list[int]
    """List of roles registered to the guild member."""

    user: UserModel
    """User data associated with the guild member."""

    nick: str
    """Server nickname of the guild member."""

    avatar: str
    """Server avatar hash of the guild mmeber."""

    joined_at: str
    """ISO8601 timestamp of when the guild member joined server."""

    deaf: bool
    """If the member is deaf in a VC (input)."""

    mute: bool
    """If the member is muted in VC (output)."""

    permissions: Optional[int]
    """Total permissions of the member in the channel, including overwrites, 
        returned when in the interaction object. [`INT_LIMIT`]
    """
