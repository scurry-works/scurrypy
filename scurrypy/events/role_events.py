from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from ..models.role import RoleModel

@dataclass
class RoleCreateEvent(Event, DataModel):
    """Received when a guild role is created."""

    guild_id: int
    """Guild ID of the role."""

    role: RoleModel
    """The new role."""

@dataclass
class RoleUpdateEvent(Event, DataModel):
    """Received when a guild role is updated."""

    guild_id: int
    """Guild ID of the role."""

    role: RoleModel
    """The new role."""

@dataclass
class RoleDeleteEvent(Event, DataModel):
    """Received when a guild role is deleted."""

    guild_id: int
    """Guild ID of the role."""

    role_id: int
    """Role ID of the role."""
