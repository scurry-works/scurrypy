from .enum_types import DiscordTypes

class WebhookType(DiscordTypes):
    """Constants associated with different webhook types."""
    
    INCOMING = 1
    """Webhooks can post messages to channels with a generated token."""

    CHANNEL_FOLLOWER = 2
    """Internal webhooks used with Channel Following to post new messages into channels."""
    
    APPLICATION = 3
    """Webhooks used with Interactions"""
