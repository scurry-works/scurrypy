from typing import TypedDict

from ..api.components.layout import ActionRow, Container
from ..api.messages import AttachmentPart, EmbedPart, MessageReferencePart

class EditMessageParams(TypedDict, total=False):
    """Parameters for editing a message."""

    content: str
    """Message text content."""

    components: list[ActionRow | Container]
    """Components to be attached to this message."""

    attachments: list[AttachmentPart]
    """Attachments to be attached to this message."""

    embeds: list[EmbedPart]
    """Embeds to be attached to this message."""

    message_reference: MessageReferencePart
    """Message reference if reply."""
