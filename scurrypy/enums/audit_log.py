from .enum_types import DiscordTypes

class AuditLogEventType(DiscordTypes):
    """Represents Audit Log event types."""

    GUILD_UPDATE = 1
    """Server settings were updated."""

    CHANNEL_CREATE = 2
    """Channel was created."""

    CHANNEL_UPDATE = 3
    """Channel settings were updated."""

    CHANNEL_DELETE = 4
    """Channel was deleted."""

    MEMBER_KICK = 20
    """Member was removed from server."""

    MEMBER_BAN_ADD = 22
    """Member was banned from server."""

    MEMBER_BAN_REMOVE = 23
    """Server ban was lifted for a member."""

    MEMBER_UPDATE = 24
    """Member was updated in server."""

    MEMBER_ROLE_UPDATE = 25
    """Member was added or removed from a role."""

    BOT_ADD = 28
    """Bot user was added to server."""

    ROLE_CREATE = 30
    """Role was created."""

    ROLE_UPDATE = 31
    """Role was edited."""

    ROLE_DELETE = 32
    """Role was deleted."""

    INVITE_CREATE = 40
    """Server invite was created."""

    INVITE_UPDATE = 41
    """Server invite was updated."""

    INVITE_DELETE = 42
    """Server invite was deleted."""

    WEBHOOK_CREATE = 50
    """Webhook was created."""

    WEBHOOK_UPDATE = 51
    """Webhook properties or channel were updated."""

    WEBHOOK_DELETE = 52
    """Webhook was deleted."""

    EMOJI_CREATE = 60
    """Emoji was created."""

    EMOJI_UPDATE = 61
    """Emoji name was updated."""

    EMOJI_DELETE = 62
    """Emoji was deleted."""

    MESSAGE_DELETE = 72
    """Single message was deleted."""

    MESSAGE_BULK_DELETE = 73
    """Multiple messages were deleted."""

    MESSAGE_PIN = 74
    """Message was pinned to a channel."""

    MESSAGE_UNPIN = 75
    """Message was unpinned from a channel."""

    INTEGRATION_CREATE = 80
    """App was added to server."""

    INTEGRATION_UPDATE = 81
    """App was updated."""

    INTEGRATION_DELETE = 82
    """App was removed from server."""

    STICKER_CREATE = 90
    """Sticker was created."""

    STICKER_UPDATE = 91
    """Sticker details were updated."""

    STICKER_DELETE = 92
    """Sticker was deleted."""

    THREAD_CREATE = 110
    """Thread was created in a channel."""

    THREAD_UPDATE = 111
    """Thread was updated."""

    THREAD_DELETE = 112
    """Thread was deleted."""

    APPLICATION_COMMAND_PERMISSION_UPDATE = 121
    """Permissions were updated for a command."""

    AUTO_MODERATION_RULE_CREATE = 140
    """Auto Moderation rule was created."""

    AUTO_MODERATION_RULE_UPDATE = 141
    """Auto Moderation rule was updated."""

    AUTO_MODERATION_RULE_DELETE = 142
    """Auto Moderation rule was deleted."""

    AUTO_MODERATION_BLOCK_MESSAGE = 143
    """Message was blocked by Auto Moderation."""

    AUTO_MODERATION_FLAG_TO_CHANNEL = 144
    """Message was flagged by Auto Moderation."""

    AUTO_MODERATION_USER_COMMUNICATION_DISABLED = 145
    """Member was timed out by Auto Moderation."""

    AUTO_MODERATION_QUARANTINE_USER = 146
    """Member was quarantined by Auto Moderation."""

    ONBOARDING_PROMPT_CREATE = 163
    """Guild Onboarding Question was created."""

    ONBOARDING_PROMPT_UPDATE = 164
    """Guild Onboarding Question was updated."""

    ONBOARDING_PROMPT_DELETE = 165
    """Guild Onboarding Question was deleted."""

    ONBOARDING_CREATE = 166
    """Guild Onboarding was created."""

    ONBOARDING_UPDATE = 167
    """Guild Onboarding was updated."""

    HOME_SETTINGS_CREATE = 190
    """Guild Server Guide was created."""

    HOME_SETTINGS_UPDATE = 191
    """Guild Server Guide was updated."""
