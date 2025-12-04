from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from ..models.guild_member import GuildMemberModel
from ..models.channel import ChannelModel

@dataclass
class GuildEvent(Event, DataModel):
    """Base guild event."""
    
    joined_at: str
    """ISO8601 timestamp of when app joined the guild."""

    large: bool
    """If the guild is considered large."""

    member_count: int
    """Total number of members in the guild."""

    members: list[GuildMemberModel]
    """Users in the guild."""

    channels: list[ChannelModel]
    """Channels in the guild."""

class GuildCreateEvent(GuildEvent):
    """Received when the bot has joined a guild."""
    pass

class GuildUpdateEvent(GuildEvent):
    """Received when a guild has been edited."""
    pass

class GuildDeleteEvent(GuildEvent):
    """Received when the bot has left a guild or the guild was deleted."""
    pass

@dataclass
class GuildMemberAddEvent(Event, GuildMemberModel):
    """Received when a member joins a guild the bot is in."""

    guild_id: int
    """ID of the guild."""


from ..models.user import UserModel

@dataclass
class GuildMemberRemoveEvent(Event, DataModel):
    """Received when a member leaves or is kicked/banned from a guild the bot is in."""

    guild_id: int
    """ID of the guild."""

    user: UserModel
    """User object of the user leaving the guild."""
