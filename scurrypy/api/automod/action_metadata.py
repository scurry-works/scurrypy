from dataclasses import dataclass

from ...core.part import Part
from ...core.snowflake import Snowflake
from ...core.types import (
    RequiredPartField, 
    OptionalNullablePartField
)

class AutoModerationActionMetadataPart:
    """Base class for auto moderation action metadata parts."""
    __slots__ = ()

@dataclass
class AutoModerationActionMetadataSendAlertMessagePart(AutoModerationActionMetadataPart, Part):
    """Represents fields for creating an auto moderation action metadata sending alert messages."""
    
    channel_id: RequiredPartField[Snowflake] = None
    """Channel ID to which user content should be logged."""

@dataclass
class AutoModerationActionMetadataTimeoutPart(AutoModerationActionMetadataPart, Part):
    """Represents fields for creating an auto moderation action metadata setting timeout."""

    duration_seconds: RequiredPartField[int] = None
    """Timeout duration in seconds."""

@dataclass
class AutoModerationActionMetadataBlockMessagePart(AutoModerationActionMetadataPart, Part): 
    """Represents fields for creating an auto moderation action metadata blocking messages."""

    custom_message: OptionalNullablePartField[str] = None
    """Additional explanation to show whenever their message is blocked."""
