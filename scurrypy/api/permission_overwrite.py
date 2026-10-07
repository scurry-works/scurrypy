from dataclasses import dataclass

from ..core.part import Part
from ..core.snowflake import Snowflake
from ..core.types import RequiredPartField

from ..enums import Permissions, PermissionOverwriteType

@dataclass
class PermissionOverwritePart(Part):
    """Represents fields for creating a permission overwrite."""

    id: RequiredPartField[Snowflake] = None
    """Role or user ID."""

    type: RequiredPartField[PermissionOverwriteType] = None
    """Type of object in which this permission applies."""

    allow: RequiredPartField[Permissions] = None
    """Permissions to allow."""

    deny: RequiredPartField[Permissions] = None
    """Permissions to deny."""
