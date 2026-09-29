from dataclasses import dataclass

from ...core.model import DataModel, datamodel
from ...core.snowflake import Snowflake
from ...core.types import (
    PresentModelField, 
    RequiredPartField, 
    OptionalPartField, 
    RequiredNullablePartField,
    ScurrypyStr
)

from ..user import UserModel

@datamodel
class GuildBanModel(DataModel):
    """Represents the guild ban object."""

    reason: RequiredNullablePartField[ScurrypyStr]
    """Reason for the ban."""
    
    user: PresentModelField[UserModel]
    """Banned user object."""

@datamodel
class BulkGuildBanModel(DataModel):
    """Response body for creating bulk guild bans."""

    banned_users: PresentModelField[list[Snowflake]]
    """IDs of successfully banned users."""

    failed_users: PresentModelField[list[Snowflake]]
    """IDs of users not banned."""

@dataclass
class BulkGuildBanPart(DataModel):
    """Represents fields for creating a bulk ban."""

    user_ids: RequiredPartField[list[Snowflake]] = None
    """List of user IDs to ban. Max `200`."""

    delete_message_seconds: OptionalPartField[int] = None
    """seconds back to delete messages. Max `604800` (7 days). Discord defaults to `0`."""
