from .enum_types import DiscordTypes

class CommandType(DiscordTypes):
    """Types of commands."""
    
    CHAT_INPUT = 1
    """Slash commands; a text-based command that shows up when a user types `/`."""

    USER = 2
    """A UI-based command that shows up when you right click or tap on a user."""
    
    MESSAGE = 3
    """A UI-based command that shows up when you right click or tap on a message."""

class CommandOptionType(DiscordTypes):
    """Slash command option input types."""

    SUB_COMMAND = 1
    """Subcommand of a command."""

    SUB_COMMAND_GROUP = 2
    """Group of subcommands."""

    STRING = 3
    """String or text."""

    INTEGER = 4
    """Integer between -2^53+1 and 2^53-1."""

    BOOLEAN = 5
    """Boolean `True`/`False`."""

    USER = 6
    """Pagination for users."""

    CHANNEL = 7
    """Pagination for channels and categories."""

    ROLE = 8
    """Pagination for roles."""

    MENTIONABLE = 9
    """Pagination for users or roles."""

    NUMBER = 10
    """Number between -2^53 and 2^53."""

    ATTACHMENT = 11
    """File upload. See [`AttachmentPart`][scurrypy.api.messages.AttachmentPart]."""
