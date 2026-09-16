from dataclasses import dataclass

from ...core.model import DataModel
from ...core.types import PresentModelField

from ..emoji import EmojiModel

@dataclass
class ReactionCountDetailsModel(DataModel):
    """Represents details for the reaction."""

    burst: PresentModelField[int]
    """Count of super reactions."""

    normal: PresentModelField[int]
    """Count of normal reactions."""

@dataclass
class ReactionModel(DataModel):
    """Represents a reaction made."""

    count: PresentModelField[int]
    """Total number of times this reaction was made."""

    count_details: PresentModelField[ReactionCountDetailsModel]

    me: PresentModelField[bool]
    """Whether the bot has reacted with this emoji."""

    me_burst: PresentModelField[bool]
    """Whether the bot has reacted with a super emoji."""

    emoji: PresentModelField[EmojiModel]
    """Emoji info."""

    burst_colors: PresentModelField[list[str]]
    """List of hext colors for the super reaction."""
