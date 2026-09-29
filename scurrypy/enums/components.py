from .enum_types import DiscordTypes, DiscordString

class ComponentType(DiscordTypes):
    """Represents component type constants"""

    ACTION_ROW = 1
    """Container to display a row of interactive components."""

    BUTTON = 2
    """Button object."""

    STRING_SELECT = 3
    """Select menu for picking from defined text options."""

    TEXT_INPUT = 4
    """Text input object."""

    USER_SELECT = 5
    """Select menu for users."""

    ROLE_SELECT = 6
    """Select menu for roles."""

    MENTIONABLE_SELECT = 7
    """Select menu for mentionables (users and roles)."""

    CHANNEL_SELECT = 8
    """Select menu for channels."""

    SECTION = 9
    """Container to display text alongside an accessory component."""

    TEXT_DISPLAY = 10
    """Markdown text."""

    THUMBNAIL = 11
    """Small image that can be used as an accessory."""

    MEDIA_GALLERY = 12
    """Display images and other media."""

    FILE = 13
    """Displays an attached file."""

    SEPARATOR = 14
    """Component to add vertical padding between other components."""

    CONTAINER = 17
    """Container that visually groups a set of components."""

    LABEL = 18
    """Container associating a label and description with a component."""

    FILE_UPLOAD = 19
    """Component for uploading files."""

    RADIO_GROUP = 21
    """Single-choice set of options."""

    CHECKBOX_GROUP = 22
    """Multi-selectable group of checkboxes."""
    
    CHECKBOX = 23
    """Single checkbox for yes/no choice."""

class SeparatorType(DiscordTypes):
    """Represents separator type constants."""

    SMALL_PADDING = 1
    """Small separator padding."""
    
    LARGE_PADDING = 2
    """Large separator padding."""

class ButtonStyle(DiscordTypes):
    """Represents button styles for a Button component."""

    PRIMARY = 1
    """The most important or recommended action in a group of options. (Blurple)"""

    SECONDARY = 2
    """Alternative or supporting actions. (Gray)"""

    SUCCESS = 3
    """Positive confirmation or completion actions. (Green)"""

    DANGER = 4
    """An action with irreversible consequences. (Red)"""

    LINK = 5
    """Navigates to a URL. (Gray + window)"""

class TextInputStyle(DiscordTypes):
    """Represents the types of Text Inputs."""

    SHORT = 1
    """One line text input."""

    PARAGRAPH = 2
    """Multi-line text input."""

class DefaultValueType(DiscordString):
    """Represents types of default values for select menus."""

    ROLE = "role"
    """Default value is a role."""

    CHANNEL = "channel"
    """Default value is a channel."""

    USER = "user"
    """Default value is a user."""
