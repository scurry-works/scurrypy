from ...core.model import DataModel, datamodel
from ...core.types import (
    PresentModelField, 
    OmittableModelField, 
    ScurrypyStr
)

from ...bases.interaction import InteractionData

from ...enums.components import ComponentType

from ..resolved import ResolvedDataModel

@datamodel
class MessageComponentDataModel(DataModel, InteractionData):
    """Represents the select response from a select component."""

    custom_id: PresentModelField[ScurrypyStr]
    """Unique ID associated with the component."""

    component_type: PresentModelField[ComponentType]
    """Type of component."""

    resolved: OmittableModelField[ResolvedDataModel]
    """Resolved entities from selected options."""

    values: OmittableModelField[list[ScurrypyStr]]
    """Select values (if any)."""
