from dataclasses import dataclass

from ...core.part import Part
from ...core.snowflake import Snowflake
from ...core.types import (
    RequiredPartField, 
    RequiredNullablePartField
)

@dataclass
class WelcomeScreenChannelPart(Part):
    """Represents fields for creating a welcome screen channel."""

    channel_id: RequiredPartField[Snowflake] = None
    """ID of the channel to display."""

    description: RequiredPartField[str] = None
    """Description for the channel to display."""

    emoji_id: RequiredNullablePartField[Snowflake] = None
    """ID of the emoji (if custom)."""

    emoji_name: RequiredNullablePartField[str] = None
    """Name of the emoji."""
