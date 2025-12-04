from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

@dataclass
class RoleColors(DataModel):
    """Parameters for setting role colors."""

    primary_color: int
    """Primary color of the role."""

    secondary_color: int
    """Secondary color of the role. Creates a gradient."""

    tertiary_color: int
    """Tertiary color of the role. Creates a holographic style."""

@dataclass
class Role(DataModel):
    """Parameters for creating/editing a role."""

    colors: RoleColors
    """Colors of the role."""

    name: str = None
    """Name of the role."""

    permissions: int = 0
    """Permission bit set."""

    hoist: bool = False
    """If the role is pinned in the user listing."""

    mentionable: bool = False
    """If the role is mentionable."""

    unicode_emoji: Optional[str] = None
    """Unicode emoji of the role."""
