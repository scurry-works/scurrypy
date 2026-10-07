from scurrypy import Client, Addon, JsonQuery
from scurrypy.enums import EventType
from scurrypy.core import Snowflake, DiscordError, MissingField

class GuildChannelCacheAddon(Addon):
    """Defines caching channels and lookup."""

    def __init__(self, client: Client):
        self.bot = client

        self.channels: dict[Snowflake, dict[Snowflake, JsonQuery]] = {}  # stores OBJECTS
        self.channel_index: dict[Snowflake, JsonQuery] = {}  # stores REFERENCES

        client.add_event_listener(EventType.GUILD_CREATE, self.on_guild_create)
        client.add_event_listener(EventType.GUILD_DELETE, self.on_guild_delete)

        client.add_event_listener(EventType.CHANNEL_CREATE, self.on_channel_create)
        client.add_event_listener(EventType.CHANNEL_UPDATE, self.on_channel_update)
        client.add_event_listener(EventType.CHANNEL_DELETE, self.on_channel_delete)

    async def on_guild_create(self, event: JsonQuery) -> None:
        """Append new guild channels to cache. Also add channels to index.

        Args:
            event (JsonQuery): the GUILD_CREATE event
        """
        id: Snowflake = event.get('id', t=Snowflake).value
        guild_dict = self.channels.setdefault(id, {})

        for ch in event.get('channels').value:
            channel = JsonQuery(ch)
            channel_id = channel.get('id', t=Snowflake).value

            guild_dict[channel_id] = channel
            self.channel_index[channel_id] = channel

    async def on_guild_delete(self, event: JsonQuery) -> None:
        """Remove guild channels from cache. Also remove channels from index

        Args:
            event (JsonQuery): the GUILD_DELETE event
        """
        id: Snowflake = event.get('id', t=Snowflake).value
        removed_channels = self.channels.pop(id, {})

        for ch in removed_channels.values():
            channel_id = ch.get('id', t=Snowflake).value
            self.channel_index.pop(channel_id, None)

    async def on_channel_create(self, event: JsonQuery) -> None:
        """Append channel to guild key. Also append channel to index.

        Raises:
            (MissingField): no associated guild ID

        Args:
            event (JsonQuery): the CHANNEL_CREATE event
        """
        guild_id: Snowflake = event.get('guild_id', t=Snowflake).value
        if guild_id is None:
            raise MissingField("This event has no associated guild ID.")
        
        id: Snowflake = event.get('id', t=Snowflake).value
        guild_dict = self.channels.setdefault(guild_id, {})

        guild_dict[id] = event
        self.channel_index[id] = event

    async def on_channel_update(self, event: JsonQuery) -> None:
        """Replace channel in guild key. Also replace channel in index.

        Raises:
            (MissingField): no associated guild ID

        Args:
            event (JsonQuery): the CHANNEL_UPDATE event
        """
        guild_id: Snowflake = event.get('guild_id', t=Snowflake).value
        if guild_id is None:
            raise MissingField("This event has no associated guild ID.")

        id: Snowflake = event.get('id', t=Snowflake).value
        guild_dict = self.channels.setdefault(guild_id, {})

        guild_dict[id] = event
        self.channel_index[id] = event

    async def on_channel_delete(self, event: JsonQuery) -> None:
        """Remove channel from guild key. Also remove channel from index.

        Raises:
            (MissingField): no associated guild ID

        Args:
            event (JsonQuery): the CHANNEL_DELETE event
        """
        guild_id: Snowflake = event.get('guild_id', t=Snowflake).value
        if guild_id is None:
            raise MissingField("This event has no associated guild ID.")

        id: Snowflake = event.get('id', t=Snowflake).value
        data = self.channel_index.pop(id, None)
        if data is not None:
            self.channels.get(guild_id, {}).pop(id, None)

    async def get_channel(self, channel_id: Snowflake) -> JsonQuery | None:
        """Fetch a guild channel. If not found, request and store it.

        Args:
            channel_id (Snowflake): ID of channel

        Returns:
            (JsonQuery | None): hydrated channel object or None if fetch failed
        """
        channel = self.channel_index.get(channel_id)
        if channel is not None:
            return channel

        try:
            channel = await self.bot.channel(channel_id).fetch()
        except DiscordError:
            return None

        self.put(channel)

        return channel

    def put(self, channel: JsonQuery) -> None:
        """Put a new channel into the cache.

        Args:
            channel (JsonQuery): the channel object

        Raises:
            (MissingField): no associated guild ID
        """
        guild_id: Snowflake = channel.get('guild_id', t=Snowflake).value
        if guild_id is None:
            raise MissingField("Cannot cache a channel without a guild_id.")

        guild_dict = self.channels.setdefault(guild_id, {})

        channel_id: Snowflake = channel.get('id', t=Snowflake).value
        guild_dict[channel_id] = channel
        self.channel_index[channel_id] = channel
