from dataclasses import dataclass, field

from ...core.part import Part
from ...core.snowflake import Snowflake
from ...core.types import (
    RequiredPartField, 
    OptionalNullablePartField
)

from ...bases import GuildChannelCreate

from ...enums import ChannelType, SortOrderType, ForumLayoutType

from ..permission_overwrite import PermissionOverwritePart

from .default_reaction import DefaultReactionPart
from .tag import TagPart

@dataclass
class GuildForumChannelPart(Part, GuildChannelCreate):
    """Represents fields for creating a guild forum channel."""

    name: RequiredPartField[str] = None
    """Name of the channel."""

    topic: OptionalNullablePartField[str] = None
    """Topic of the channel."""

    position: OptionalNullablePartField[int] = None
    """Sorting position of the channel (channels with the same position are sorted by id)."""

    permission_overwrites: OptionalNullablePartField[list[PermissionOverwritePart]] = None
    """Explicit permission overwrites for members and roles."""

    rate_limit_per_user: OptionalNullablePartField[int] = None
    """Seconds user must wait between sending messages in the channel."""

    parent_id: OptionalNullablePartField[Snowflake] = None
    """Category ID of the channel."""

    nsfw: OptionalNullablePartField[bool] = None
    """If the channel is flagged NSFW."""

    default_auto_archive_duration: OptionalNullablePartField[int] = None
    """Default duration in minutes threads will be hidden after period of inactivity."""

    default_reaction_emoji: OptionalNullablePartField[DefaultReactionPart] = None
    """Emoji to show in the add reaction button in a `GUILD_FORUM` post."""

    available_tags: OptionalNullablePartField[list[TagPart]] = None
    """Set of tags that can be applied to a `GUILD_FORUM` post."""

    default_sort_order: OptionalNullablePartField[SortOrderType] = None
    """Default forum sort order."""

    default_forum_layout: OptionalNullablePartField[ForumLayoutType] = None
    """Default forum layout view."""

    default_thread_rate_limit_per_user: OptionalNullablePartField[int] = None
    """Rate limit per user set on newly created threads.
    
    !!! note
        This field does not live update!
    """

    type: ChannelType = field(init=False, default=ChannelType.GUILD_FORUM)
    """Type of channel. Always `ChannelType.GUILD_FORUM` for this class."""
