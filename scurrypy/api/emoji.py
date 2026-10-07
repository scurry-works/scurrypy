from dataclasses import dataclass

from ..core.part import Part
from ..core.snowflake import Snowflake
from ..core.types import (
    RequiredNullablePartField, 
    OptionalPartField, 
    RequiredPartField, 
)

from .image_data import ImageDataPart

from urllib.parse import quote

@dataclass
class EmojiPart(Part):
    """Represents a Discord emoji."""
    
    name: RequiredNullablePartField[str] = None
    """Name of emoji."""

    id: OptionalPartField[Snowflake] = None
    """ID of the emoji (if custom)."""

    animated: OptionalPartField[bool] = None
    """If the emoji is animated."""

    @property
    def api_code(self) -> str | None:
        """API code for this emoji (URL-safe)."""
        if self.name is None:
            return None
        # unicode emoji
        if self.id is None:
            return quote(self.name)
        # custom emoji
        if self.animated:
            return quote(f"a:{self.name}:{self.id}")
        
        return quote(f"{self.name}:{self.id}")

@dataclass
class ApplicationEmojiPart(Part):
    """Represents fields for creating a bot emoji."""
    
    name: RequiredPartField[str] = None
    """Name of the emoji."""
    
    image: RequiredPartField[ImageDataPart] = None
    """Image data for the icon of the emoji."""

@dataclass
class GuildEmojiPart(Part):
    """Represents fields for creating a guild emoji."""
    
    name: RequiredPartField[str] = None
    """Name of the emoji."""
    
    image: RequiredPartField[ImageDataPart] = None
    """Image data for the icon of the emoji."""
    
    roles: RequiredPartField[list[Snowflake]] = None
    """Roles able to use the emoji."""
