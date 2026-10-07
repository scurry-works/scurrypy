from dataclasses import dataclass

from ...core.part import Part
from ...core.types import RequiredPartField

from ...enums import AutoModerationKeywordPresetType

class AutoModerationTriggerMetadataPart:
    """Base class for auto moderation trigger metadata parts."""
    __slots__ = ()

@dataclass
class AutoModerationTriggerMetadataKeywordPart(AutoModerationTriggerMetadataPart, Part):
    """Represents fields for creating an auto moderation trigger metadata keyword."""

    keyword_filter: RequiredPartField[list[str]] = None
    """Substrings to be searched."""

    regex_patterns: RequiredPartField[list[str]] = None
    """Regular expression patterns to be matched against."""

    allow_list: RequiredPartField[list[str]] = None
    """Substrings which should not trigger the rule."""

@dataclass
class AutoModerationTriggerMetadataMemberProfilePart(AutoModerationTriggerMetadataPart, Part):
    """Represents fields for creating an auto moderation trigger metadata member profile."""

    keyword_filter: RequiredPartField[list[str]] = None
    """Substrings to be searched."""

    regex_patterns: RequiredPartField[list[str]] = None
    """Regular expression patterns to be matched against."""

    allow_list: RequiredPartField[list[str]] = None
    """Substrings which should not trigger the rule."""

@dataclass
class AutoModerationTriggerMetadataKeywordPresetPart(AutoModerationTriggerMetadataPart, Part):
    """Represents fields for creating an auto moderation trigger metadata keyword preset."""

    presets: RequiredPartField[list[AutoModerationKeywordPresetType]] = None
    """Pre-defined wordsets to be searched."""

    allow_list: RequiredPartField[list[str]] = None
    """Substrings which should not trigger the rule."""

@dataclass
class AutoModerationTriggerMetadataMentionSpamPart(AutoModerationTriggerMetadataPart, Part):
    """Represents fields for creating an auto moderation trigger metadata mention spam."""
    
    mention_total_limit: RequiredPartField[int] = None
    """Total number of unique role and user mentions allowed per message."""

    mention_raid_protection_enabled: RequiredPartField[bool] = None
    """Whether to automatically detect mention raids."""

@dataclass
class AutoModerationTriggerMetadataSpamPart(AutoModerationTriggerMetadataPart, Part):
    """Represents fields for creating an auto moderation trigger metadata spam."""
    # no fields?
    pass
