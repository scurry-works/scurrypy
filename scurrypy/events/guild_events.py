from dataclasses import dataclass
from ..core.model import DataModel
from typing import Optional
from .base_event import Event

from ..models.guild_member import GuildMemberModel
from ..models.channel import ChannelModel
from ..models.guild import UnavailableGuild, GuildModel

@dataclass
class GuildCreateEvent(Event, GuildModel):
    """Received when the bot has joined a guild."""
    
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

    threads: list[ChannelModel]
    """All active threads in the guild that are viewable."""

    unavailable: Optional[bool]
    """`True` if the guild is unavailable due to an outage."""

@dataclass
class GuildUpdateEvent(Event, DataModel):
    """Received when a guild has been edited."""

    id: int
    """ID of the guild."""

    name: str
    """Name of the guild."""

    icon: str
    """Image hash of the guild's icon."""

    description: str
    """Description of the guild."""

    banner: str
    """Image hash of the guild's banner."""

    joined_at: str
    """ISO8601 timestamp of when app joined the guild."""

    large: bool
    """If the guild is considered large."""

    member_count: int
    """Total number of members in the guild."""

@dataclass
class GuildDeleteEvent(Event, UnavailableGuild):
    """Received when the bot has left a guild or the guild was deleted."""
    pass

@dataclass
class GuildMemberAddEvent(Event, GuildMemberModel):
    """Received when a member joins a guild the bot is in.

    !!! warning
        Requires privileged `GUILD_MEMBERS` intent.
    """

    guild_id: int
    """ID of the guild."""


from ..models.user import UserModel

@dataclass
class GuildMemberUpdateEvent(Event, DataModel):
    """Received when a guild member is updated.
    
    !!! warning
        Requires privileged `GUILD_MEMBERS` intent.
    """
    guild_id: int
    """ID of the guild."""

    roles: list[int]
    """List of user's roles (their IDs)."""

    user: UserModel
    """The User object."""

    avatar: str
    """Guild avatar hash."""

    banner: str
    """Guild banner hash."""

    joined_at: str
    """When the user joined the guild"""

@dataclass
class GuildMemberRemoveEvent(Event, DataModel):
    """Received when a member leaves or is kicked/banned from a guild the bot is in.
    
    !!! warning
        Requires privileged `GUILD_MEMBERS` intent.
    """

    guild_id: int
    """ID of the guild."""

    user: UserModel
    """User object of the user leaving the guild."""


from ..models.emoji import EmojiModel

@dataclass
class GuildEmojisUpdateEvent(Event, DataModel):
    """Received when a guild updates their emojis."""

    guild_id: int
    """ID of the guild."""

    emojis: list[EmojiModel]
    """Complete set of guild emojis with changes."""
