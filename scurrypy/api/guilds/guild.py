from ...core.model import DataModel, datamodel
from ...core.snowflake import Snowflake
from ...core.types import (
    PresentModelField, 
    PresentNullableModelField, 
    OmittableModelField, 
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool
)

from ..emoji import EmojiModel
from .role import GuildRoleModel
from ..messages.sticker import StickerModel

@datamodel
class UnavailableGuildModel(DataModel):
    """Guild info during an outage or before bot bootup."""

    id: PresentModelField[Snowflake]
    """ID of the associated guild."""

    unavailable: PresentModelField[ScurrypyBool]
    """If the guild is offline."""

@datamodel
class GuildModel(DataModel):
    """Represents a Discord guild."""

    id: PresentModelField[Snowflake]
    """ID of the guild."""
    
    name: PresentModelField[ScurrypyStr]
    """Name of the guild."""

    icon: PresentNullableModelField[ScurrypyStr]
    """Image hash of the guild's icon."""

    splash: PresentNullableModelField[ScurrypyStr]
    """Image hash of the guild's splash."""

    owner: OmittableModelField[ScurrypyBool]
    """If the member is the owner."""

    owner_id: PresentModelField[Snowflake]
    """ID of the owner of the guild."""

    roles: PresentModelField[list[GuildRoleModel]]
    """Roles in the guild."""

    emojis: PresentModelField[list[EmojiModel]]
    """List of emojis registered in the guild."""

    stickers: OmittableModelField[list[StickerModel]]
    """List of custom guild stickers."""

    mfa_level: PresentModelField[ScurrypyInt]
    """Required MFA level of the guild."""

    application_id: PresentNullableModelField[Snowflake]
    """ID of the application if the guild is created by a bot."""

    system_channel_id: PresentNullableModelField[Snowflake]
    """Channel ID where system messages go (e.g., welcome messages, boost events)."""

    system_channel_flags: PresentModelField[ScurrypyInt]
    """System channel flags."""

    rules_channel_id: PresentNullableModelField[Snowflake]
    """Channel ID where rules are posted."""

    max_members: OmittableModelField[ScurrypyInt]
    """Maximum member capacity for the guild."""

    description: PresentNullableModelField[ScurrypyStr]
    """Description of the guild."""

    banner: PresentNullableModelField[ScurrypyStr]
    """Image hash of the guild's banner."""

    preferred_locale: PresentModelField[ScurrypyStr]
    """Preferred locale of the guild."""

    public_updates_channel_id: PresentNullableModelField[Snowflake]
    """Channel ID of announcement or public updates."""

    approximate_member_count: OmittableModelField[ScurrypyInt]
    """Approximate number of members in the guild."""

    nsfw_level: PresentModelField[ScurrypyInt]
    """NSFW level of the guild."""

    safety_alerts_channel_id: PresentNullableModelField[Snowflake]
    """Channel ID for safety alerts."""
