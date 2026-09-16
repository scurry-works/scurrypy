from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import PresentModelField, PresentNullableModelField, RequiredPartField, RequiredNullablePartField

@dataclass
class GuildWelcomeChannelModel(DataModel):
    """Represents channels shown on a welcome screen."""

    channel_id: PresentModelField[Snowflake]
    """ID of the channel."""

    description: PresentModelField[str]
    """Description for the channel."""

    emoji_id: PresentNullableModelField[Snowflake]
    """Emoji ID for the welcome screen (if custom)."""

    emoji_name: PresentNullableModelField[str]
    """Emoji name for the welcome screen."""

@dataclass
class GuildWelcomeScreenModel(DataModel):
    """Represents a guild's welcome screen."""

    description: PresentNullableModelField[str]
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
