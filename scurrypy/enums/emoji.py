from .enum_types import DiscordTypes

class ReactionType(DiscordTypes):
    """Represents types of reactions."""

    NORMAL = 0
    """Normal emoji reaction."""

    BURST = 1
    """Super emoji reaction."""
