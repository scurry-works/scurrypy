from typing import Any

JSON = dict[str, Any]
"""JSON in key value pairs rather than a raw string."""

Serialized = JSON | str | None
"""Dataclass turned into a serialized dictionary.
!!! note
    Can be partially or fully serialized depending on the structure.
"""

HTTPResponse = JSON | str | None
"""Raw HTTP response from a request."""

# Part Types
type RequiredPartField[T] = T | None
"""This field requires a non-`None` value.
    
    Equivalent Discord notation is `name, type`.
"""

type OptionalPartField[T] = T | None
"""This field can be left blank.
    If this field is left `None`, it will be omitted from the request.
    
    Equivalent Discord notation is `name?, type`.
"""

type RequiredNullablePartField[T] = T | None
"""This field must be present in the request.
    If this field is `None`, it will serialize as JSON `null`.

    Equivalent Discord notation is `name, ?type`.
"""

type OptionalNullablePartField[T] = T | None
"""This field can be left blank.
    If this field is left `None`, it will serialize as `None` (or JSON's `null`).

    Equivalent Discord notation is `name?, ?type`.
"""

# Model Types
type PresentModelField[T] = T
"""Discord always includes this field in the payload.

    Equivalent Discord notation is `name, type`.
"""

type OmittableModelField[T] = T | None
"""Discord may omit this field from the payload.
    This applies only to omitted fields.

    Equivalent Discord notation is `name?, type`.
"""

type PresentNullableModelField[T] = T | None
"""Discord always includes this field in the payload.
    If this field is `None`, it will serialize as JSON `null`.

    Equivalent Discord notation is `name, ?type`.
"""

type OmittableNullableModelField[T] = T | None
"""Discord may omit this field from the payload.
    This applies to both omitted fields and fields with `None` (or JSON's `null`).

    Equivalent Discord notation is `name?, ?type`.    
"""

from ..bases.scurrypy_type import ScurrypyType

class ScurrypyPrimitive(ScurrypyType):
    """Represents a dataclass field containing an unconverted primitive value."""

    @classmethod
    def from_dict(cls, v: Any) -> Any:
        """Returns the value without conversion.

        Args:
            v (Any): value

        Returns:
            (Any): value unchanged
        """
        return v

class ScurrypyInt(ScurrypyType, int):
    """Represents JSON value to dataclass field int conversion."""

    @classmethod
    def from_dict(cls, v: str | None) -> int | None:
        """Converts value to an int.

        Args:
            v (str): JSON value

        Returns:
            (int): JSON value as an int
        """
        if v is None:
            return None
        return int(v)

class ScurrypyFloat(ScurrypyType, float):
    """Represents JSON value to dataclass field float conversion."""

    @classmethod
    def from_dict(cls, v: str | None) -> float | None:
        """Converts value to a float.

        Args:
            v (str): JSON value

        Returns:
            (float): JSON value as a float
        """
        if v is None:
            return None
        return float(v)

class ScurrypyStr(ScurrypyType, str):
    """Represents JSON value to dataclass field str conversion."""

    @classmethod
    def from_dict(cls, v: str | None) -> str | None:
        """Converts value to a str.

        Args:
            v (str): JSON value

        Returns:
            (str): JSON value as a str
        """
        if v is None:
            return None
        return str(v)

class ScurrypyBool(ScurrypyType):
    """Represents JSON value to dataclass field bool conversion."""

    @classmethod
    def from_dict(cls, v: str | None) -> bool | None:
        """Converts value to a bool.

        Args:
            v (str): JSON value

        Returns:
            (bool | None): JSON value as a bool or None if no value was passed
        """
        if v is None:
            return None
        return v in (True, "True", "true")
