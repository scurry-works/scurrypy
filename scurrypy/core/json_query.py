from typing import Self, Any, get_args, get_origin

from scurrypy.core.types import JSON

import logging

logger = logging.getLogger("scurrypy.json_query")
logger.addHandler(logging.NullHandler())

def _convert(value: Any, t: type) -> Any:
    if t is bool:
        return value in ('true', 'True', True)
    return t(value)

class JsonQuery:
    def __init__(self, data: JSON | list[JSON]):
        self.data = data
        self.value: Any = None

    def get(self, path: str, *, t: Any = None) -> Self:
        """Traverse data with path

        Args:
            path (str): dot-separated key path to value
            t (Any): type value should be (leave blank to return query unchanged)

        Returns:
            (Self): self
        """
        self.value = self.data

        for token in path.split('.'):
            try:
                key: int | str = int(token)
            except ValueError:
                key = token

            try:
                self.value = self.value[key]
            except (KeyError, IndexError):
                logger.error(f"Key '{key}' not found")
                self.value = None
                break

        if t is None or self.value is None:
            return self

        o = get_origin(t)
        if o is None:
            if t is bool:
                self.value = self.value in ('true', 'True', True)
            else:
                self.value = t(self.value)

        elif o is list:
            elem_type = get_args(t)[0]
            self.value = [_convert(i, elem_type) for i in self.value]

        elif o is dict:
            assert isinstance(self.value, dict)
            key_type, value_type = get_args(t)
            self.value = {
                _convert(k, key_type): _convert(v, value_type)
                for k, v in self.value.items()
            }

        return self
    
    def pprint(self) -> Self:
        """Pretty print data!

        Returns:
            (Self): self
        """
        from pprint import pprint
        pprint(self.data)
        return self

    def __repr__(self) -> str:
        return f"JsonQuery({self.data!r})"
