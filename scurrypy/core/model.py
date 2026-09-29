from dataclasses import dataclass, fields, field
from typing import (
    Any, 
    TypeAlias,
    Self, 
    ClassVar, 
    dataclass_transform
)

from ..bases import ScurrypyType

from .types import JSON, Serialized
from .exceptions import DataModelTypeError
from .serialization import (
    Converter,
    is_nullable_field, 
    serialize, 
    determine_converter
)

CompiledField: TypeAlias = tuple[str, Converter]
"""Compiled conversion information for a single model field (which converter belongs to which field)."""

CompiledFields: TypeAlias = tuple[CompiledField, ...]
"""Compiled conversion information for a model's fields (model's precomputed conversion plan)."""

@dataclass
class DataModel(ScurrypyType):
    """DataModel is a base class for Discord JSONs that provides 
        hydration from raw dicts, and optional field defaults.
    """

    __fields__: ClassVar[CompiledFields] = field(default=(), init=False)
    """Maps dataclass fields to their respective converter."""

    @classmethod
    def from_dict(cls, data: JSON) -> Self:
        """Hydrates the given data into the dataclass.

        Args:
            data (JSON): the JSON data

        Raises:
            (DataModelTypeError): expects JSON data

        Returns:
            (cls): hydrated dataclass
        """
        if not isinstance(data, dict):
            raise DataModelTypeError(
                f"{cls.__name__}.from_dict expects JSON; "
                f"got {type(data).__name__}"
            )
        
        kwargs = {}

        for name, converter in cls.__fields__:
            d = data.get(name)
            kwargs[name] = converter(d) if d is not None else None

        return cls(**kwargs)

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

@dataclass_transform()
def datamodel[T: Any](cls: T) -> T: # what goes in must come out
    """Decorator to add `__fields__` to dataclass model.

    Returns:
        (T): modified dataclass
    """
    cls = dataclass(cls)

    cls.__fields__ = tuple(
        (field.name, determine_converter(field.type))
        for field in fields(cls)
        if field.init
    )

    return cls
