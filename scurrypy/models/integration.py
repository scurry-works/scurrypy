from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from .application import ApplicationModel

@dataclass
class IntegrationModel(DataModel):
    """Represents a guild integration."""

    id: int
    """ID of the integration."""

    name: str
    """Name of the integration."""

    type: str
    """Type of integration (e.g.,`'twitch'`, `'youtube'`, `'discord'`, or `'guild_subscription'`)."""

    enabled: bool
    """If the integration is enabled."""

    application: Optional[ApplicationModel]
    """The bot application for Discord integrations."""
