from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake
from ..core.part import serialize

from ..params import EditUserParams

@dataclass
class User(BaseResource):
    """Represents a Discord user resource."""

    async def fetch(self, user_id: Snowflake) -> JsonQuery:
        """Fetch this user by ID.

        Args:
            user_id (Snowflake): ID of user to fetch

        Returns:
            (JsonQuery): queried user
        """
        data = await self.http.request_json('GET', f'/users/{user_id}')

        return JsonQuery(data)

    async def fetch_guild_member(self, guild_id: Snowflake, user_id: Snowflake) -> JsonQuery:
        """Fetch this user's guild member data.

        Args:
            guild_id (Snowflake): ID of guild to fetch data from
            user_id (Snowflake): ID of user to fetch

        Returns:
            (JsonQuery): queried guild member for the user
        """
        data = await self.http.request_json('GET', f'/guilds/{guild_id}/members/{user_id}')

        return JsonQuery(data)

    async def modify_current_user(self, **options: Unpack[EditUserParams]) -> JsonQuery:
        """Modify the bot's account settings.
        Fires [**User Update**](https://docs.discord.com/developers/events/gateway-events#user-update).

        Args:
            options (EditUserParams): fields to edit

        Returns:
            (JsonQuery): edited user
        """
        data = await self.http.request_json(
            'PATCH', 
            '/users/@me', 
            data=serialize(dict(options)) # nested objects in EditUserParams
        )

        return JsonQuery(data)

    async def leave_guild(self, guild_id: Snowflake) -> None:
        """Make the bot leave a guild.
        Fires [**Guild Delete**](https://docs.discord.com/developers/events/gateway-events#guild-delete)
        and [**Guild Member Remove**](https://docs.discord.com/developers/events/gateway-events#guild-member-remove).

        Args:
            guild_id (Snowflake): ID of the guild to leave
        """
        await self.http.request('DELETE', f'/users/@me/guilds/{guild_id}')

    async def create_dm(self, user_id: Snowflake) -> JsonQuery:
        """Create a DM between the bot and this user.

        Args:
            user_id (Snowflake): ID of user to create DM with
        
        Returns:
            (JsonQuery): created or existing DM channel
        """
        data = await self.http.request_json(
            'POST', 
            '/users/@me/channels', 
            data={
                'recipient_id': user_id
            }
        )

        return JsonQuery(data)
