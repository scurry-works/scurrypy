from dataclasses import dataclass, field

from ...core.types import RequiredPartField, OptionalPartField

from ...bases.components import (
    Component,
    ActionRowChild, 
    SectionAccessoryChild
)

from ...enums.components import (
    ComponentType,
    ButtonStyle
)

from ..emoji import EmojiModel

@dataclass
class Button(Component, ActionRowChild, SectionAccessoryChild):
    """Represents the Button component.
    
    A pressable button!
    """

    style: RequiredPartField[ButtonStyle] = None
    """A button style."""

    custom_id: OptionalPartField[str] = None
    """ID for the button. Do not supply for `ButtonStyles.LINK` style buttons."""

    label: OptionalPartField[str] = None
    """Text that appears on the button."""

    emoji: OptionalPartField[EmojiModel] = None
    """Emoji icon for the button."""

    url: OptionalPartField[str] = None
    """URL for link-style buttons."""

    disabled: OptionalPartField[bool] = None
    """Whether the button is disabled. Discord defaults to `False`."""

    type: ComponentType = field(init=False, default=ComponentType.BUTTON)
    """Component type. Always `ComponentType.BUTTON` for this class."""
