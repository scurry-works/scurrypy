from dataclasses import dataclass

from ...core.model import DataModel, datamodel
from ...core.exceptions import DataModelTypeError
from ...core.types import (
    OptionalPartField,
    RequiredPartField,
    ScurrypyBool,
    ScurrypyInt,
    ScurrypyStr,
    Serialized,
)

from ..user import UserModel

from datetime import datetime, timezone

@dataclass
class EmbedAuthorPart(DataModel):
    """Represents fields for creating an embed author."""

    name: RequiredPartField[str] = None
    """Name of the author."""

    url: OptionalPartField[str] = None
    """URL of the author. http or attachment://<filename> scheme."""

    icon_url: OptionalPartField[str] = None
    """URL of author's icon. http or attachment://<filename> scheme."""

@datamodel
class EmbedAuthorModel(DataModel):
    """Represents fields for an embed author."""

    name: RequiredPartField[ScurrypyStr]
    """Name of the author."""

    url: OptionalPartField[ScurrypyStr]
    """URL of the author. http or attachment://<filename> scheme."""

    icon_url: OptionalPartField[ScurrypyStr]
    """URL of author's icon. http or attachment://<filename> scheme."""

@dataclass
class EmbedThumbnailPart(DataModel):
    """Represents fields for creating an embed thumbnail."""

    url: RequiredPartField[str] = None
    """Thumbnail content. http or attachment://<filename> scheme."""

@datamodel
class EmbedThumbnailModel(DataModel):
    """Represents fields for an embed thumbnail."""

    url: RequiredPartField[ScurrypyStr]
    """Thumbnail content. http or attachment://<filename> scheme."""

@dataclass
class EmbedFieldPart(DataModel):
    """Represents fields for creating an embed field."""

    name: RequiredPartField[str] = None
    """Name of the field."""

    value: RequiredPartField[str] = None
    """Value of the field."""

    inline: OptionalPartField[bool] = None
    """Whether or not this field should display inline."""

@datamodel
class EmbedFieldModel(DataModel):
    """Represents fields for an embed field."""

    name: RequiredPartField[ScurrypyStr]
    """Name of the field."""

    value: RequiredPartField[ScurrypyStr]
    """Value of the field."""

    inline: OptionalPartField[ScurrypyBool]
    """Whether or not this field should display inline."""

@dataclass
class EmbedImagePart(DataModel):
    """Represents fields for creating an embed image."""

    url: RequiredPartField[str] = None
    """Image content. http or attachment://<filename> scheme."""

@datamodel
class EmbedImageModel(DataModel):
    """Represents fields for an embed image."""

    url: RequiredPartField[ScurrypyStr]
    """Image content. http or attachment://<filename> scheme."""

@dataclass
class EmbedFooterPart(DataModel):
    """Represents fields for creating an embed footer."""

    text: RequiredPartField[str] = None
    """Footer text."""

    icon_url: OptionalPartField[str] = None
    """URL of the footer icon. http or attachment://<filename> scheme."""

@datamodel
class EmbedFooterModel(DataModel):
    """Represents fields for an embed footer."""

    text: RequiredPartField[ScurrypyStr]
    """Footer text."""

    icon_url: OptionalPartField[ScurrypyStr]
    """URL of the footer icon. http or attachment://<filename> scheme."""

@dataclass
class EmbedPart(DataModel):
    """Represents fields for creating an embed."""

    title: OptionalPartField[str] = None
    """This embed's title."""

    description: OptionalPartField[str] = None
    """This embed's description."""

    timestamp: OptionalPartField[str] = None
    """Timestamp of when the embed was sent."""

    color: OptionalPartField[int] = None
    """Embed's accent color."""

    author: OptionalPartField[EmbedAuthorPart] = None
    """Embed's author."""

    thumbnail: OptionalPartField[EmbedThumbnailPart] = None
    """Embed's thumbnail attachment."""

    image: OptionalPartField[EmbedImagePart] = None
    """Embed's image attachment."""

    fields: OptionalPartField[list[EmbedFieldPart]] = None
    """List of embed's fields."""

    footer: OptionalPartField[EmbedFooterPart] = None
    """Embed's footer."""

    def set_user_author(self, user: UserModel) -> None:
        """Embed author builder.

        Args:
            user (UserModel): user author
        """
        self.author = EmbedAuthorPart(
            name=user.username,
            icon_url=f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png"
        )

    def set_timestamp(self, dt: datetime | None = None) -> None:
        """Embed timestamp builder. Adheres to ISO8601 format.

        Args:
            dt (datetime, optional): datetime object
        """
        dt = dt or datetime.now(timezone.utc)

        self.timestamp = dt.isoformat()

    def to_dict(self) -> Serialized:
        """Serialize this embed.

        Raises:
            (DataModelTypeError): incorrect thumbnail part

        Returns:
            (Serialized): serialized embed
        """
        from ..components import Thumbnail as V2Thumbnail

        if isinstance(self.thumbnail, V2Thumbnail):
            raise DataModelTypeError(
                "EmbedPart.thumbnail received a ComponentV2 Thumbnail.\n"
                "Use scurrypy.EmbedThumbnailPart(url) for embed thumbnails."
            )
        
        if isinstance(self.image, V2Thumbnail):
            raise DataModelTypeError(
                "EmbedPart.image received a ComponentV2 Thumbnail.\n"
                "Use scurrypy.EmbedImagePart(url) for embed thumbnails."
            )
        
        return super().to_dict()

@datamodel
class EmbedModel(DataModel):
    """Represents fields for an embed."""

    title: OptionalPartField[ScurrypyStr]
    """This embed's title."""

    description: OptionalPartField[ScurrypyStr]
    """This embed's description."""

    timestamp: OptionalPartField[ScurrypyStr]
    """Timestamp of when the embed was sent."""

    color: OptionalPartField[ScurrypyInt]
    """Embed's accent color."""

    author: OptionalPartField[EmbedAuthorModel]
    """Embed's author."""

    thumbnail: OptionalPartField[EmbedThumbnailModel]
    """Embed's thumbnail attachment."""

    image: OptionalPartField[EmbedImageModel]
    """Embed's image attachment."""

    fields: OptionalPartField[list[EmbedFieldModel]]
    """List of embed's fields."""

    footer: OptionalPartField[EmbedFooterModel]
    """Embed's footer."""
