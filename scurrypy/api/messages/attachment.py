from dataclasses import dataclass, field

from ...core.part import Part
from ...core.exceptions import MissingField
from ...core.types import (
    Serialized,
    RequiredPartField,
    OptionalPartField
)

@dataclass
class AttachmentPart(Part):
    """Represents an attachment."""

    path: RequiredPartField[str] = None
    """Relative path to the file."""

    description: OptionalPartField[str] = None
    """Description of the file."""

    is_spoiler: OptionalPartField[bool] = None
    """Whether this attachment should be blurred."""

    id: RequiredPartField[int] = field(init=False, default=None)
    """ID of the attachment (internally set)."""

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
