from dataclasses import dataclass, field
from typing import Self

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.exceptions import OptionNotFound
from ...core.types import HTTPResponse, PresentModelField, OmittableModelField

from ...bases.interaction import InteractionData

from ...enums.permissions import Permissions
from ...enums.interaction import InteractionCallbackType, InteractionType
from ...enums.command import CommandType, CommandOptionType
from ...enums.components import ComponentType

from ..channels.channel import ChannelModel
from ..guilds.guild import GuildModel
from ..messages.message import MessageModel

from ..user import GuildMemberModel

from .resolved import ResolvedDataModel

@dataclass
class InteractionCallbackDataModel(DataModel):
    """Represents the interaction callback object."""

    id: PresentModelField[Snowflake]
    """ID of the interaction."""

    type: PresentModelField[InteractionCallbackType]
    """Type of interaction."""

    activity_instance_id: OmittableModelField[str]
    """Instance ID of activity if an activity was launched or joined."""

    response_message_id: OmittableModelField[Snowflake]
    """ID of the message created by the interaction."""

    response_message_loading: OmittableModelField[bool]
    """If the interaction is in a loading state."""

    response_message_ephemeral: OmittableModelField[bool]
    """If the interaction is ephemeral."""

@dataclass
class InteractionCallbackModel(DataModel):
    """Represents the interaction callback response object."""

    interaction: PresentModelField[InteractionCallbackDataModel]
    """The interaction object associated with the interaction response."""

@dataclass
class InteractionModel(DataModel):
    """Represents the interaction model."""

    type: PresentModelField[InteractionType]
    """Type of interaction."""

    id: PresentModelField[Snowflake]
    """ID of interaction."""

    token: PresentModelField[str]
    """token of interaction."""

    application_id: PresentModelField[Snowflake]
    """ID of the application that owns the interaction."""

    app_permissions: PresentModelField[Permissions]
    """Bitwise set of permissions pertaining to the location of the interaction. [`INT_LIMIT`]"""

    member: OmittableModelField[GuildMemberModel]
    """Guild member invoking the interaction."""

    message: OmittableModelField[MessageModel]
    """Message associated with interaction (components or modals)."""

    guild_id: OmittableModelField[Snowflake]
    """ID of guild the interaction was invoked (if invoked in a guild)."""

    guild: OmittableModelField[GuildModel]
    """Partial guild object of the guild the interaction was invoked (if invoked in a guild)."""

    channel_id: OmittableModelField[Snowflake]
    """ID of the channel where the interaction was sent."""

    channel: OmittableModelField[ChannelModel]
    """Partial channel object the interaction was invoked."""

# ----- Command Interaction -----

@dataclass
class ApplicationCommandOptionDataModel(DataModel):
    """Represents the response options from a slash command."""
    
    name: PresentModelField[str]
    """Name of the command option."""

    type: PresentModelField[CommandOptionType]
    """Type of command option."""

    value: PresentModelField[str]
    """
    Raw value from Discord as a string.
    
    Convert based on option type:
        - INTEGER/USER/CHANNEL/ROLE/ATTACHMENT: int(value)
        - NUMBER: float(value)  
        - BOOLEAN: value.lower() == 'true'

    otherwise the value is expected to be str
    """

    focused: OmittableModelField[bool]
    """Whether this option is the currently focused option for autocomplete."""

@dataclass
class CommandDataModel(InteractionData):
    """Represents common command interaction data fields."""
    
    id: PresentModelField[Snowflake]
    """ID of the command."""

    name: PresentModelField[str]
    """Name of the command."""
    
    type: PresentModelField[CommandType]
    """Type of command (e.g., message, user, slash)."""

    guild_id: OmittableModelField[Snowflake]
    """ID of guild from which the command was invoked."""

    target_id: OmittableModelField[Snowflake]
    """ID of the user or message from which the command was invoked (message/user commands only)."""

    resolved: OmittableModelField[ResolvedDataModel]
    """Converted users + roles + channels + attachments."""

    options: OmittableModelField[list[ApplicationCommandOptionDataModel]] = field(default_factory=list)
    """Options of the command (slash command only)."""

    def get_focused_value(self) -> str:
        """Get the next focused value in options.

        Returns:
            (str): next focused value or an empty string if no values are focused
        """
        if not self.options:
            return ""

        opt = next((o for o in self.options if o.focused), None)

        return opt.value if opt else ""

    def get_option(self, option_name: str) -> int | float | bool | str | None:
        """Get the input for a command option by name and convert it to its proper type.

        Args:
            option_name (str): option to fetch input from

        Returns:
            (int | float | bool | str | None): converted input data of specified option
        """
        if not self.options:
            return None
        
        for option in self.options:
            if option.name != option_name:
                continue

            if option.type in [
                CommandOptionType.INTEGER,
                CommandOptionType.USER,
                CommandOptionType.CHANNEL,
                CommandOptionType.ROLE,
                CommandOptionType.ATTACHMENT
            ]:
                return int(option.value)
            
            if option.type == CommandOptionType.NUMBER:
                return float(option.value)
            
            if option.type == CommandOptionType.BOOLEAN:
                return option.value.lower() == 'true'
            
            return option.value
        
        return None

@dataclass
class ApplicationCommandDataModel(CommandDataModel):
    """Represents the response from a command."""
    pass


@dataclass
class AutocompleteApplicationCommandDataModel(CommandDataModel):
    """Represents the response from an autocomplete command."""
    pass

# ----- Component Interaction -----

@dataclass
class MessageComponentDataModel(InteractionData):
    """Represents the select response from a select component."""

    custom_id: PresentModelField[str]
    """Unique ID associated with the component."""

    component_type: PresentModelField[ComponentType]
    """Type of component."""

    resolved: OmittableModelField[ResolvedDataModel]
    """Resolved entities from selected options."""

    values: OmittableModelField[list[str]]
    """Select values (if any)."""

# ----- Modal Interaction -----

@dataclass
class ModalComponentDataModel(DataModel):
    """Represents the modal field response from a modal."""

    type: PresentModelField[ComponentType]
    """Type of component."""
    
    custom_id: PresentModelField[str]
    """Unique ID associated with the component."""

    resolved: OmittableModelField[ResolvedDataModel]
    """Resolved entities from selected options."""

@dataclass
class ModalComponentInputDataModel(ModalComponentDataModel):
    """Represents modal component variants with the value field."""

    value: OmittableModelField[str]
    """Text input value.
    
    Convert based on option type:
        - CHECKBOX: value.lower() == 'true'

    otherwise the value is expected to be str
    """

@dataclass 
class ModalComponentSelectDataModel(ModalComponentDataModel):
    """Represents modal component variants with the values field."""
    
    values: OmittableModelField[list[str]]
    """String select values."""

@dataclass
class ModalComponentModel(DataModel):
    """Represents the modal component response from a modal."""

    component: PresentModelField[ModalComponentDataModel] = field(init=False)
    """Data associated with the component."""

    @classmethod
    def from_dict(cls, data: HTTPResponse) -> Self:
        assert isinstance(data, dict)

        obj = super().from_dict(data)

        component_data = data.get("component")
        assert isinstance(component_data, dict)
        component_type = component_data.get("type")

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

@dataclass
class ModalDataModel(InteractionData):
    """Represents the modal response from a modal."""
    
    custom_id: PresentModelField[str]
    """Unique ID associated with the modal."""

    components: PresentModelField[list[ModalComponentModel]]
    """Components on the modal."""

    resolved: OmittableModelField[ResolvedDataModel]
    """Resolved entities from modal data."""

    def get_modal_data(self, custom_id: str) -> bool | str | list[str] | None:
        """Fetch a modal field's data by its custom ID

        Args:
            custom_id (str): custom ID of field to fetch

        Raises:
            (OptionNotFound): invalid custom ID

        Returns:
            (bool | str | list[str]): component values (if select component) or value or bool if checkbox
        """

        for component in self.components:
            if custom_id != component.component.custom_id:
                continue

            if isinstance(component.component, ModalComponentInputDataModel):
                if component.component.type == ComponentType.CHECKBOX and component.component.value:
                    return component.component.value.lower() == 'true'
                return component.component.value
        
            if isinstance(component.component, ModalComponentSelectDataModel):
                return component.component.values

        raise OptionNotFound(f"Component custom ID '{custom_id}' not found.")
