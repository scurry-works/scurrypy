from dataclasses import dataclass, field

from ..core.model import DataModel
from ..core.exceptions import InvalidFile, MissingField
from ..core.types import Serialized, RequiredPartField

@dataclass
class ImageDataPart(DataModel):
    """Represents Discord's data URI scheme for images."""
    
    path: RequiredPartField[str] = None
    """Path to image."""

    def to_dict(self) -> Serialized:
        """Serialize this image data.

        Raises:
            (InvalidFile): invalid file type

        Returns:
            (str): serialized image data
        """
        import base64, mimetypes

        if self.path is None:
            raise MissingField("ImageDataPart.path must be set.")

        mime, _ = mimetypes.guess_type(self.path)
        if mime is None:
            raise InvalidFile("Unknown file type.")

        with open(self.path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        return f"data:{mime};base64,{encoded}"

@dataclass
class ImageAssetPart(DataModel):
    """Represents fields for creating an image asset."""

    filename: RequiredPartField[str] = None
    """Name of the file."""

    content_type: str = field(init=False)
    """Content type (internally set)."""

    data: bytes = field(init=False)
    """Binary data (internally set)."""

    def to_dict(self) -> Serialized:
        """Serialize this image asset.

        Raises:
            (InvalidFile): unknown file type

        Returns:
            (dict): serialized image asset
        """
        import mimetypes

        if self.filename is None:
            raise MissingField("ImageAssetPart.path must be set.")

        mime, _ = mimetypes.guess_type(self.filename)
        if mime is None:
            raise InvalidFile("Unknown file type.")
        
        with open(self.filename, 'rb') as f:
            self.data = f.read()

        return {
            'filename': self.filename,
            'content_type': mime,
            "value": self.data
        }
