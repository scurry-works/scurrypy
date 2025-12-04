from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

@dataclass
class UserModel(DataModel):
    """Describes the User object."""

    id: int
    """ID of the user."""

    username: str
    """Username of the user."""

    discriminator: str
    """Discriminator of the user (#XXXX)"""

    global_name: str
    """Global name of the user."""

    avatar: str
    """Image hash of the user's avatar."""

    bot: Optional[bool]
    """If the user is a bot."""

    system: Optional[bool]
    """If the user belongs to an OAuth2 application."""

    mfa_enabled: Optional[bool]
    """Whether the user has two factor enabled."""

    banner: Optional[str]
    """Image hash of the user's banner."""

    accent_color: Optional[int]
    """Color of user's banner represented as an integer."""

    locale: Optional[str]
    """Chosen language option of the user."""
