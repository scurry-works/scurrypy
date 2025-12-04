from dataclasses import dataclass
from typing import Any

from ..core.http import HTTPClient

@dataclass
class BaseResource:
    """Represents a Discord Resource object."""

    _http: HTTPClient
    """HTTP session for requests."""

    context: Any
    """Associated user data."""
