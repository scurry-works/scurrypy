from dataclasses import dataclass

from ..core.part import Part
from ..core.types import (
    RequiredPartField,
    OptionalNullablePartField
)

@dataclass
class GuildTemplatePart(Part):
    """Parameters for creating a guild tempalte."""

    name: RequiredPartField[str]
    """Name of the template."""
    
    description: OptionalNullablePartField[str]
    """Description of the template."""
