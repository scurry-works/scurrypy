from dataclasses import dataclass

from ...bases.components import Component

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import Serialized, PresentModelField, OmittableModelField, OptionalPartField

from ...enums.message import MessageType, MessageFlags, MessageReferenceType

from ..components.layout import Container, ActionRow
from ..messages.attachment import AttachmentModel, AttachmentPart
from ..messages.embed import Embed
from ..messages.reaction import ReactionModel
from ..channels.channel import ChannelModel
from ..guilds.role import GuildRoleModel

from ..user import UserModel

from typing import Self

@dataclass
class MessageModel(DataModel):
    """Represents a Discord message."""

    id: PresentModelField[Snowflake]
    """ID of the message."""

    channel_id: PresentModelField[Snowflake]
    """Channel ID of the message."""

    author: PresentModelField[UserModel]
    """User data of author of the message."""
    
    content: PresentModelField[str]
    """Content of the message."""

    timestamp: PresentModelField[str]
    """Timestamp of when the message was sent."""

    edited_timestamp: PresentModelField[str]
    """Timestamp of when the message was last edited."""

    mention_everyone: PresentModelField[bool]
    """Whether the message mentions everyone."""

    mentions: PresentModelField[list[UserModel]]
    """List of mentioned users in the message."""

    mention_roles: PresentModelField[list[GuildRoleModel]]
    """List of mentioned roles in the message."""

    mention_channels: OmittableModelField[list[ChannelModel]]
    """List of mentioned channels in the message"""

    attachments: PresentModelField[list[AttachmentModel]]
    """Attached files."""

    webhook_id: OmittableModelField[Snowflake]
    """ID of the webhook if the message is a webhook."""

    embeds: PresentModelField[list[Embed]]
    """Embedded content."""

    reactions: OmittableModelField[list[ReactionModel]]
    """Reactions to the message."""

    pinned: PresentModelField[bool]
    """If the message is pinned."""

    type: PresentModelField[MessageType]
    """Type of message."""

    flags: OmittableModelField[MessageFlags]
    """Message flags."""

    thread: OmittableModelField[ChannelModel]
    """Thread created from the message."""

    components: OmittableModelField[list[Component]]
    """Components contained in the message."""

@dataclass
class PinnedMessageModel(DataModel):
    """Represents a pinned message."""

    message: PresentModelField[MessageModel]
    """Message resource of the pinned message."""

    pinned_at: PresentModelField[str]
    """ISO8601 timestamp of when the message was pinned."""

@dataclass
class MessageReferencePart(DataModel):
    """Represents the Message Reference object."""

    message_id: OptionalPartField[Snowflake] = None
    """ID of the originating message."""

    channel_id: OptionalPartField[Snowflake] = None
    """
        Channel ID of the originating message.
        !!! note
            Optional for default type, but REQUIRED for forwards.
    """

    type: OptionalPartField[MessageReferenceType] = None
    """Type of reference. Discord defaults to `MessageReferenceTypes.DEFAULT`."""

@dataclass
class MessagePart(DataModel):
    """Represents a Discord Message."""

    content: OptionalPartField[str] = None
    """Message text content."""

    flags: OptionalPartField[MessageFlags] = None
    """Message flags. Discord defaults to `MessageFlags.NO_FLAGS`."""

    components: OptionalPartField[list[ActionRow | Container]] = None
    """Components to be attached to this message."""

    attachments: OptionalPartField[list[AttachmentPart]] = None
    """Attachments to be attached to this message."""

    embeds: OptionalPartField[list[Embed]] = None
    """Embeds to be attached to this message."""

    message_reference: OptionalPartField[MessageReferencePart] = None
    """Message reference if reply."""

    def _prepare(self) -> Self:
        """Prepares MessagePart for ANY internally set attributes.

        Returns:
            (MessagePart): self
        """
        # set attachment IDs (if any)
        if self.attachments:
            for idx, file in enumerate(self.attachments):
                file.id = idx
        else:
            self.attachments = []
        
        return self

    def to_dict(self) -> Serialized:
        if self.components:
            for component in self.components:
                if not isinstance(component, Container):
                    continue

                if not self.flags or MessageFlags.IS_COMPONENTS_V2 not in self.flags:
                    raise ValueError("V2 components are used but MessageFlags.IS_COMPONENTS_V2 is not set.")
        
        return super().to_dict()
