from ..core.model import datamodel
from ..core.snowflake import Snowflake
from ..core.types import PresentModelField, OmittableModelField, ScurrypyBool

from .base_event import Event

from ..enums.events import EventType
from ..enums.emoji import ReactionType

from ..api.user import GuildMemberModel
from ..api.emoji import EmojiModel

@datamodel
class ReactionAddEvent(Event):
    """Reaction added event."""

    dispatch_name = EventType.MESSAGE_REACTION_ADD

    type: PresentModelField[ReactionType]
    """Type of reaction added."""

    user_id: PresentModelField[Snowflake]
    """ID of user who added the emoji."""

    emoji: PresentModelField[EmojiModel]
    """Emoji used to react."""

    channel_id: PresentModelField[Snowflake]
    """ID of the channel where the reaction took place."""

    message_id: PresentModelField[Snowflake]
    """ID of the message where the reaction took place."""

    guild_id: OmittableModelField[Snowflake]
    """ID of the guild where the reaction took place (if in a guild)."""

    burst: PresentModelField[ScurrypyBool]
    """Whether the emoji is super."""

    member: OmittableModelField[GuildMemberModel]
    """Partial member object of the guild member that added the emoji (if in a guild)."""

    message_author_id: OmittableModelField[Snowflake]
    """ID of the user who sent the message where the reaction was added."""

@datamodel
class ReactionRemoveEvent(Event):
    """Reaction removed event."""

    dispatch_name = EventType.MESSAGE_REACTION_REMOVE

    type: PresentModelField[ReactionType]
    """Type of reaction removed."""

    user_id: PresentModelField[Snowflake]
    """ID of user who removed their reaction."""

    emoji: PresentModelField[EmojiModel]
    """Emoji data of the emoji where the reaction was removed."""

    channel_id: PresentModelField[Snowflake]
    """ID of the channel where the reaction was removed."""

    message_id: PresentModelField[Snowflake]
    """ID of the message where the reaction was removed."""

    guild_id: OmittableModelField[Snowflake]
    """ID of the guild where the reaction was removed (if in a guild)."""

    burst: PresentModelField[ScurrypyBool]
    """If the emoji of the removed reaction is super."""

@datamodel
class ReactionRemoveEmojiEvent(Event):
    """All reactions of a specific emoji removed."""

    dispatch_name = EventType.MESSAGE_REACTION_REMOVE_EMOJI

    emoji: PresentModelField[EmojiModel]
    """Emoji data of the removed reaction emoji."""

    channel_id: PresentModelField[Snowflake]
    """ID of the channel where the reaction emoji was removed."""

    message_id: PresentModelField[Snowflake]
    """ID of the message where the reaction emoji was removed."""

    guild_id: OmittableModelField[Snowflake]
    """ID of the guild where the reaction emoji was removed. (if in a guild)"""

@datamodel
class ReactionRemoveAllEvent(Event):
    """Remove all reactions event."""

    dispatch_name = EventType.MESSAGE_REACTION_REMOVE_ALL

    channel_id: PresentModelField[Snowflake]
    """ID of the channel where all reaction were removed."""

    message_id: PresentModelField[Snowflake]
    """ID of the message where all reaction were removed."""

    guild_id: OmittableModelField[Snowflake]
    """ID of the guild where all reaction were removed (if in a guild)."""
