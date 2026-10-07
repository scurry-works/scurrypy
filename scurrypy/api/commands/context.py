from dataclasses import dataclass, field

from ...core.part import Part
from ...core.types import RequiredPartField

from ...enums.command import CommandType

@dataclass
class UserCommandPart(Part):
    """Represents fields for creating an user command object."""

    name: RequiredPartField[str] = None
    """Name of the command."""

    type: CommandType = field(init=False, default=CommandType.USER)
    """Command type. Always `CommandType.USER` for this class."""

@dataclass
class MessageCommandPart(Part):
    """Represents fields for creating a message command object."""
    
    name: RequiredPartField[str] = None
    """Name of the command."""

    type: CommandType = field(init=False, default=CommandType.MESSAGE)
    """Command type. Always `CommandType.MESSAGE` for this class."""
