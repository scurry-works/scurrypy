from dataclasses import dataclass, field

from ...core.model import DataModel
from ...core.types import RequiredPartField, OptionalPartField

from ...enums.command import CommandOptionType, CommandType

@dataclass
class CommandOptionChoicePart(DataModel):
    """Choice for a command option."""

    name: RequiredPartField[str] = None
    """Name of the choice."""

    value: RequiredPartField[str] = None
    """Value for the user to select (same as option type)."""

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
class SubcommandPart(DataModel):
    """Represents the subcommand."""

    name: RequiredPartField[str] = None
    """Name of the subcommand."""

    description: OptionalPartField[str] = None
    """Description of the subcommand."""

    options: OptionalPartField[list[CommandOptionPart]] = None
    """Parameters or options for the subcommand."""

    type: CommandOptionType = field(init=False, default=CommandOptionType.SUB_COMMAND)
    """Command type. Always `CommandOptionType.SUB_COMMAND` for this class."""

@dataclass
class SubcommandGroupPart(DataModel):
    """Represents a subcommand group."""

    name: RequiredPartField[str] = None
    """Name of the subcommand group."""
    
    description: OptionalPartField[str] = None
    """Description of the subcommand group."""

    options: RequiredPartField[list[SubcommandPart]] = None
    """Subcommands for the subcommand group."""

    type: CommandOptionType = field(init=False, default=CommandOptionType.SUB_COMMAND_GROUP)
    """Command type. Always `CommandOptionType.SUB_COMMAND_GROUP` for this class."""

@dataclass
class SlashCommandFamilyPart(DataModel):
    """Represents a slash command with subcommands."""

    name: RequiredPartField[str] = None
    """Name of the command."""

    description: OptionalPartField[str] = None
    """Description of the command."""

    options: RequiredPartField[list[SubcommandGroupPart | SubcommandPart]] = None
    """Subcommands or subcommand groups for the command."""

@dataclass
class SlashCommandPart(DataModel):
    """Represents the slash command."""

    name: RequiredPartField[str] = None
    """Name of the command."""

    description: OptionalPartField[str] = None
    """Description of the command."""

    options: OptionalPartField[list[CommandOptionPart]] = None
    """Parameters or options for the command."""

    type: CommandType = field(init=False, default=CommandType.CHAT_INPUT)
    """Command type. Always `CommandType.CHAT_INPUT` for this class."""
