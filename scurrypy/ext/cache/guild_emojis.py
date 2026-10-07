from scurrypy import Client, Addon, Intents, JsonQuery
from scurrypy.core import Snowflake, MissingIntents
from scurrypy.enums import EventType

class GuildEmojiCacheAddon(Addon):
    """Defines caching guild emojis and lookup.
    
    !!! important
        This cache requires `Intents.GUILD_EXPRESSIONS` to keep up-to-date.
    """

    def __init__(self, client: Client):
        self.bot = client

        if not Intents.GUILD_EXPRESSIONS in client.intents:
            raise MissingIntents("GuildEmojiCache requires Intents.GUILD_EXPRESSIONS for GUILD_EMOJIS_UPDATE event.")

        self.guild_emojis: dict[Snowflake, dict[Snowflake, JsonQuery]] = {}  # owns emoji objects
        self.guild_emoji_index: dict[Snowflake, JsonQuery] = {}        # index by ID (reference)

        client.add_event_listener(EventType.GUILD_CREATE, self.on_guild_create)
        client.add_event_listener(EventType.GUILD_DELETE, self.on_guild_delete)

        client.add_event_listener(EventType.GUILD_EMOJIS_UPDATE, self.on_emojis_update)

    async def on_guild_create(self, event: JsonQuery) -> None:
        """Append new guild emojis to cache. Also add emojis to index.

        Raises:
            (MissingField): missing emoji ID

        Args:
            event (JsonQuery): the GUILD_CREATE event
        """
        id: Snowflake = event.get('id', t=Snowflake).value
        guild_dict = self.guild_emojis.setdefault(id, {})

        for emoji in event.get('emojis').value:
            em = JsonQuery(emoji)
            emoji_id: Snowflake = em.get('id', t=Snowflake).value

            guild_dict[emoji_id] = em
            self.guild_emoji_index[emoji_id] = em

    async def on_guild_delete(self, event: JsonQuery) -> None:
        """Remove guild emojis from cache. Also remove emojis from index

        Raises:
            (MissingField): missing emoji ID

        Args:
            event (JsonQuery): the GUILD_DELETE event
        """
        id: Snowflake = event.get('id', t=Snowflake).value
        removed = self.guild_emojis.pop(id, {})

        for emoji in removed.values():
            emoji_id: Snowflake = emoji.get('id', t=Snowflake).value
            self.guild_emoji_index.pop(emoji_id, None)

    async def on_emojis_update(self, event: JsonQuery) -> None:
        """Refresh guild emojis with new list. Also refresh the index

        Raises:
            (MissingField): missing emoji ID

        Args:
            event (JsonQuery): the GUILD_EMOJIS_UPDATE event
        """
        guild_id: Snowflake = event.get('guild_id', t=Snowflake).value

        # remove old emojis
        removed = self.guild_emojis.pop(guild_id, {})

        for emoji in removed.values():
            emoji_id: Snowflake = emoji.get('id', t=Snowflake).value
            self.guild_emoji_index.pop(emoji_id, None)

        # add new emoji set (full replacement)
        guild_dict = self.guild_emojis.setdefault(guild_id, {})

        for emoji in event.get('emojis').value:
            em = JsonQuery(emoji)
            emoji_id = em.get('id', t=Snowflake).value
            
            guild_dict[emoji_id] = em
            self.guild_emoji_index[emoji_id] = em

    def get_emoji(self, emoji_id: Snowflake) -> JsonQuery | None:
        """Get an emoji from the cache.

        Args:
            emoji_id (Snowflake): ID of the emoji

        Returns:
            (JsonQuery | None): the Emoji object if found, else None
        """
        return self.guild_emoji_index.get(emoji_id, None)
