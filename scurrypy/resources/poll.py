from dataclasses import dataclass

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake

from ..resources import BaseResource

@dataclass
class Poll(BaseResource):
    """A poll!"""

    channel_id: Snowflake
    """Channel ID of the poll."""

    message_id: Snowflake
    """Message ID of the poll."""

    async def fetch_poll_voters(self, answer_id: Snowflake, after: Snowflake | None = None, limit: int = 25) -> JsonQuery:
        """Fetch users that voted on the answer.

        Args:
            answer_id (Snowflake): ID of the answer
            after (Snowflake, optional): users after this user ID
            limit (int, optional): Max number of users to return. Defaults to `25`.

        Returns:
            (JsonQuery): users that voted on the answer
        """        
        data = await self.http.request_list(
            'GET', 
            f'/channels/{self.channel_id}/polls/{self.message_id}/answers/{answer_id}',
            params={
                'after': after,
                'limit': limit
            }
        )
        
        return JsonQuery(data)

    async def end(self) -> JsonQuery:
        """End the poll.
        Fires [**Message Update Event**](https://docs.discord.com/developers/events/gateway-events#message-update).

        !!! warning
            Polls from other users cannot be terminated.

        Returns:
            (JsonQuery): updated message
        """
        data = await self.http.request_json('POST', f'/channels/{self.channel_id}/polls/{self.message_id}/expire')
        
        return JsonQuery(data)
