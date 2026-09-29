from ...core.model import DataModel, datamodel
from ...core.types import (
    PresentModelField, 
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool
)

from ..emoji import EmojiModel

@datamodel
class ReactionCountDetailsModel(DataModel):
    """Represents details for the reaction."""

    burst: PresentModelField[ScurrypyInt]
    """Count of super reactions."""

    normal: PresentModelField[ScurrypyInt]
    """Count of normal reactions."""

@datamodel
class ReactionModel(DataModel):
    """Represents a reaction made."""

    count: PresentModelField[ScurrypyInt]
    """Total number of times this reaction was made."""

    count_details: PresentModelField[ReactionCountDetailsModel]

    me: PresentModelField[ScurrypyBool]
    """Whether the bot has reacted with this emoji."""

    me_burst: PresentModelField[ScurrypyBool]
    """Whether the bot has reacted with a super emoji."""

    emoji: PresentModelField[EmojiModel]
    """Emoji info."""

    burst_colors: PresentModelField[list[ScurrypyStr]]
    """List of hext colors for the super reaction."""
