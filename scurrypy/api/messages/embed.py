from dataclasses import dataclass

from ...core.model import DataModel
from ...core.exceptions import DataModelTypeError
from ...core.types import Serialized, RequiredPartField, OptionalPartField

from ..user import UserModel

from datetime import datetime, timezone

@dataclass
class EmbedAuthor(DataModel):
    """Represents fields for creating an embed author."""

    name: RequiredPartField[str] = None
    """Name of the author."""

    url: OptionalPartField[str] = None
    """URL of the author. http or attachment://<filename> scheme."""

    icon_url: OptionalPartField[str] = None
    """URL of author's icon. http or attachment://<filename> scheme."""

@dataclass
class EmbedThumbnail(DataModel):
    """Represents fields for creating an embed thumbnail."""

    url: RequiredPartField[str] = None
    """Thumbnail content. http or attachment://<filename> scheme."""

@dataclass
class EmbedField(DataModel):
    """Represents fields for creating an embed field."""

    name: RequiredPartField[str] = None
    """Name of the field."""

    value: RequiredPartField[str] = None
    """Value of the field."""

    inline: OptionalPartField[bool] = False
    """Whether or not this field should display inline. Defaults to `False`."""

@dataclass
class EmbedImage(DataModel):
    """Represents fields for creating an embed image."""

    url: RequiredPartField[str] = None
    """Image content. http or attachment://<filename> scheme."""

@dataclass
class EmbedFooter(DataModel):
    """Represents fields for creating an embed footer."""

    text: RequiredPartField[str] = None
    """Footer text."""

    icon_url: OptionalPartField[str] = None
    """URL of the footer icon. http or attachment://<filename> scheme."""

@dataclass
class Embed(DataModel):
    """Represents fields for creating an embed."""

    title: OptionalPartField[str] = None
    """This embed's title."""

    description: OptionalPartField[str] = None
    """This embed's description."""

    timestamp: OptionalPartField[str] = None
    """Timestamp of when the embed was sent."""

    color: OptionalPartField[int] = None
    """Embed's accent color."""

    author: OptionalPartField[EmbedAuthor] = None
    """Embed's author."""

    thumbnail: OptionalPartField[EmbedThumbnail] = None
    """Embed's thumbnail attachment."""

    image: OptionalPartField[EmbedImage] = None
    """Embed's image attachment."""

    fields: OptionalPartField[list[EmbedField]] = None
    """List of embed's fields."""

    footer: OptionalPartField[EmbedFooter] = None
    """Embed's footer."""

    def set_user_author(self, user: UserModel) -> None:
        """Embed author builder.

        Args:
            user (UserModel): user author
        """
        self.author = EmbedAuthor(
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
                "Use scurrypy.EmbedThumbnail(url) for embed thumbnails."
            )
        
        if isinstance(self.image, V2Thumbnail):
            raise DataModelTypeError(
                "EmbedPart.image received a ComponentV2 Thumbnail.\n"
                "Use scurrypy.EmbedImage(url) for embed thumbnails."
            )
        
        return super().to_dict()
