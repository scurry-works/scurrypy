from dataclasses import dataclass
from ..core.model import DataModel

@dataclass
class ImageData(DataModel):
    """Represents Discord's data URI scheme for images."""
    
    path: str = None
    """Path to image."""

    @property
    def uri(self):
        """Creates the Base64 data URI scheme.

        Raises:
            ValueError: Unknown file type

        Returns:
            (str): the formatted data URI scheme
        """
        import base64, mimetypes

        mime, _ = mimetypes.guess_type(self.path)
        if mime is None:
            raise ValueError("Unknown file type.")

        with open(self.path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        return f"data:{mime};base64,{encoded}"
