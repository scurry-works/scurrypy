from ..addon import Addon
from ...client import Client

from ...models import *
from ...events import *

class GuildChannelCacheAddon(Addon):
    """Defines caching channels and lookup."""

    def __init__(self, client: Client):
        self.bot = client

        self.channels: dict[int, dict[int, ChannelModel]] = {}  # stores OBJECTS
        self.channel_index: dict[int, ChannelModel] = {}        # stores REFERENCES

        client.addons.add(self)

    def setup(self):
        self.bot.add_startup_hook(self.on_startup)

    def on_startup(self):
        self.bot.add_event_listener('GUILD_CREATE', self.on_guild_create)
        self.bot.add_event_listener('GUILD_DELETE', self.on_guild_delete)

        self.bot.add_event_listener('CHANNEL_CREATE', self.on_channel_create)
        self.bot.add_event_listener('CHANNEL_UPDATE', self.on_channel_update)
        self.bot.add_event_listener('CHANNEL_DELETE', self.on_channel_delete)

    def on_guild_create(self, event: GuildCreateEvent):
        """Append new guild channels to cache. Also add channels to index.

        Args:
            event (GuildCreateEvent): the GUILD_CREATE event
        """
        guild_dict = self.channels.setdefault(event.id, {})

        for ch in event.channels:
            guild_dict[ch.id] = ch
            self.channel_index[ch.id] = ch

    def on_guild_delete(self, event: GuildDeleteEvent):
        """Remove guild channels from cache. Also remove channels from index

        Args:
            event (GuildDeleteEvent): the GUILD_DELETE event
        """
        removed_channels = self.channels.pop(event.id, {})

        for ch in removed_channels.values():
            self.channel_index.pop(ch.id, None)

    def on_channel_create(self, event: GuildChannelCreateEvent):
        """Append channel to guild key. Also append channel to index.

        Args:
            event (GuildChannelCreateEvent): the CHANNEL_CREATE event
        """
        model = ChannelModel.from_dict(event.raw)
        guild_dict = self.channels.setdefault(event.guild_id, {})

        guild_dict[event.id] = model
        self.channel_index[event.id] = model

    def on_channel_update(self, event: GuildChannelUpdateEvent):
        """Replace channel in guild key. Also replace channel in index.

        Args:
            event (GuildChannelUpdateEvent): the CHANNEL_UPDATE event
        """
        model = ChannelModel.from_dict(event.raw)
        guild_dict = self.channels.setdefault(event.guild_id, {})

        guild_dict[event.id] = model
        self.channel_index[event.id] = model

    def on_channel_delete(self, event: GuildChannelDeleteEvent):
        """Remove channel from guild key. Also remove channel from index.

        Args:
            event (GuildChannelDeleteEvent): the CHANNEL_DELETE event
        """
        model = self.channel_index.pop(event.id, None)
        if model:
            self.channels.get(event.guild_id, {}).pop(event.id, None)

    def get_channel(self, channel_id: int):
        """Get a channel from the cache.

        Args:
            channel_id (int): ID of the channel

        Returns:
            (ChannelModel | None): the channel object if found else None
        """
        return self.channel_index.get(channel_id)

    def put(self, channel: ChannelModel):
        """Put a new channel into the cache.

        Args:
            channel (ChannelModel): the channel object

        Raises:
            ValueError: missing `guild_id`
        """
        if channel.guild_id is None:
            raise ValueError("Cannot cache a channel without a guild_id.")
        
        guild_dict = self.channels.setdefault(channel.guild_id, {})
        guild_dict[channel.id] = channel
        self.channel_index[channel.id] = channel
