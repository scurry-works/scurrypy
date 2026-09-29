from dataclasses import Field
from typing import (
    Any, 
    TypeAlias,
    get_args, 
    get_origin, 
    cast
)
from collections.abc import Callable

from ..core.snowflake import Snowflake
from ..core.types import (
    JSON, 
    OptionalNullablePartField,
    ScurrypyStr,
    ScurrypyInt,
    ScurrypyBool,
    ScurrypyFloat
)
from ..core.exceptions import DataModelTypeError

CONVERTER_TYPE_MAP = {
    str: ScurrypyStr,
    int: ScurrypyInt,
    bool: ScurrypyBool,
    float: ScurrypyFloat,
    Snowflake: Snowflake
}
"""Maps primitive Python types to their Scurrypy conversion types."""

Converter: TypeAlias = Callable[[Any], Any]
"""Callback used to deserialize a field value (what can convert a value)."""

def determine_converter(field_type: Any) -> Converter:
    """Resolves a field type to its value conversion callback.

    Args:
        field_type (Any): inner field type

    Raises:
        (DataModelTypeError): dict key must be Snowflake

    Returns:
        (Converter): `from_dict` callback
    """
    o = get_args(field_type)[0]
    t = get_origin(o)

    from ..bases.components import Component, ContainerComponent

    if t is list:
        p = get_args(o)[0]

        if p in (Component, ContainerComponent):
            from ..api.components import MessageComponentFactory
            item_converter = MessageComponentFactory.from_dict
        elif p in CONVERTER_TYPE_MAP:
            item_converter = CONVERTER_TYPE_MAP[p]
        else:
            item_converter = p.from_dict

        return lambda value: (
            None
            if value is None
            else [item_converter(item) for item in value]
        )

    if t is dict:
        key_type = get_args(o)[0]

        if key_type is not Snowflake:
            raise DataModelTypeError("dict key must be Snowflake")

        p = get_args(o)[1]

        if p in (Component, ContainerComponent):
            from ..api.components import MessageComponentFactory
            v_converter = MessageComponentFactory.from_dict
        elif p in CONVERTER_TYPE_MAP:
            v_converter = CONVERTER_TYPE_MAP[p]
        else:
            v_converter = p.from_dict

        return lambda value: (
            None
            if value is None
            else {
                Snowflake(k): v_converter(v)
                for k, v in value.items()
            }
        )

    if t in (Component, ContainerComponent):
        from ..api.components import MessageComponentFactory
        return MessageComponentFactory.from_dict

    return cast(Converter, o.from_dict)

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

