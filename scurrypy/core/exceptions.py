class ScurrypyError(Exception):
    """Base exception for all scurrypy-specific errors."""
    pass


class InvalidCallbackSignature(ScurrypyError):
    """Raised when a callback is applied to an event with an invalid signature."""
    pass


class NotCallable(ScurrypyError):
    """Raised when an object expected to be callable is not."""
    pass


class DispatchError(ScurrypyError):
    """Raised when an event dispatch fails."""
    pass


class DataModelTypeError(ScurrypyError):
    """Raised when an unexpected type is passed to a DataModel."""
    pass


class InvalidFile(ScurrypyError):
    """Raised when a file name is invalid."""
    pass


class OptionNotFound(ScurrypyError):
    """Raised when a specified option could not be found."""
    pass


class MissingField(ScurrypyError):
    """Raised when an optional field is not present."""
    pass


class MissingIntents(ScurrypyError):
    """Raised when an intent is missing for the client."""
    pass


class NoSession(ScurrypyError):
    """Raised when a session is not active."""
    pass


class EventNotFound(ScurrypyError):
    """Raised when an event dispatch name has no corressponding event data model."""
    pass
