from dataclasses import dataclass

from ...core.model import DataModel
from ...core.types import RequiredPartField

from ..components.layout import Label

@dataclass
class ModalPart(DataModel):
    """Represents the Modal object."""

    title: RequiredPartField[str] = None
    """Title of the popup modal."""

    custom_id: RequiredPartField[str] = None
    """ID for the modal."""

    components: RequiredPartField[list[Label]] = None
    """1 to 5 components that make up the modal."""
