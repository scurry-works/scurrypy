from dataclasses import dataclass, fields, is_dataclass
from typing import get_args, get_origin, Union

@dataclass
class DataModel:    
    """DataModel is a base class for Discord JSONs that provides 
        hydration from raw dicts, and optional field defaults.
    """
    
    @classmethod
    def from_dict(cls, data: dict):
        """Hydrates the given data into the dataclass child.

        Args:
            data (dict): JSON data

        Returns:
            (dataclass): hydrated dataclass
        """
        if not data:
            return None
        
        def unwrap_optional(t):
            if get_origin(t) is Union:
                args = tuple(a for a in get_args(t) if a is not type(None))
                return args[0] if len(args) == 1 else Union[args]
            return t

        kwargs = {}
        for f in fields(cls):
            v = data.get(f.name)
            t = unwrap_optional(f.type)

            if v is None:
                kwargs[f.name] = None
            elif is_dataclass(t):
                kwargs[f.name] = t.from_dict(v)
            elif get_origin(t) is list:
                lt = get_args(t)[0]
                kwargs[f.name] = [lt.from_dict(x) if is_dataclass(lt) else x for x in v]
            else:
                try:
                    kwargs[f.name] = t(v)
                except Exception:
                    kwargs[f.name] = v  # fallback to raw

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
