from ..core.model import DataModel, datamodel
from ..core.snowflake import Snowflake
from ..core.types import (
    PresentModelField, 
    OmittableModelField, 
    PresentNullableModelField, 
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool
)

from ..enums.application import ApplicationFlags, ApplicationNewFlags

from .guilds.guild import GuildModel

from .user import UserModel

@datamodel
class ApplicationModel(DataModel):
    """Represents a Discord application."""

    id: PresentModelField[Snowflake]
    """ID of the application."""

    name: PresentModelField[ScurrypyStr]
    """Name of the application."""

    icon: PresentNullableModelField[ScurrypyStr]
    """Icon hash of the application."""

    description: PresentModelField[ScurrypyStr]
    """Description of the application."""

    bot_public: PresentModelField[ScurrypyBool]
    """If the application is public."""

    bot_require_code_grant: PresentModelField[ScurrypyBool]
    """If full OAuth2 code grant is required."""

    bot: OmittableModelField[UserModel]
    """Partial bot user object of the application."""

    terms_of_service_url: OmittableModelField[ScurrypyStr]
    """Terms of Service URL of the application"""

    privacy_policy: OmittableModelField[ScurrypyStr]
    """Privacy Policy URL of the application."""

    owner: OmittableModelField[UserModel]
    """Partial user object of the owner of the application."""

    guild_id: OmittableModelField[Snowflake]
    """Guild ID associated with the application."""

    guild: OmittableModelField[GuildModel]
    """Partial guild object of the associated guild."""

    cover_image: OmittableModelField[ScurrypyStr]
    """Image hash of rich presence invite cover."""

    flags: OmittableModelField[ApplicationFlags]
    """Public flags of the application."""

    flags_new: OmittableModelField[ApplicationNewFlags]
    """Plublic flags of the application beyond bit 30."""

    approximate_guild_count: OmittableModelField[ScurrypyInt]
    """Approximate guild count of the guilds that installed the application."""
