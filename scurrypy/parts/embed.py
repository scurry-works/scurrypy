from dataclasses import dataclass, field
from ..core.model import DataModel

from typing import Optional

@dataclass
class EmbedAuthor(DataModel):
    """Embed author parameters."""

    name: str
    """Name of the author."""

    url: Optional[str] = None
    """URL of the author. http or attachment://<filename> scheme."""

    icon_url: Optional[str] = None
    """URL of author's icon. http or attachment://<filename> scheme."""

@dataclass
class EmbedThumbnail(DataModel):
    """Embed thumbnail."""

    url: str
    """Thumbnail content. http or attachment://<filename> scheme."""

@dataclass
class EmbedField(DataModel):
    """Embed field."""

    name: str
    """Name of the field."""

    value: str
    """Value of the field."""

    inline: Optional[bool] = None
    """Whether or not this field should display inline."""

@dataclass
class EmbedImage(DataModel):
    """Embed image."""

    url: str
    """Image content. http or attachment://<filename> scheme."""

@dataclass
class EmbedFooter(DataModel):
    """Embed footer."""
    text: str
    """Footer text."""

    icon_url: Optional[str] = None
    """URL of the footer icon. http or attachment://<filename> scheme."""

@dataclass
class EmbedPart(DataModel):
    """Represents the Embed portion of a message."""

    title: Optional[str] = None
    """This embed's title."""

    description: Optional[str] = None
    """This embed's description."""

    timestamp: Optional[str] = None
    """Timestamp of when the embed was sent."""

    color: Optional[int] = None
    """Embed's accent color."""

    author: Optional[EmbedAuthor] = None
    """Embed's author."""

    thumbnail: Optional[EmbedThumbnail] = None
    """Embed's thumbnail attachment."""

    image: Optional[EmbedImage] = None
    """Embed's image attachment."""

    fields: Optional[list[EmbedField]] = field(default_factory=list)
    """List of embed's fields."""

    footer: Optional[EmbedFooter] = None
    """Embed's footer."""

    def to_dict(self):
        """
        EXCEPTION to the "models contain no custom methods" rule for two reasons:

        1. `to_dict` already exists on all models via inheritance, so overriding it
        does not break the design model.

        2. `Thumbnail` (Component V2) and `EmbedThumbnail` (Embed-only) are extremely
        easy to confuse. This guard catches the mistake early and provides a clear,
        actionable error instead of allowing Discord to return an obscure 400 error.
        """
        from .components_v2 import Thumbnail as V2Thumbnail

        if isinstance(self.thumbnail, V2Thumbnail):
            raise TypeError(
                "EmbedPart.thumbnail received a ComponentV2 Thumbnail.\n"
                "Use scurrypy.EmbedThumbnail(url) for embed thumbnails."
            )
        
        if isinstance(self.image, V2Thumbnail):
            raise TypeError(
                "EmbedPart.image received a ComponentV2 Thumbnail.\n"
                "Use scurrypy.EmbedImage(url) for embed thumbnails."
            )
        
        return super().to_dict()