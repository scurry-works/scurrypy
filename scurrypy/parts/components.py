from dataclasses import dataclass, field
from ..core.model import DataModel

from typing import Literal, Optional

from .component_types import *
from ..models import EmojiModel

class ComponentTypes:
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8

@dataclass
class ActionRowPart(DataModel, ContainerChild):
    """Represents a container of interactable components."""
    
    components: list[ActionRowChild] = field(default_factory=list)
    """Up to 5 interactive button components or a single select component."""

    type: int = field(init=False, default=ComponentTypes.ACTION_ROW)
    """Component type. Always `ComponentTypes.ACTION_ROW` for this class. See [`ComponentTypes`][scurrypy.parts.components.ComponentTypes]."""

class ButtonStyles:
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

@dataclass
class Button(DataModel, ActionRowChild, SectionAccessoryChild):
    """Represents the Button component."""

    style: int = None
    """A button style. See [`ButtonStyles`][scurrypy.parts.components.ButtonStyles]."""

    custom_id: str = None
    """ID for the button. Do not supply for `LINK` style buttons."""

    label: Optional[str] = None
    """Text that appears on the button."""

    emoji: EmojiModel = None
    """Emoji icon as emoji string or EmojiModel if custom."""

    url: Optional[str] = None
    """URL for link-style buttons."""

    disabled: Optional[bool] = False
    """Whether the button is disabled. Defaults to False."""

    link: Optional[str] = None
    """Hyperlink for button. For `LINK` style only."""

    type: int = field(init=False, default=ComponentTypes.BUTTON)
    """Component type. Always `ComponentTypes.BUTTON` for this class. See [`ComponentTypes`][scurrypy.parts.components.ComponentTypes]."""

@dataclass
class SelectOption(DataModel):
    """Represents the Select Option component"""

    label: str = None
    """User-facing name of the option."""

    value: str = None
    """Developer-defined value of the option."""

    description: Optional[str] = None
    """Additional description of the option."""

    emoji: Optional[EmojiModel] = None
    """Partial emoji object."""

    default: Optional[bool] = False
    """Whether this option is selected by default."""

@dataclass
class StringSelect(DataModel, ActionRowChild, LabelChild):
    """Represents the String Select component."""

    custom_id: str = None
    """ID for the select menu."""

    options: list[SelectOption] = field(default_factory=list)
    """Specified choices in a select menu. See [`SelectOption`][scurrypy.parts.components.SelectOption]."""

    placeholder: Optional[str] = None
    """Placeholder text if nothing is selected or default."""

    min_values: Optional[int] = 1
    """Minimum number of items that must be chosen."""

    max_values: Optional[int] = 1
    """Maximum number of items that can be chosen."""

    required: Optional[bool] = False
    """Whether the string select is required to answer in a modal. Defaults to False."""

    disabled: Optional[bool] = False # does not work on Modals!
    """Whether select menu is disabled in a message. Defaults to False."""

    type: int = field(init=False, default=ComponentTypes.STRING_SELECT)
    """Component type. Always `ComponentTypes.STRING_SELECT` for this class. See [`ComponentTypes`][scurrypy.parts.components.ComponentTypes]."""

class TextInputStyles:
    """Represents the types of Text Inputs."""

    SHORT = 1
    """One line text input."""

    PARAGRAPH = 2
    """Multi-line text input."""

@dataclass
class TextInput(DataModel, LabelChild):
    """Represents the Text Input component."""

    custom_id: str = None
    """ID for the input."""

    style: TextInputStyles = TextInputStyles.SHORT
    """Text input style. See [`TextInputStyles`][scurrypy.parts.components.TextInputStyles]."""

    min_length: Optional[int] = None
    """Minimum input length for a text input."""

    max_length: Optional[int] = None
    """Maximum input length for a text input."""

    required: Optional[bool] = True
    """Whether this component is required to be filled. Defaults to True."""

    value: Optional[str] = None
    """Pre-filled value for this component."""

    placeholder: Optional[str] = None
    """Custom placeholder text if the input is empty."""

    type: int = field(init=False, default=ComponentTypes.TEXT_INPUT)
    """Component type. Always `ComponentTypes.TEXT_INPUT` for this class. See [`ComponentTypes`][scurrypy.parts.components.ComponentTypes]."""

@dataclass
class DefaultValue(DataModel):
    """Represents the Default Value for Select components."""

    id: int = None
    """ID of role, user, or channel."""

    type: Literal["role", "user", "channel"] = None
    """Type of value that `id` represents."""

@dataclass
class SelectMenu(DataModel):
    """Represents common fields for Discord's select menus."""

    custom_id: str = None
    """ID for the select menu."""

    placeholder: Optional[str] = None
    """Placeholder text if nothing is selected."""

    default_values: Optional[list[DefaultValue]] = field(default_factory=list)
    """
        List of default values for auto-populated select menu components. See [`DefaultValue`][scurrypy.parts.components.DefaultValue].
        Number of default values must be in the range of `min_values` to `max_values`.
    """

    min_values: Optional[int] = 1
    """Minimum number of items that must be chosen. Defaults to 1."""

    max_values: Optional[int] = 1
    """Maximum number of items that can be chosen. Defaults to 1."""

    required: Optional[bool] = False
    """Whether the select is required to answer in a modal. Defaults to False."""

    disabled: Optional[bool] = False
    """Whether select menu is disabled in a message. Defaults to False."""


@dataclass
class UserSelect(SelectMenu, ActionRowChild, LabelChild):
    """Represents the User Select component."""

    type: int = field(init=False, default=ComponentTypes.USER_SELECT)
    """Component type. Always `ComponentTypes.USER_SELECT` for this class. See [`ComponentTypes`][scurrypy.parts.components.ComponentTypes]."""

@dataclass
class RoleSelect(SelectMenu, ActionRowChild, LabelChild):
    """Represents the Role Select component."""

    type: int = field(init=False, default=ComponentTypes.ROLE_SELECT)
    """Component type. Always `ComponentTypes.ROLE_SELECT` for this class. See [`ComponentTypes`][scurrypy.parts.components.ComponentTypes]."""

@dataclass
class MentionableSelect(SelectMenu, ActionRowChild, LabelChild):
    """Represents the Mentionable Select component."""

    type: int = field(init=False, default=ComponentTypes.MENTIONABLE_SELECT)
    """Component type. Always `ComponentTypes.MENTIONABLE_SELECT` for this class. See [`ComponentTypes`][scurrypy.parts.components.ComponentTypes]."""

@dataclass
class ChannelSelect(SelectMenu, ActionRowChild, LabelChild):
    """Represents the Channel Select component."""

    type: int = field(init=False, default=ComponentTypes.CHANNEL_SELECT)
    """Component type. Always `ComponentTypes.CHANNEL_SELECT` for this class. See [`ComponentTypes`][scurrypy.parts.components.ComponentTypes]."""
