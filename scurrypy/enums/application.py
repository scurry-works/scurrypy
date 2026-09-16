from .enum_types import DiscordFlags

class ApplicationFlags(DiscordFlags):
    """Application flags."""

    GATEWAY_PRESENCE = 1 << 12
    """Privileged intent to receive presence_update events."""

    GATEWAY_PRESENCE_LIMITED = 1 << 13
    """Intent to receive presence_update events."""

    GATEWAY_GUILD_MEMBERS = 1 << 14
    """Privileged intent to receive member-related events."""

    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    """Intent to receive member-related events."""

    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    """Indicates unusual growth of an app that prevents verification."""

    GATEWAY_MESSAGE_CONTENT = 1 << 18
    """Privileged intent to receive message content."""

    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    """Intent to receive message content."""

class ApplicationNewFlags(DiscordFlags):
    """New Application Flags beyond 1 << 30."""
    names = ()
