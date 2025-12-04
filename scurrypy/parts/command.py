from dataclasses import dataclass, field
from ..core.model import DataModel

from typing import Optional

class CommandTypes:
    CHAT_INPUT = 1
    USER_COMMAND = 2
    MESSAGE_COMMAND = 3

class CommandOptionTypes:
    """Slash command option input types."""

    STRING = 3
    """string (text)"""

    INTEGER = 4
    """integer (Any integer between -2^53+1 and 2^53-1)"""

    BOOLEAN = 5
    """boolean (true/false)"""

    USER = 6
    """user pangination"""

    CHANNEL = 7
    """channel pangination (category and channels)"""

    ROLE = 8
    """role pangination"""

    MENTIONABLE = 9
    """any pangination (role and user)"""

    NUMBER = 10
    """number (Any double between -2^53 and 2^53)"""

    ATTACHMENT = 11
    """file upload (See [Attachment][scurrypy.parts.message.Attachment])"""

@dataclass
class CommandOptionChoice(DataModel):
    """Choice for a command option."""

    name: str = None
    """Name of the choice."""

    value: str | int | float = None
    """Value for the user to select (same as option type)."""

    name_localizations: Optional[dict] = None
    """Dictionary with keys in available locales."""

@dataclass
class CommandOption(DataModel):
    """Option for a slash command."""

    type: int = None
    """Type of option. See [`CommandOptionTypes`][scurrypy.parts.command.CommandOptionTypes]."""

    name: str = None
    """Name of option."""

    description: str = None
    """Description of option."""

    required: bool = False
    """Whether this option is required. Defaults to False."""

    choices: list[CommandOptionChoice] = field(default_factory=list)
    """Choices for the user to pick from, max 25. Only valid for STRING, INTEGER, NUMBER option types."""

    autocomplete: bool = False
    """Whether autocomplete interactions are enabled for this option. Defaults to False."""

@dataclass
class SlashCommand(DataModel):
    """Represents the slash command object."""

    name: str = None
    """Name of the command."""

    description: str = None
    """Description of the command."""

    options: list[CommandOption] = field(default_factory=list)
    """Parameters or options for the command."""

    type: int = field(init=False, default=CommandTypes.CHAT_INPUT)
    """Command type. Always `CommandTypes.CHAT_INPUT` for this class. See [`CommandTypes`][scurrypy.parts.command.CommandTypes]."""

@dataclass
class UserCommand(DataModel):
    """Represents the user command object."""

    name: str = None
    """Name of the command."""

    type: int = field(init=False, default=CommandTypes.USER_COMMAND)
    """Command type. Always `CommandTypes.USER_COMMAND` for this class. See [`CommandTypes`][scurrypy.parts.command.CommandTypes]."""

@dataclass
class MessageCommand(DataModel):
    """Represents the message command object."""
    
    name: str = None
    """Name of the command."""

    type: int = field(init=False, default=CommandTypes.MESSAGE_COMMAND)
    """Command type. Always `CommandTypes.MESSAGE_COMMAND` for this class. See [`CommandTypes`][scurrypy.parts.command.CommandTypes]."""
