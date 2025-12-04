from dataclasses import dataclass
from typing import TypedDict, Unpack

from .base_resource import BaseResource

from ..models.guild import GuildModel
from ..models.guild_member import GuildMemberModel
from ..models.user import UserModel

class FetchUserGuildsParams(TypedDict, total=False):
    before: int
    """Get guilds before this guild ID."""

    after: int
    """Get guilds after this guild ID."""

    limit: int
    """Max number of guilds to return. Range 1 - 200. Default 200."""

    with_counts: bool
    """Include approximate member and presence count."""

@dataclass
class User(BaseResource):
    """A Discord user."""

    id: int
    """ID of the user."""

    async def fetch(self):
        """Fetch this user by ID.
        !!! note
            Fetch includes both /users/@me AND /users/{user.id}!

        Returns:
            (UserModel): the User object
        """
        data = await self._http.request('GET', f'/users/{self.id}')

        return UserModel.from_dict(data)
    
    async def fetch_guilds(self, **kwargs: Unpack[FetchUserGuildsParams]):
        """Fetch this user's guilds.
        !!! warning "Important"
            Requires the OAuth2 guilds scope!

        Args:
            **kwargs: user guilds fetch params
                !!! note
                    If no kwargs are provided, default to 200 guilds limit.

        Returns:
            (list[GuildModel]): each guild's data
        """
        params = {
            'limit': 200,
            'with_counts': False,
            **kwargs
        }

        data = await self._http.request('GET', '/users/@me/guilds', params=params)

        return [GuildModel.from_dict(guild) for guild in data]

    async def fetch_guild_member(self, guild_id: int):
        """Fetch this user's guild member data.
        !!! warning "Important"
            Requires the OAuth2 guilds.members.read scope!

        Args:
            guild_id (int): ID of guild to fetch data from

        Returns:
            (GuildMemberModel): member data from guild
        """
        data = await self._http.request('GET', f'/users/@me/{guild_id}/member')

        return GuildMemberModel.from_dict(data)
