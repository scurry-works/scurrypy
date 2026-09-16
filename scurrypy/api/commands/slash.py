from dataclasses import dataclass, field

from ...core.model import DataModel
from ...core.types import JSON, RequiredPartField, OptionalPartField, OmittableNullableModelField

from ...enums.command import CommandOptionType, CommandType

@dataclass
class CommandOptionChoicePart(DataModel):
    """Choice for a command option."""

    name: RequiredPartField[str] = None
    """Name of the choice."""

    value: RequiredPartField[str | int | float] = None
    """Value for the user to select (same as option type)."""

    name_localizations: OmittableNullableModelField[JSON] = None
    """Dictionary with keys in available locales."""

@dataclass
class CommandOptionPart(DataModel):
    """Option for a slash command."""

    type: RequiredPartField[CommandOptionType] = None
    """Type of option."""

    name: RequiredPartField[str] = None
    """Name of option."""

    description: RequiredPartField[str] = None
    """Description of option."""

    required: OptionalPartField[bool] = None
    """Whether this option is required. Discord defaults to `False`."""

    choices: OptionalPartField[list[CommandOptionChoicePart]] = None
    """Choices for the user to pick from, max 25. Only valid for STRING, INTEGER, NUMBER option types."""

    autocomplete: OptionalPartField[bool] = None
    """Whether autocomplete interactions are enabled for this option. Discord defaults to `False`."""

@dataclass
class SlashCommandPart(DataModel):
    """Represents the slash command object."""

    name: RequiredPartField[str] = None
    """Name of the command."""

    description: OptionalPartField[str] = None
    """Description of the command."""

    options: OptionalPartField[list[CommandOptionPart]] = None
    """Parameters or options for the command."""

    type: CommandType = field(init=False, default=CommandType.CHAT_INPUT)
    """Command type. Always `CommandType.CHAT_INPUT` for this class."""
