from scurrypy.api.interactions import (
    MessageComponentDataModel, 
    ModalDataModel, 
    ModalComponentInputDataModel, 
    ModalComponentSelectDataModel
)
from scurrypy.core.exceptions import OptionNotFound
from scurrypy.enums import ComponentType

from ..interactions.ctx import InteractionContext

class ComponentContext(InteractionContext):
    pass

class MessageComponentContext(ComponentContext):
    data: MessageComponentDataModel

class ComponentModalContext(ComponentContext):
    data: ModalDataModel

    def get_modal_value(self, custom_id: str) -> str | list[str] | bool | None:
        """Get a modal interaction value by its custom ID

        Args:
            custom_id (str): custom ID of field to fetch

        Raises:
            (OptionNotFound): invalid custom ID

        Returns:
            (str | list[str] | bool | None): component values if select component 
                or value if input 
                or bool if checkbox
                or None if the component has no submitted value
        """

        for component in self.data.components:
            if custom_id != component.component.custom_id:
                continue

            if isinstance(component.component, ModalComponentInputDataModel):
                if component.component.value is None:
                    return None
                if component.component.type == ComponentType.CHECKBOX:
                    return component.component.value.lower() == 'true'
                return component.component.value
        
            if isinstance(component.component, ModalComponentSelectDataModel):
                if not component.component.values:
                    return None
                return list(component.component.values)

        raise OptionNotFound(f"Component custom ID '{custom_id}' not found.")
