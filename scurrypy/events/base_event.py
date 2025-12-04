class Event:
    """Marker class for all gateway events."""

    name: str
    """Dispatch name of event."""

    raw: dict
    """Event's raw JSON payload. NOT A DATACLASS."""
