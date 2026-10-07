from dataclasses import dataclass

from ..core.part import Part
from ..core.types import (
    RequiredPartField,
    OptionalPartField
)

from ..enums import PollLayoutType

from .emoji import EmojiPart

@dataclass
class PollMediaPart(Part):
    """Represents fields for creating a poll media field."""

    text: OptionalPartField[str] = None
    """Text of the field."""

    emoji: OptionalPartField[EmojiPart] = None # EITHER id or name
    """Emoji of the field.
    
    !!! note
        Only fill ID (if custom emoji) OR name (if standard emoji).
    """

@dataclass
class PollAnswerPart(Part):
    """Represents fields for creating a poll answer."""

    poll_media: RequiredPartField[PollMediaPart] = None
    """Data of the answer."""

@dataclass
class PollPart(Part):
    """Represents fields for creating a poll."""

    question: RequiredPartField[PollMediaPart] = None
    """Question of the poll."""

    answers: RequiredPartField[list[PollAnswerPart]] = None
    """Possible answers to the poll."""

    duration: OptionalPartField[int] = None
    """Duration (in hours) before poll expires."""

    allow_multiselect: OptionalPartField[bool] = None
    """Whether a user can select multiple answers."""

    layout_type: OptionalPartField[PollLayoutType] = None
    """Layout type of the poll."""
