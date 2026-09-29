from dataclasses import dataclass

from ..core.http import HTTPClient

@dataclass
class BaseResource:
    """Represents a Discord Resource object."""

    http: HTTPClient
    """HTTP session for requests."""
