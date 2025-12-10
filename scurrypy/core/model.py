from dataclasses import dataclass, fields, is_dataclass
from typing import get_args, get_origin, Union

def unwrap_optional(t):
    """Extract the type from Optional[t]."""
    if get_origin(t) is Union:
        args = tuple(a for a in get_args(t) if a is not type(None))
        return args[0] if len(args) == 1 else Union[args]
    return t

@dataclass
class DataModel:    
    """DataModel is a base class for Discord JSONs that provides 
        hydration from raw dicts, and optional field defaults.
    """
    
    @classmethod
    def from_dict(cls, data: dict):
        """Hydrates the given data into the dataclass.

        Args:
            data (dict): the JSON data

        Returns:
            (cls): hydrated dataclass
        """
        
        if not data:
            return None

        kwargs = {}

        for f in fields(cls):
            key = f.name
            value = data.get(key)
            type_ = unwrap_optional(f.type)

            # missing field
            if value is None:
                kwargs[key] = None
                continue

            # nested dataclass
            if is_dataclass(type_):
                kwargs[key] = type_.from_dict(value)
                continue

            # list field
            if get_origin(type_) is list:
                element_type = get_args(type_)[0]
                if is_dataclass(element_type):
                    kwargs[key] = [
                        element_type.from_dict(x) for x in value
                    ]
                else:
                    kwargs[key] = [element_type(x) for x in value]
                continue

            # primitive field
            try:
                kwargs[key] = type_(value)
            except Exception:
                kwargs[key] = value

        return cls(**kwargs)
    
    def to_dict(self):
        """Recursively turns the dataclass into a dictionary and drops empty fields.

        Returns:
            (dict): serialized dataclasss
        """
        def serialize(val):
            if isinstance(val, list):
                return [serialize(v) for v in val if v is not None]
            if isinstance(val, DataModel):
                return val.to_dict()
            return val

        result = {}
        for f in fields(self):
            if f.name.startswith('_'):
                continue
            val = getattr(self, f.name)
            # if val not in (None, [], {}, "", 0):
            result[f.name] = serialize(val)
        return result
