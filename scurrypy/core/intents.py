from typing import TypedDict, Unpack

class Intents:
    """Gateway intent flags (bitwise).  
        For an exhaustive list what intents let your bot listen to what events, see <a href="https://discord.com/developers/docs/events/gateway#list-of-intents" target="_blank" rel="noopener">list of intents</a>.

    !!! note
        Not all intents are listed. Intents not listed are not yet supported.
    """

    GUILDS = 1 << 0
    """Receive events related to guilds."""

    GUILD_MEMBERS = 1 << 1
    """
    !!! warning "Privileged Intent"
        Requires the app setting `Server Members Intent` to be toggled.
    Receive events related to guild members.
    """

    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    """Receive events related to custom emojis and stickers."""

    GUILD_INTEGRATIONS = 1 << 4
    """Receive events related to integrations within a guild."""

    GUILD_WEBHOOKS = 1 << 5
    """Track webhook events within a guild."""

    GUILD_MESSAGES = 1 << 9
    """Receive events about messages within a guild."""

    GUILD_MESSAGE_REACTIONS = 1 << 10
    """Track changes in reactions on messages."""

    MESSAGE_CONTENT = 1 << 15
    """
    !!! warning "Privileged Intent"
        Requires the app setting `Message Content Intent` to be toggled.
    Access content of messages.
    """

    DEFAULT = GUILDS | GUILD_MESSAGES

class IntentFlagParams(TypedDict, total=False):
    """Gateway intent selection parameters."""
    guilds: bool
    guild_members: bool
    guild_emojis_and_stickers: bool
    guild_integrations: bool
    guild_webhooks: bool
    guild_messages: bool
    guild_message_reactions: bool
    message_content: bool

def set_intents(**flags: Unpack[IntentFlagParams]):
    """Set bot intents. See [`Intents`][scurrypy.core.intents.Intents].
    `Intents.DEFAULT` will also be set.

    Args:
        **flags (Unpack[IntentFlagParams]): intents to set

    Raises:
        (ValueError): invalid flag

    Returns:
        (int): combined intents field
    """
    _flag_map = {
        'guilds': Intents.GUILDS,
        'guild_members': Intents.GUILD_MEMBERS,
        'guild_emojis_and_stickers': Intents.GUILD_EMOJIS_AND_STICKERS,
        'guild_integrations': Intents.GUILD_INTEGRATIONS,
        'guild_webhooks': Intents.GUILD_WEBHOOKS,
        'guild_messages': Intents.GUILD_MESSAGES,
        'guild_message_reactions': Intents.GUILD_MESSAGE_REACTIONS,
        'message_content': Intents.MESSAGE_CONTENT
    }

    intents = Intents.DEFAULT
    for k, v in flags.items():
        if v:
            intents |= _flag_map.get(k)
    
    return intents
