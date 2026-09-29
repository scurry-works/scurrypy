from ..core.model import DataModel, datamodel
from ..core.snowflake import Snowflake
from ..core.types import (
    PresentModelField, 
    OmittableModelField, 
    ScurrypyStr, 
    ScurrypyBool
)

from ..enums.integration import IntegrationType

from .application import ApplicationModel

@datamodel
class IntegrationModel(DataModel):
    """Represents a guild integration."""

    id: PresentModelField[Snowflake]
    """ID of the integration."""

    name: PresentModelField[ScurrypyStr]
    """Name of the integration."""

    type: PresentModelField[IntegrationType]
    """Type of integration."""

    enabled: PresentModelField[ScurrypyBool]
    """If the integration is enabled."""

    application: OmittableModelField[ApplicationModel]
    """The bot application for Discord integrations."""
