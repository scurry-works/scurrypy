from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from ..models.user import UserModel
from ..models.guild import GuildModel

class ApplicationFlags:
    """Application flags (bitwise constants)."""

    GATEWAY_PRESENCE = 1 << 12
    """Privileged intent to receive presence_update events."""

    GATEWAY_PRESENCE_LIMITED = 1 << 13
    """Intent to receive presence_update events."""

    GATEWAY_GUILD_MEMBERS = 1 << 14
    """Privileged intent to receive member-related events."""

    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    """Intent to receive member-related events."""

    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    """Indicates unusual growth of an app that prevents verification."""

    GATEWAY_MESSAGE_CONTENT = 1 << 18
    """Privileged intent to receive message content."""

    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    """Intent to receive message content."""

@dataclass
class ApplicationModel(DataModel):
    """Represents a Discord application."""

    id: int
    """ID of the application."""

    name: str
    """Name of the application."""

    icon: Optional[str]
    """Icon hash of the application."""

    description: Optional[str]
    """Description of the application."""

    bot_public: Optional[bool]
    """If the application is public."""

    bot_require_code_grant: Optional[bool]
    """If full OAuth2 code grant is required."""

    bot: Optional[UserModel]
    """Partial bot user object of the application."""

    terms_of_service_url: Optional[str]
    """Terms of Service URL of the application"""

    privacy_policy: Optional[str]
    """Privacy Policy URL of the application."""

    owner: Optional[UserModel]
    """Partial user object of the owner of the application."""

    guild_id: Optional[int]
    """Guild ID associated with the application."""

    guild: Optional[GuildModel]
    """Partial guild object of the associated guild."""

    cover_image: Optional[str]
    """Image hash of rich presence invite cover."""

    flags: Optional[int]
    """Public flags of the application.
        See [`ApplicationFlags`][scurrypy.models.application.ApplicationFlags].
    """

    approximate_guild_count: Optional[int]
    """Approximate guild count of the guilds that installed the application."""
