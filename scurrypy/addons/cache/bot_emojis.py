from ..addon import Addon
from ...client import Client

from ...models import *
from ...events import *

class BotEmojisCacheAddon(Addon):
    """Defines caching bot emojis and lookup."""

    def __init__(self, client: Client):
        self.bot = client
        self.emojis: dict[str, EmojiModel] = {}   # index by unique name
        client.addons.add(self)

    def setup(self):
        self.bot.add_startup_hook(self.load_bot_emojis)

    async def load_bot_emojis(self):
        """Fetch all bot's emojis and add them to the cache."""
        emojis = await self.bot.bot_emoji().fetch_all()

        for emoji in emojis:
            self.emojis[emoji.name] = emoji

    def get_emoji(self, name: str):
        """Get an emoji from the cache.

        Args:
            name (str): name of the emoji

        Returns:
            (EmojiModel | None): the emoji object if found else None
        """
        return self.emojis.get(name)
