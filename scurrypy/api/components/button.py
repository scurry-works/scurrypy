from dataclasses import dataclass, field

from ...core.part import Part
from ...core.types import RequiredPartField, OptionalPartField

from ...bases import (
    Component,
    ActionRowChild, 
    SectionAccessoryChild
)

from ...enums import ComponentType, ButtonStyle

from ..emoji import EmojiPart

@dataclass
class Button(Part, Component, ActionRowChild, SectionAccessoryChild):
    """A pressable button!"""

    style: RequiredPartField[ButtonStyle] = None
    """A button style."""

    custom_id: OptionalPartField[str] = None
    """ID for the button. Do not supply for `ButtonStyles.LINK` style buttons."""

    label: OptionalPartField[str] = None
    """Text that appears on the button."""

    emoji: OptionalPartField[EmojiPart] = None
    """Emoji icon for the button."""

    url: OptionalPartField[str] = None
    """URL for link-style buttons."""

    disabled: OptionalPartField[bool] = None
    """Whether the button is disabled. Discord defaults to `False`."""

    type: ComponentType = field(init=False, default=ComponentType.BUTTON)
    """Component type. Always `ComponentType.BUTTON` for this class."""
