from .enum_types import DiscordTypes

class InviteType(DiscordTypes):
    """Represents types of invites."""

    GUILD = 0
    """This invite is for a guild."""

    GROUP_DM = 1
    """This invite is for a group DM."""

    FRIEND = 2
    """This invite is for a friend."""
