from dataclasses import dataclass, field

from ...core.model import DataModel
from ...core.types import RequiredPartField

from ...enums.command import CommandType

@dataclass
class UserCommandPart(DataModel):
    """Represents the user command object."""

    name: RequiredPartField[str] = None
    """Name of the command."""

    type: CommandType = field(init=False, default=CommandType.USER)
    """Command type. Always `CommandType.USER` for this class."""

@dataclass
class MessageCommandPart(DataModel):
    """Represents the message command object."""
    
    name: RequiredPartField[str] = None
    """Name of the command."""

    type: CommandType = field(init=False, default=CommandType.MESSAGE)
    """Command type. Always `CommandType.MESSAGE` for this class."""
