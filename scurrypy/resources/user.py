from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..core.snowflake import Snowflake
from ..core.serialization import serialize

from ..api.channels import ChannelModel
from ..api.user import UserModel, GuildMemberModel

from ..params.user import EditUserParams

@dataclass
class User(BaseResource):
    """A Discord user."""

    async def fetch(self, user_id: Snowflake) -> UserModel:
        """Fetch this user by ID.

        Args:
            user_id (Snowflake): ID of user to fetch

        Returns:
            (UserModel): queried user
        """
        data = await self.http.request_json('GET', f'/users/{user_id}')

        return UserModel.from_dict(data)

    async def fetch_guild_member(self, guild_id: Snowflake, user_id: Snowflake) -> GuildMemberModel:
        """Fetch this user's guild member data.

        Args:
            guild_id (Snowflake): ID of guild to fetch data from
            user_id (Snowflake): ID of user to fetch

        Returns:
            (GuildMemberModel): queried guild member for the user
        """
        data = await self.http.request_json('GET', f'/guilds/{guild_id}/members/{user_id}')

        return GuildMemberModel.from_dict(data)

    async def modify_current_user(self, **options: Unpack[EditUserParams]) -> UserModel:
        """Modify the bot's account settings.
        Fires [`UserUpdateEvent`][scurrypy.events.user_events.UserUpdateEvent].

        Args:
            options (EditUserParams): fields to edit

        Returns:
            (UserModel): edited user
        """
        opts = serialize(dict(options)) # nested objects in EditUserParams

        data = await self.http.request_json('PATCH', '/users/@me', data=opts)

        return UserModel.from_dict(data)

    async def leave_guild(self, guild_id: Snowflake) -> None:
        """Make the bot leave a guild.
        Fires [`GuildDeleteEvent`][scurrypy.events.guild_events.GuildDeleteEvent]
        and [`GuildMemberRemoveEvent`][scurrypy.events.user_events.GuildMemberRemoveEvent].

        Args:
            guild_id (Snowflake): ID of the guild to leave
        """
        await self.http.request('DELETE', f'/users/@me/guilds/{guild_id}')

    async def create_dm(self, user_id: Snowflake) -> ChannelModel:
        """Create a DM between the bot and this user.

        Args:
            user_id (Snowflake): ID of user to create DM with
        
        Returns:
            (ChannelModel): created or existing DM channel
        """
        data = await self.http.request_json(
            'POST', 
            '/users/@me/channels', 
            data={'recipient_id': user_id}
        )

        return ChannelModel.from_dict(data)
