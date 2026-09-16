from .enum_types import DiscordFlags, DiscordTypes

class MessageReferenceType(DiscordTypes):
    """Constants associated with how reference data is populated."""

    DEFAULT = 0
    """Standard reference used by replies."""

    FORWARD = 1
    """Reference used to point to a message at a point in time.
    
    !!! warning
        Applications must be able to read the message content in order to forward it.
    """

class MessageFlags(DiscordFlags):
    """Flags that can be applied to a message."""

    NO_FLAGS = 0
    """Message has no flags."""

    CROSSPOSTED = 1 << 0
    """Message has been published."""

    IS_CROSSPOST = 1 << 1
    """Message originated from another channel."""

    SUPPRESS_EMBEDS = 1 << 2
    """Hide embeds."""

    EPHEMERAL = 1 << 6
    """Only visible to the invoking user."""

    IS_COMPONENTS_V2 = 1 << 15
    """This message includes Discord's V2 Components."""

class MessageType(DiscordTypes):
    """Tyoes of messages."""

    DEFAULT = 0
    CHANNEL_PINNED_MESSAGE = 4
    GUILD_BOOST = 8
    GUILD_BOOST_TIER_1 = 9
    GUILD_BOOST_TIER_2 = 10
    GUILD_BOOST_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23
