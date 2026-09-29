from dataclasses import dataclass

from ...core.model import DataModel, datamodel
from ...core.snowflake import Snowflake
from ...core.types import (
    PresentModelField, 
    PresentNullableModelField, 
    RequiredPartField, 
    RequiredNullablePartField,
    ScurrypyStr
)

@datamodel
class GuildWelcomeChannelModel(DataModel):
    """Represents channels shown on a welcome screen."""

    channel_id: PresentModelField[Snowflake]
    """ID of the channel."""

    description: PresentModelField[ScurrypyStr]
    """Description for the channel."""

    emoji_id: PresentNullableModelField[Snowflake]
    """Emoji ID for the welcome screen (if custom)."""

    emoji_name: PresentNullableModelField[ScurrypyStr]
    """Emoji name for the welcome screen."""

@datamodel
class GuildWelcomeScreenModel(DataModel):
    """Represents a guild's welcome screen."""

    description: PresentNullableModelField[ScurrypyStr]
    """Guild description displayed."""

    welcome_channels: PresentModelField[list[GuildWelcomeChannelModel]]
    """Channels displayed on the welcome screen. Max `5`."""

@dataclass
class WelcomeScreenChannelPart(DataModel):
    """Represents fields for creating a welcome screen channel."""

    channel_id: RequiredPartField[Snowflake] = None
    """ID of the channel to display."""

    description: RequiredPartField[str] = None
    """Description for the channel to display."""

    emoji_id: RequiredNullablePartField[Snowflake] = None
    """ID of the emoji (if custom)."""

    emoji_name: RequiredNullablePartField[str] = None
    """Name of the emoji."""
