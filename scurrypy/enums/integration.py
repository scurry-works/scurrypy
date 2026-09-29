from .enum_types import DiscordString

class IntegrationType(DiscordString):
    """Represents types of integrations."""

    TWITCH = 'twitch'
    """This integration is connected to Twitch."""

    YOUTUBE = 'youtube'
    """This integration is connected to Youtube."""

    DISCORD = 'discord'
    """This integration is connected to Discord."""
