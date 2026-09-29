from ..core.model import datamodel
from ..core.snowflake import Snowflake
from ..core.types import PresentModelField

from .base_event import Event

from ..enums.events import EventType

from ..api.guilds import GuildRoleModel

@datamodel
class RoleCreateEvent(Event):
    """Received when a guild role is created."""

    dispatch_name = EventType.ROLE_CREATE

    guild_id: PresentModelField[Snowflake]
    """Guild ID of the role."""

    role: PresentModelField[GuildRoleModel]
    """The new role."""

@datamodel
class RoleUpdateEvent(Event):
    """Received when a guild role is updated."""

    dispatch_name = EventType.ROLE_UPDATE

    guild_id: PresentModelField[Snowflake]
    """Guild ID of the role."""

    role: PresentModelField[GuildRoleModel]
    """The new role."""

@datamodel
class RoleDeleteEvent(Event):
    """Received when a guild role is deleted."""

    dispatch_name = EventType.ROLE_DELETE

    guild_id: PresentModelField[Snowflake]
    """Guild ID of the role."""

    role_id: PresentModelField[Snowflake]
    """Role ID of the role."""
