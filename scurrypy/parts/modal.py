from dataclasses import dataclass, field
from ..core.model import DataModel

from .components_v2 import Label

@dataclass
class ModalPart(DataModel):
    """Represents the Modal object."""

    title: str
    """Title of the popup modal."""

    custom_id: str = None
    """ID for the modal."""

    components: list[Label] = field(default_factory=list)
    """1 to 5 components that make up the modal."""
