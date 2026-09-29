from ..core.model import datamodel
from ..core.snowflake import Snowflake
from ..core.timestamp import Timestamp
from ..core.types import PresentModelField, PresentNullableModelField, ScurrypyStr

from .base_event import Event

from ..enums.events import EventType

from ..api.user import UserModel, GuildMemberModel

@datamodel
class UserUpdateEvent(Event, UserModel):
    """Received when a user's settings are updated."""
    
    dispatch_name = EventType.USER_UPDATE

@datamodel
class GuildMemberAddEvent(Event, GuildMemberModel):
    """Received when a member joins a guild the bot is in.

    !!! warning
        Requires privileged `GUILD_MEMBERS` intent.
    """

    dispatch_name = EventType.GUILD_MEMBER_ADD

    guild_id: PresentModelField[Snowflake]
    """ID of the guild."""

@datamodel
class GuildMemberUpdateEvent(Event):
    """Received when a guild member is updated.
    
    !!! warning
        Requires privileged `GUILD_MEMBERS` intent.
    """

    dispatch_name = EventType.GUILD_MEMBER_UPDATE

    guild_id: PresentModelField[Snowflake]
    """ID of the guild."""

    roles: PresentModelField[list[Snowflake]]
    """List of user's roles (their IDs)."""

    user: PresentModelField[UserModel]
    """The User object."""

    avatar: PresentNullableModelField[ScurrypyStr]
    """Guild avatar hash."""

    banner: PresentNullableModelField[ScurrypyStr]
    """Guild banner hash."""

    joined_at: PresentNullableModelField[Timestamp]
    """When the user joined the guild"""

@datamodel
class GuildMemberRemoveEvent(Event):
    """Received when a member leaves or is kicked/banned from a guild the bot is in.
    
    !!! warning
        Requires privileged `GUILD_MEMBERS` intent.
    """

    dispatch_name = EventType.GUILD_MEMBER_REMOVE

    guild_id: PresentModelField[Snowflake]
    """ID of the guild."""

    user: PresentModelField[UserModel]
    """User object of the user leaving the guild."""
