from .enum_types import DiscordTypes

class PermissionOverwriteType(DiscordTypes):
    """Represents permission overwrite types."""

    ROLE = 0
    """This overwrite is for a role."""

    MEMBER = 1
    """This overwrite is for a member."""
