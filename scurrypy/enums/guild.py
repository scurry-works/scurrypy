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

class StickerType(DiscordTypes):
    """Sticker types."""

    STANDARD = 1
    """An official sticker in a pack."""

    GUILD = 2
    """A sticker uploaded to a guild for the guild's members."""

class StickerFormatType(DiscordTypes):
    """Represents constants for sticker format types."""

    PNG = 1
    """Sticker is a PNG."""

    APNG = 2
    """Sticker is an animated PNG"""

    LOTTIE = 3
    """Sticker is a JSON-based vector animation."""

    GIF = 4
    """Sticker is a GIF."""

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
