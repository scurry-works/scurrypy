from dataclasses import  field
from typing import Self

from ..core.model import datamodel
from ..core.types import JSON

from .base_event import Event

from ..bases.interaction import InteractionData

from ..enums.interaction import InteractionType
from ..enums.events import EventType

from ..api.interactions import (
    InteractionModel, 
    ApplicationCommandDataModel, 
    MessageComponentDataModel, 
    ModalDataModel
)

@datamodel
class InteractionEvent(Event, InteractionModel):

    dispatch_name = EventType.INTERACTION_CREATE

    data: InteractionData = field(init=False)
    """Interaction response data. Can be one of [`InteractionData`][scurrypy.bases.InteractionData]'s variants."""

    @classmethod
    def from_dict(cls, data: JSON) -> Self:
        assert isinstance(data, dict)

        obj = super().from_dict(data) # InteractionModel's DataModel

        interaction_data = data["data"]
        interaction_type = data["type"]

        match interaction_type:
            case InteractionType.APPLICATION_COMMAND | InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
                obj.data = ApplicationCommandDataModel.from_dict(interaction_data)
            case InteractionType.MESSAGE_COMPONENT:
                obj.data = MessageComponentDataModel.from_dict(interaction_data)
            case InteractionType.MODAL_SUBMIT:
                obj.data = ModalDataModel.from_dict(interaction_data)
        
        return obj
