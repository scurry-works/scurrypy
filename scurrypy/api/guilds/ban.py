from dataclasses import dataclass

from ...core.part import Part
from ...core.snowflake import Snowflake
from ...core.types import (
    RequiredPartField, 
    OptionalPartField
)

@dataclass
class BulkGuildBanPart(Part):
    """Represents fields for creating a bulk ban."""

    user_ids: RequiredPartField[list[Snowflake]] = None
    """List of user IDs to ban. Max `200`."""

    delete_message_seconds: OptionalPartField[int] = None
    """seconds back to delete messages. Max `604800` (7 days). Discord defaults to `0`."""
