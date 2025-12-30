from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

class ApplicationCommandTypes:

    CHAT_INPUT = 1
    """Slash commands; a text-based command that shows up when a user types `/`."""

    USER = 2
    """A UI-based command that shows up when you right click or tap on a user."""
    
    MESSAGE = 3
    """A UI-based command that shows up when you right click or tap on a message."""

    PRIMARY_ENTRY_POINT = 4
    """A UI-based command that represents the primary way to invoke an app's Activity."""

class ApplicationCommandOptionTypes:
    
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
class ApplicationCommandOptionChoiceModel(DataModel):
    """Represents the application command option choice object."""

    name: str
    """Name of the choice."""

    value: str
    """Value for the choice.
    
    !!! note
        Convert based on expected type (str, int or double)
    """

@dataclass
class ApplicationCommandOptionModel(DataModel):
    """Represents the application command option object."""

    type: int
    """Type of command option. See [`ApplicationCommandOptionTypes`][scurrypy.models.command.ApplicationCommandOptionTypes]."""

    name: str
    """Name of the command option."""

    descripton: str
    """Description for the command option."""
    
    required: Optional[bool]
    """Whether this option is required. Defaults to `False`."""

    choices: Optional[list[ApplicationCommandOptionChoiceModel]]
    """Choices for the user to pick from."""

    channel_types: Optional[list[int]]
    """Channels shown will be restricted to these types."""

    min_value: Optional[int]
    """Minimum value allowed."""

    max_value: Optional[int]
    """Maximum value allowed."""

    min_length: Optional[int]
    """Minimum length allowed."""

    max_length: Optional[int]
    """Maximum length allowed."""

    autocomplete: Optional[bool]
    """Whether autocomplete interactions are enabled for this option."""


@dataclass
class ApplicationCommandModel(DataModel):
    """Represents the application command object."""

    id: int
    """Unique ID of command."""

    type: Optional[int]
    """Type of command, defaults to `1`. See [`ApplicationCommandTypes`][scurrypy.models.command.ApplicationCommandTypes]."""

    application_id: int
    """ID of the parent application."""

    guild_id: Optional[int]
    """Guild ID of the command, if not global."""

    name: str
    """Name of the command."""

    description: str
    """Description for `CHAT_INPUT` commands. 
    
    !!! note
        Empty for `USER` and `MESSAGE` commands.
    """

    options: Optional[list[ApplicationCommandOptionModel]]
    """Parameters for the command."""

    default_member_permissions: int
    """Set of permissions represented as a bit set. See [`Permissions`][scurrypy.core.permissions.Permissions]. [`INT_LIMIT`]"""

    nsfw: Optional[bool]
    """Whether the command is age-restricted. Defaults to `False`."""
