from .enum_types import DiscordString, DiscordTypes

class StickerType(DiscordTypes):
    """Represents sticker types."""

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