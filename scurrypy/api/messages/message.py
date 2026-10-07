from dataclasses import dataclass
from typing import Self

from ...bases.components import ContainerComponent

from ...core.part import Part
from ...core.snowflake import Snowflake
from ...core.types import (
    Serialized, 
    OptionalPartField
)

from ...enums import (
    MessageFlags, 
    MessageReferenceType
)

from ..components import Container
from ..poll import PollPart

from .embed import EmbedPart
from .attachment import AttachmentPart

@dataclass
class MessageReferencePart(Part):
    """Represents fields for creating a message reference."""

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
class MessagePart(Part):
    """Represents fields for creating a Discord message."""

    content: OptionalPartField[str] = None
    """Message text content."""

    flags: OptionalPartField[MessageFlags] = None
    """Message flags. Discord defaults to `MessageFlags.NO_FLAGS`."""

    components: OptionalPartField[list[ContainerComponent]] = None
    """Components to be attached to this message."""

    attachments: OptionalPartField[list[AttachmentPart]] = None
    """Attachments to be attached to this message."""

    embeds: OptionalPartField[list[EmbedPart]] = None
    """Embeds to be attached to this message."""

    message_reference: OptionalPartField[MessageReferencePart] = None
    """Message reference if reply."""

    poll: OptionalPartField[PollPart] = None
    """A poll!"""

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
