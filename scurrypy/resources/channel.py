from dataclasses import dataclass
from typing import Unpack

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake
from ..core.part import serialize

from .base_resource import BaseResource

from ..api.messages import MessagePart
from ..api.channels import (
    ThreadFromMessagePart, 
    ThreadWithoutMessagePart
)
from ..api import InvitePart

from ..params import EditGuildChannelParams, EditThreadChannelParams

@dataclass
class Channel(BaseResource):
    """Represents a Discord channel resource."""

    id: Snowflake
    """ID of the channel."""

    # --- CHANNEL ---
    async def fetch(self) -> JsonQuery:
        """Fetch the full channel data from Discord.

        Returns:
            (JsonQuery): queried channel
        """
        data = await self.http.request_json("GET", f"/channels/{self.id}")

        return JsonQuery(data)

    async def delete(self) -> None:
        """Deletes this channel from the server. 
        
        Fires [**Channel Update**](https://docs.discord.com/developers/events/gateway-events#channel-update) if success,
        and [**Channel Delete**](https://docs.discord.com/developers/events/gateway-events#channel-delete) 
            (or [**Thread Delete**](https://docs.discord.com/developers/events/gateway-events#thread-delete) if a thread).

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS` if channel is a guild channel or `MANAGE_THREADS` if channel is a thread
        """
        await self.http.request("DELETE", f"/channels/{self.id}")

    async def follow(self, webhook_channel_id: Snowflake) -> JsonQuery:
        """Follow announcement channel to send messages to a target channel.
        
        Fires [**Webhooks Update**](https://docs.discord.com/developers/events/gateway-events#webhooks-update).

        !!! important "Permissions"
            Requires `MANAGE_WEBHOOKS` in the target channel

        Args:
            webhook_channel_id (Snowflake): ID of target channel

        Returns:
            (JsonQuery): followed channel
        """
        data = await self.http.request_json(
            'POST', 
            f'/channels/{self.id}/followers', 
            params={
                'webhook_channel_id': webhook_channel_id
            }
        )

        return JsonQuery(data)

    # --- GUILD CHANNEL ---
    async def edit_guild_channel(self, **options: Unpack[EditGuildChannelParams]) -> JsonQuery:
        """Edit this channel. 
        
        Fires [**Channel Update**](https://docs.discord.com/developers/events/gateway-events#channel-update).
        
        !!! note
            If modifying a category, all child channels also fire [**ChannelUpdateEvent**](https://docs.discord.com/developers/events/gateway-events#channel-update).

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS` for the guild

        Args:
            options (EditGuildChannelParams): channel fields to edit

        Returns:
            (JsonQuery): updated channel
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/channels/{self.id}', 
            data=serialize(dict(options)) # nested objects in EditGuildChannelParams
        )
        
        return JsonQuery(data)
    
    # --- MESSAGES ---
    async def fetch_messages(self, limit: int = 50, before: Snowflake | None = None, after: Snowflake | None = None, around: Snowflake | None = None) -> JsonQuery:
        """Fetches this channel's messages.

        !!! important "Permissions"
            Requires `VIEW_CHANNEL` and `READ_MESSAGE_HISTORY`

        Args:
            limit (int, optional): Max number of messages to return. Range 1 - 100. Defaults to `50`.
            before (Snowflake, optional): get messages before this message ID
            after (Snowflake, optional): get messages after this message ID
            around (Snowflake, optional): get messages around this message ID

        Returns:
            (JsonQuery): queried list of messages
        """

        data = await self.http.request_list(
            'GET', 
            f'/channels/{self.id}/messages', 
            params={
                "limit": limit,
                "before": before,
                "after": after,
                "around": around
            }
        )

        return JsonQuery(data)

    async def fetch_pins(self, limit: int = 50, before: str | None = None) -> JsonQuery:
        """Get this channel's pinned messages.

        !!! important "Permissions"
            Requires `VIEW_CHANNEL` and `READ_MESSAGE_HISTORY`
            
        !!! warning
            Does not work on a `GUILD_FORUM` channel!

        Args:
            limit (int, optional): Max number of pinned messages to return. Range 1 - 50. Defaults to `50`.
            before (str, optional): get pinned messages before this ISO8601 timestamp
        
        Returns:
            (JsonQuery): queried list of pinned messages
        """
        data = await self.http.request_list(
            'GET', 
            f'/channels/{self.id}/pins', 
            params={
                "limit": limit,
                "before": before
            }
        )

        return JsonQuery(data)

    async def send(self, message: str | MessagePart) -> JsonQuery:
        """Send a message to this channel.
        
        Fires [**Message Create**](https://docs.discord.com/developers/events/gateway-events#message-create).

        !!! important "Permissions"
            Requires `SEND_MESSAGES` if in a guild channel.

            Requires `READ_MESSAGE_HISTORY` of replying to another message.

        Args:
            message (str | MessagePart): content as a string or MessagePart

        Returns:
            (JsonQuery): created message
        """
        # normalize to MessagePart
        msg = MessagePart(content=message) if isinstance(message, str) else message

        msg = msg._prepare()

        files = [str(f.path) for f in msg.attachments] if msg.attachments else None
        
        data = await self.http.request_json(
            "POST", 
            f"/channels/{self.id}/messages", 
            data=msg.to_dict(),
            files=files
        )

        return JsonQuery(data)
    
    async def bulk_delete_messages(self, message_ids: list[Snowflake]) -> None:
        """Delete multiple messages in a single request.
        
        Fires [**Bulk Message Delete**](https://docs.discord.com/developers/events/gateway-events#message-delete-bulk).
        
        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`

        !!! important
            Messages **older than 2 weeks** will not get deleted!

        !!! note
            Only available for `GUILD_TEXT` channels.

        Args:
            message_ids (list[Snowflake]): IDs of the messages to delete. Range 2 to 100 (inclusive).
        """
        await self.http.request(
            'POST', 
            f'/channels/{self.id}/messages/bulk-delete', 
            data={
                'messages': message_ids
            }
        )

    # --- INVITES ---
    async def fetch_invites(self) -> JsonQuery:
        """Fetch a list of invites for this channel.

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS`

        !!! note
            Only usable on guild channels.

        Returns:
            (JsonQuery): queried list of invites
        """
        data = await self.http.request_list('GET', f'/channels/{self.id}/invites')

        return JsonQuery(data)

    async def create_invite(self, invite: InvitePart) -> JsonQuery:
        """Create a new invite for this channel.
        
        Fires [**Invite Create**](https://docs.discord.com/developers/events/gateway-events#invite-create).

        !!! important "Permissions"
            Requires `CREATE_INSTANT_INVITE`

        !!! note
            Only usable for guild channels.

        Args:
            invite (InvitePart): invite to create

        Returns:
            (JsonQuery): created invite object 
        """
        data = await self.http.request_json(
            'POST', 
            f'/channels/{self.id}/invites', 
            data=invite.to_dict()
        )

        return JsonQuery(data)

    # --- THREAD CHANNELS ---
    async def fetch_thread_member(self, user_id: Snowflake, with_member: bool = False) -> JsonQuery:
        """Fetch a thread member of the specified user ID from this thread.

        Args:
            user_id (Snowflake): ID of the user to fetch
            with_member (bool, optional): whether to include the member object. Defaults to `False`.
        
        Returns:
            (JsonQuery): queried thread member
        """
        data = await self.http.request_json(
            'GET', 
            f'/channels/{self.id}/thread-members/{user_id}', 
            params={ 
                'with_member': with_member
            }
        )

        return JsonQuery(data)
    
    async def fetch_thread_members(self, limit: int = 100, after: Snowflake | None = None, with_member: bool = False) -> JsonQuery:
        """Fetch all members of this thread.

        !!! warning
            Requires the `GUILD_MEMBERS` privileged intent to use!

        !!! warning
            Starting in API v11, paginated results will always be returned.

            Enable paginated results before v11 by setting `with_member` to `True`.

        Args:
            limit (int, optional): Max number of thread members to return. Range 0 to 100 (inclusive). Defaults to `100`.
            after (Snowflake, optional): members after this user ID
            with_member (bool, optional): whether to include the member object. Defaults to `False`.

        Returns:
            (JsonQuery): queried list of thread members
        """
        data = await self.http.request_list(
            'GET', 
            f"/channels/{self.id}/thread-members", 
            params={
                'with_member': with_member,
                'after': after,
                'limit': limit
            }
        )

        return JsonQuery(data)

    async def create_thread_from_message(self, message_id: Snowflake, thread: ThreadFromMessagePart) -> JsonQuery:
        """Create a thread from a message (attached to the message). 
        
        Fires [**Thread Create**](https://docs.discord.com/developers/events/gateway-events#thread-create) 
        and [**Message Update**](https://docs.discord.com/developers/events/gateway-events#thread-update).

        !!! note
            Creates a `PUBLIC_THREAD` when created in a `GUILD_TEXT` channel.

            Creates a `ANNOUNCEMENT_THREAD` when created in a `GUILD_ANNOUNCEMENT` channel

        Args:
            message_id (Snowflake): ID of the message to attach the thread
            thread (ThreadFromMessagePart): thread to attach

        Returns:
            (JsonQuery): new thread
        """
        data = await self.http.request_json(
            'POST', 
            f"/channels/{self.id}/messages/{message_id}/threads", 
            data=thread.to_dict()
        )

        return JsonQuery(data)

    async def create_thread_without_message(self, thread: ThreadWithoutMessagePart) -> JsonQuery:
        """Create a thread not connected to an existing message.
        
        Fires [**Thread Create**](https://docs.discord.com/developers/events/gateway-events#thread-create).

        Args:
            thread (ThreadWithoutMessagePart): thread to create

        Returns:
            (JsonQuery): new thread
        """
        data = await self.http.request_json(
            'POST', 
            f'/channels/{self.id}/threads', 
            data=thread.to_dict()
        )

        return JsonQuery(data)

    async def edit_thread(self, **options: Unpack[EditThreadChannelParams]) -> JsonQuery:
        """Edit this thread. 
        
        Fires [**Channel Update**](https://docs.discord.com/developers/events/gateway-events#channel-update).

        !!! important "Permissions"
            Requires `MANAGE_THREADS`

        !!! important
            Requires `archived` be `False` or set to `False`.

        Args:
            options (EditThreadChannelParams): channel fields to edit

        Returns:
            (JsonQuery): updated channel
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/channels/{self.id}', 
            data=dict(options)
        )

        return JsonQuery(data)

    async def join_thread(self) -> None:
        """Add the bot to this thread.
        
        Fires [**Thread Members Update**](https://docs.discord.com/developers/events/gateway-events#thread-members-update) 
        and [**Thread Create**](https://docs.discord.com/developers/events/gateway-events#thread-create).

        !!! important
            Requires the thread is NOT archived.
        """
        await self.http.request('PUT', f'/channels/{self.id}/thread-members/@me')

    async def leave_thread(self) -> None:
        """Remove the bot from a thread.
        
        Fires [**Thread Members Update**](https://docs.discord.com/developers/events/gateway-events#thread-members-update).

        !!! important
            Requires the thread is NOT archived.
        """
        await self.http.request('DELETE', f'/channels/{self.id}/thread-members/@me')

    async def add_thread_member(self, user_id: Snowflake) -> None:
        """Add a user to this thread.
        
        Fires [**Thread Members Update**](https://docs.discord.com/developers/events/gateway-events#thread-members-update).

        !!! important
            Requires the thread is NOT archived.

        Args:
            user_id (Snowflake): ID of the user to add
        """
        await self.http.request('PUT', f'/channels/{self.id}/thread-members/{user_id}')

    async def remove_thread_member(self, user_id: Snowflake) -> None:
        """Remove a user to this thread.
        
        Fires [**Thread Members Update**](https://docs.discord.com/developers/events/gateway-events#thread-members-update).

        !!! important "Permissions"
            Requires `MANAGE_THREADS` or thread creator if `PRIVATE_THREAD`

        !!! important
            Requires the thread is NOT archived.

        Args:
            user_id (Snowflake): ID of the user to remove
        """
        await self.http.request('DELETE', f'/channels/{self.id}/thread-members/{user_id}')

    async def fetch_public_archived_threads(self, before: str | None = None, limit: int | None = None) -> JsonQuery:
        """Fetch archived public threads in this channel.

        !!! important "Permissions"
            Requires `READ_MESSAGE_HISTORY`

        !!! note
            Returns `PUBLIC_THREAD` threads if this is a `GUILD_TEXT` channel.
            Returns `ANNOUNCEMENT_THREAD` if this is a `GUILD_ANNOUNCEMENT` channel.

        !!! note
            Threads are ordered by `archive_timestamp` in descending order.

        Args:
            before (str, optional): threads archived before this timestamp
            limit (int, optional): max number of threads to fetch

        Returns:
            (JsonQuery): queried public archived threads
        """
        data = await self.http.request_json(
            'GET', 
            f'/channels/{self.id}/threads/archived/public', 
            params={
                'before': before, 
                'limit': limit
            }
        )

        return JsonQuery(data)
    
    async def fetch_private_archived_threads(self, before: str | None = None, limit: int | None = None) -> JsonQuery:
        """Fetch archived private threads in this channel.

        !!! important "Permissions"
            Requires `READ_MESSAGE_HISTORY` and `MANAGE_THREADS`

        !!! note
            Threads are ordered by `archive_timestamp` in descending order.

        Args:
            before (str, optional): threads archived before this timestamp
            limit (int, optional): max numer of threads to fetch

        Returns:
            (JsonQuery): queried private archived threads
        """
        data = await self.http.request_json(
            'GET', 
            f'/channels/{self.id}/threads/archived/private', 
            params={
                'before': before, 
                'limit': limit
            }
        )

        return JsonQuery(data)
    
    async def fetch_joined_private_archived_threads(self, before: str | None = None, limit: int | None = None) -> JsonQuery:
        """Fetch archived private threads in this channel the bot has joined.

        !!! important "Permissions"
            Requires `READ_MESSAGE_HISTORY`

        !!! note
            Threads are ordered by their `id` in descending order.

        Args:
            before (str, optional): threads archived before this timestamp
            limit (int, optional): max numer of threads to fetch

        Returns:
            (JsonQuery): queried private archived threads
        """
        data = await self.http.request_json(
            'GET', 
            f'/channels/{self.id}/users/@me/threads/archived/private', 
            params={
                'before': before, 
                'limit': limit
            }
        )

        return JsonQuery(data)
