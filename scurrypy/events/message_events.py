from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from typing import Optional

from ..models.message import MessageModel
from ..models.guild_member import GuildMemberModel

@dataclass
class MessageCreateEvent(Event, MessageModel):
    """Received when a message is created. (This event IS the MessageModel with extra fields)
    
    !!! note
        `member` may be missing on `MESSAGE_CREATE` and `MESSAGE_UPDATE`. Use `author` when you need the user.
    """

    guild_id: Optional[int]
    """Guild ID of the updated message (if in a guild channel)."""

    member: Optional[GuildMemberModel]  # guild-only author info
    """Partial Member object of the author of the message. See [`GuildMemberModel`][scurrypy.models.GuildMemberModel]."""

@dataclass
class MessageUpdateEvent(Event, MessageModel):
    """Received when a message is updated. (This event IS the MessageModel with extra fields)"""

    guild_id: Optional[int]
    """Guild ID of the updated message (if in a guild channel)."""

    member: Optional[GuildMemberModel]
    """Partial Member object of the author of the message. See [`GuildMemberModel`][scurrypy.models.GuildMemberModel]."""

@dataclass
class MessageDeleteEvent(Event, DataModel):
    """Received when a message is deleted."""

    id: int
    """ID of the deleted message."""

    channel_id: int
    """Channel ID of the deleted message."""

    guild_id: Optional[int]
    """Guild ID of the deleted message (if in a guild channel)."""
