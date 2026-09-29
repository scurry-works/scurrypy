from ..core.model import DataModel, datamodel
from ..core.snowflake import Snowflake
from ..core.timestamp import Timestamp
from ..core.types import (
    PresentModelField, 
    PresentNullableModelField, 
    OmittableModelField, 
    OmittableNullableModelField,
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool
)

from ..enums.permissions import Permissions

@datamodel
class UserModel(DataModel):
    """Represents the User object."""

    id: PresentModelField[Snowflake]
    """ID of the user."""

    username: PresentModelField[ScurrypyStr]
    """Username of the user."""

    discriminator: PresentModelField[ScurrypyStr]
    """Discriminator of the user (#XXXX)"""

    global_name: PresentNullableModelField[ScurrypyStr]
    """Global name of the user."""

    avatar: PresentNullableModelField[ScurrypyStr]
    """Image hash of the user's avatar."""

    bot: OmittableModelField[ScurrypyBool]
    """If the user is a bot."""

    banner: OmittableNullableModelField[ScurrypyStr]
    """Image hash of the user's banner."""

    accent_color: OmittableNullableModelField[ScurrypyInt]
    """Color of user's banner represented as an integer."""

    locale: OmittableModelField[ScurrypyStr]
    """Chosen language option of the user."""

@datamodel
class GuildMemberModel(DataModel):
    """Represents a guild member."""

    user: OmittableModelField[UserModel]
    """User data associated with the guild member."""

    nick: OmittableNullableModelField[ScurrypyStr]
    """Server nickname of the guild member."""

    avatar: OmittableNullableModelField[ScurrypyStr]
    """Server avatar hash of the guild mmeber."""

    roles: PresentModelField[list[Snowflake]]
    """List of roles registered to the guild member."""

    joined_at: PresentNullableModelField[Timestamp]
    """ISO8601 timestamp of when the guild member joined server."""

    permissions: OmittableModelField[Permissions]
    """Total permissions of the member in the channel, including overwrites, 
        returned when in the interaction object. [`INT_LIMIT`]
    """
