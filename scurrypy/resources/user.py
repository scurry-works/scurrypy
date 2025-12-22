from dataclasses import dataclass

from .base_resource import BaseResource

from ..models.guild_member import GuildMemberModel
from ..models.user import UserModel

@dataclass
class User(BaseResource):
    """A Discord user."""

    id: int
    """ID of the user."""

    async def fetch(self):
        """Fetch this user by ID.

        Returns:
            (UserModel): the User object
        """
        data = await self._http.request('GET', f'/users/{self.id}')

        return UserModel.from_dict(data)

    async def fetch_guild_member(self, guild_id: int):
        """Fetch this user's guild member data.

        Args:
            guild_id (int): ID of guild to fetch data from

        Returns:
            (GuildMemberModel): member data from guild
        """
        data = await self._http.request('GET', f'/guilds/{guild_id}/members/{self.id}')

        return GuildMemberModel.from_dict(data)
