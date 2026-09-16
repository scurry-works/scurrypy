from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import PresentModelField, RequiredPartField, RequiredNullablePartField

from ..user import UserModel

@dataclass
class GuildBanModel(DataModel):
    """Represents the guild ban object."""

    reason: RequiredNullablePartField[str]
    """Reason for the ban."""
    
    user: PresentModelField[UserModel]
    """Banned user object."""

@dataclass
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

    delete_message_seconds: RequiredPartField[int] = None
    """seconds back to delete messages. Max `604800` (7 days). Discord defaults to `0`."""
