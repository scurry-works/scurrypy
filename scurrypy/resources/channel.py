from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..core.snowflake import Snowflake
from ..core.serialization import serialize

from ..api.messages import MessageModel, PinnedMessageModel, MessagePart
from ..api.channels import (
    ChannelModel, 
    FollowedChannelModel, 
    ThreadMemberModel, 
    ArchivedThreadsModel, 
    ThreadFromMessagePart, 
    ThreadWithoutMessagePart
)
from ..api.invite import InviteModel, InvitePart, InviteWithMetadataModel

from ..params.channel import EditGuildChannelParams, EditThreadChannelParams

@dataclass
class Channel(BaseResource):
    """Represents a Discord channel."""

    id: Snowflake
    """ID of the channel."""

    # --- CHANNEL ---
    async def fetch(self) -> ChannelModel:
        """Fetch the full channel data from Discord.

        Returns:
            (ChannelModel): queried channel
        """
        data = await self.http.request_json("GET", f"/channels/{self.id}")

        return ChannelModel.from_dict(data)

    async def delete(self) -> None:
        """Deletes this channel from the server. 
        Fires [`ChannelUpdateEvent`][scurrypy.events.channel_events.ChannelUpdateEvent] if success,
        and [`ChannelDeleteEvent`][scurrypy.events.channel_events.ChannelDeleteEvent] 
            (or [`ThreadDeleteEvent`][scurrypy.events.thread_events.ThreadDeleteEvent] if a thread).

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS` if channel is a guild channel or `MANAGE_THREADS` if channel is a thread
        """
        await self.http.request("DELETE", f"/channels/{self.id}")

    async def follow(self, webhook_channel_id: Snowflake) -> FollowedChannelModel:
        """Follow announcement channel to send messages to a target channel.
        Fires [`WebhooksUpdateEvent`][scurrypy.events.channel_events.WebhooksUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_WEBHOOKS` in the target channel

        Args:
            webhook_channel_id (Snowflake): ID of target channel

        Returns:
            (FollowedChannelModel): followed channel
        """
        data = await self.http.request_json(
            'POST', 
            f'/channels/{self.id}/followers', 
            params={'webhook_channel_id': webhook_channel_id}
        )

        return FollowedChannelModel.from_dict(data)

    # --- GUILD CHANNEL ---
    async def edit_guild_channel(self, **options: Unpack[EditGuildChannelParams]) -> ChannelModel:
        """Edit this channel. 
        Fires [`ChannelUpdateEvent`][scurrypy.events.channel_events.ChannelUpdateEvent].
        
        !!! note
            If modifying a category, all child channels also fire [`ChannelUpdateEvent`][scurrypy.events.channel_events.ChannelUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS` for the guild

        Args:
            options (EditGuildChannelParams): channel fields to edit

        Returns:
            (ChannelModel): updated channel
        """
        opts = serialize(dict(options)) # nested objects in EditGuildChannelParams

        data = await self.http.request_json('PATCH', f'/channels/{self.id}', data=opts)

        return ChannelModel.from_dict(data)
    
    # --- MESSAGES ---
    async def fetch_messages(self, limit: int = 50, before: Snowflake | None = None, after: Snowflake | None = None, around: Snowflake | None = None) -> list[MessageModel]:
        """Fetches this channel's messages.

        !!! important "Permissions"
            Requires `VIEW_CHANNEL` and `READ_MESSAGE_HISTORY`

        Args:
            limit (int, optional): Max number of messages to return. Range 1 - 100. Defaults to `50`.
            before (Snowflake, optional): get messages before this message ID
            after (Snowflake, optional): get messages after this message ID
            around (Snowflake, optional): get messages around this message ID

        Returns:
            (list[MessageModel]): queried list of messages
        """
        params = {
            "limit": limit,
            "before": before,
            "after": after,
            "around": around
        }

        data = await self.http.request_list('GET', f'/channels/{self.id}/messages', params=params)

        return [MessageModel.from_dict(msg) for msg in data]

    async def fetch_pins(self, limit: int = 50, before: str | None = None) -> list[PinnedMessageModel]:
        """Get this channel's pinned messages.

        !!! important "Permissions"
            Requires `VIEW_CHANNEL` and `READ_MESSAGE_HISTORY`
            
        !!! warning
            Does not work on a `GUILD_FORUM` channel!

        Args:
            limit (int, optional): Max number of pinned messages to return. Range 1 - 50. Defaults to `50`.
            before (str, optional): get pinned messages before this ISO8601 timestamp
        
        Returns:
            (list[PinnedMessageModel]): queried list of pinned messages
        """
        # Set default limit if user didn't supply one
        params = {
            "limit": limit,
            "before": before
        }

        data = await self.http.request_list('GET', f'/channels/{self.id}/pins', params=params)

        return [PinnedMessageModel.from_dict(item) for item in data]

    async def send(self, message: str | MessagePart) -> MessageModel:
        """Send a message to this channel.
        Fires [`MessageCreateEvent`][scurrypy.events.message_events.MessageCreateEvent].

        !!! important "Permissions"
            Requires `SEND_MESSAGES` if in a guild channel.

            Requires `READ_MESSAGE_HISTORY` of replying to another message.

        Args:
            message (str | MessagePart): content as a string or MessagePart

        Returns:
            (MessageModel): created message
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

        return MessageModel.from_dict(data)
    
    async def bulk_delete_messages(self, message_ids: list[Snowflake]) -> None:
        """Delete multiple messages in a single request.
        Fires [`BulkMessageDeleteEvent`][scurrypy.events.message_events.BulkMessageDeleteEvent].
        
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
            data={'messages': message_ids}
        )

    # --- INVITES ---
    async def fetch_invites(self) -> list[InviteWithMetadataModel]:
        """Fetch a list of invites for this channel.

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS`

        !!! note
            Only usable on guild channels.

        Returns:
            list[InviteWithMetadataModel]: queried list of invites
        """
        data = await self.http.request_list('GET', f'/channels/{self.id}/invites')

        return [InviteWithMetadataModel.from_dict(i) for i in data]

    async def create_invite(self, invite: InvitePart) -> InviteModel:
        """Create a new invite for this channel.
        Fires [`InviteCreateEvent`][scurrypy.events.invite_events.InviteCreateEvent].

        !!! important "Permissions"
            Requires `CREATE_INSTANT_INVITE`

        !!! note
            Only usable for guild channels.

        Args:
            invite (InvitePart): invite to create

        Returns:
            (InviteModel): created invite object 
        """
        data = await self.http.request_json('POST', f'/channels/{self.id}/invites', data=invite.to_dict())

        return InviteModel.from_dict(data)

    # --- THREAD CHANNELS ---
    async def fetch_thread_member(self, user_id: Snowflake, with_member: bool = False) -> ThreadMemberModel:
        """Fetch a thread member of the specified user ID from this thread.

        Args:
            user_id (Snowflake): ID of the user to fetch
            with_member (bool, optional): whether to include the member object. Defaults to `False`.
        
        Returns:
            (ThreadMemberModel): queried thread member
        """

        params = { 'with_member': with_member }

        data = await self.http.request_json('GET', f'/channels/{self.id}/thread-members/{user_id}', params=params)

        return ThreadMemberModel.from_dict(data)
    
    async def fetch_thread_members(self, limit: int = 100, after: Snowflake | None = None, with_member: bool = False) -> list[ThreadMemberModel]:
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
            (list[ThreadMemberModel]): queried list of thread members
        """

        params = {
            'with_member': with_member,
            'after': after,
            'limit': limit
        }

        data = await self.http.request_list('GET', f"/channels/{self.id}/thread-members", params=params)

        return [ThreadMemberModel.from_dict(n) for n in data]

    async def create_thread_from_message(self, message_id: Snowflake, thread: ThreadFromMessagePart) -> ChannelModel:
        """Create a thread from a message (attached to the message). 
        Fires [`ThreadCreateEvent`][scurrypy.events.thread_events.ThreadCreateEvent] 
        and [`MessageUpdateEvent`][scurrypy.events.message_events.MessageUpdateEvent].

        !!! note
            Creates a `PUBLIC_THREAD` when created in a `GUILD_TEXT` channel.

            Creates a `ANNOUNCEMENT_THREAD` when created in a `GUILD_ANNOUNCEMENT` channel

        Args:
            message_id (Snowflake): ID of the message to attach the thread
            thread (ThreadFromMessagePart): thread to attach

        Returns:
            (ChannelModel): new thread
        """

        data = await self.http.request_json('POST', f"/channels/{self.id}/messages/{message_id}/threads", data=thread.to_dict())

        return ChannelModel.from_dict(data)

    async def create_thread_without_message(self, thread: ThreadWithoutMessagePart) -> ChannelModel:
        """Create a thread not connected to an existing message.
        Fires [`ThreadCreateEvent`][scurrypy.events.thread_events.ThreadCreateEvent].

        Args:
            thread (ThreadWithoutMessagePart): thread to create

        Returns:
            (ChannelModel): new thread
        """

        data = await self.http.request_json('POST', f'/channels/{self.id}/threads', data=thread.to_dict())

        return ChannelModel.from_dict(data)

    async def edit_thread(self, **options: Unpack[EditThreadChannelParams]) -> ChannelModel:
        """Edit this thread. 
        Fires [`ChannelUpdateEvent`][scurrypy.events.channel_events.ChannelUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_THREADS`

        !!! important
            Requires `archived` be `False` or set to `False`.

        Args:
            options (EditThreadChannelParams): channel fields to edit

        Returns:
            (ChannelModel): updated channel
        """

        opts = dict(options)

        data = await self.http.request_json('PATCH', f'/channels/{self.id}', data=opts)

        return ChannelModel.from_dict(data)

    async def join_thread(self) -> None:
        """Add the bot to this thread.
        Fires [`ThreadMembersUpdateEvent`][scurrypy.events.thread_events.ThreadMembersUpdateEvent] 
        and [`ThreadCreateEvent`][scurrypy.events.thread_events.ThreadCreateEvent].

        !!! important
            Requires the thread is NOT archived.
        """
        await self.http.request('PUT', f'/channels/{self.id}/thread-members/@me')

    async def leave_thread(self) -> None:
        """Remove the bot from a thread.
        Fires [`ThreadMembersUpdateEvent`][scurrypy.events.thread_events.ThreadMembersUpdateEvent].

        !!! important
            Requires the thread is NOT archived.
        """
        await self.http.request('DELETE', f'/channels/{self.id}/thread-members/@me')

    async def add_thread_member(self, user_id: Snowflake) -> None:
        """Add a user to this thread.
        Fires [`ThreadMembersUpdateEvent`][scurrypy.events.thread_events.ThreadMembersUpdateEvent].

        !!! important
            Requires the thread is NOT archived.

        Args:
            user_id (Snowflake): ID of the user to add
        """
        await self.http.request('PUT', f'/channels/{self.id}/thread-members/{user_id}')

    async def remove_thread_member(self, user_id: Snowflake) -> None:
        """Remove a user to this thread.
        Fires [`ThreadMembersUpdateEvent`][scurrypy.events.thread_events.ThreadMembersUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_THREADS` or thread creator if `PRIVATE_THREAD`

        !!! important
            Requires the thread is NOT archived.

        Args:
            user_id (Snowflake): ID of the user to remove
        """
        await self.http.request('DELETE', f'/channels/{self.id}/thread-members/{user_id}')

    async def fetch_public_archived_threads(self, before: str | None = None, limit: int | None = None) -> ArchivedThreadsModel:
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
            (ArchivedThreadsModel): queried public archived threads
        """
        data = await self.http.request_json(
            'GET', 
            f'/channels/{self.id}/threads/archived/public', 
            params={
                'before': before, 
                'limit': limit
            }
        )

        return ArchivedThreadsModel.from_dict(data)
    
    async def fetch_private_archived_threads(self, before: str | None = None, limit: int | None = None) -> ArchivedThreadsModel:
        """Fetch archived private threads in this channel.

        !!! important "Permissions"
            Requires `READ_MESSAGE_HISTORY` and `MANAGE_THREADS`

        !!! note
            Threads are ordered by `archive_timestamp` in descending order.

        Args:
            before (str, optional): threads archived before this timestamp
            limit (int, optional): max numer of threads to fetch

        Returns:
            (ArchivedThreadsModel): queried private archived threads
        """
        data = await self.http.request_json(
            'GET', 
            f'/channels/{self.id}/threads/archived/private', 
            params={
                'before': before, 
                'limit': limit
            }
        )

        return ArchivedThreadsModel.from_dict(data)
    
    async def fetch_joined_private_archived_threads(self, before: str | None = None, limit: int | None = None) -> ArchivedThreadsModel:
        """Fetch archived private threads in this channel the bot has joined.

        !!! important "Permissions"
            Requires `READ_MESSAGE_HISTORY`

        !!! note
            Threads are ordered by their `id` in descending order.

        Args:
            before (str, optional): threads archived before this timestamp
            limit (int, optional): max numer of threads to fetch

        Returns:
            (ArchivedThreadsModel): queried private archived threads
        """
        data = await self.http.request_json(
            'GET', 
            f'/channels/{self.id}/users/@me/threads/archived/private', 
            params={
                'before': before, 
                'limit': limit
            }
        )

        return ArchivedThreadsModel.from_dict(data)
