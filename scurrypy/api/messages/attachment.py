from dataclasses import dataclass

from ...core.model import DataModel, datamodel
from ...core.snowflake import Snowflake
from ...core.exceptions import MissingField
from ...core.types import (
    Serialized, 
    PresentModelField, 
    OmittableModelField, 
    OmittableNullableModelField, 
    RequiredPartField, 
    OptionalPartField,
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool
)

from ...enums.attachment import AttachmentFlags

@datamodel
class AttachmentModel(DataModel):
    """Represents an attachment object."""

    id: PresentModelField[Snowflake]
    """Attachment ID.
    
    For new uploads, this value is assigned internally to the
    attachment's index in the upload list.
    """

    filename: PresentModelField[ScurrypyStr]
    """Name of the file."""

    title: OmittableModelField[ScurrypyStr]
    """Title of the file."""

    description: OmittableModelField[ScurrypyStr]
    """Description of the file."""

    content_type: OmittableModelField[ScurrypyStr]
    """Media type of the file."""

    size: PresentModelField[ScurrypyInt]
    """Size of file (in bytes)."""

    url: PresentModelField[ScurrypyStr]
    """Source URL of the file."""

    proxy_url:PresentModelField [ScurrypyStr]
    """A proxied URL of the file."""

    height: OmittableNullableModelField[ScurrypyInt]
    """Height of file (if image)."""

    width: OmittableNullableModelField[ScurrypyInt]
    """Width of file (if image)."""

    ephemeral: OmittableModelField[ScurrypyBool]
    """Whether this file is ephemeral."""

    flags: OmittableModelField[AttachmentFlags]
    """Attachment flags as a combined bitfield."""

@dataclass
class AttachmentPart(DataModel):
    """Represents an attachment."""

    path: RequiredPartField[str] = None
    """Relative path to the file."""

    description: OptionalPartField[str] = None
    """Description of the file."""

    is_spoiler: OptionalPartField[bool] = None
    """Whether this attachment should be blurred."""

    id: RequiredPartField[int] = None
    """ID of the attachment.

    For editing attachments, this should be the Discord attachment ID.
    For new attachments, the ID is internally set.
    """

    def to_dict(self) -> Serialized:
        """Serialize this attachment.

        Raises:
            (MissingField): missing path

        Returns:
            (Serialized): serialized attachment
        """
        if self.path is None:
            raise MissingField("AttachmentPart.path must be set before serialization")
        
        return {
            'id': self.id,
            'filename': self.path.split('/')[-1],
            'description': self.description,
            'is_spoiler': self.is_spoiler
        }
