from dataclasses import dataclass
from typing import Unpack

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake
from ..core.part import serialize

from .base_resource import BaseResource

from ..params import GuildScheduledEventParams

from ..api import GuildScheduledEventPart

@dataclass
class GuildScheduledEvent(BaseResource):
    """Represents the guild scheduled event resource."""

    guild_id: Snowflake
    """Guild ID of the scheduled events."""

    async def fetch(self, 
        event_id: Snowflake, 
        with_user_count: bool | None = None
    ) -> JsonQuery:
        """Fetch a scheduled event.

        Args:
            event_id (Snowflake): ID of the scheduled event
            with_user_count (bool, optional): include number of users subscribed to this event

        Returns:
            (JsonQuery): queried scheduled event
        """
        data = await self.http.request_json(
            'GET',
            f'/guilds/{self.guild_id}/scheduled-events/{event_id}',
            params={
                'with_user_count': with_user_count
            }
        )

        return JsonQuery(data)

    async def fetch_all(self, with_user_count: bool | None = None) -> JsonQuery:
        """Fetch all scheduled events for this guild.

        Args:
            with_user_count (bool, optional): include number of users subscribed to this event

        Returns:
            (JsonQuery): list of queried scheduled events
        """
        data = await self.http.request_list(
            'GET',
            f'/guilds/{self.guild_id}/scheduled-events/',
            params={
                'with_user_count': with_user_count
            }
        )

        return JsonQuery(data)

    async def create(self, event: GuildScheduledEventPart) -> JsonQuery:
        """Create a scheduled event for this guild.
        Fires [**Guild Scheduled Event Create Event**](https://docs.discord.com/developers/events/gateway-events#guild-scheduled-event-create).

        Args:
            event (GuildScheduledEventPart): scheduled event to create

        Returns:
            (JsonQuery): created scheduled event
        """
        data = await self.http.request_json(
            'POST', 
            f'/guilds/{self.guild_id}/scheduled-events',
            data=event.to_dict()
        )

        return JsonQuery(data)

    async def edit(self, 
        event_id: Snowflake, 
        **options: Unpack[GuildScheduledEventParams]
    ) -> JsonQuery:
        """Edit a scheduled event.
        Fires [**Guild Scheduled Event Update**](https://docs.discord.com/developers/events/gateway-events#guild-scheduled-event-update).

        !!! note
            `COMPLETED` and `CANCELED` events cannot be updated.

        Args:
            event_id (Snowflake): ID of the scheduled event to edit

        Returns:
            (JsonQuery): edited scheduled event
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/guilds/{self.guild_id}/scheduled-events/{event_id}',
            data=serialize(dict(options)) # nested objects in GuildScheduledEventParams
        )

        return JsonQuery(data)

    async def delete(self, event_id: Snowflake) -> None:
        """Delete a scheduled event.
        Fires [**Guild Scheduled Event Delete**](https://docs.discord.com/developers/events/gateway-events#guild-scheduled-event-delete).

        Args:
            event_id (Snowflake): ID of the scheduled event to delete
        """
        await self.http.request_json('DELETE', f'/guilds/{self.guild_id}/scheduled-events/{event_id}')

    async def fetch_users(self, 
        event_id: Snowflake, 
        limit: int = 100, 
        with_member: bool = False, 
        before: Snowflake | None = None, 
        after: Snowflake | None = None
    ) -> JsonQuery:
        """Fetch users subscribed to this scheduled event.

        Args:
            event_id (Snowflake): ID of the scheduled event
            limit (int, optional): Max number of users to return. Defaults to `100`.
            with_member (bool, optional): Include guild member data if it exists. Defaults to `False`.
            before (Snowflake, optional): consider only users before this user ID
            after (Snowflake, optional): consider only users after this user ID

        Returns:
            (JsonQuery): list of queried scheduled event users
        """
        data = await self.http.request_list(
            'GET',
            f'/guilds/{self.guild_id}/scheduled-events/{event_id}/users',
            params={
                'limit': limit,
                'with_member': with_member,
                'before': before,
                'after': after
            }
        )

        return JsonQuery(data)
