from dataclasses import dataclass

from ..core.part import Part
from ..core.snowflake import Snowflake
from ..core.types import OptionalPartField

@dataclass
class InvitePart(Part):
    """Represents fields for creating an invite."""

    max_age: OptionalPartField[int] = None
    """Duration of invite (in seconds) before it expires. 
    `0` for never or up to `604800` (max 7 days).
    Discord defaults to `86400` (24 hours).
    """

    max_uses: OptionalPartField[int] = None
    """Max number of uses for this invite.
    `0` for unlimited or up to `100`.
    Discord defaults to `0`.
    """

    temporary: OptionalPartField[bool] = None
    """Whether this invite grants temporary membership.
    Discord defaults to `False`.
    """

    unique: OptionalPartField[bool] = None
    """Whether to reuse similar invite codes.
    Discord defaults to `False`.
    """

    role_ids: OptionalPartField[list[Snowflake]] = None
    """Role IDs to be given when the user accept this invite.
    
    !!! important "Permissions"
        Requires `MANAGE_ROLES` and cannot assign roles with higher
        permissions than the sender.
    """

    target_user_ids: OptionalPartField[list[Snowflake]] = None
    """IDs of all users able to see and accept this invite."""
