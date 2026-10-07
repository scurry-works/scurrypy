from dataclasses import dataclass

from ...core.part import Part
from ...core.types import (
    RequiredNullablePartField, 
    RequiredPartField
)

from ...enums import Permissions
from ..image_data import ImageDataPart

@dataclass
class GuildRoleColorsPart(Part):
    """Represents fields for setting role colors."""

    primary_color: RequiredPartField[int] = None
    """Primary color of the role."""

    secondary_color: RequiredNullablePartField[int] = None
    """Secondary color of the role. Creates a gradient."""

    tertiary_color: RequiredNullablePartField[int] = None
    """Tertiary color of the role. Creates a holographic style."""

@dataclass
class GuildRolePart(Part):
    """Represents fields for creating a role."""

    name: RequiredPartField[str] = None
    """Name of the role. Discord defaults to \"user role\"."""

    colors: RequiredPartField[GuildRoleColorsPart] = None
    """Colors of the role. Discord defaults to primary color set to `0`."""

    icon: RequiredNullablePartField[ImageDataPart] = None
    """Icon of the role (if guild has `ROLE_ICONS` feature)."""

    permissions: RequiredPartField[Permissions] = None
    """Permission bit set. [`INT_LIMIT`]"""

    hoist: RequiredPartField[bool] = None
    """If the role is pinned in the user listing. Discord defaults to `False`."""

    mentionable: RequiredPartField[bool] = None
    """If the role is mentionable. Discord defaults to `False`."""

    unicode_emoji: RequiredNullablePartField[str] = None
    """Unicode emoji of the role."""
