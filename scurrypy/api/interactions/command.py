from typing import Self

from ...core.model import DataModel, datamodel
from ...core.snowflake import Snowflake
from ...core.types import (
    JSON, 
    PresentModelField, 
    OmittableModelField, 
    ScurrypyStr, 
    ScurrypyBool
)
from ...core.exceptions import DataModelTypeError

from ...bases.interaction import InteractionData

from ...enums.command import CommandType, CommandOptionType

from ..resolved import ResolvedDataModel

@datamodel
class ApplicationCommandOption(DataModel):
    """Represents common fields among all application command options."""
    
    type: PresentModelField[CommandOptionType]
    """Type of command option."""

    name: PresentModelField[ScurrypyStr]
    """Name of the command option."""

@datamodel
class ApplicationCommandOptionDataModel(ApplicationCommandOption):
    """Represents an option received from an application command."""
    
    value: PresentModelField[ScurrypyStr]
    """
    Raw option value received from Discord.
    
    Convert based on option type:
        - INTEGER/USER/CHANNEL/ROLE/ATTACHMENT: int(value)
        - NUMBER: float(value)  
        - BOOLEAN: value.lower() == 'true'

    otherwise the value is expected to be str
    """

@datamodel
class CommandDataModel(DataModel):
    """Represents common command interaction data fields."""
    
    id: PresentModelField[Snowflake]
    """ID of the command."""

    name: PresentModelField[ScurrypyStr]
    """Name of the command."""
    
    type: PresentModelField[CommandType]
    """Type of command."""

    guild_id: OmittableModelField[Snowflake]
    """ID of guild from which the command was invoked."""

    target_id: OmittableModelField[Snowflake]
    """ID of the user or message from which the command was invoked (message/user commands only)."""

    resolved: OmittableModelField[ResolvedDataModel]
    """Converted users + roles + channels + attachments."""

@datamodel
class ApplicationSubcommandDataModel(ApplicationCommandOption):
    """Represents a command option containing command options."""

    options: OmittableModelField[list[ApplicationCommandOptionDataModel]]
    """Options of the subcommand."""

@datamodel
class ApplicationSubcommandGroupDataModel(ApplicationCommandOption):
    """Represents the response from a subcommand group interaction."""

    options: PresentModelField[list[ApplicationSubcommandDataModel]]
    """Selected subcommand of the subcommand group.
    
    !!! note
        Although Discord represents options as an array, only **one** option can be selected.
    """

@datamodel
class ApplicationCommandDataModel(InteractionData, CommandDataModel):
    """Represents the response from an application command."""

    options: OmittableModelField[list[ApplicationCommandOption]]
    """Options selected with the command."""

    @classmethod
    def from_dict(cls, data: JSON) -> Self:
        
        obj = super().from_dict(data) # CommandDataModel's fields

        options = data.get('options')

        if options is None: # options are either not present or a list when coming from Discord
            return obj

        if not isinstance(options, list):
            raise DataModelTypeError(f"Options is expected to be list; got {type(options).__name__}")
        
        match int(options[0]['type']):
            case CommandOptionType.SUB_COMMAND_GROUP:
                obj.options = [
                    ApplicationSubcommandGroupDataModel.from_dict(opt)
                    for opt in options
                ]
            case CommandOptionType.SUB_COMMAND:
                obj.options = [
                    ApplicationSubcommandDataModel.from_dict(opt)
                    for opt in options
                ]
            case _:
                obj.options = [
                    ApplicationCommandOptionDataModel.from_dict(opt)
                    for opt in options
                ]

        return obj

@datamodel
class ApplicationCommandOptionAutocompleteDataModel(ApplicationCommandOptionDataModel):
    """Represents an option received from an autocomplete interaction."""
    
    focused: OmittableModelField[ScurrypyBool]
    """Whether this option is the currently focused option for autocomplete."""

@datamodel
class AutocompleteApplicationCommandDataModel(InteractionData, CommandDataModel):
    """Represents the response from an autocomplete command."""

    options: OmittableModelField[list[ApplicationCommandOptionAutocompleteDataModel]]
    """Options of the command."""
