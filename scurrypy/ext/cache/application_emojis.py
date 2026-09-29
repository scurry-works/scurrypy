from scurrypy import Client, Addon
from scurrypy.core import Snowflake, MissingField
from scurrypy.api import EmojiModel

class ApplicationEmojisCacheAddon(Addon):
    """Defines caching bot emojis and lookup."""

    def __init__(self, client: Client, application_id: Snowflake):
        self.bot = client
        self.application_id = application_id

        self.emojis: dict[str, EmojiModel] = {}   # index by unique name

        client.add_startup_hook(self.load_bot_emojis)

    async def load_bot_emojis(self) -> None:
        """Fetch all bot's emojis and add them to the cache.

        Raises:
            (MissingField): missing emoji name
        """
        emojis = await self.bot.application_emoji(self.application_id).fetch_all()

        for emoji in emojis:
            if emoji.name is None:
                raise MissingField("Missing emoji name")
            self.emojis[emoji.name] = emoji

    def get_emoji(self, name: str) -> EmojiModel | None:
        """Get an emoji from the cache.

        Args:
            name (str): name of the emoji

        Returns:
            (EmojiModel | None): the emoji object if found else None
        """
        return self.emojis.get(name)
