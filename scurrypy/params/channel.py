from typing import TypedDict, Literal

from ..enums.channel import ChannelType, ChannelFlags, SortOrderType, ForumLayoutType

from ..api.channels.default_reaction import DefaultReactionPart
from ..api.channels.tag import TagPart

class EditGuildChannelParams(TypedDict, total=False):
    """Parameters for editing a guild channel."""

    name: str
    """Name of the channel."""

    type: ChannelType
    """Type of channel.
    
    !!! important
        Only conversion between text and announcement is supported in guilds with `NEWS` feature.
    """

    position: int
    """Sorting position of the channel (channels with the same position are sorted by id)."""

    topic: str
    """Topic of the channel."""

    nsfw: bool
    """If the channel is flagged NSFW."""

    rate_limit_per_user: int
    """Seconds user must wait between sending messages in the channel."""

    parent_id: int
    """Category ID of the channel."""

    default_auto_archive_duration: int
    """Default duration in minutes threads will be hidden after period of inactivity."""

    flags: ChannelFlags
    """Channel flags."""

    default_reaction_emoji: DefaultReactionPart
    """Emoji to show in the add reaction button in a `GUILD_FORUM` post."""

    available_tags: list[TagPart]
    """Set of tags that can be applied to a `GUILD_FORUM` post."""

    default_sort_order: SortOrderType
    """Default forum sort order."""

    default_forum_layout: ForumLayoutType
    """Default forum layout view."""

    default_thread_rate_limit_per_user: int
    """Rate limit per user set on newly created threads.
    
    !!! note
        This field does not live update!
    """

class EditThreadChannelParams(TypedDict, total=False):
    """Parameters for editing a thread channel."""

    name: str
    """Name of the channel."""

    archived: bool
    """Whether the thread is archived."""

    auto_archive_duration: Literal[60, 1440, 4320, 10080]
    """Duration in minutes threads will be hidden after period of inactivity."""

    locked: bool
    """Whether the thread is locked.
    
    !!! note
        Only users with `MANAGE_THREADS` can unarchive the thread.
    """

    invitable: bool
    """Whether non-moderators can add other non-moderators to the thread (private threads only)."""

    rate_limit_per_user: int
    """Seconds user must wait between sending messages in the channel."""

    flags: ChannelFlags
    """Channel flags."""

    applied_tags: list[int]
    """Set of tags applied to a `GUILD_FORUM` post."""
