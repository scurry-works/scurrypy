from scurrypy import Client, Addon, JsonQuery
from scurrypy.core import Snowflake

class ApplicationEmojisCacheAddon(Addon):
    """Defines caching bot emojis and lookup."""

    def __init__(self, client: Client, application_id: Snowflake):
        self.bot = client
        self.application_id = application_id

        self.emojis: dict[str, JsonQuery] = {}   # index by unique name

        client.add_startup_hook(self.load_bot_emojis)

    async def load_bot_emojis(self) -> None:
        """Fetch all bot's emojis and add them to the cache.

        Raises:
            (MissingField): missing emoji name
        """
        emojis = await self.bot.application_emoji(self.application_id).fetch_all()

        for emoji in emojis.get('items').value:
            name: str = JsonQuery(emoji).get('name').value
            self.emojis[name] = JsonQuery(emoji)

    def get_emoji(self, name: str) -> JsonQuery | None:
        """Get an emoji from the cache.

        Args:
            name (str): name of the emoji

        Returns:
            (JsonQuery | None): the emoji object if found else None
        """
        return self.emojis.get(name)
