from dataclasses import dataclass

from ...core.part import Part
from ...core.types import RequiredNullablePartField

@dataclass
class DefaultReactionPart(Part):
    """Represents fields for creating a default reaction for a `GUILD_FORUM` post."""

    emoji_id: RequiredNullablePartField[int] = None
    """ID of the guild's custom emoji."""

    emoji_name: RequiredNullablePartField[str] = None
    """Unicode character of the emoji."""
