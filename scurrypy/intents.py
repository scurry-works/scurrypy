from .enums.enum_types import DiscordFlags

class Intents(DiscordFlags):
    """Gateway intent flags (bitwise).  
    
    For an exhaustive list what intents let your bot listen to what events, 
    see the [list of intents](https://discord.com/developers/docs/events/gateway#list-of-intents).

    !!! note
        Not all intents are listed. Intents not listed are not yet supported.
    """

    GUILDS = 1 << 0
    """Receive events related to guilds."""

    GUILD_MEMBERS = 1 << 1
    """Receive events related to guild members.

    !!! warning "Privileged Intent"
        Requires the app setting `Server Members Intent` to be toggled.
    """

    GUILD_MODERATION = 1 << 2
    """Receive events related to guild moderation."""

    GUILD_EXPRESSIONS = 1 << 3
    """Receive events related to custom emojis and stickers."""

    GUILD_INTEGRATIONS = 1 << 4
    """Receive events related to integrations within a guild."""

    GUILD_WEBHOOKS = 1 << 5
    """Receive events related to webhooks."""

    GUILD_INVITES = 1 << 6
    """Receive events related to creating guild invites."""

    GUILD_MESSAGES = 1 << 9
    """Receive events about messages within a guild."""

    GUILD_MESSAGE_REACTIONS = 1 << 10
    """Track changes in reactions on messages."""

    DIRECT_MESSAGES = 1 << 12
    """Receive events related to DMs."""

    DIRECT_MESSAGE_REACTIONS = 1 << 13
    """Receive events related to DM reactions."""

    MESSAGE_CONTENT = 1 << 15
    """Access content of messages.

    !!! warning "Privileged Intent"
        Requires the app setting `Message Content Intent` to be toggled.
    """

    GUILD_SCHEDULED_EVENTS = 1 << 16
    """Receive events related to guild scheduled events."""

    AUTO_MODERATION_CONFIGURATION = 1 << 20
    """Receive events related to when an auto moderation rule is configured."""

    AUTO_MODERATION_EXECUTION = 1 << 21
    """Receive events related to when an auto moderation rule is executed."""

    GUILD_MESSAGE_POLLS = 1 << 24
    """Receive events related to polls in guilds."""

    DEFAULT = GUILDS | GUILD_MESSAGES
