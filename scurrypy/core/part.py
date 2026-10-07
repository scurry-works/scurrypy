from dataclasses import dataclass, fields, Field
from typing import Any, get_origin

from .types import (
    Serialized,
    JSON, 
    OptionalNullablePartField
)

@dataclass
class Part:
    """Part is a base class that serializes a dataclass into a JSON."""

    def to_dict(self) -> Serialized:
        """Recursively serializes the dataclass and omits non-nullable None fields.

        Returns:
            (Serialized): serialized dataclass
        """
        result = {}
        for f in fields(self):
            if f.name.startswith('_'):
                continue
            val = getattr(self, f.name)
            # only include real or nullable values
            if val is not None or is_nullable_field(f):
                result[f.name] = serialize(val)
        return result

def serialize(val: JSON) -> JSON:
    """Serialize the value.

    Args:
        val (dict): value to serialize

    Returns:
        (JSON): serialized value
    """
    if hasattr(val, "to_dict"):
        return JSON(val.to_dict())

    if isinstance(val, list):
        return [serialize(v) for v in val if v is not None]

    if isinstance(val, dict):
        return {k: serialize(v) for k, v in val.items()}

    return val


def is_nullable_field(field: Field[Any]) -> bool:
    """Determines whether the specified field is of type OptionalNullablePartField.

    Args:
        field (Field): dataclass field

    Returns:
        bool: whether field is optional and nullable
    """
    return get_origin(field.type) is OptionalNullablePartField
