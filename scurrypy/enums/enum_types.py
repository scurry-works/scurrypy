from enum import IntFlag, IntEnum, StrEnum
from typing import Self

class DiscordTypes(IntEnum):
    """Base class for Discord's types."""

    @classmethod
    def from_dict(cls, v: str) -> Self | int:
        """Deserialize this Discord type.

        Args:
            v (str): serialized Discord type

        Returns:
            (DiscordTypes | int): DiscordTypes object if the value is known,
                otherwise the raw integer value.
        """
        int_v = int(v)
        if int_v in cls:
            return cls(int_v)
        return int_v
    
class DiscordFlags(IntFlag):
    """Base class for Discord's flags."""

    @classmethod
    def from_dict(cls, v: str | None) -> Self | int:
        """Deserialize this Discord flag.

        Args:
            v (str | None): serialized Discord flag

        Returns:
            (DiscordFlags | int): DiscordFlags object if the value is known,
                otherwise the raw int value.
        """
        if not v:
            return cls(0)
        int_v = int(v)
        if int_v in cls:
            return cls(int(v))
        return int_v

class DiscordString(StrEnum):
    """Base class for Discord's pre-defined strings."""

    @classmethod
    def from_dict(cls, v: str) -> Self | str:
        """Deserialize this pre-defined Discord string.

        Args:
            v (str): serialized Discord string

        Returns:
            (DiscordString | str): DiscordString object if the value is known,
                otherwise the raw string value.
        """
        str_v = str(v)
        if str_v in cls:
            return cls(str_v)
        return str_v
