from .enum_types import DiscordTypes

class AutoModerationTriggerType(DiscordTypes):
    """Represents the type of content which can trigger the rule."""

    KEYWORD = 1
    """Check if content contains words from a user defined list of keywords."""
    
    SPAM = 3
    """Check if content represents generic spam."""

    KEYWORD_PRESET = 4
    """Check if content contains words from internal pre-defined wordsets."""
    
    MENTION_SPAM = 5
    """Check if content contains more unique mentions than allowed."""
    
    MEMBER_PROFILE = 6
    """Check if member profile contains words from a user defined list of keywords."""

class AutoModerationKeywordPresetType(DiscordTypes):
    """Represents auto moderation keyword preset types."""
    
    PROFANITY = 1
    """Words that may be considered forms of swearing or cursing."""

    SEXUAL_CONTENT = 2
    """Words that refer to sexually explicit behavior or activity."""

    SLURS = 3
    """Personal insults or words that may be considered hate speech."""

class AutoModerationEventType(DiscordTypes):
    """Represents event types in which a rule should be checked."""

    MESSAGE_SEND = 1
    """When a member sends or edits a message in the guild."""

    MEMBER_UPDATE = 2
    """When a member edits their profile."""

class AutoModerationActionType(DiscordTypes):
    """Represents action types taken when an automoderation rule triggers."""

    BLOCK_MESSAGE = 1
    """Blocks a member's message and prevents it from being posted."""
    
    SEND_ALERT_MESSAGE = 2
    """Logs user content to a specified channel."""
    
    TIMEOUT = 3
    """Timeout user for a specified duration (`TIMEOUT` and `MENTION_SPAM` only).
    
    !!! important "Permissions"
        Requires `MODERATE_MEMBERS` to use `TIMEOUT`
    """

    BLOCK_MEMBER_INTERACTION = 4
    """Prevents a member from using text, voice, or other interactions."""
