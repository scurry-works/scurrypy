from dataclasses import dataclass

from ..models.application import ApplicationModel

from .base_resource import BaseResource

@dataclass
class Application(BaseResource):
    """Represents a Discord application."""

    id: int
    """ID of the application."""

    async def fetch(self):
        """Fetch this application's data.

        Returns:
            (Application): the Application data
        """
        data = await self._http.request('GET', '/applications/@me')

        return ApplicationModel.from_dict(data)
