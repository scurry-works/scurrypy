class ActionRowChild: 
    """Marker class for all components that go into an action row.

    !!! tip "Children"
        [`Button`][scurrypy.parts.components.Button], 
        [`StringSelect`][scurrypy.parts.components.StringSelect], 
        [`UserSelect`][scurrypy.parts.components.UserSelect], 
        [`RoleSelect`][scurrypy.parts.components.RoleSelect], 
        [`MentionableSelect`][scurrypy.parts.components.MentionableSelect], 
        [`ChannelSelect`][scurrypy.parts.components.ChannelSelect]
    """
    ...

class SectionChild: 
    """Marker class for all components that go into a section.

    !!! tip "Children"
        [`TextDisplay`][scurrypy.parts.components_v2.TextDisplay]
    """
    ...

class SectionAccessoryChild: 
    """Marker class for all components that go into a section accessory.
    
    !!! tip "Children"
        [`Button`][scurrypy.parts.components.Button], 
        [`Thumbnail`][scurrypy.parts.components_v2.Thumbnail]
    """
    ...

class ContainerChild: 
    """Marker class for all components that go into a container.
    
    !!! tip "Children"
        [`ActionRowPart`][scurrypy.parts.components.ActionRowPart], 
        [`TextDisplay`][scurrypy.parts.components_v2.TextDisplay], 
        [`SectionPart`][scurrypy.parts.components_v2.SectionPart], 
        [`MediaGallery`][scurrypy.parts.components_v2.MediaGallery], 
        [`Separator`][scurrypy.parts.components_v2.Separator], 
        [`File`][scurrypy.parts.components_v2.File]
        [`FileUpload`][scurrypy.parts.components_v2.FileUpload]
    """
    ...

class LabelChild: 
    """Marker class for all components that go into a label.
    
    !!! tip "Children"
        [`TextInput`][scurrypy.parts.components.TextInput], 
        [`StringSelect`][scurrypy.parts.components.StringSelect], 
        [`UserSelect`][scurrypy.parts.components.UserSelect], 
        [`RoleSelect`][scurrypy.parts.components.RoleSelect], 
        [`MentionableSelect`][scurrypy.parts.components.MentionableSelect], 
        [`ChannelSelect`][scurrypy.parts.components.ChannelSelect], 
        [`FileUpload`][scurrypy.parts.components_v2.FileUpload]
    """
    ...

class ComponentTypes:
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8
    SECTION = 9
    TEXT_DISPLAY = 10
    THUMBNAIL = 11
    MEDIA_GALLERY = 12
    FILE = 13
    SEPARATOR = 14
    CONTAINER = 17
    LABEL = 18
    FILE_UPLOAD = 19
