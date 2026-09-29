from dataclasses import dataclass
from typing import Self

from ...core.model import DataModel
from ...core.types import JSON, RequiredPartField

@dataclass
class UnfurledMediaPart(DataModel):
    """Represents unfurled media for Discord components.

    !!! note
        This part is a Components-specific structure.
        It is not meant to be used outside of Components.
    """
    url: RequiredPartField[str] = None

    @classmethod
    def from_attachment(cls, filename: str) -> Self:
        """Convert a file name to attachment scheme.

        Args:
            filename (str): file name

        Returns:
            UnfurledMediaPart: self
        """
        return cls(url=f"attachment://{filename}")

    def to_dict(self) -> JSON:
        """Serialize this unfurled media.

        Returns:
            (Serialized): serialized media
        """
        return {'url': self.url}
