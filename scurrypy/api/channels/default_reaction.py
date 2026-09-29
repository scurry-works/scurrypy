from dataclasses import dataclass

from ...core.model import DataModel, datamodel
from ...core.snowflake import Snowflake
from ...core.types import PresentNullableModelField, RequiredNullablePartField, ScurrypyStr

@datamodel
class DefaultReactionModel(DataModel):
    """Represents the default reaction for a `GUILD_FORUM` post."""

    emoji_id: PresentNullableModelField[Snowflake]
    """ID of the guild's custom emoji."""

    emoji_name: PresentNullableModelField[ScurrypyStr]
    """Unicode character of the emoji."""

@dataclass
class DefaultReactionPart(DataModel):
    """Represents the default reaction for a `GUILD_FORUM` post."""

    emoji_id: RequiredNullablePartField[int] = None
    """ID of the guild's custom emoji."""

    emoji_name: RequiredNullablePartField[ScurrypyStr] = None
    """Unicode character of the emoji."""
