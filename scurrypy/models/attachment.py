from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

@dataclass
class AttachmentModel(DataModel):
    """Represents an attachment object."""

    id: int
    """Attachment ID."""

    filename: str
    """Name of the file."""

    title: Optional[str]
    """Title of the file."""

    description: Optional[str]
    """Description of the file."""

    content_type: Optional[str]
    """Media type of the file."""

    size: int
    """Size of file (in bytes)."""

    url: str
    """Source URL of the file."""

    proxy_url: str
    """A proxied URL of the file."""

    height: Optional[int]
    """Height of file (if image)."""

    width: Optional[int]
    """Width of file (if image)."""

    ephemeral: Optional[bool]
    """Whether this file is ephemeral."""

    duration_secs: Optional[float]
    """Duration of the file (for voice messages)."""

    waveform: Optional[str]
    """base64 encoded bytearray representing a sampled waveform (for voice messages)."""

    flags: Optional[int]
    """Attachment flags as a combined bitfield."""
