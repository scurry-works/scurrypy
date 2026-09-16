from dataclasses import dataclass, field

from ...core.snowflake import Snowflake
from ...core.types import RequiredPartField, OptionalNullablePartField

from ...bases.channel import GuildChannelCreate

from ...enums.channel import ChannelType

@dataclass
class GuildTextChannelPart(GuildChannelCreate):
    """Parameters for creating a guild text channel."""

    name: RequiredPartField[str] = None
    """Name of the channel."""

    topic: OptionalNullablePartField[str] = None
    """Topic of the channel."""

    position: OptionalNullablePartField[int] = None
    """Sorting position of the channel (channels with the same position are sorted by id)."""

    rate_limit_per_user: OptionalNullablePartField[int] = None
    """Seconds user must wait between sending messages in the channel."""

    parent_id: OptionalNullablePartField[Snowflake] = None
    """Category ID of the channel."""

    nsfw: OptionalNullablePartField[bool] = None
    """If the channel is flagged NSFW."""

    default_auto_archive_duration: OptionalNullablePartField[int] = None
    """Default duration in minutes threads will be hidden after period of inactivity."""

    default_thread_rate_limit_per_user: OptionalNullablePartField[int] = None
    """Rate limit per user set on newly created threads.
    
    !!! note
        This field does not live update!
    """

    type: ChannelType = field(init=False, default=ChannelType.GUILD_TEXT)
    """Type of channel. Always `ChannelType.GUILD_TEXT` for this class."""
