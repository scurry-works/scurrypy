from dataclasses import dataclass
from typing import Unpack

from ..core.json_query import JsonQuery
from ..core.part import serialize
from ..core.snowflake import Snowflake
from ..core.types import JSON

from ..resources import BaseResource

from ..api import WebhookMessagePart, WebhookPart

from ..params import WebhookParams

from .message import _EditMessageMixin

@dataclass
class Webhook(BaseResource, _EditMessageMixin):
    """Represents a webhook resource."""

    async def create(self, channel_id: Snowflake, webhook: WebhookPart) -> JsonQuery:
        """Create a webhook to be sent to a channel.

        !!! important "Permissions"
            Requires `MANAGE_WEBHOOKS`

        Args:
            channel_id (Snowflake): channel ID to send webhook messages
            webhook (WebhookPart): the webhook to create

        Returns:
            (JsonQuery): created webhook
        """
        data = await self.http.request_json(
            'POST', 
            f'/channels/{channel_id}/webhooks', 
            data=webhook.to_dict()
        )

        return JsonQuery(data)

    async def fetch_guild(self, guild_id: Snowflake) -> JsonQuery:
        """Fetch webhooks from a guild.

        !!! important "Permissions"
            Requires `MANAGE_WEBHOOKS`

        Args:
            guild_id (Snowflake): guild ID of the webhook to fetch

        Returns:
            (JsonQuery): queried guild webhooks
        """
        data = await self.http.request_list('GET', f'/guilds/{guild_id}/webhooks')

        return JsonQuery(data)

    async def fetch_webhooks(self, channel_id: Snowflake) -> JsonQuery:
        """Fetch webhooks from a channel.

        !!! important "Permissions"
            Requires `MANAGE_WEBHOOKS`

        Args:
            channel_id (Snowflake): channel ID of the webhook to fetch

        Returns:
            (JsonQuery): queried channel webhooks
        """
        data = await self.http.request_list('GET', f'/channels/{channel_id}/webhooks')

        return JsonQuery(data)

    async def fetch(self, webhook_id: Snowflake) -> JsonQuery:
        """Fetch a webhook.

        !!! important "Permissions"
            Requires `MANAGE_WEBHOOKS`

        Args:
            webhook_id (Snowflake): ID of the webhook to fetch

        Returns:
            (JsonQuery): queried webhook
        """
        data = await self.http.request_json('GET', f'/webhooks/{webhook_id}')

        return JsonQuery(data)

    async def edit(self, webhook_id: Snowflake, **options: Unpack[WebhookParams]) -> JsonQuery:
        """Edit a webhook.

        !!! important "Permissions"
            Requires `MANAGE_WEBHOOKS`

        Args:
            webhook_id (Snowflake): ID of the webhook to edit

        Returns:
            (JsonQuery): edited webhook
        """        
        data = await self.http.request_json(
            'PATCH', 
            f'/webhooks/{webhook_id}', 
            data=serialize(dict(options))
        )

        return JsonQuery(data)

    async def delete(self, webhook_id: Snowflake) -> None:
        """Delete a webhook.

        !!! important "Permissions"
            Requires `MANAGE_WEBHOOKS`

        Args:
            webhook_id (Snowflake): ID of the webhook to delete
        """
        await self.http.request('DELETE', f'/webhooks/{webhook_id}')

    async def execute(self, 
        webhook_id: Snowflake, 
        token: str, 
        message: WebhookMessagePart | str, 
        wait: bool = False, 
        thread_id: Snowflake | None = None, 
        with_components: bool = False
    ) -> JsonQuery | None:
        """Execute a webhook.

        Args:
            webhook_id (Snowflake): ID of the webhook to send message
            token (str): token of the webhook to send message
            message (WebhookMessagePart | str): webhook message
            wait (bool, optional): whether to return message. Defaults to `False`.
            thread_id (Snowflake, optional): thread ID to send message
                !!! note
                    Thread will also be unarchived.
            with_components (bool, optional): Whether to respect the `components` field. Defaults to `False`.

        Returns:
            (JsonQuery | None): webhook message if `wait = True` else `None`
        """
        # normalize to WebhookMessagePart
        msg = WebhookMessagePart(content=message) if isinstance(message, str) else message

        files = [str(f.path) for f in msg.attachments] if msg.attachments else None
        
        data = await self.http.request(
            "POST", 
            f'/webhooks/{webhook_id}/{token}', 
            data=msg._prepare().to_dict(),
            params={
                'wait': wait,
                'thread_id': thread_id,
                'with_components': with_components
            },
            files=files
        )

        if wait is True:
            assert isinstance(data, dict)
            return JsonQuery(data)

        return None
