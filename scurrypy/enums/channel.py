from .enum_types import DiscordFlags, DiscordTypes

class ChannelType(DiscordTypes):
    """Represents the types of channels."""

    GUILD_TEXT = 0
    """Text channel within a guild."""

    GUILD_CATEGORY = 4
    """Organizational category for channels."""

    GUILD_ANNOUNCEMENT = 5
    """Channel users can follow and crosspost into their own server."""

    ANNOUNCEMENT_THREAD = 10
    """Temporary sub-channel within a `GUILD_ANNOUNCEMENT` channel."""

    PUBLIC_THREAD = 11
    """Temporary sub-channel within a `GUILD_TEXT` or `GUILD_FORUM` channel."""

    PRIVATE_THREAD = 12
    """Temporary sub-channel within a `GUILD_TEXT` channel only viewable by invitees and members with `MANAGE_THREADS`."""

    GUILD_DIRECTORY = 14
    """Channel in a hub containing the listed servers."""

    GUILD_FORUM = 15
    """Channel that can only contain threads."""

class ChannelFlags(DiscordFlags):
    """Represents constant bit fields for channel flags."""

    PINNED = 1 << 1
    """This thread is pinned to the top of its parent `GUILD_FORUM` channel."""

    REQUIRE_TAG = 1 << 4
    """Whether a tag is required when creating a thread in a `GUILD_FORUM` channel."""

    HIDE_MEDIA_DOWNLOAD_OPTIONS = 1 << 15
    """hides the embedded media download options. 
    
    !!! warning
        Only for media channels.
    """

    CHANNEL_OBFUSCATED = 1 << 17
    """Channel's metadata has been obfuscated because the current user cannot view it.
    
    !!! warning
        Only ever set for channels received over the gateway, not HTTP.
    """

    IS_SPOILER_CHANNEL = 1 << 21
    """Channel in which users must opt in to view its contents.
    
    !!! warning
        Cannot be set for `GUILD_STAGE` channels.
        Can only be set if `nsfw` is `False`.
    """

class SortOrderType(DiscordTypes):
    """Represents sort order types for `GUILD_FORUM` channels."""

    LATEST_ACTIVITY = 0
    """Sort by activity."""

    CREATION_DATE = 1
    """Sort by creation time (recent to oldest)."""

class ForumLayoutType(DiscordTypes):
    """Represents `GUILD_FORUM` layout types."""

    NOT_SET = 0
    """No default layout has been set."""

    LIST_VIEW = 1
    """Display posts as a list."""

    GALLERY_VIEW = 2
    """Display posts as a collection of tiles."""

class AutoArchiveDurationType(DiscordTypes):
    """Auto archive duration options."""
    ONE_HR = 60
    ONE_DAY = 1440
    THREE_DAYS = 4320
    ONE_WEEK = 10080
