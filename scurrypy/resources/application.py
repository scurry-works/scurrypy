from dataclasses import dataclass

from .base_resource import BaseResource

from ..core.snowflake import Snowflake

from ..api.application import ApplicationModel

@dataclass
class Application(BaseResource):
    """Represents a Discord application."""

    id: Snowflake
    """ID of the application."""

    async def fetch(self) -> ApplicationModel:
        """Fetch this application's data.

        Returns:
            (Application): queried application
        """
        data = await self.http.request_json('GET', '/applications/@me')

        return ApplicationModel.from_dict(data)
