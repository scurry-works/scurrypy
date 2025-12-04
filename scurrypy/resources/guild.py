from dataclasses import dataclass
from typing import Optional, TypedDict, Unpack

from .base_resource import BaseResource

from ..parts.channel import GuildChannel
from ..parts.role import Role

from ..models.role import RoleModel
from ..models.guild import GuildModel
from ..models.guild_member import GuildMemberModel
from ..models.channel import ChannelModel

class FetchGuildMembersParams(TypedDict, total=False):
    """Params when fetching guild members."""

    limit: int
    """Max number of members to return Range 1 - 1000. Default 1."""

    after: int
    """Highest user ID in previous page."""

class FetchGuildParams(TypedDict, total=False):
    """Params when fetching a guild."""

    with_counts: Optional[bool]
    """If True, return the approximate member and presence counts for the guild."""

@dataclass
class Guild(BaseResource):
    """Represents a Discord guild."""
    
    id: int
    """ID of the guild."""

    async def fetch(self, **kwargs: Unpack[FetchGuildParams]):
        """Fetch the Guild object by the given ID.

        Args:
            **kwargs: guild fetch params
                !!! note
                    If no kwargs are provided, default to with_counts = False
            
        Returns:
            (GuildModel): the Guild object
        """
        params = {'with_counts': False, **kwargs}

        data = await self._http.request('GET', f'/guilds/{self.id}', params=params)

        return GuildModel.from_dict(data)

    async def fetch_channels(self):
        """Fetch this guild's channels.

        Returns:
            (list[ChannelModel]): list of the guild's channels
        """
        data = await self._http.request('GET', f'guilds/{self.id}/channels')

        return [ChannelModel.from_dict(channel) for channel in data]

    async def create_channel(self, channel: GuildChannel):
        """Create a channel in this guild.

        Permissions:
            * MANAGE_CHANNELS → required to create a channel

        Args:
            channel (GuildChannel): the buildable guild channel

        Returns:
            (ChannelModel): the created channel
        """
        data = await self._http.request('POST', f'/guilds/{self.id}/channels', data=channel.to_dict())

        return ChannelModel.from_dict(data)

    async def fetch_guild_member(self, user_id: int):
        """Fetch a member in this guild.
        !!! warning "Important"
            Requires the GUILD_MEMBERS privileged intent!

        Args:
            user_id (int): user ID of the member to fetch

        Returns:
            (GuildMemberModel): member's data
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/members/{user_id}')

        return GuildMemberModel.from_dict(data)
    
    async def fetch_guild_members(self, **kwargs: Unpack[FetchGuildMembersParams]):
        """Fetch guild members in this guild.
        !!! warning "Important"
            Requires the GUILD_MEMBERS privileged intent!

        Args:
            **kwargs: guild members fetch params
                !!! note
                    If no kwargs are provided, default to 1 guild member limit.

        Returns:
            (list[GuildMemberModel]): list of member data
        """
        params = {"limit": 1, **kwargs}

        data = await self._http.request('GET', f'/guilds/{self.id}/members', params=params)

        return [GuildMemberModel.from_dict(member) for member in data]

    async def add_guild_member_role(self, user_id: int, role_id: int):
        """Append a role to a guild member of this guild.

        Permissions:
            * MANAGE_ROLES → required to add a role to the user
        
        Args:
            user_id (int): ID of the member for the role
            role_id (int): ID of the role to append
        """
        await self._http.request('PUT', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')
    
    async def remove_guild_member_role(self, user_id: int, role_id: int):
        """Remove a role from a guild member of this guild.

        Permissions:
            * MANAGE_ROLES → required to remove a role from the user

        Args:
            user_id (int): ID of the member with the role
            role_id (int): ID of the role to remove
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')

    async def fetch_guild_role(self, role_id: int):
        """Fetch a role in this guild.

        Args:
            role_id (int): ID of the role to fetch

        Returns:
            (RoleModel): fetched role's data
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/roles/{role_id}')
        
        return RoleModel.from_dict(data)

    async def fetch_guild_roles(self):
        """Fetch all roles in this guild.

        Returns:
            (list[RoleModel]): list of fetched roles' data
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/roles')
        
        return [RoleModel.from_dict(role) for role in data]

    async def create_guild_role(self, role: Role):
        """Create a role in this guild.

        Permissions:
            * MANAGE_ROLES → required to add a role to the guild

        Args:
            role (Role): role to create

        Returns:
            (RoleModel): new role data
        """
        data = await self._http.request('POST', f'/guilds/{self.id}/roles', data=role.to_dict())

        return RoleModel.from_dict(data)

    async def modify_guild_role(self, role_id: int, role: Role):
        """Modify a role in this guild.

        Permissions:
            * MANAGE_ROLES → required to modify a role in the guild

        Args:
            role (Role): role with changes

        Returns:
            (RoleModel): role with changes
        """
        data = await self._http.request('PATCH', f'/guilds/{self.id}/roles/{role_id}', data=role.to_dict())

        return RoleModel.from_dict(data)
    
    async def delete_guild_role(self, role_id: int):
        """Delete a role in this guild.

        Permissions:
            * MANAGE_ROLES → required to delete a role in the guild

        Args:
            role_id (int): ID of role to delete
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/roles/{role_id}')
