from dataclasses import dataclass
from typing import TypedDict, Unpack, Literal

from .base_resource import BaseResource

from ..parts.channel import GuildChannel
from ..parts.message import MessagePart

from ..models.message import MessageModel
from ..models.channel import ChannelModel, PinnedMessageModel

class MessagesFetchParams(TypedDict, total=False):
    """Params when fetching guild channel messages."""

    limit: int
    """Max number of messages to return. Range 1 - 100. Default 50."""

    before: int
    """Get messages before this message ID."""

    after: int
    """Get messages after this message ID."""

    around: int
    """Get messages around this message ID."""

class PinsFetchParams(TypedDict, total=False):
    """Params when fetching pinned messages."""

    before: str
    """Get pinned messages before this ISO8601 timestamp."""

    limit: int
    """Max number of pinned messages to return. Range 1 - 50. Default 50."""

class ThreadFromMessageParams(TypedDict, total=False):
    """Params when attaching a thread to a message."""

    rate_limit_per_user: Literal[60, 1440, 4320, 10080]
    """time (minutes) of inactivity before thread is archived."""

    rate_limit_per_user: int
    """time (seconds) user waits before sending another message."""

@dataclass
class Channel(BaseResource):
    """Represents a Discord guild channel."""

    id: int
    """ID of the channel."""

    async def fetch(self):
        """Fetch the full channel data from Discord.

        Returns:
            (ChannelModel): A new Channel object with all fields populated
        """
        data = await self._http.request("GET", f"/channels/{self.id}")

        return ChannelModel.from_dict(data)
    
    async def fetch_messages(self, **kwargs: Unpack[MessagesFetchParams]):
        """Fetches this channel's messages.

        Permissions:
            * VIEW_CHANNEL → required to access channel messages
            * READ_MESSAGE_HISTORY → required for user, otherwise no messages are returned

        Args:
            **kwargs: message fetch params
                !!! note
                    if no kwargs are provided, default to 50 fetched messages limit.

        Returns:
            (list[MessageModel]): queried messages
        """
        params = {"limit": 50, **kwargs}

        data = await self._http.request('GET', f'/channels/{self.id}/messages', params=params)

        return [MessageModel.from_dict(msg) for msg in data]
    
    async def send(self, message: str | MessagePart):
        """
        Send a message to this channel.

        Permissions:
            * SEND_MESSAGES → required to create a message in this channel

        Args:
            message (str | MessagePart): can be just text or the MessagePart for dynamic messages

        Returns:
            (MessageModel): The created Message object
        """
        if isinstance(message, str):
            message = MessagePart(content=message)

        message = message._prepare()

        data = await self._http.request(
            "POST", 
            f"/channels/{self.id}/messages", 
            data=message._prepare().to_dict(),
            files=[fp.path for fp in message.attachments]
        )

        return MessageModel.from_dict(data)

    async def edit(self, channel: GuildChannel):
        """Edit this channel's settings.

        Permissions:
            * MANAGE_CHANNELS → required to edit this channel

        Args:
            channel (GuildChannel): channel changes

        Returns:
            (ChannelModel): The updated channel object
        """
        data = await self._http.request("PATCH", f"/channels/{self.id}", data=channel.to_dict())

        return ChannelModel.from_dict(data)
    
    async def create_thread_from_message(self, message_id: int, name: str, **kwargs: Unpack[ThreadFromMessageParams]):
        """Create a thread from this message

        Args:
            message_id: ID of message to attach thread
            name (str): thread name
            **kwargs (Unpack[ThreadFromMessageParams]): thread create params

        Returns:
            (ChannelModel): The updated channel object
        """

        content = {
            'name': name, 
            **kwargs
        }

        data = await self._http.request('POST', f"channels/{self.id}/messages/{message_id}/threads", data=content)

        return ChannelModel.from_dict(data)
    
    async def fetch_pins(self, **kwargs: Unpack[PinsFetchParams]):
        """Get this channel's pinned messages.

        Permissions:
            * VIEW_CHANNEL → required to access pinned messages
            * READ_MESSAGE_HISTORY → required for reading pinned messages

        Args:
            **kwargs: pinned message fetch params
                !!! note
                    If no kwargs are provided, default to 50 fetched messages limit.
            
        Returns:
            (list[PinnedMessage]): list of pinned messages
        """
        # Set default limit if user didn't supply one
        params = {"limit": 50, **kwargs}

        data = await self._http.request('GET', f'/channels/{self.id}/pins', params=params)

        return [PinnedMessageModel.from_dict(item) for item in data]

    async def delete(self):
        """Deletes this channel from the server.

        Permissions:
            * MANAGE_CHANNELS → required to delete this channel
        """
        await self._http.request("DELETE", f"/channels/{self.id}")
