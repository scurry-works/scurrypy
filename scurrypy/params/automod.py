from typing import TypedDict
from ..core.snowflake import Snowflake

from ..enums.automod import AutoModerationEventType
from ..api.automod import AutoModerationTriggerMetadataPart, AutoModerationActionPart

class AutoModerationRuleParams(TypedDict, total=False):
    """Parameters for editing an auto moderation rule."""
    
    name: str
    """Rule name."""

    event_type: AutoModerationEventType
    """Event type."""

    trigger_metadata: AutoModerationTriggerMetadataPart
    """Additional data used to determine whether a rule should be triggered.
    
    !!! note
        Must be the same AutoModerationTriggerMetadataPart child 
        used when the rule was created.
    """

    actions: list[AutoModerationActionPart]
    """The actions which will execute when the rule is triggered."""
    
    enabled: bool
    """Whether the rule is enabled."""

    exempt_roles: list[Snowflake]
    """Role ids that should not be affected by the rule."""
    
    exempt_channels: list[Snowflake]
    """Channel ids that should not be affected by the rule."""
