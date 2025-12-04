from dataclasses import dataclass, field
from ..core.model import DataModel
from .base_event import Event

from typing import Optional

from ..models.interaction import InteractionModel

from ..parts.components import ComponentTypes

class InteractionCallback: ...

# ----- Command Interaction -----

@dataclass
class ApplicationCommandOptionData(DataModel):
    """Represents the response options from a slash command."""
    
    name: str
    """Name of the command option."""

    type: int
    """Type of command option. See [`CommandOptionTypes`][scurrypy.parts.command.CommandOptionTypes]."""

    value: str | int | float | bool
    """Input value for option."""

    focused: bool
    """Whether this option is the currently focused option for autocomplete."""

@dataclass
class ApplicationCommandData(DataModel):
    """Represents the response from a command."""

    id: int
    """ID of the command."""

    name: str
    """Name of the command."""
    
    type: int
    """Type of command (e.g., message, user, slash)."""

    guild_id: Optional[int]
    """ID of guild from which the command was invoked."""

    target_id: Optional[int]
    """ID of the user or message from which the command was invoked (message/user commands only)."""

    options: Optional[list[ApplicationCommandOptionData]] = field(default_factory=list)
    """Options of the command (slash command only)."""

    def get_focused_value(self):
        opt = next((opt for opt in self.options if opt), None)
        
        return opt.value if opt else ""

    def get_option(self, option_name: str, default = None):
        """Get the input for a command option by name.

        Args:
            option_name (str): option to fetch input from

        Raises:
            ValueError: invalid option name

        Returns:
            (str | int | float | bool): input data of specified option
        """
        for option in self.options:
            if option.name == option_name:
                return option.value
        
        if default is not None:
            return default
        
        raise ValueError(f"Option '{option_name}' not found")

# ----- Component Interaction -----

@dataclass
class MessageComponentData(DataModel):
    """Represents the select response from a select component."""

    custom_id: str
    """Unique ID associated with the component."""

    component_type: int
    """Type of component."""

    values: Optional[list[str]] = field(default_factory=list)
    """Select values (if any)."""

# ----- Modal Interaction -----

@dataclass
class ModalComponentData(DataModel):
    """Represents the modal field response from a modal."""

    type: int
    """Type of component."""
    
    value: Optional[str]
    """Text input value (Text Input component only)."""

    custom_id: str
    """Unique ID associated with the component."""

    values: Optional[list[str]] = field(default_factory=list)
    """String select values (String Select component only)."""

@dataclass
class ModalComponent(DataModel):
    """Represents the modal component response from a modal."""

    type: int
    """Type of component."""

    component: ModalComponentData
    """Data associated with the component."""

@dataclass
class ModalData(DataModel):
    """Represents the modal response from a modal."""
    
    custom_id: str
    """Unique ID associated with the modal."""

    components: list[ModalComponent] = field(default_factory=list)
    """Components on the modal."""

    def get_modal_data(self, custom_id: str):
        """Fetch a modal field's data by its custom ID

        Args:
            custom_id (str): custom ID of field to fetch

        Raises:
            ValueError: invalid custom ID

        Returns:
            (str | list[str]): component values (if string select) or value (if text input)
        """
        for component in self.components:
            if custom_id != component.component.custom_id:
                continue

            t = component.component.type

            if t in [
                ComponentTypes.STRING_SELECT, 
                ComponentTypes.USER_SELECT, 
                ComponentTypes.ROLE_SELECT, 
                ComponentTypes.MENTIONABLE_SELECT, 
                ComponentTypes.CHANNEL_SELECT      # select menus (w. possibly many option selects!)
            ]:
                return component.component.values
            
            # text input
            return component.component.value

        raise ValueError(f"Component custom ID '{custom_id}' not found.")

@dataclass
class InteractionEvent(Event, InteractionModel):
    """Represents the interaction response."""

    data: Optional[ApplicationCommandData | MessageComponentData | ModalData]
    """Interaction response data."""

    @classmethod
    def from_dict(cls, data: dict):
        from ..models.interaction import InteractionTypes
        
        obj = super().from_dict(data) # InteractionModel's DataModel

        interaction_data = data.get("data")
        interaction_type = data.get("type")

        match interaction_type:
            case InteractionTypes.APPLICATION_COMMAND | InteractionTypes.APPLICATION_COMMAND_AUTOCOMPLETE:
                obj.data = ApplicationCommandData.from_dict(interaction_data)
            case InteractionTypes.MESSAGE_COMPONENT:
                obj.data = MessageComponentData.from_dict(interaction_data)
            case InteractionTypes.MODAL_SUBMIT:
                obj.data = ModalData.from_dict(interaction_data)

        return obj