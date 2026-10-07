from typing import TypedDict

from ..enums import InteractionContextType

from ..api.commands import CommandOptionPart

class EditGlobalCommandParams(TypedDict, total=False):
    """Parameters for editing a global command."""

    name: str
    """Name of the command."""

    description: str
    """Description for the command."""

    contexts: list[InteractionContextType]
    """Where the command can be used."""

    options: list[CommandOptionPart]
    """Options with the command."""

    nsfw: bool
    """Whether this command is age restricted."""

class EditGuildCommandParams(TypedDict, total=False):
    """Parameters for editing a guild command."""

    name: str
    """Name of the command."""

    description: str
    """Description for the command."""

    options: list[CommandOptionPart]
    """Options with the command."""

    nsfw: bool
    """Whether this command is age restricted."""
