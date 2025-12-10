from ..addon import Addon
from ...client import Client
from ...core.intents import Intents

from ...models import *
from ...events import *

class GuildEmojiCacheAddon(Addon):
    """Defines caching guild emojis and lookup.
    
    !!! important
        This cache requires `Intents.GUILD_EMOJIS_AND_STICKERS` to keep up-to-date.
    """

    def __init__(self, client: Client):
        self.bot = client

        if not Intents.has(client.intents, Intents.GUILD_EMOJIS_AND_STICKERS):
            raise ValueError("GuildEmojiCache requires Intents.GUILD_EMOJIS_AND_STICKERS for GUILD_EMOJIS_UPDATE event.")

        self.guild_emojis: dict[int, dict[int, EmojiModel]] = {}  # owns emoji objects
        self.guild_emoji_index: dict[int, EmojiModel] = {}        # index by ID (reference)

        client.addons.add(self)

    def setup(self):
        self.bot.add_startup_hook(self.on_startup)

    def on_startup(self):
        self.bot.add_event_listener('GUILD_CREATE', self.on_guild_create)
        self.bot.add_event_listener('GUILD_DELETE', self.on_guild_delete)

        self.bot.add_event_listener('GUILD_EMOJIS_UPDATE', self.on_emojis_update)

    def on_guild_create(self, event: GuildCreateEvent):
        """Append new guild emojis to cache. Also add emojis to index.

        Args:
            event (GuildCreateEvent): the GUILD_CREATE event
        """
        guild_dict = self.guild_emojis.setdefault(event.id, {})

        # event.emojis is already hydrated
        for emoji in event.emojis:
            guild_dict[emoji.id] = emoji
            self.guild_emoji_index[emoji.id] = emoji

    def on_guild_delete(self, event: GuildDeleteEvent):
        """Remove guild emojis from cache. Also remove emojis from index

        Args:
            event (GuildDeleteEvent): the GUILD_DELETE event
        """
        removed = self.guild_emojis.pop(event.id, {})

        for emoji in removed.values():
            self.guild_emoji_index.pop(emoji.id, None)

    def on_emojis_update(self, event: GuildEmojisUpdateEvent):
        """Refresh guild emojis with new list. Also refresh the index

        Args:
            event (GuildEmojisUpdateEvent): the GUILD_EMOJIS_UPDATE event
        """
        guild_id = event.guild_id

        # remove old emojis
        removed = self.guild_emojis.pop(guild_id, {})

        for emoji in removed.values():
            self.guild_emoji_index.pop(emoji.id, None)

        # add new emoji set (full replacement)
        guild_dict = self.guild_emojis.setdefault(guild_id, {})

        for emoji in event.emojis:
            guild_dict[emoji.id] = emoji
            self.guild_emoji_index[emoji.id] = emoji

    def get_emoji(self, emoji_id: int):
        """Get an emoji from the cache.

        Args:
            emoji_id (int): ID of the emoji

        Returns:
            (EmojiModel | None): the Emoji object if found, else None
        """
        return self.guild_emoji_index.get(emoji_id, None)
    