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

    SOURCE_MESSAGE_DELETED = 1 << 3
    """Source message for this crosspost has been deleted."""

    URGENT = 1 << 4
    """This message came from the urgent message system."""

    HAS_THREAD = 1 << 5
    """This message has an associated thread, with the same id as the message."""

    EPHEMERAL = 1 << 6
    """Only visible to the invoking user."""

    LOADING = 1 << 7
    """This message is an Interaction Response and the bot is \“thinking.\”"""

    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8
    """This message failed to mention some roles and add their members to the thread."""

    SUPPRESS_NOTIFICATIONS = 1 << 12
    """This message will not trigger push and desktop notifications."""

    IS_COMPONENTS_V2 = 1 << 15
    """This message includes Discord's V2 Components."""

class MessageType(DiscordTypes):
    """Tyoes of messages."""

    DEFAULT = 0
    """This message is a default message."""

    CHANNEL_PINNED_MESSAGE = 6
    """This message is pinned to its channel."""

    GUILD_BOOST = 8
    """This message resulted from a guild boost."""

    GUILD_BOOST_TIER_1 = 9
    """This message resulted from a guild boost Tier 1."""

    GUILD_BOOST_TIER_2 = 10
    """This message resulted from a guild boost Tier 2."""

    GUILD_BOOST_TIER_3 = 11
    """This message resulted from a guild boost Tier 3."""

    CHANNEL_FOLLOW_ADD = 12
    """This message resulted from a guild following a channel."""

    GUILD_DISCOVERY_DISQUALIFIED = 14
    """This message resulted from a guild losing Discovery."""

    GUILD_DISCOVERY_REQUALIFIED = 15
    """This message resulted from a guild requalifying for Discovery."""

    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    """This message resulted from a Discovery Grace Period initial warning."""

    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    """This message resulted from a Discovery Grace Period final warning."""

    THREAD_CREATED = 18
    """This message has a thread attached."""

    REPLY = 19
    """This message has a reply attached."""

    CHAT_INPUT_COMMAND = 20
    """This message resulted from a slash command."""

    THREAD_STARTER_MESSAGE = 21
    """This message is a thread starter message."""

    GUILD_INVITE_REMINDER = 22
    """This message resulted from a guild invite reminder."""

    CONTEXT_MENU_COMMAND = 23
    """This message resulted from a context menu command."""

    AUTO_MODERATION_ACTION = 24
    """This message resulted from an auto moderation action."""

    POLL_RESULT = 46
    """This message is a poll."""
