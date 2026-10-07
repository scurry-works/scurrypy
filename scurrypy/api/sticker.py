from dataclasses import dataclass

from ..core.part import Part
from ..core.types import RequiredPartField

@dataclass
class StickerPart(Part):
    """Represents fields for creating a sticker."""

    name: RequiredPartField[str] = None
    """Name of the sticker."""

    description: RequiredPartField[str] = None
    """Description of the sticker."""

    tags: RequiredPartField[str] = None
    """Autocomplete/suggestion tags for the sticker."""
