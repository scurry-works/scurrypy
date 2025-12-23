from dataclasses import dataclass, fields, is_dataclass
from typing import get_args, get_origin, Union

"""Extract the type from Optional[t]."""
unwrap_optional = lambda t: get_args(t)[0] if get_origin(t) is Union else t

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
        
        def convert(t, v):
            t = unwrap_optional(t)
            o = get_origin(t)
            
            # missing field
            if v is None:
                return None
            
            if t is bool:
                return v == 'true'
            
            if is_dataclass(t):
                return t.from_dict(v)
            
            if o is dict:
                vt = get_args(t)[1]
                return {
                    int(k): convert(vt, x) 
                    for k, x in v.items()
                }
            
            if o is list:
                lt = get_args(t)[0]
                return [convert(lt, x) for x in v]
            
            # primitive / fallback
            return t(v)
        
        kwargs = {
            f.name: convert(f.type, data.get(f.name)) 
            for f in fields(cls)
        }

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
