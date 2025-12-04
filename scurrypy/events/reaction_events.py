from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from typing import Optional

from ..models.guild_member import GuildMemberModel
from ..models.emoji import EmojiModel

class ReactionType:
    """Reaction types."""

    NORMAL = 0
    """A standard emoji."""

    BURST = 1
    """A super emoji."""

@dataclass
class ReactionAddEvent(Event, DataModel):
    """Reaction added event."""

    type: int
    """Type of reaction added."""

    user_id: int
    """ID of user who added the emoji."""

    emoji: EmojiModel
    """Emoji used to react."""

    channel_id: int
    """ID of the channel where the reaction took place."""

    message_id: int
    """ID of the message where the reaction took place."""

    guild_id: Optional[int]
    """ID of the guild where the reaction took place (if in a guild)."""

    burst: bool
    """Whether the emoji is super."""

    member: Optional[GuildMemberModel]
    """Partial member object of the guild member that added the emoji (if in a guild)."""

    message_author_id: Optional[int]
    """ID of the user who sent the message where the reaction was added."""

@dataclass
class ReactionRemoveEvent(Event, DataModel):
    """Reaction removed event."""

    type: int
    """Type of reaction removed."""

    user_id: int
    """ID of user who removed their reaction."""

    emoji: EmojiModel
    """Emoji data of the emoji where the reaction was removed."""

    channel_id: int
    """ID of the channel where the reaction was removed."""

    message_id: int
    """ID of the message where the reaction was removed."""

    guild_id: Optional[int]
    """ID of the guild where the reaction was removed (if in a guild)."""

    burst: bool
    """If the emoji of the removed reaction is super."""

class ReactionRemoveAllEvent(Event, DataModel):
    """Remove all reactions event."""

    channel_id: int
    """ID of the channel where all reaction were removed."""

    message_id: int
    """ID of the message where all reaction were removed."""

    guild_id: Optional[int]
    """ID of the guild where all reaction were removed (if in a guild)."""

@dataclass
class ReactionRemoveEmojiEvent(Event, DataModel):
    """All reactions of a specific emoji removed."""

    emoji: EmojiModel
    """Emoji data of the removed reaction emoji."""

    channel_id: int
    """ID of the channel where the reaction emoji was removed."""

    message_id: int
    """ID of the message where the reaction emoji was removed."""

    guild_id: Optional[int]
    """ID of the guild where the reaction emoji was removed. (if in a guild)"""
