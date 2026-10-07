from scurrypy import JsonQuery
from scurrypy.core.exceptions import OptionNotFound
from scurrypy.enums import ComponentType

from ..interactions.ctx import InteractionContext

class ComponentContext(InteractionContext):
    pass

class MessageComponentContext(ComponentContext):
    event: JsonQuery

class ComponentModalContext(ComponentContext):
    event: JsonQuery

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
        modal_components = self.event.get('data.components').value

        for component in modal_components:
            comp = JsonQuery(component)

            comp_custom_id: str = comp.get('component.custom_id').value

            if custom_id != comp_custom_id:
                continue

            comp_type: ComponentType = comp.get('type', t=ComponentType).value

            if comp_type not in { # NOT a select component
                ComponentType.STRING_SELECT, 
                ComponentType.USER_SELECT, 
                ComponentType.ROLE_SELECT, 
                ComponentType.MENTIONABLE_SELECT, 
                ComponentType.CHANNEL_SELECT,
                ComponentType.FILE_UPLOAD,
                ComponentType.CHECKBOX_GROUP
            }:
                comp_value: str = comp.get('component.value').value

                if comp_value is None:
                    return None
                if comp_type == ComponentType.CHECKBOX:
                    return comp_value.lower() == 'true'
                return comp_value
        
            else: # otherwise, pick up select values (always a list if present)
                comp_values: str = comp.get('values').value

                if comp_values is None:
                    return None
                
                return comp_values

        raise OptionNotFound(f"Component custom ID '{custom_id}' not found.")
