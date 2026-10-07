from dataclasses import dataclass

from ..core.json_query import JsonQuery

from .base_resource import BaseResource

@dataclass
class Invite(BaseResource):
    """Represents a Discord invite resource."""
    
    code: str
    """Invite code."""

    async def fetch(self, with_counts: bool | None = None) -> JsonQuery:
        """Fetch the invite object for the given code.

        Args:
            with_counts (bool, optional): whether the model should contain approximate member counts

        Returns:
            (JsonQuery): queried invite object
        """
        data = await self.http.request_json(
            'GET', 
            f'/invites/{self.code}', 
            params={
                'with_counts': with_counts
            }
        )

        return JsonQuery(data)

    async def delete(self) -> JsonQuery:
        """Delete the invite for the given code.
        Fires [**Invite Delete**]https://docs.discord.com/developers/events/gateway-events#invite-delete).
        
        !!! important "Permissions"
            Requires `MANAGE_CHANNELS` on the channel this invite belongs to
            or `MANAGE_GUILD` to remove any invite across the guild

        Returns:
            (JsonQuery): deleted invite object
        """
        data = await self.http.request_json('DELETE', f'/invites/{self.code}')

        return JsonQuery(data)
