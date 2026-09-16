from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import PresentModelField, PresentNullableModelField, RequiredPartField, RequiredNullablePartField, OptionalPartField

@dataclass
class TagModel(DataModel):
    """Represents the tag object found in `GUILD_FORUM` channels."""
    
    id: PresentModelField[Snowflake]
    """ID of the tag."""

    name: PresentModelField[str]
    """Name of the tag."""

    moderated: PresentModelField[bool]
    """Whether the tag can only be added/removed by a member with `MANAGE_THREADS`."""
    
    emoji_id: PresentNullableModelField[Snowflake]
    """ID of a guild's custom emoji."""
    
    emoji_name: PresentNullableModelField[str]
    """Unicode character of the emoji."""

@dataclass
class TagPart(DataModel):
    """Represents the tag object found in `GUILD_FORUM` channels."""
    
    name: RequiredPartField[str] = None
    """Name of the tag."""

    moderated: OptionalPartField[bool] = None
    """Whether the tag can only be added/removed by a member with `MANAGE_THREADS`."""
    
    emoji_id: RequiredNullablePartField[Snowflake] = None
    """ID of a guild's custom emoji."""
    
    emoji_name: RequiredNullablePartField[str] = None
    """Unicode character of the emoji."""
