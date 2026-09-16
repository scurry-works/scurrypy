from dataclasses import dataclass
from urllib.parse import quote

from ..core.model import DataModel
from ..core.snowflake import Snowflake
from ..core.types import PresentModelField, OmittableModelField, RequiredPartField

from .image_data import ImageDataPart

@dataclass
class EmojiModel(DataModel):
    """Represents a Discord emoji."""
    
    name: PresentModelField[str]
    """Name of emoji."""

    id: OmittableModelField[Snowflake] = None
    """ID of the emoji (if custom)."""

    animated: OmittableModelField[bool] = False
    """If the emoji is animated. Defaults to `False`."""

    @property
    def is_custom(self) -> bool:
        return self.id is not None

    @property
    def mention(self) -> str:
        """Mention this emoji in a message."""
        if self.id is None: # standard emoji
            return self.name
        if self.animated:
            return f"<a:{self.name}:{self.id}>"
        
        return f"<:{self.name}:{self.id}>"

    @property
    def api_code(self) -> str:
        """API code for this emoji (URL-safe)."""
        if self.id is None:
            # unicode emoji
            return quote(self.name)

        # custom emoji
        if self.animated:
            return quote(f"a:{self.name}:{self.id}")
        
        return quote(f"{self.name}:{self.id}")

    @property
    def url(self) -> str | None:
        """Full qualifying link for this emoji.

        !!! warning "Important"
            This only works for custom Discord emojis (those with an ID). 
            Unicode emojis will return `None`.
        """
        if not self.id:
            return None
        
        ext = 'gif' if self.animated else 'png'

        return f"https://cdn.discordapp.com/emojis/{self.id}.{ext}"

@dataclass
class ApplicationEmojiPart(DataModel):
    """Represents fields for creating a bot emoji."""
    
    name: RequiredPartField[str] = None
    """Name of the emoji."""
    
    image: RequiredPartField[ImageDataPart] = None
    """Image data for the icon of the emoji."""

@dataclass
class GuildEmojiPart(DataModel):
    """Represents fields for creating a guild emoji."""
    
    name: RequiredPartField[str] = None
    """Name of the emoji."""
    
    image: RequiredPartField[ImageDataPart] = None
    """Image data for the icon of the emoji."""
    
    roles: RequiredPartField[list[Snowflake]] = None
    """Roles able to use the emoji."""
