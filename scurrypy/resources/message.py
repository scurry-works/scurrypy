from dataclasses import dataclass
from typing import Unpack

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake
from ..core.part import serialize
from ..core.types import JSON

from .base_resource import BaseResource

from ..enums import MessageFlags, ReactionType

from ..api.messages import AttachmentPart
from ..api import EmojiPart

from ..params.message import EditMessageParams

class _EditMessageMixin:
    """Common message edit methods."""

    def _apply_suppress_embeds(
        self,
        payload: JSON,
        suppress_embeds: bool | None
    ) -> None:
        """Suppress embeds in the new message.

        Args:
            payload (JSON): partially serialized payload
            suppress_embeds (bool | None): whether to suppress embeds
        """
        if suppress_embeds is not None:
            flags = payload.get("flags", 0)

            if suppress_embeds:
                flags |= MessageFlags.SUPPRESS_EMBEDS
            else:
                flags &= ~MessageFlags.SUPPRESS_EMBEDS

            payload["flags"] = flags

    def _prepare_attachments(
        self,
        payload: JSON
    ) -> list[str]:
        """Index new files and prepare a list to be passed to HTTPClient.

        Args:
            payload (JSON): partially serialized payload

        Returns:
            list[str]: list of file paths for `files` request param.
        """
        if "attachments" not in payload:
            return []

        attachments: list[AttachmentPart] = payload["attachments"]

        assert isinstance(attachments, list)

        for idx, attachment in enumerate(attachments):
            if attachment.id is None: # only set new attachments
                attachment.id = idx

        payload["attachments"] = [
            attachment.to_dict()
            for attachment in attachments
        ]

        return [attachment.path for attachment in attachments if attachment.path is not None]

@dataclass
class Message(BaseResource, _EditMessageMixin):
    """Represents a Discord message resource."""

    id: Snowflake
    """ID of the message"""

    channel_id: Snowflake
    """Channel ID of the message."""

    async def fetch(self) -> JsonQuery:
        """Fetches the message data based on the given channel ID and message ID.

        !!! important "Permissions"
            Requires `VIEW_CHANNEL` and `READ_MESSAGE_HISTORY`

        Returns:
            (JsonQuery): queried message
        """
        data = await self.http.request_json('GET', f"/channels/{self.channel_id}/messages/{self.id}")

        return JsonQuery(data)
    
    async def edit(
        self,
        *,
        suppress_embeds: bool | None = None,
        **options: Unpack[EditMessageParams]
    ) -> JsonQuery:
        """Edits this message.

        Fires [**Message Update Event**](https://docs.discord.com/developers/events/gateway-events#message-update).

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES` *only* if editing another user's message or to edit flags

        Args:
            options (EditMessageParams): fields to edit for the message
            suppress_embeds (optional, bool): whether the response's embeds should be removed

        Returns:
            (JsonQuery): updated message
        """
        files = self._prepare_attachments(dict(options))
        opts = serialize(dict(options)) # nested objects in EditMessageParams
        self._apply_suppress_embeds(opts, suppress_embeds)

        data = await self.http.request_json(
            "PATCH",
            f"/channels/{self.channel_id}/messages/{self.id}",
            data=opts,
            files=files,
        )

        return JsonQuery(data)

    async def crosspost(self) -> JsonQuery:
        """Crosspost this message in an Annoucement channel to all following channels.

        Fires [**Message Update Event**](https://docs.discord.com/developers/events/gateway-events#message-update).

        !!! important "Permissions"
            Requires `SEND_MESSAGES` to publish your own messages

            Requires `MANAGE_MESSAGES` to publish messages from others

        Returns:
            (JsonQuery): published (crossposted) message
        """
        data = await self.http.request_json('POST', f'/channels/{self.channel_id}/messages/{self.id}/crosspost')

        return JsonQuery(data)

    async def delete(self) -> None:
        """Deletes this message.

        Fires [**Message Delete**](https://docs.discord.com/developers/events/gateway-events#message-delete).

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`
        """
        await self.http.request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}")

    async def pin(self) -> None:
        """Pin this message to its channel's pins.

        Fires [**Channel Pins Update**](https://docs.discord.com/developers/events/gateway-events#channel-pins-update).

        !!! important "Permissions"
            Requires `PIN_MESSAGES`
        """
        await self.http.request('PUT', f'/channels/{self.channel_id}/messages/pins/{self.id}')
    
    async def unpin(self) -> None:
        """Unpin this message from its channel's pins.

        Fires [**Channel Pins Update**](https://docs.discord.com/developers/events/gateway-events#channel-pins-update).

        !!! important "Permissions"
            Requires `PIN_MESSAGES`
        """
        await self.http.request('DELETE', f'/channels/{self.channel_id}/messages/pins/{self.id}')

    async def fetch_emoji_reactions(self, 
        emoji: EmojiPart | str, 
        type: ReactionType = ReactionType.NORMAL, 
        after: int | None = None, 
        limit: int = 25
    ) -> JsonQuery:
        """Fetches users who reacted with the specified emoji parameters.

        Args:
            emoji (EmojiPart | str): the standard emoji (str) or custom emoji (EmojiPart)
            type (ReactionType, optional): Type of emoji. Defaults to `ReactionType.NORMAL`.
            after (int, optional): users after this ID
            limit (int, optional): Max number of users to return. Defaults to `25`.

        Returns:
            (JsonQuery): list of users who reacted with this emoji
        """
        if isinstance(emoji, str):
            emoji = EmojiPart(name=emoji)

        data = await self.http.request_list(
            'GET',
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}",
            params={
                'type': type,
                'after': after,
                'limit': limit
            }
        )
        
        return JsonQuery(data)

    async def add_reaction(self, emoji: EmojiPart | str) -> None:
        """Add a reaction to this message.

        Fires [**Message Reaction Add**](https://docs.discord.com/developers/events/gateway-events#message-reaction-add).

        !!! important "Permissions"
            Requires `READ_MESSAGE_HISTORY`.

            Requires `ADD_REACTIONS` of no reactions with this emoji are present.

        Args:
            emoji (EmojiPart | str): the standard emoji (str) or custom emoji (EmojiPart)
        """
        if isinstance(emoji, str):
            emoji = EmojiPart(emoji)

        await self.http.request_json("PUT", f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")

    async def remove_reaction(self, emoji: EmojiPart | str) -> None:
        """Remove the bot's reaction from this message.

        Fires [**Message Reaction Remove**](https://docs.discord.com/developers/events/gateway-events#message-reaction-remove).

        Args:
            emoji (EmojiPart | str): the standard emoji (str) or custom emoji (EmojiPart)
        """
        if isinstance(emoji, str):
            emoji = EmojiPart(emoji)

        await self.http.request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")

    async def remove_user_reaction(self, emoji: EmojiPart | str, user_id: Snowflake) -> None:
        """Remove a specific user's reaction from this message.

        Fires [**Message Reaction Remove**](https://docs.discord.com/developers/events/gateway-events#message-reaction-remove).

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`

        Args:
            emoji (EmojiPart | str): the standard emoji (str) or custom emoji (EmojiPart)
            user_id (Snowflake): user's ID
        """
        if isinstance(emoji, str):
            emoji = EmojiPart(emoji)

        await self.http.request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/{user_id}")

    async def remove_emoji_reaction(self, emoji: EmojiPart | str) -> None:
        """Clear all reactions for a given emoji from this message.
        Fires [**Message Reaction Remove Emoji**](https://docs.discord.com/developers/events/gateway-events#message-reaction-remove-emoji).

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`

        Args:
            emoji (EmojiPart | str): the standard emoji (str) or custom emoji (EmojiPart)
        """
        if isinstance(emoji, str):
            emoji = EmojiPart(emoji)

        await self.http.request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}")

    async def remove_all_reactions(self) -> None:
        """Clear all reactions from this message.

        Fires [**Message Reaction Remove All**](https://docs.discord.com/developers/events/gateway-events#message-reaction-remove-all).

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`
        """
        await self.http.request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}/reactions")
