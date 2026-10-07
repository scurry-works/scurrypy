from dataclasses import dataclass

from ...core.part import Part
from ...core.types import (
    RequiredPartField, 
    OptionalPartField, 
    OptionalNullablePartField
)

from ...enums import ChannelType, AutoArchiveDurationType

from ..permission_overwrite import PermissionOverwritePart

@dataclass
class ThreadFromMessagePart(Part):
    """Represents fields for creating a thread attached to a message."""

    name: RequiredPartField[str] = None
    """Name of the thread."""

    auto_archive_duration: OptionalPartField[AutoArchiveDurationType] = None
    """Duration in minutes threads will be hidden after period of inactivity."""

    rate_limit_per_user: OptionalNullablePartField[int] = None
    """Seconds user must wait between sending messages in the channel."""

    permission_overwrites: OptionalNullablePartField[list[PermissionOverwritePart]] = None
    """Explicit permission overwrites for members and roles."""

@dataclass
class ThreadWithoutMessagePart(Part):
    """Represents fields for creating a thread without a message."""

    name: RequiredPartField[str] = None
    """Name of the thread."""

    auto_archive_duration: OptionalPartField[AutoArchiveDurationType] = None
    """Duration in minutes threads will be hidden after period of inactivity."""

    type: OptionalPartField[ChannelType] = None
    """Type of thread to create. If omitted, Discord defaults to `ChannelType.PRIVATE_THREAD`."""

    invitable: OptionalPartField[bool] = None
    """Whether non-moderators can add other non-moderators to the thread (private threads only)."""

    rate_limit_per_user: OptionalNullablePartField[int] = None
    """Seconds user must wait between sending messages in the channel."""

    permission_overwrites: OptionalNullablePartField[list[PermissionOverwritePart]] = None
    """Explicit permission overwrites for members and roles."""
