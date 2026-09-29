from enum import IntFlag, IntEnum, StrEnum
from typing import Self

class DiscordTypes(IntEnum):
    """Base class for Discord's types."""

    @classmethod
    def from_dict(cls, v: str) -> Self:
        """Deserialize this Discord type.

        Args:
            v (str): serialized Discord type

        Returns:
            (DiscordTypes): DiscordTypes object
        """
        return cls(int(v))
    
class DiscordFlags(IntFlag):
    """Base class for Discord's flags."""

    @classmethod
    def from_dict(cls, v: str | None) -> Self:
        """Deserialize this Discord flag.

        Args:
            v (str | None): serialized Discord flag

        Returns:
            (DiscordFlags): DiscordFlags object
        """
        if not v:
            return cls(0)
        return cls(int(v))

class DiscordString(StrEnum):
    """Base class for Discord's pre-defined strings."""

    @classmethod
    def from_dict(cls, v: str) -> Self:
        """Deserialize this pre-defined Discord string.

        Args:
            v (str): serialized Discord string

        Returns:
            (DiscordString): DiscordString object
        """
        return cls(str(v))
