from .scurrypy_type import ScurrypyType

class Component(ScurrypyType):
    """Marker class for all interaction components."""
    __slots__ = ()

class ContainerComponent(Component):
    """Marker class for all container components."""
    __slots__ = ()

class ActionRowChild: 
    """Marker class for all components that go into an action row.

    !!! tip "Children"
        [`Button`][scurrypy.api.components.Button], 
        [`StringSelect`][scurrypy.api.components.StringSelect], 
        [`UserSelect`][scurrypy.api.components.UserSelect], 
        [`RoleSelect`][scurrypy.api.components.RoleSelect], 
        [`MentionableSelect`][scurrypy.api.components.MentionableSelect], 
        [`ChannelSelect`][scurrypy.api.components.ChannelSelect]
    """
    __slots__ = ()

class SectionChild: 
    """Marker class for all components that go into a section.

    !!! tip "Children"
        [`TextDisplay`][scurrypy.api.components.TextDisplay]
    """
    __slots__ = ()

class SectionAccessoryChild: 
    """Marker class for all components that go into a section accessory.
    
    !!! tip "Children"
        [`Button`][scurrypy.api.components.Button], 
        [`Thumbnail`][scurrypy.api.components.Thumbnail]
    """
    __slots__ = ()

class ContainerChild: 
    """Marker class for all components that go into a container.
    
    !!! tip "Children"
        [`ActionRow`][scurrypy.api.components.ActionRow], 
        [`TextDisplay`][scurrypy.api.components.TextDisplay], 
        [`Section`][scurrypy.api.components.Section], 
        [`MediaGallery`][scurrypy.api.components.MediaGallery], 
        [`Separator`][scurrypy.api.components.Separator], 
        [`File`][scurrypy.api.components.File]
    """
    __slots__ = ()

class LabelChild: 
    """Marker class for all components that go into a label.
    
    !!! tip "Children"
        [`TextInput`][scurrypy.api.components.TextInput], 
        [`StringSelect`][scurrypy.api.components.StringSelect], 
        [`UserSelect`][scurrypy.api.components.UserSelect], 
        [`RoleSelect`][scurrypy.api.components.RoleSelect], 
        [`MentionableSelect`][scurrypy.api.components.MentionableSelect], 
        [`ChannelSelect`][scurrypy.api.components.ChannelSelect], 
        [`FileUpload`][scurrypy.api.components.FileUpload],
        [`RadioGroup`][scurrypy.api.components.RadioGroup],
        [`CheckboxGroup`][scurrypy.api.components.CheckboxGroup],
        [`Checkbox`][scurrypy.api.components.Checkbox]
    """
    __slots__ = ()
