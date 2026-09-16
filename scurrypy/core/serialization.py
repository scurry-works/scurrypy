from typing import get_args, get_origin, Union, TypeAliasType, Any
from types import UnionType

from .exceptions import DataModelTypeError
from .types import JSON

def _serialize(val: JSON) -> JSON:
    if hasattr(val, "to_dict"):
        return JSON(val.to_dict())

    if isinstance(val, list):
        return [_serialize(v) for v in val if v is not None]

    if isinstance(val, dict):
        return {k: _serialize(v) for k, v in val.items()}

    return val

def serialize(val: JSON) -> JSON:
    """Serialize the value.

    Args:
        val (dict): value to serialize

    Returns:
        (JSON): serialized value
    """
    return _serialize(val)

def convert(t: object, v: object) -> object:
    """Convert the given value to the given type.

    Args:
        t (type[Any] | Any): type in which to convert value
        v (object): value to be converted

    Raises:
        (DataModelTypeError): ambiguous type

    Returns:
        (object): converted value
    """
    o = get_origin(t)

    if o in (Union, UnionType) or type(o) is TypeAliasType: # optional[T] or similar
        non_none = [a for a in get_args(t) if a is not type(None)]

        if len(non_none) > 1:
            raise DataModelTypeError(f"Expected deterministic type; got {non_none}.")
        
        return convert(non_none[0], v)

    if v is None: # missing field
        return None
    
    if t is bool:
        return v in ('true', 'True', True)
    
    if o is dict: # mappings
        assert isinstance(v, dict)
        from .snowflake import Snowflake
        vt = get_args(t)[1]
        return {
            Snowflake(k): convert(vt, x) 
            for k, x in v.items()
        }
    
    if o is list:
        assert isinstance(v, list)
        lt = get_args(t)[0]
        return [convert(lt, x) for x in v]
    
    from ..bases.components import Component
    if t is Component:
        assert isinstance(v, dict)
        from ..api.components import MessageComponentFactory
        return MessageComponentFactory.from_dict(v)

    if hasattr(t, "from_dict"):
        return t.from_dict(v)

    # primitive / fallback
    assert not isinstance(t, str)

    if callable(t):
        return t(v)

    return v

from ..core.types import OptionalNullablePartField
from dataclasses import Field

def is_nullable_field(field: Field[Any]) -> bool:
    """Determines whether the specified field is of type OptionalNullablePartField.

    Args:
        field (Field): dataclass field

    Returns:
        bool: whether field is optional and nullable
    """
    return get_origin(field.type) is OptionalNullablePartField
