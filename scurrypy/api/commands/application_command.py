from ...core.model import DataModel, datamodel
from ...core.snowflake import Snowflake
from ...core.types import (
    PresentModelField, 
    OmittableModelField, 
    PresentNullableModelField, 
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool
)

from ...enums.permissions import Permissions
from ...enums.command import CommandOptionType, CommandType

@datamodel
class ApplicationCommandOptionChoiceModel(DataModel):
    """Represents the application command option choice object."""

    name: PresentModelField[ScurrypyStr]
    """Name of the choice."""

    value: PresentModelField[ScurrypyStr]
    """Value for the choice.
    
    !!! note
        Convert based on expected type (str, int or double)
    """

@datamodel
class ApplicationCommandOptionModel(DataModel):
    """Represents the application command option object.
    
    !!! warning
        Required options MUST be listed before optional options.
    """

    type: PresentModelField[CommandOptionType]
    """Type of command option."""

    name: PresentModelField[ScurrypyStr]
    """Name of the command option."""

    descripton: PresentModelField[ScurrypyStr]
    """Description for the command option."""
    
    required: OmittableModelField[ScurrypyBool]
    """Whether this option is required. Discord defaults to `False`."""

    choices: OmittableModelField[list[ApplicationCommandOptionChoiceModel]]
    """Choices for the user to pick from."""

    channel_types: OmittableModelField[list[ScurrypyInt]]
    """Channels shown will be restricted to these types."""

    min_value: OmittableModelField[ScurrypyInt]
    """Minimum value allowed."""

    max_value: OmittableModelField[ScurrypyInt]
    """Maximum value allowed."""

    min_length: OmittableModelField[ScurrypyInt]
    """Minimum length allowed."""

    max_length: OmittableModelField[ScurrypyInt]
    """Maximum length allowed."""

    autocomplete: OmittableModelField[ScurrypyBool]
    """Whether autocomplete interactions are enabled for this option."""

    file_types: OmittableModelField[list[ScurrypyStr]]
    """File types in which to filter (e.g., `.pdf`, `.gif`, `.mp4`, etc.)."""

@datamodel
class ApplicationCommandModel(DataModel):
    """Represents the application command object."""

    id: PresentModelField[Snowflake]
    """Unique ID of command."""

    type: OmittableModelField[CommandType]
    """Type of command. Discord defaults to `ApplicationCommandTypes.CHAT_INPUT`."""

    application_id: PresentModelField[Snowflake]
    """ID of the parent application."""

    guild_id: OmittableModelField[Snowflake]
    """Guild ID of the command, if not global."""

    name: PresentModelField[ScurrypyStr]
    """Name of the command."""

    description: PresentModelField[ScurrypyStr]
    """Description for `CHAT_INPUT` commands. 
    
    !!! note
        Empty for `USER` and `MESSAGE` commands.
    """

    options: OmittableModelField[list[ApplicationCommandOptionModel]]
    """Parameters for the command."""

    default_member_permissions: PresentNullableModelField[Permissions]
    """Set of permissions represented as a bit set. [`INT_LIMIT`]"""

    nsfw: OmittableModelField[ScurrypyBool]
    """Whether the command is age-restricted. Discord defaults to `False`."""
