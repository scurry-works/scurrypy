from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import PresentModelField, PresentNullableModelField, OmittableModelField, OmittableNullableModelField, RequiredNullablePartField, OptionalPartField, RequiredPartField

from ...enums.permissions import Permissions
from ..image_data import ImageDataPart

@dataclass
class GuildRoleColorModel(DataModel):
    """Represents role color data."""

    primary_color: PresentModelField[int]
    """Primary color of the role."""

    secondary_color: PresentNullableModelField[int]
    """Secondary color of the role. Creates a gradient."""

    tertiary_color: PresentNullableModelField[int]
    """Tertiary color of the role. Creates a holographic style."""

@dataclass
class GuildRoleModel(DataModel):
    """Represents a Discord role."""

    id: PresentModelField[Snowflake]
    """ID of the role."""

    name: PresentModelField[str]
    """Name of the role."""

    colors: PresentModelField[GuildRoleColorModel]
    """Colors of the role."""

    hoist: PresentModelField[bool]
    """If the role is pinned in user listing."""

    position: PresentModelField[int]
    """Position of the role."""

    permissions: PresentModelField[Permissions]
    """Permission bit set. [INT_LIMIT]"""

    managed: PresentModelField[bool]
    """If the role is managed by an integration."""

    mentionable: PresentModelField[bool]
    """If the role is mentionable."""

    flags: PresentModelField[int]
    """Role flags combined as a bitfield."""

    icon: OmittableModelField[str]
    """Icon hash of the role."""

    unicode_emoji: OmittableNullableModelField[str]
    """Unicode emoji of the role."""

@dataclass
class GuildRoleColorsPart(DataModel):
    """Parameters for setting role colors."""

    primary_color: RequiredPartField[int] = None
    """Primary color of the role."""

    secondary_color: RequiredNullablePartField[int] = None
    """Secondary color of the role. Creates a gradient."""

    tertiary_color: RequiredNullablePartField[int] = None
    """Tertiary color of the role. Creates a holographic style."""

@dataclass
class GuildRolePart(DataModel):
    """Parameters for creating a role."""

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
