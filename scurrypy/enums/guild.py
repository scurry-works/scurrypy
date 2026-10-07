from .enum_types import DiscordString, DiscordTypes

class PromptType(DiscordTypes):
    """Represents Onboarding prompt types."""

    MULTIPLE_CHOICE = 0
    """Multiple choice select."""

    DROPDOWN = 1
    """Dropdown menu select."""

class OnboardingMode(DiscordTypes):
    """Represents constants used to define criteria for satisfying Onboarding constraints."""

    ONBOARDING_DEFAULT = 0
    """Counts only Default Channels towards constraints."""

    ONBOARDING_ADVANCED = 1
    """Counts Default Channels and Questions towards constraints."""

class GuildFeature(DiscordString):
    """Represents features available to a guild."""

    NEWS = "NEWS"
    """Guild has access to create announcement channels."""

    ROLE_ICONS = "ROLE_ICONS"
    """Guild is able to set role icons."""

    ANIMATED_ICON = "ANIMATED_ICON"
    """Guild has access to set an animated guild icon."""

    INVITE_SPLASH = "INVITE_SPLASH"
    """Guild has access to set an invite splash background."""

    DISCOVERABLE = "DISCOVERABLE"
    """Guild is able to be discovered in the directory."""

    BANNER = "BANNER"
    """Guild has access to set a guild banner image"""

    ANIMATED_BANNER = "ANIMATED_BANNER"
    """Guild has access to set an animated guild banner image,"""

    PARTNERED = "PARTNERED"
    """Guild is partnered."""

class GuildVerificationLevel(DiscordTypes):
    """Represents verification levels for a guild."""

    NONE = 0
    """Unrestricted."""

    LOW = 1
    """Must have verified email on account."""

    MEDIUM = 2
    """Must be registered on Discord for longer than 5 minutes."""

    HIGH = 3
    """Must be a member of the server for longer than 10 minutes."""

    VERY_HIGH = 4
    """Must have a verified phone number"""

class GuildDefaultMessageNotificationLevel(DiscordTypes):
    """Represents default message notification levels in a guild."""

    ALL_MESSAGES = 0
    """Members will receive notifications for all messages by default."""

    ONLY_MENTIONS = 1
    """Members will receive notifications only for messages that mention them by default."""

class GuildExplicitContentFilterLevel(DiscordTypes):
    """Represents explicit content filter levels in a guild."""

    DISABLED = 0
    """Media content will not be scanned."""

    MEMBERS_WITHOUT_ROLES = 1
    """Media content sent by members without roles will be scanned"""

    ALL_MEMBERS = 2
    """Media content sent by all members will be scanned."""

class MFA_Level(DiscordTypes):
    """Represents MFA levels within in a guild.
    
    !!! note
        MFA = Multi-factor Authentication
        2FA = 2-Factor Authentication
    """

    NONE = 0
    """Guild has no MFA/2FA requirement for moderation actions."""

    ELEVATED = 1
    """Guild has a 2FA requirement for moderation actions."""
