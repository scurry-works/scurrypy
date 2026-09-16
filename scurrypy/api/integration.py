from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake
from ..core.types import PresentModelField, OmittableModelField

from ..enums.integration import IntegrationType

from .application import ApplicationModel

@dataclass
class IntegrationModel(DataModel):
    """Represents a guild integration."""

    id: PresentModelField[Snowflake]
    """ID of the integration."""

    name: PresentModelField[str]
    """Name of the integration."""

    type: PresentModelField[IntegrationType]
    """Type of integration."""

    enabled: PresentModelField[bool]
    """If the integration is enabled."""

    application: OmittableModelField[ApplicationModel]
    """The bot application for Discord integrations."""
