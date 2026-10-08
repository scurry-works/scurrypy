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
    """Discord payload traversal utility."""

    def __init__(self, data: JSON | list[JSON]):
        """
        Args:
            data (JSON | list[JSON]): Discord payload
        """
        
        self.data = data
        """Discord payload."""

        self.value: Any = None
        """Resulting query."""

    def get(self, path: str, *, t: Any = None) -> Self:
        """Traverse data with path.

        Args:
            path (str): dot-separated key path to value
            t (Any): type value should be (leave blank to return query unchanged)

        Returns:
            (Self): self
        """
        self.value = self.data

        for token in path.split('.'):
            try:
                key = int(token) if isinstance(self.value, list) else token
                self.value = self.value[key]
            except (KeyError, IndexError, ValueError):
                logger.error(f"Key '{token}' not found")
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

        return self

    def pprint(self) -> Self:
        """Pretty print value!

        Returns:
            (Self): self
        """
        from pprint import pprint
        pprint(self.value)
        return self

    def __repr__(self) -> str:
        return f"JsonQuery({self.data!r})"
