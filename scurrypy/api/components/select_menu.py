from dataclasses import dataclass, field

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import RequiredPartField, OptionalPartField

from ...bases.components import (
    ActionRowChild, 
    LabelChild,
    Component
)

from ...enums.components import ComponentType, DefaultValueType

from ..emoji import EmojiModel

@dataclass
class SelectOption(DataModel):
    """Represents the Select Option component."""

    label: RequiredPartField[str] = None
    """User-facing name of the option."""

    value: RequiredPartField[str] = None
    """Developer-defined value of the option."""

    description: OptionalPartField[str] = None
    """Additional description of the option."""

    emoji: OptionalPartField[EmojiModel] = None
    """Partial emoji object."""

    default: OptionalPartField[bool] = None
    """Whether this option is selected by default. Discord defaults to `False`."""

@dataclass
class StringSelect(Component, ActionRowChild, LabelChild):
    """Represents the String Select component.
    
    A String Select allows users to select one or more provided options.
    """

    custom_id: RequiredPartField[str] = None
    """ID for the select menu."""

    options: RequiredPartField[list[SelectOption]] = None
    """Specified choices in a select menu."""

    placeholder: OptionalPartField[str] = None
    """Placeholder text if nothing is selected or default."""

    min_values: OptionalPartField[int] = None
    """Minimum number of items that must be chosen. Discord defaults to `1`."""

    max_values: OptionalPartField[int] = None
    """Maximum number of items that can be chosen. Discord defaults to `1`."""

    required: OptionalPartField[bool] = None
    """Whether the string select is required to answer in a modal. Discord defaults to `True`."""

    disabled: OptionalPartField[bool] = None
    """Whether select menu is disabled in a message. Discord defaults to `False`.
    
    !!! warning
        Does not work on Modals!
    """

    type: ComponentType = field(init=False, default=ComponentType.STRING_SELECT)
    """Component type. Always `ComponentType.STRING_SELECT` for this class."""


@dataclass
class DefaultValue(DataModel):
    """Represents the Default Value for Select components."""

    id:RequiredPartField [Snowflake] = None
    """ID of role, user, or channel."""

    type: RequiredPartField[DefaultValueType] = None
    """Type of value that `id` represents."""

@dataclass
class SelectMenuMixin:
    """Represents common fields for Discord's select menus."""

    custom_id: RequiredPartField[str] = None
    """ID for the select menu."""

    placeholder: OptionalPartField[str] = None
    """Placeholder text if nothing is selected."""

    default_values: OptionalPartField[list[DefaultValue]] = None
    """
        List of default values for auto-populated select menu components.
        Number of default values must be in the range of `min_values` to `max_values`.
    """

    min_values: OptionalPartField[int] = None
    """Minimum number of items that must be chosen. Discord defaults to `1`."""

    max_values: OptionalPartField[int] = None
    """Maximum number of items that can be chosen. Discord defaults to `1`."""

    required: OptionalPartField[bool] = None
    """Whether the select is required to answer in a modal. Discord defaults to `True`."""

    disabled: OptionalPartField[bool] = None
    """Whether select menu is disabled in a message. Discord defaults to `False`."""

@dataclass
class UserSelect(SelectMenuMixin, Component, ActionRowChild, LabelChild):
    """Represents the User Select component.
    
    User Select allows users to select one or more users.
    """

    type: ComponentType = field(init=False, default=ComponentType.USER_SELECT)
    """Component type. Always `ComponentType.USER_SELECT` for this class."""

@dataclass
class RoleSelect(SelectMenuMixin, Component, ActionRowChild, LabelChild):
    """Represents the Role Select component.
    
    A Role Select allows users to select one or more roles
    """

    type: ComponentType = field(init=False, default=ComponentType.ROLE_SELECT)
    """Component type. Always `ComponentType.ROLE_SELECT` for this class."""

@dataclass
class MentionableSelect(SelectMenuMixin, Component, ActionRowChild, LabelChild):
    """Represents the Mentionable Select component.
    
    A Mentionable Select allows users to select one or more mentionables.
    """

    type: ComponentType = field(init=False, default=ComponentType.MENTIONABLE_SELECT)
    """Component type. Always `ComponentType.MENTIONABLE_SELECT` for this class."""

@dataclass
class ChannelSelect(SelectMenuMixin, Component, ActionRowChild, LabelChild):
    """Represents the Channel Select component.
    
    A Channel Select allows users to select one or more channels.
    """

    type: ComponentType = field(init=False, default=ComponentType.CHANNEL_SELECT)
    """Component type. Always `ComponentType.CHANNEL_SELECT` for this class."""
