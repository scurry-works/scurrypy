from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import PresentModelField, OmittableModelField, OmittableNullableModelField

from ...enums.permissions import Permissions
from ...enums.channel import ChannelFlags

@dataclass
class ChannelModel(DataModel):
    """Represents common channel fields."""

    id: PresentModelField[Snowflake]
    """ID of the channel."""

    guild_id: OmittableModelField[Snowflake]
    """Guild ID of the channel."""

    position: OmittableModelField[int]
    """Position of the channel."""

    name: OmittableNullableModelField[str]
    """Name of the channel."""

    topic: OmittableNullableModelField[str]
    """Topic of the channel."""

    nsfw: OmittableModelField[bool]
    """If the channel is flagged NSFW."""

    last_message_id: OmittableNullableModelField[Snowflake]
    """ID of the last message sent in the channel."""

    rate_limit_per_user: OmittableModelField[int]
    """Seconds user must wait between sending messages in the channel."""

    parent_id: OmittableNullableModelField[Snowflake]
    """Category ID of the channel."""

    last_pin_timestamp: OmittableNullableModelField[str]
    """ISO8601 timestamp of the last pinned messsage in the channel."""

    permissions: OmittableModelField[Permissions]
    """Permissions for the invoking user in this channel.
        Includes role and overwrite calculations. [`INT_LIMIT`]
    """

    flags: OmittableModelField[ChannelFlags]
    """Channel flags combined as a bitfield."""
