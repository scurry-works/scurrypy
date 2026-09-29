from scurrypy import Client, Addon, Intents
from scurrypy.core import Snowflake, MissingIntents, MissingField
from scurrypy.enums import EventType
from scurrypy.api import EmojiModel
from scurrypy.events import GuildCreateEvent, GuildDeleteEvent, GuildEmojisUpdateEvent

class GuildEmojiCacheAddon(Addon):
    """Defines caching guild emojis and lookup.
    
    !!! important
        This cache requires `Intents.GUILD_EXPRESSIONS` to keep up-to-date.
    """

    def __init__(self, client: Client):
        self.bot = client

        if not Intents.GUILD_EXPRESSIONS in client.intents:
            raise MissingIntents("GuildEmojiCache requires Intents.GUILD_EXPRESSIONS for GUILD_EMOJIS_UPDATE event.")

        self.guild_emojis: dict[Snowflake, dict[Snowflake, EmojiModel]] = {}  # owns emoji objects
        self.guild_emoji_index: dict[Snowflake, EmojiModel] = {}        # index by ID (reference)

        client.add_event_listener(EventType.GUILD_CREATE, self.on_guild_create)
        client.add_event_listener(EventType.GUILD_DELETE, self.on_guild_delete)

        client.add_event_listener(EventType.GUILD_EMOJIS_UPDATE, self.on_emojis_update)

    async def on_guild_create(self, event: GuildCreateEvent) -> None:
        """Append new guild emojis to cache. Also add emojis to index.

        Raises:
            (MissingField): missing emoji ID

        Args:
            event (GuildCreateEvent): the GUILD_CREATE event
        """
        guild_dict = self.guild_emojis.setdefault(event.id, {})

        # event.emojis is already hydrated
        for emoji in event.emojis:
            if emoji.id is None:
                raise MissingField("Guild emoji missing ID")
            
            guild_dict[emoji.id] = emoji
            self.guild_emoji_index[emoji.id] = emoji

    async def on_guild_delete(self, event: GuildDeleteEvent) -> None:
        """Remove guild emojis from cache. Also remove emojis from index

        Raises:
            (MissingField): missing emoji ID

        Args:
            event (GuildDeleteEvent): the GUILD_DELETE event
        """
        removed = self.guild_emojis.pop(event.id, {})

        for emoji in removed.values():
            if emoji.id is None:
                raise MissingField("Guild emoji missing ID")
            self.guild_emoji_index.pop(emoji.id, None)

    async def on_emojis_update(self, event: GuildEmojisUpdateEvent) -> None:
        """Refresh guild emojis with new list. Also refresh the index

        Raises:
            (MissingField): missing emoji ID

        Args:
            event (GuildEmojisUpdateEvent): the GUILD_EMOJIS_UPDATE event
        """
        guild_id = event.guild_id

        # remove old emojis
        removed = self.guild_emojis.pop(guild_id, {})

        for emoji in removed.values():
            if emoji.id is None:
                raise MissingField("Guild emoji missing ID")
            self.guild_emoji_index.pop(emoji.id, None)

        # add new emoji set (full replacement)
        guild_dict = self.guild_emojis.setdefault(guild_id, {})

        for emoji in event.emojis:
            if emoji.id is None:
                raise MissingField("Guild emoji missing ID")
            guild_dict[emoji.id] = emoji
            self.guild_emoji_index[emoji.id] = emoji

    def get_emoji(self, emoji_id: Snowflake) -> EmojiModel | None:
        """Get an emoji from the cache.

        Args:
            emoji_id (Snowflake): ID of the emoji

        Returns:
            (EmojiModel | None): the Emoji object if found, else None
        """
        return self.guild_emoji_index.get(emoji_id, None)
    