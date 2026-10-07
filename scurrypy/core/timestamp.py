from datetime import datetime

from ..enums.enum_types import DiscordString

class TimestampStyle(DiscordString):
    """Represents styles for Discord's timestamps."""

    SHORT_TIME = 't'
    """Format `HH:MM`."""

    MEDIUM_TIME = 'T'
    """Format `HH:MM:SS`."""

    SHORT_DATE = 'd'
    """Format `MM/DD/YYYY`."""
    
    LONG_DATE = 'D'
    """Format `Month DD, YYYY`."""

    LONG_DATE_SHORT_TIME = 'f'
    """Format `Month DD, YYYY HH:MM`."""

    FULL_DATE_SHORT_TIME = 'F'
    """Format `Day, Month DD, YYYY HH:MM`."""

    SHORT_DATE_SHORT_TIME = 's'
    """Format `MM/DD/YYYY HH:MM`."""

    SHORT_DATE_MEDIUM_TIME = 'S'
    """Format `MM/DD/YYYY HH:MM:SS`."""

    RELATIVE_TIME = 'R'
    """Format from now (e.g., 4 years ago or 5 hours ago)."""

class Timestamp(str):
    """Represents a Discord timestamp in ISO8601 format."""

    @property
    def seconds(self) -> int:
        """Convert this timestamp to seconds.

        Returns:
            (int): timestamp in seconds
        """
        return int(datetime.fromisoformat(self).timestamp())

    def styled_format(self, style: TimestampStyle = TimestampStyle.LONG_DATE_SHORT_TIME) -> str:
        """Convert this timestamp to one of Discord's format styles.

        Args:
            style (TimestampStyle, optional): Format style. Defaults to `TimestampStyle.LONG_DATE_SHORT_TIME`.

        Returns:
            (str): formatted timestamp
        """
        return f"<t:{self.seconds}:{style}>"
