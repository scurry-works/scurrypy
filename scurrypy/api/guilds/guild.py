from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import PresentModelField, PresentNullableModelField, OmittableModelField

from ..emoji import EmojiModel
from .role import GuildRoleModel

@dataclass
class UnavailableGuildModel(DataModel):
    """Guild info during an outage or before bot bootup."""

    id: PresentModelField[Snowflake]
    """ID of the associated guild."""

    unavailable: PresentModelField[bool]
    """If the guild is offline."""

@dataclass
class GuildModel(DataModel):
    """Represents a Discord guild."""

    id: PresentModelField[Snowflake]
    """ID of the guild."""
    
    name: PresentModelField[str]
    """Name of the guild."""

    icon: PresentNullableModelField[str]
    """Image hash of the guild's icon."""

    splash: PresentNullableModelField[str]
    """Image hash of the guild's splash."""

    owner: OmittableModelField[bool]
    """If the member is the owner."""

    owner_id: PresentModelField[Snowflake]
    """ID of the owner of the guild."""

    roles: PresentModelField[list[GuildRoleModel]]
    """Roles in the guild."""

    emojis: PresentModelField[list[EmojiModel]]
    """List of emojis registered in the guild."""

    mfa_level: PresentModelField[int]
    """Required MFA level of the guild."""

    application_id: PresentNullableModelField[Snowflake]
    """ID of the application if the guild is created by a bot."""

    system_channel_id: PresentNullableModelField[Snowflake]
    """Channel ID where system messages go (e.g., welcome messages, boost events)."""

    system_channel_flags: PresentModelField[int]
    """System channel flags."""

    rules_channel_id: PresentNullableModelField[Snowflake]
    """Channel ID where rules are posted."""

    max_members: OmittableModelField[int]
    """Maximum member capacity for the guild."""

    description: PresentNullableModelField[str]
    """Description of the guild."""

    banner: PresentNullableModelField[str]
    """Image hash of the guild's banner."""

    preferred_locale: PresentModelField[str]
    """Preferred locale of the guild."""

    public_updates_channel_id: PresentNullableModelField[Snowflake]
    """Channel ID of announcement or public updates."""

    approximate_member_count: OmittableModelField[int]
    """Approximate number of members in the guild."""

    nsfw_level: PresentModelField[int]
    """NSFW level of the guild."""

    safety_alerts_channel_id: PresentNullableModelField[Snowflake]
    """Channel ID for safety alerts."""
