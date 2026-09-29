from ..core.model import datamodel
from ..core.snowflake import Snowflake
from ..core.types import PresentModelField, OmittableModelField

from .base_event import Event

from ..enums.events import EventType

from ..api.integration import IntegrationModel

@datamodel
class GuildIntegrationCreateEvent(Event, IntegrationModel):
    """Received when an integration is created."""

    dispatch_name = EventType.INTEGRATION_CREATE

    guild_id: PresentModelField[Snowflake]
    """Guild ID of the created integration."""

@datamodel
class GuildIntegrationUpdateEvent(Event, IntegrationModel):
    """Received when an integration is created."""

    dispatch_name = EventType.INTEGRATION_UPDATE

    guild_id: PresentModelField[Snowflake]
    """Guild ID of the updated integration."""

@datamodel
class GuildIntegrationsUpdateEvent(Event):
    """Received when a guild's integration is updated."""

    dispatch_name = EventType.GUILD_INTEGRATIONS_UPDATE

    guild_id: PresentModelField[Snowflake]
    """ID of the guild whose integrations were updated."""

@datamodel
class GuildIntegrationDeleteEvent(Event):
    """Received when a guild's integration is deleted."""

    dispatch_name = EventType.INTEGRATION_DELETE

    id: PresentModelField[Snowflake]
    """ID of the deleted integration."""

    guild_id: PresentModelField[Snowflake]
    """Guild ID of the deleted integration."""

    application_id: OmittableModelField[Snowflake]
    """ID of the bot for this Discord integration."""
