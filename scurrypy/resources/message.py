from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..core.snowflake import Snowflake
from ..core.serialization import serialize
from ..core.types import JSON

from ..enums.message import MessageFlags
from ..enums.emoji import ReactionType

from ..api.messages.message import MessageModel
from ..api.messages.attachment import AttachmentPart

from ..api.emoji import EmojiModel
from ..api.user import UserModel

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
    """A Discord message."""

    id: Snowflake
    """ID of the message"""

    channel_id: Snowflake
    """Channel ID of the message."""

    async def fetch(self) -> MessageModel:
        """Fetches the message data based on the given channel ID and message ID.

        Returns:
            (MessageModel): queried message
        """
        data = await self.http.request('GET', f"/channels/{self.channel_id}/messages/{self.id}")

        return MessageModel.from_dict(data)
    
    async def edit(
        self,
        *,
        suppress_embeds: bool | None = None,
        **options: Unpack[EditMessageParams]
    ) -> MessageModel:
        """Edits this message.
        Fires [`MessageUpdateEvent`][scurrypy.events.message_events.MessageUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES` *only* if editing another user's message or to edit flags

        Args:
            options (EditMessageParams): fields to edit for the message
            suppress_embeds (optional, bool): whether the response's embeds should be removed

        Returns:
            (MessageModel): updated message
        """
        
        files = self._prepare_attachments(dict(options))
        opts = serialize(dict(options))
        self._apply_suppress_embeds(opts, suppress_embeds)

        data = await self.http.request(
            "PATCH",
            f"/channels/{self.channel_id}/messages/{self.id}",
            data=opts,
            files=files,
        )

        return MessageModel.from_dict(data)

    async def crosspost(self) -> MessageModel:
        """Crosspost this message in an Annoucement channel to all following channels.
        Fires [`MessageUpdateEvent`][scurrypy.events.message_events.MessageUpdateEvent].

        !!! important "Permissions"
            * `SEND_MESSAGES` → required to publish your own messages
            * `MANAGE_MESSAGES` → required to publish messages from others

        Returns:
            (MessageModel): published (crossposted) message
        """
        data = await self.http.request('POST', f'/channels/{self.channel_id}/messages/{self.id}/crosspost')

        return MessageModel.from_dict(data)

    async def delete(self) -> None:
        """Deletes this message.
        Fires [`MessageDeleteEvent`][scurrypy.events.message_events.MessageDeleteEvent].
        """
        await self.http.request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}")

    async def pin(self) -> None:
        """Pin this message to its channel's pins.
        Fires [`ChannelPinsUpdateEvent`][scurrypy.events.channel_events.ChannelPinsUpdateEvent].
        """
        await self.http.request('PUT', f'/channels/{self.channel_id}/messages/pins/{self.id}')
    
    async def unpin(self) -> None:
        """Unpin this message from its channel's pins.
        Fires [`ChannelPinsUpdateEvent`][scurrypy.events.channel_events.ChannelPinsUpdateEvent].
        """
        await self.http.request('DELETE', f'/channels/{self.channel_id}/messages/pins/{self.id}')

    async def fetch_emoji_reactions(self, 
        emoji: EmojiModel | str, 
        type: ReactionType = ReactionType.NORMAL, 
        after: int | None = None, 
        limit: int = 25
    ) -> list[UserModel]:
        """Fetches users who reacted with the specified emoji parameters.

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
            type (ReactionType, optional): Type of emoji. Defaults to `ReactionType.NORMAL`.
            after (int, optional): users after this ID
            limit (int, optional): Max number of users to return. Defaults to `25`.

        Returns:
            list[UserModel]: list of users who reacted with this emoji
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        data = await self.http.request(
            'GET',
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}",
            params={
                'type': type,
                'after': after,
                'limit': limit
            }
        )
        assert isinstance(data, list)
        return [UserModel.from_dict(user) for user in data]

    async def add_reaction(self, emoji: EmojiModel | str) -> None:
        """Add a reaction to this message.
        Fires [`MessageReactionAddEvent`][scurrypy.events.reaction_events.ReactionAddEvent].

        !!! important "Permissions"
            Requires `READ_MESSAGE_HISTORY` and `ADD_REACTIONS`

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        await self.http.request(
            "PUT",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")

    async def remove_reaction(self, emoji: EmojiModel | str) -> None:
        """Remove the bot's reaction from this message.
        Fires [`MessageReactionRemoveEvent`][scurrypy.events.reaction_events.ReactionRemoveEvent].

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        await self.http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")

    async def remove_user_reaction(self, emoji: EmojiModel | str, user_id: Snowflake) -> None:
        """Remove a specific user's reaction from this message.
        Fires [`MessageReactionRemoveEvent`][scurrypy.events.reaction_events.ReactionRemoveEvent].

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
            user_id (Snowflake): user's ID
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        await self.http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/{user_id}")

    async def remove_emoji_reaction(self, emoji: EmojiModel | str) -> None:
        """Clear all reactions for a given emoji from this message.

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)
        
        await self.http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}")

    async def remove_all_reactions(self) -> None:
        """Clear all reactions from this message.
        Fires [`MessageReactionRemoveAllEvent`][scurrypy.events.reaction_events.ReactionRemoveAllEvent].

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`
        """
        await self.http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions")
