from dataclasses import dataclass, field
from ..core.model import DataModel

from typing import Optional, TypedDict, Unpack

from .embed import EmbedPart
from .components import ActionRowPart
from .components_v2 import ContainerPart

class MessageFlags:
    """Flags that can be applied to a message."""

    CROSSPOSTED = 1 << 0
    """Message has been published."""

    IS_CROSSPOST = 1 << 1
    """Message originated from another channel."""

    SUPPRESS_EMBEDS = 1 << 2
    """Hide embeds (if any)."""

    EPHEMERAL = 1 << 6
    """Only visible to the invoking user."""

    LOADING = 1 << 7
    """Thinking response."""

    IS_COMPONENTS_V2 = 1 << 15
    """This message includes Discord's V2 Components."""

class MessageFlagParams(TypedDict, total=False):
    """Parameters for setting message flags. See [`MessageFlags`][scurrypy.parts.message.MessageFlags]."""
    crossposted: bool
    is_crosspost: bool
    suppress_embeds: bool
    ephemeral: bool
    loading: bool
    is_components_v2: bool

class MessageReferenceTypes:
    """Constants associated with how reference data is populated."""

    DEFAULT = 0
    """Standard reference used by replies."""

    FORWARD = 1
    """Reference used to point to a message at a point in time."""

@dataclass
class MessageReference(DataModel):
    """Represents the Message Reference object."""

    message_id: int
    """ID of the originating message."""

    channel_id: int
    """
        Channel ID of the originating message.
        !!! note
            Optional for default type, but REQUIRED for forwards.
    """

    type: int = MessageReferenceTypes.DEFAULT
    """Type of reference. Defaults to `DEFAULT`. See [`MessageReferenceTypes`][scurrypy.parts.message.MessageReferenceTypes]."""

@dataclass
class Attachment(DataModel):
    """Represents an attachment."""

    id: int = field(init=False, default=None)
    """ID of the attachment (internally set)."""

    path: str
    """Relative path to the file."""

    description: str
    """Description of the file."""

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.path.split('/')[-1],
            'description': self.description
        }

@dataclass
class MessagePart(DataModel):
    """Describes expected params when editing/creating a message."""

    content: Optional[str] = None
    """Message text content."""

    flags: Optional[int] = 0
    """Message flags. See [`MessageFlags`][scurrypy.parts.message.MessageFlags].

    !!! note
        Flags are ignored if editing an existing message.
    """

    components: Optional[list[ActionRowPart | ContainerPart]] = field(default_factory=list)
    """Components to be attached to this message."""

    attachments: Optional[list[Attachment]] = field(default_factory=list)
    """Attachments to be attached to this message."""

    embeds: Optional[list[EmbedPart]] = field(default_factory=list)
    """Embeds to be attached to this message."""

    message_reference: Optional[MessageReference] = None
    """Message reference if reply."""

    def _prepare(self):
        """Prepares MessagePart for ANY internally set attributes.

        Returns:
            (MessagePart): self
        """
        # set attachment IDs (if any)
        if self.attachments:
            for idx, file in enumerate(self.attachments):
                file.id = idx
        
        return self

    def set_flags(self, **flags: Unpack[MessageFlagParams]):
        """Set this message's flags using MessageFlagParams.

        Args:
            **flags (Unpack[MessageFlagParams]): message flags to set. (set respective flag to True to toggle.)

        Raises:
            (ValueError): invalid flag

        Returns:
            (MessagePart): self
        """
        _flag_map = {
            'crossposted': MessageFlags.CROSSPOSTED,
            'is_crosspost': MessageFlags.IS_CROSSPOST,
            'suppress_embeds': MessageFlags.SUPPRESS_EMBEDS,
            'ephemeral': MessageFlags.EPHEMERAL,
            'loading': MessageFlags.LOADING,
            'is_components_v2': MessageFlags.IS_COMPONENTS_V2,
        }

        # each flag maps to a specific bit position!
        for name, value in flags.items():
            if name not in _flag_map:
                raise ValueError(f"Invalid flag: {name}")
            if value:
                self.flags |= _flag_map[name]
                
        return self
