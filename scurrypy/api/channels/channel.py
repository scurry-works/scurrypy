from ...core.model import DataModel, datamodel
from ...core.snowflake import Snowflake
from ...core.timestamp import Timestamp
from ...core.types import (
    PresentModelField, 
    OmittableModelField, 
    OmittableNullableModelField, 
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool
)

from ...enums.permissions import Permissions
from ...enums.channel import ChannelFlags

@datamodel
class ChannelModel(DataModel):
    """Represents common channel fields."""

    id: PresentModelField[Snowflake]
    """ID of the channel."""

    guild_id: OmittableModelField[Snowflake]
    """Guild ID of the channel."""

    position: OmittableModelField[ScurrypyInt]
    """Position of the channel."""

    name: OmittableNullableModelField[ScurrypyStr]
    """Name of the channel."""

    topic: OmittableNullableModelField[ScurrypyStr]
    """Topic of the channel."""

    nsfw: OmittableModelField[ScurrypyBool]
    """If the channel is flagged NSFW."""

    last_message_id: OmittableNullableModelField[Snowflake]
    """ID of the last message sent in the channel."""

    rate_limit_per_user: OmittableModelField[ScurrypyInt]
    """Seconds user must wait between sending messages in the channel."""

    parent_id: OmittableNullableModelField[Snowflake]
    """Category ID of the channel."""

    last_pin_timestamp: OmittableNullableModelField[Timestamp]
    """ISO8601 timestamp of the last pinned messsage in the channel."""

    permissions: OmittableModelField[Permissions]
    """Permissions for the invoking user in this channel.
        Includes role and overwrite calculations. [`INT_LIMIT`]
    """

    flags: OmittableModelField[ChannelFlags]
    """Channel flags combined as a bitfield."""
