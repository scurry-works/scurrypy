from dataclasses import dataclass
from typing import Self

from ..core.part import Part
from ..core.snowflake import Snowflake
from ..core.types import (
    Serialized,
    RequiredPartField,
    OptionalPartField,
    OptionalNullablePartField
)

from ..bases import ContainerComponent

from ..enums.message import MessageFlags

from .components import Container
from .messages import EmbedPart, AttachmentPart
from .image_data import ImageDataPart
from .poll import PollPart

@dataclass
class WebhookPart(Part):
    """Represents fields for creating a webhook."""

    name: RequiredPartField[str] = None
    """Name of the webhook."""

    avatar: OptionalNullablePartField[ImageDataPart] = None
    """Image for the default webhook avatar."""

@dataclass
class WebhookMessagePart(Part):
    """Represents fields for creating a webhook message.
    
    !!! important
        Requires at least ONE of `content`, `attachments`, `embeds`, or `polls`.
    """

    content: RequiredPartField[str] = None
    """Message text content."""

    flags: OptionalPartField[MessageFlags] = None
    """Message flags. Discord defaults to `MessageFlags.NO_FLAGS`.
    
    !!! note
        Can only set `SUPPRESS_EMBEDS`, `SUPPRESS_NOTIFICATIONS`, and `IS_COMPONENTS_V2`.
    """

    components: OptionalPartField[list[ContainerComponent]] = None
    """Components to be attached to this message."""

    attachments: OptionalPartField[list[AttachmentPart]] = None
    """Attachments to be attached to this message."""

    embeds: OptionalPartField[list[EmbedPart]] = None
    """Embeds to be attached to this message."""

    thread_name: OptionalPartField[str] = None
    """Name of thread to create.
    
    !!! important
        Requires forum or media channel.
    """

    applied_tags: OptionalPartField[list[Snowflake]] = None
    """Array of tag IDs to apply to the thread.

    !!! important
        Requires forum or media channel.
    """

    poll: RequiredPartField[PollPart] = None
    """A poll!"""

    def _prepare(self) -> Self:
        """Prepares WebhookMessagePart for ANY internally set attributes.

        Returns:
            (WebhookMessagePart): self
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
