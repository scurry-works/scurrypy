from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import PresentModelField

@dataclass
class FollowedChannelModel(DataModel):
    """Represents the followed channel object."""

    channel_id: PresentModelField[Snowflake]
    """ID of the source channel."""

    webhook_id: PresentModelField[Snowflake]
    """Target webhook ID created."""
