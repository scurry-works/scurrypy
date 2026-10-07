from dataclasses import dataclass
from typing import TypedDict

from ..core.snowflake import Snowflake

from ..api import ImageDataPart

@dataclass
class WebhookParams(TypedDict, total=False):
    """Parameters for editing a webhook."""

    name: str
    """Name of the webhook."""

    channel_id: Snowflake
    """Channel ID of the webhook."""

    avatar: ImageDataPart | None
    """Default user avatar has of the webhook."""

@dataclass
class WebhookWithTokenParams(TypedDict, total=False):
    """Parameters for editing a webhook with token."""

    name: str
    """Name of the webhook."""
    
    avatar: ImageDataPart | None
    """Default user avatar has of the webhook."""
