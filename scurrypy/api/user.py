from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake
from ..core.types import PresentModelField, PresentNullableModelField, OmittableModelField, OmittableNullableModelField

from ..enums.permissions import Permissions

@dataclass
class UserModel(DataModel):
    """Represents the User object."""

    id: PresentModelField[Snowflake]
    """ID of the user."""

    username: PresentModelField[str]
    """Username of the user."""

    discriminator: PresentModelField[str]
    """Discriminator of the user (#XXXX)"""

    global_name: PresentNullableModelField[str]
    """Global name of the user."""

    avatar: PresentNullableModelField[str]
    """Image hash of the user's avatar."""

    bot: OmittableModelField[bool]
    """If the user is a bot."""

    banner: OmittableNullableModelField[str]
    """Image hash of the user's banner."""

    accent_color: OmittableNullableModelField[int]
    """Color of user's banner represented as an integer."""

    locale: OmittableModelField[str]
    """Chosen language option of the user."""

@dataclass
class GuildMemberModel(DataModel):
    """Represents a guild member."""

    user: OmittableModelField[UserModel]
    """User data associated with the guild member."""

    nick: OmittableNullableModelField[str]
    """Server nickname of the guild member."""

    avatar: OmittableNullableModelField[str]
    """Server avatar hash of the guild mmeber."""

    roles: PresentModelField[list[Snowflake]]
    """List of roles registered to the guild member."""

    joined_at: PresentNullableModelField[str]
    """ISO8601 timestamp of when the guild member joined server."""

    permissions: OmittableModelField[Permissions]
    """Total permissions of the member in the channel, including overwrites, 
        returned when in the interaction object. [`INT_LIMIT`]
    """
