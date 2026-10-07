from dataclasses import dataclass

from ...core.part import Part
from ...core.snowflake import Snowflake
from ...core.types import (
    RequiredPartField, 
    OptionalPartField
)

from ...enums import AutoModerationTriggerType, AutoModerationEventType

from .trigger_metadata import AutoModerationTriggerMetadataPart

from .action import AutoModerationActionPart

@dataclass
class AutoModerationRulePart(Part):
    """Represents fields for creating an auto moderation rule."""

    name: RequiredPartField[str] = None
    """Name of this rule."""

    event_type: RequiredPartField[AutoModerationEventType] = None
    """Event type of this rule."""

    trigger_type: RequiredPartField[AutoModerationTriggerType] = None
    """Trigger type of this rule."""

    trigger_metadata: OptionalPartField[AutoModerationTriggerMetadataPart] = None
    """Trigger metadata of this rule."""

    actions: RequiredPartField[list[AutoModerationActionPart]] = None
    """Actions executed when this rule is triggered."""

    enabled: OptionalPartField[bool] = None
    """Whether this rule is enabled."""

    exempt_roles: OptionalPartField[list[Snowflake]] = None
    """Role IDs that should not be affected by the rule."""

    exempt_channels: OptionalPartField[list[Snowflake]] = None
    """Channel IDs that should not be affected by the rule."""
