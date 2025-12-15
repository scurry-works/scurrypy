from dataclasses import dataclass, field
from ..core.model import DataModel

from typing import Optional

from .component_types import *

class ComponentV2Types:
    SECTION = 9
    TEXT_DISPLAY = 10
    THUMBNAIL = 11
    MEDIA_GALLERY = 12
    FILE = 13
    SEPARATOR = 14
    CONTAINER = 17
    LABEL = 18
    FILE_UPLOAD = 19

@dataclass
class SectionPart(DataModel, ContainerChild):
    """Represents the Section component."""

    accessory: SectionAccessoryChild = None
    """A component that is contextually associated to the content of the section."""

    components: list[SectionChild] = field(default_factory=list)
    """Component(s) representing the content of the section that is contextually associated to the accessory."""

    type: int = field(init=False, default=ComponentV2Types.SECTION)
    """Component type. Always `ComponentV2Types.SECTION` for this class. See [`ComponentV2Types`][scurrypy.parts.components_v2.ComponentV2Types]."""

@dataclass
class TextDisplay(DataModel, ContainerChild, SectionChild):
    """Represents the Text Display component."""

    content: str = None
    """Text that will be displayed similar to a message."""

    type: int = field(init=False, default=ComponentV2Types.TEXT_DISPLAY)
    """Component type. Always `ComponentV2Types.TEXT_DISPLAY` for this class. See [`ComponentV2Types`][scurrypy.parts.components_v2.ComponentV2Types]."""

@dataclass
class Thumbnail(DataModel, SectionAccessoryChild):
    """Represents the Thumbnail component."""
    
    media: str = None
    """Media of the thumbnail. http or attachment://<filename> scheme."""

    description: Optional[str] = None
    """Description for the media."""

    spoiler: Optional[bool] = False
    """Whether the thumbnail should be a spoiler (or blurred out)."""

    type: int = field(init=False, default=ComponentV2Types.THUMBNAIL)
    """Component type. Always `ComponentV2Types.THUMBNAIL` for this class. See [`ComponentV2Types`][scurrypy.parts.components_v2.ComponentV2Types]."""

@dataclass
class MediaGalleryItem(DataModel):
    """Represents the Media Gallery Item component."""

    media: str = None
    """Image data. http or attachment://<filename> scheme."""

    description: Optional[str] = None
    """Alt text for the media."""

    spoiler: Optional[bool] = False
    """Whether the thumbnail should be a spoiler (or blurred out)."""

@dataclass
class MediaGallery(DataModel, ContainerChild):
    """Represents the Media Gallery component."""

    items: list[MediaGalleryItem] = field(default_factory=list)
    """1 to 10 nedia gallery items. See [`MediaGalleryItem`][scurrypy.parts.components_v2.MediaGalleryItem]."""

    type: int = field(init=False, default=ComponentV2Types.MEDIA_GALLERY)
    """Component type. Always `ComponentV2Types.MEDIA_GALLERY` for this class. See [`ComponentV2Types`][scurrypy.parts.components_v2.ComponentV2Types]."""

@dataclass
class File(DataModel, ContainerChild):
    """Represents the File component."""

    file: str = None
    """File name. ONLY supports attachment://<filename> scheme."""

    spoiler: Optional[bool] = False
    """Whether the thumbnail should be a spoiler (or blurred out)."""

    type: int = field(init=False, default=ComponentV2Types.FILE)
    """Component type. Always `ComponentV2Types.File` for this class. See [`ComponentV2Types`][scurrypy.parts.components_v2.ComponentV2Types]."""

class SeparatorTypes:
    """Represents separator types constants."""

    SMALL_PADDING = 1
    """Small separator padding."""
    
    LARGE_PADDING = 2
    """Large separator padding."""

@dataclass
class Separator(DataModel, ContainerChild):
    """Represents the Separator component."""

    divider: Optional[bool] = True
    """Whether a visual divider should be displayed in the component. Defaults to True."""

    spacing: Optional[int] = SeparatorTypes.SMALL_PADDING
    """Size of separator padding. Defaults to `SMALL_PADDING`. See [`SeparatorTypes`][scurrypy.parts.components_v2.SeparatorTypes]."""

    type: int = field(init=False, default=ComponentV2Types.SEPARATOR)
    """Component type. Always `ComponentV2Types.SEPARATOR` for this class. See [`ComponentV2Types`][scurrypy.parts.components_v2.ComponentV2Types]."""

@dataclass
class ContainerPart(DataModel):
    """Represents a container of display and interactable components."""

    components: list[ContainerChild] = field(default_factory=list)
    """Child components that are encapsulated within the Container."""

    accent_color: Optional[int] = None
    """Color for the accent as an integer."""

    spoiler: Optional[bool] = False
    """If the container should be blurred out. Defaults to False."""

    type: int = field(init=False, default=ComponentV2Types.CONTAINER)
    """Component type. Always `ComponentV2Types.CONTAINER` for this class. See [`ComponentV2Types`][scurrypy.parts.components_v2.ComponentV2Types]."""

@dataclass
class Label(DataModel):
    """Represents the Discord Label component."""

    label: str = None
    """Label text."""

    component: LabelChild = None
    """A component within the label."""

    description: Optional[str] = None
    """An optional description text for the label."""

    type: int = field(init=False, default=ComponentV2Types.LABEL)
    """Component type. Always `ComponentV2Types.LABEL` for this class. See [`ComponentV2Types`][scurrypy.parts.components_v2.ComponentV2Types]."""

@dataclass
class FileUpload(DataModel, ContainerChild):
    """Represents the file upload component."""

    custom_id: str = None
    """ID for the file upload."""

    min_values: Optional[int] = 1
    """Minimum number of items that must be uploaded."""

    max_values: Optional[int] = 1
    """Maximum number of items that can be uploaded."""

    required: Optional[bool] = True
    """Whether files are required to be uploaded."""

    type: int = field(init=False, default=ComponentV2Types.FILE_UPLOAD)
    """Component type. Always `ComponentV2Types.FILE_UPLOAD` for this class. See [`ComponentV2Types`][scurrypy.parts.components_v2.ComponentV2Types]."""
