from datetime import datetime, timezone

DISCORD_EPOCH = 1420070400000

class Snowflake(int):
    """Represents a Discord snowflake ID."""

    @property
    def timestamp_ms(self) -> int:
        """Timestamp associated with the ID as an integer in milliseconds (ms)."""
        return (self >> 22) + DISCORD_EPOCH

    @property
    def datetime(self) -> datetime:
        """Timestamp associated with the ID as a `datetime` object."""
        return datetime.fromtimestamp(self.timestamp_ms / 1000, tz=timezone.utc)

    @property
    def isoformat(self) -> str:
        """Timestamp associated with the ID as a string in ISO8601 format."""
        return self.datetime.isoformat()

    @property
    def worker_id(self) -> int:
        """Worker ID associated with the ID."""
        return (self & 0x3E0000) >> 17

    @property
    def process_id(self) -> int:
        """Process ID associated with the ID."""
        return (self & 0x1F000) >> 12

    @property
    def increment(self) -> int:
        """Increment associated with the ID."""
        return self & 0xFFF
