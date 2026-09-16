from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import PresentModelField, OmittableModelField, PresentNullableModelField

from ...enums.permissions import Permissions
from ...enums.command import CommandOptionType, CommandType

@dataclass
class ApplicationCommandOptionChoiceModel(DataModel):
    """Represents the application command option choice object."""

    name: PresentModelField[str]
    """Name of the choice."""

    value: PresentModelField[str]
    """Value for the choice.
    
    !!! note
        Convert based on expected type (str, int or double)
    """

@dataclass
class ApplicationCommandOptionModel(DataModel):
    """Represents the application command option object.
    
    !!! warning
        Required options MUST be listed before optional options.
    """

    type: PresentModelField[CommandOptionType]
    """Type of command option."""

    name: PresentModelField[str]
    """Name of the command option."""

    descripton: PresentModelField[str]
    """Description for the command option."""
    
    required: OmittableModelField[bool]
    """Whether this option is required. Discord defaults to `False`."""

    choices: OmittableModelField[list[ApplicationCommandOptionChoiceModel]]
    """Choices for the user to pick from."""

    channel_types: OmittableModelField[list[int]]
    """Channels shown will be restricted to these types."""

    min_value: OmittableModelField[int]
    """Minimum value allowed."""

    max_value: OmittableModelField[int]
    """Maximum value allowed."""

    min_length: OmittableModelField[int]
    """Minimum length allowed."""

    max_length: OmittableModelField[int]
    """Maximum length allowed."""

    autocomplete: OmittableModelField[bool]
    """Whether autocomplete interactions are enabled for this option."""

    file_types: OmittableModelField[list[str]]
    """File types in which to filter (e.g., `.pdf`, `.gif`, `.mp4`, etc.)."""

@dataclass
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

    name: PresentModelField[str]
    """Name of the command."""

    description: PresentModelField[str]
    """Description for `CHAT_INPUT` commands. 
    
    !!! note
        Empty for `USER` and `MESSAGE` commands.
    """

    options: OmittableModelField[list[ApplicationCommandOptionModel]]
    """Parameters for the command."""

    default_member_permissions: PresentNullableModelField[Permissions]
    """Set of permissions represented as a bit set. [`INT_LIMIT`]"""

    nsfw: OmittableModelField[bool]
    """Whether the command is age-restricted. Discord defaults to `False`."""
