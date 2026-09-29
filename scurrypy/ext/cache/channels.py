from scurrypy import Client, Addon
from scurrypy.enums import EventType
from scurrypy.core import Snowflake, DiscordError, MissingField
from scurrypy.api.channels import ChannelModel
from scurrypy.events import (
    GuildCreateEvent, 
    GuildDeleteEvent, 
    ChannelCreateEvent, 
    ChannelUpdateEvent, 
    ChannelDeleteEvent
)

class GuildChannelCacheAddon(Addon):
    """Defines caching channels and lookup."""

    def __init__(self, client: Client):
        self.bot = client

        self.channels: dict[Snowflake, dict[Snowflake, ChannelModel]] = {}  # stores OBJECTS
        self.channel_index: dict[Snowflake, ChannelModel] = {}  # stores REFERENCES

        client.add_event_listener(EventType.GUILD_CREATE, self.on_guild_create)
        client.add_event_listener(EventType.GUILD_DELETE, self.on_guild_delete)

        client.add_event_listener(EventType.CHANNEL_CREATE, self.on_channel_create)
        client.add_event_listener(EventType.CHANNEL_UPDATE, self.on_channel_update)
        client.add_event_listener(EventType.CHANNEL_DELETE, self.on_channel_delete)

    async def on_guild_create(self, event: GuildCreateEvent) -> None:
        """Append new guild channels to cache. Also add channels to index.

        Args:
            event (GuildCreateEvent): the GUILD_CREATE event
        """
        guild_dict = self.channels.setdefault(event.id, {})

        for ch in event.channels:
            guild_dict[ch.id] = ch
            self.channel_index[ch.id] = ch

    async def on_guild_delete(self, event: GuildDeleteEvent) -> None:
        """Remove guild channels from cache. Also remove channels from index

        Args:
            event (GuildDeleteEvent): the GUILD_DELETE event
        """
        removed_channels = self.channels.pop(event.id, {})

        for ch in removed_channels.values():
            self.channel_index.pop(ch.id, None)

    async def on_channel_create(self, event: ChannelCreateEvent) -> None:
        """Append channel to guild key. Also append channel to index.

        Raises:
            (MissingField): no associated guild ID

        Args:
            event (GuildChannelCreateEvent): the CHANNEL_CREATE event
        """
        if not event.guild_id:
            raise MissingField("This event has no associated guild ID.")
        
        model = ChannelModel.from_dict(event.raw)
        guild_dict = self.channels.setdefault(event.guild_id, {})

        guild_dict[event.id] = model
        self.channel_index[event.id] = model

    async def on_channel_update(self, event: ChannelUpdateEvent) -> None:
        """Replace channel in guild key. Also replace channel in index.

        Raises:
            (MissingField): no associated guild ID

        Args:
            event (GuildChannelUpdateEvent): the CHANNEL_UPDATE event
        """
        if not event.guild_id:
            raise MissingField("This event has no associated guild ID.")

        model = ChannelModel.from_dict(event.raw)
        guild_dict = self.channels.setdefault(event.guild_id, {})

        guild_dict[event.id] = model
        self.channel_index[event.id] = model

    async def on_channel_delete(self, event: ChannelDeleteEvent) -> None:
        """Remove channel from guild key. Also remove channel from index.

        Raises:
            (MissingField): no associated guild ID

        Args:
            event (GuildChannelDeleteEvent): the CHANNEL_DELETE event
        """
        if not event.guild_id:
            raise MissingField("This event has no associated guild ID.")
        
        model = self.channel_index.pop(event.id, None)
        if model:
            self.channels.get(event.guild_id, {}).pop(event.id, None)

    async def get_channel(self, channel_id: Snowflake) -> ChannelModel | None:
        """Fetch a guild channel. If not found, request and store it.

        Args:
            channel_id (Snowflake): ID of channel

        Returns:
            (ChannelModel | None): hydrated channel object or None if fetch failed
        """
        channel = self.channel_index.get(channel_id)
        if channel:
            return channel

        try:
            channel = await self.bot.channel(channel_id).fetch()
        except DiscordError:
            return None

        self.put(channel)

        return channel

    def put(self, channel: ChannelModel) -> None:
        """Put a new channel into the cache.

        Args:
            channel (ChannelModel): the channel object

        Raises:
            (MissingField): no associated guild ID
        """
        if channel.guild_id is None:
            raise MissingField("Cannot cache a channel without a guild_id.")
        
        guild_dict = self.channels.setdefault(channel.guild_id, {})
        guild_dict[channel.id] = channel
        self.channel_index[channel.id] = channel
