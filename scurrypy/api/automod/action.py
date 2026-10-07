from dataclasses import dataclass, field

from ...core.part import Part
from ...core.types import OptionalPartField

from ...enums import AutoModerationActionType

from .action_metadata import (
    AutoModerationActionMetadataSendAlertMessagePart,
    AutoModerationActionMetadataTimeoutPart,
    AutoModerationActionMetadataBlockMessagePart
)

class AutoModerationActionPart:
    """Base class for auto moderation action parts."""
    __slots__ = ()

@dataclass
class AutoModerationActionSendMessageAlertPart(AutoModerationActionPart, Part):
    """Represents fields for creating an auto moderation action sending alert messages."""
    
    metadata: OptionalPartField[AutoModerationActionMetadataSendAlertMessagePart] = None
    """Additional metadata needed during execution."""

    type: AutoModerationActionType = field(init=False, default=AutoModerationActionType.SEND_ALERT_MESSAGE)
    """Type of action. Always `AutoModerationActionType.SEND_ALERT_MESSAGE` for this class."""

@dataclass
class AutoModerationActionTimeoutPart(AutoModerationActionPart, Part):
    """Represents fields for creating an auto moderation action setting timeouts."""

    metadata: OptionalPartField[AutoModerationActionMetadataTimeoutPart] = None
    """Additional metadata needed during execution."""

    type: AutoModerationActionType = field(init=False, default=AutoModerationActionType.TIMEOUT)
    """Type of action. Always `AutoModerationActionType.TIMEOUT` for this class."""

@dataclass
class AutoModerationActionBlockMessagePart(AutoModerationActionPart, Part):
    """Represents fields for creating an auto moderation action blocking messages."""

    metadata: OptionalPartField[AutoModerationActionMetadataBlockMessagePart] = None
    """Additional metadata needed during execution."""
    
    type: AutoModerationActionType = field(init=False, default=AutoModerationActionType.BLOCK_MESSAGE)
    """Type of action. Always `AutoModerationActionType.BLOCK_MESSAGE` for this class."""
