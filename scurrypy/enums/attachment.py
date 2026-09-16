from .enum_types import DiscordFlags

class AttachmentFlags(DiscordFlags):
    IS_CLIP = 1 << 0
    """This attachment is a Clip from a stream."""

    IS_THUMBNAIL = 1 << 1
    """This attachment is the thumbnail of a thread in a media channel. 
        Displayed in the grid but not on the message.
    """

    IS_SPOILER = 1 << 3
    """This attachment was marked as a spoiler and is blurred until clicked."""

    IS_ANIMATED = 1 << 5
    """This attachment is an animated image."""
