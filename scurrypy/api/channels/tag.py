from dataclasses import dataclass

from ...core.part import Part
from ...core.snowflake import Snowflake
from ...core.types import (
    RequiredPartField, 
    RequiredNullablePartField, 
    OptionalPartField
)

@dataclass
class TagPart(Part):
    """Represents fields for creating a tag object found in `GUILD_FORUM` channels."""
    
    name: RequiredPartField[str] = None
    """Name of the tag."""

    moderated: OptionalPartField[bool] = None
    """Whether the tag can only be added/removed by a member with `MANAGE_THREADS`."""
    
    emoji_id: RequiredNullablePartField[Snowflake] = None
    """ID of a guild's custom emoji."""
    
    emoji_name: RequiredNullablePartField[str] = None
    """Unicode character of the emoji."""
