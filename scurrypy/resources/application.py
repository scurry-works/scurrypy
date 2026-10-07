from dataclasses import dataclass

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake

from .base_resource import BaseResource

@dataclass
class Application(BaseResource):
    """Represents a Discord application resource."""

    id: Snowflake
    """ID of the application."""

    async def fetch(self) -> JsonQuery:
        """Fetch this application's data.

        Returns:
            (JsonQuery): queried application
        """
        data = await self.http.request_json('GET', '/applications/@me')

        return JsonQuery(data)
