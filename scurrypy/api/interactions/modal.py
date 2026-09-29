from dataclasses import dataclass
from typing import Self

from ...core.model import DataModel, datamodel
from ...core.types import (
    JSON, 
    PresentModelField, 
    OmittableModelField, 
    RequiredPartField,
    ScurrypyStr
)

from ...bases.interaction import InteractionData

from ...enums.components import ComponentType

from ..resolved import ResolvedDataModel
from ..components import Label

@dataclass
class ModalPart(DataModel):
    """Represents the Modal object."""

    title: RequiredPartField[str] = None
    """Title of the popup modal."""

    custom_id: RequiredPartField[str] = None
    """ID for the modal."""

    components: RequiredPartField[list[Label]] = None
    """1 to 5 components that make up the modal."""

@datamodel
class ModalComponentDataModel(DataModel):
    """Represents the modal field response from a modal."""

    type: PresentModelField[ComponentType]
    """Type of component."""
    
    custom_id: PresentModelField[ScurrypyStr]
    """Unique ID associated with the component."""

    resolved: OmittableModelField[ResolvedDataModel]
    """Resolved entities from selected options."""

@datamodel
class ModalComponentInputDataModel(ModalComponentDataModel):
    """Represents modal component variants with the value field."""

    value: OmittableModelField[ScurrypyStr]
    """Text input value.
    
    Convert based on option type:
        - CHECKBOX: value.lower() == 'true'

    otherwise the value is expected to be str
    """

@datamodel 
class ModalComponentSelectDataModel(ModalComponentDataModel):
    """Represents modal component variants with the values field."""
    
    values: OmittableModelField[list[ScurrypyStr]]
    """String select values."""

@datamodel
class ModalComponentModel(DataModel):
    """Represents the modal component response from a modal."""

    component: PresentModelField[ModalComponentDataModel]
    """Data associated with the component."""

    @classmethod
    def from_dict(cls, data: JSON) -> Self:
        obj = super().from_dict(data)

        component_data = data['component'] # always present
        component_type = ComponentType(int(data['type'])) # always present

        if component_type in {
            ComponentType.STRING_SELECT, 
            ComponentType.USER_SELECT, 
            ComponentType.ROLE_SELECT, 
            ComponentType.MENTIONABLE_SELECT, 
            ComponentType.CHANNEL_SELECT,
            ComponentType.FILE_UPLOAD,
            ComponentType.CHECKBOX_GROUP
        }:
            obj.component = ModalComponentSelectDataModel.from_dict(component_data)
        else:
            obj.component = ModalComponentInputDataModel.from_dict(component_data)

        return obj

@datamodel
class ModalDataModel(DataModel, InteractionData):
    """Represents the modal response from a modal."""
    
    custom_id: PresentModelField[ScurrypyStr]
    """Unique ID associated with the modal."""

    components: PresentModelField[list[ModalComponentModel]]
    """Components on the modal."""

    resolved: OmittableModelField[ResolvedDataModel]
    """Resolved entities from modal data."""
