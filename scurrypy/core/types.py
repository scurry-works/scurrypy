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

type PresentNullableModelField[T] = T
"""Discord always includes this field in the payload.
    If this field is `None`, it will serialize as JSON `null`.

    Equivalent Discord notation is `name, ?type`.
"""

type OmittableNullableModelField[T] = T | None
"""Discord may omit this field from the payload.
    This applies to both omitted fields and fields with `None` (or JSON's `null`).

    Equivalent Discord notation is `name?, ?type`.    
"""
