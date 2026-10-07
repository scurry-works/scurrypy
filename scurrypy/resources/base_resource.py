from dataclasses import dataclass

from ..core.http import HttpClient

@dataclass
class BaseResource:
    """Represents a Discord resource."""

    http: HttpClient
    """HTTP session for requests."""
