from typing import TypedDict

from ..enums.message import MessageFlags

from ..api.components.layout import ActionRow, Container
from ..api.messages.attachment import AttachmentPart
from ..api.messages.embed import Embed
from ..api.messages.message import MessageReferencePart

class EditMessageParams(TypedDict, total=False):
    """Parameters for editing a message."""

    content: str
    """Message text content."""

    flags: MessageFlags
    """Message flags.
    
    !!! note
        If omitted, existing message flags are not preserved automatically.
        Passing endpoint flags without explicitly setting `flags`
        will construct a new flags value.
    """

    components: list[ActionRow | Container]
    """Components to be attached to this message."""

    attachments: list[AttachmentPart]
    """Attachments to be attached to this message."""

    embeds: list[Embed]
    """Embeds to be attached to this message."""

    message_reference: MessageReferencePart
    """Message reference if reply."""
