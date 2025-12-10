from dataclasses import dataclass

from .base_resource import BaseResource

from ..models.emoji import EmojiModel
from ..models.message import MessageModel

from ..parts.message import MessagePart

@dataclass
class Message(BaseResource):
    """A Discord message."""

    id: int
    """ID of the message"""

    channel_id: int
    """Channel ID of the message."""

    async def fetch(self):
        """Fetches the message data based on the given channel ID and message id.

        Returns:
            (MessageModel): the message object
        """
        data = await self._http.request('GET', f"/channels/{self.channel_id}/messages/{self.id}")

        return MessageModel.from_dict(data)

    async def send(self, message: str | MessagePart):
        """Sends a new message to the current channel.

        Permissions:
            * SEND_MESSAGES → required to senf your own messages

        Args:
            message (str | MessagePart): can be just text or the MessagePart for dynamic messages

        Returns:
            (MessageModel): the new Message object with all fields populated
        """
        if isinstance(message, str):
            message = MessagePart(content=message)
        elif not message:
            raise ValueError("Missing message.")

        data = await self._http.request(
            "POST",
            f"/channels/{self.channel_id}/messages",
            data=message._prepare().to_dict(),
            files=[fp.path for fp in message.attachments] if message.attachments else None
        )
        return MessageModel.from_dict(data)

    async def edit(self, message: str | MessagePart):
        """Edits this message.

        Permissions:
            * MANAGE_MESSAGES → ONLY if editing another user's message

        Args:
            message (str | MessagePart): can be just text or the MessagePart for dynamic messages

        Returns:
            (MessageModel): the edited message
        """
        if isinstance(message, str):
            message = MessagePart(content=message)
        elif not message:
            raise ValueError("Missing message.")

        data = await self._http.request(
            "PATCH", 
            f"/channels/{self.channel_id}/messages/{self.id}", 
            data=message._prepare().to_dict(),
            files=[fp.path for fp in message.attachments] if message.attachments else None)

        return MessageModel.from_dict(data)

    async def crosspost(self):
        """Crosspost this message in an Annoucement channel to all following channels.

        Permissions:
            * SEND_MESSAGES → required to publish your own messages
            * MANAGE_MESSAGES → required to publish messages from others

        Returns:
            (MessageModel): the published (crossposted) message
        """
        data = await self._http.request('POST', f'/channels/{self.channel_id}/messages/{self.id}/crosspost')

        return MessageModel.from_dict(data)

    async def delete(self):
        """Deletes this message."""
        await self._http.request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}")

    async def add_reaction(self, emoji: EmojiModel | str):
        """Add a reaction from this message.

        Permissions:
            * READ_MESSAGE_HISTORY → required to view message
            * ADD_REACTIONS → required to create reaction

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)
        elif not emoji:
            raise ValueError("Missing emoji.")

        await self._http.request(
            "PUT",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")
    
    async def remove_reaction(self, emoji: EmojiModel | str):
        """Remove the bot's reaction from this message.

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)
        elif not emoji:
            raise ValueError("Missing emoji.")

        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")

    async def remove_user_reaction(self, emoji: EmojiModel | str, user_id: int):
        """Remove a specific user's reaction from this message.

        Permissions:
            * MANAGE_MESSAGES → required to remove another user's reaction

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
            user_id (int): user's ID
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)
        elif not emoji:
            raise ValueError("Missing emoji.")

        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/{user_id}")

    async def remove_all_reactions(self):
        """Clear all reactions from this message.

        Permissions:
            * MANAGE_MESSAGES → required to remove all reaction
        """
        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions")

    async def pin(self):
        """Pin this message to its channel's pins."""
        await self._http.request('PUT', f'/channels/{self.channel_id}/messages/pins/{self.id}')

    async def unpin(self):
        """Unpin this message from its channel's pins."""
        await self._http.request('DELETE', f'/channels/{self.channel_id}/messages/pins/{self.id}')
