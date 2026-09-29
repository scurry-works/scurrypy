from ..core.model import datamodel
from ..core.snowflake import Snowflake
from ..core.timestamp import Timestamp
from ..core.types import (
    PresentModelField, 
    OmittableModelField, 
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool
)

from .base_event import Event

from ..enums.events import EventType

from ..api.channels import ChannelModel
from ..api.guilds import UnavailableGuildModel, GuildModel
from ..api.messages import StickerModel
from ..api.emoji import EmojiModel
from ..api.user import UserModel, GuildMemberModel

@datamodel
class GuildCreateEvent(Event, GuildModel):
    """Received when the bot has joined a guild."""

    dispatch_name = EventType.GUILD_CREATE
    
    joined_at: PresentModelField[Timestamp]
    """ISO8601 timestamp of when app joined the guild."""

    large: PresentModelField[ScurrypyBool]
    """If the guild is considered large."""

    member_count: PresentModelField[ScurrypyInt]
    """Total number of members in the guild."""

    members: PresentModelField[list[GuildMemberModel]]
    """Users in the guild."""

    channels: PresentModelField[list[ChannelModel]]
    """Channels in the guild."""

    threads: PresentModelField[list[ChannelModel]]
    """All active threads in the guild that are viewable."""

    unavailable: OmittableModelField[ScurrypyBool]
    """`True` if the guild is unavailable due to an outage."""

@datamodel
class GuildUpdateEvent(Event, GuildModel):
    """Received when a guild has been edited."""

    dispatch_name = EventType.GUILD_UPDATE

@datamodel
class GuildDeleteEvent(Event, UnavailableGuildModel):
    """Received when the bot has left a guild or the guild was deleted."""
    
    dispatch_name = EventType.GUILD_DELETE

@datamodel
class GuildBanAddEvent(Event):
    """Received when a user is banned from a guild.

    !!! important "Permissions"
        Requires `BAN_MEMBERS` or `VIEW_AUDIT_LOG`
    """

    dispatch_name = EventType.GUILD_BAN_ADD

    guild_id: PresentModelField[Snowflake]
    """ID of the guild in which the ban took place."""

    user: PresentModelField[UserModel]
    """The user who was banned."""

@datamodel
class GuildBanRemoveEvent(Event):
    """Received when a user is unbanned from a guild.

    !!! important "Permissions"
        Requires `BAN_MEMBERS` or `VIEW_AUDIT_LOG`
    """

    dispatch_name = EventType.GUILD_BAN_REMOVE

    guild_id: PresentModelField[Snowflake]
    """ID of the guild in which the ban took place."""

    user: PresentModelField[UserModel]
    """The user who was banned."""

@datamodel
class GuildEmojisUpdateEvent(Event):
    """Received when a guild updates their emojis."""

    dispatch_name = EventType.GUILD_EMOJIS_UPDATE

    guild_id: PresentModelField[Snowflake]
    """ID of the guild."""

    emojis: PresentModelField[list[EmojiModel]]
    """Complete set of guild emojis with changes."""

@datamodel
class GuildStickersUpdateEvent(Event):
    """Received when a guild's stickers have been updated."""

    dispatch_name = EventType.GUILD_STICKERS_UPDATE

    guild_id: PresentModelField[Snowflake]
    """ID of the guild."""

    stickers: PresentModelField[list[StickerModel]]
    """List of the guild's stickers."""
