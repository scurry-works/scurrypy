from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from .emoji import EmojiModel
from .role import RoleModel

@dataclass
class ReadyGuildModel(DataModel):
    """Guild info from Ready event."""
    
    id: int
    """ID of the associated guild."""

    unavailable: bool
    """If the guild is offline."""

@dataclass
class UnavailableGuild(DataModel):
    id: int
    unavailable: bool

@dataclass
class GuildModel(DataModel):
    """Represents a Discord guild."""

    id: int
    """ID of the guild."""
    
    name: str
    """Name of the guild."""

    icon: str
    """Image hash of the guild's icon."""

    splash: str
    """Image hash of the guild's splash."""

    owner: Optional[bool]
    """If the member is the owner."""

    owner_id: int
    """OD of the owner of the guild."""

    roles: list[int]
    """List of IDs registered in the guild."""

    emojis: list[EmojiModel]
    """List of emojis registered in the guild."""

    roles: list[RoleModel]
    """Roles in the guild."""

    mfa_level: int
    """Required MFA level of the guild."""

    application_id: int
    """ID of the application if the guild is created by a bot."""

    system_channel_id: int
    """Channel ID where system messages go (e.g., welcome messages, boost events)."""

    system_channel_flags: int
    """System channel flags."""

    rules_channel_id: int
    """Channel ID where rules are posted."""

    max_members: Optional[int]
    """Maximum member capacity for the guild."""

    description: str
    """Description of the guild."""

    banner: str
    """Image hash of the guild's banner."""

    preferred_locale: str
    """Preferred locale of the guild."""

    public_updates_channel_id: int
    """Channel ID of announcement or public updates."""

    approximate_member_count: int
    """Approximate number of members in the guild."""

    nsfw_level: int
    """NSFW level of the guild."""

    safety_alerts_channel_id: int
    """Channel ID for safety alerts."""
