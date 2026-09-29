from dataclasses import dataclass

from .base_resource import BaseResource

from ..api.invite import InviteModel

@dataclass
class Invite(BaseResource):
    """Represents a Discord invite."""
    
    code: str
    """Invite code."""

    async def fetch(self, with_counts: bool | None = None) -> InviteModel:
        """Fetch the invite object for the given code.

        Args:
            with_counts (bool, optional): whether the model should contain approximate member counts

        Returns:
            (InviteModel): queried invite object
        """
        data = await self.http.request_json(
            'GET', 
            f'/invites/{self.code}', 
            params={'with_counts': with_counts}
        )

        return InviteModel.from_dict(data)

    async def delete(self) -> InviteModel:
        """Delete the invite for the given code.
        Fires [`InviteDeleteEvent`][scurrypy.events.invite_events.InviteDeleteEvent].
        
        !!! important "Permissions"
            Requires `MANAGE_CHANNELS` on the channel this invite belongs to
            or `MANAGE_GUILD` to remove any invite across the guild

        Returns:
            (InviteModel): deleted invite object
        """
        data = await self.http.request_json('DELETE', f'/invites/{self.code}')

        return InviteModel.from_dict(data)
