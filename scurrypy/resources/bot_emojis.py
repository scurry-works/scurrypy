from ..core.http import HTTPClient
from ..models.emoji import EmojiModel

class BotEmojis:
    """Represents a collection of the bot's emojis."""

    def __init__(self, _http: HTTPClient, application_id: int):

        self._http = _http
        """HTTP session for requests."""

        self.application_id = application_id
        """Bot's application ID."""
        
        self._cache: dict[int, EmojiModel] = {}
        """Cache of bot's repository emojis mapped by id."""

    async def fetch_all(self):
        """Fetches all the bot's emojis from its repository."""
        data = await self._http.request('GET', f'/applications/{self.application_id}/emojis')
        items = data.get('items', [])
        for e in items:
            emoji = EmojiModel.from_dict(e)
            self._cache[emoji.name] = emoji

    async def fetch(self, emoji_id: int):
        """Fetches a single emoji from the bot's repository.

        Args:
            emoji_id (int): the emoji's id

        Returns:
            (EmojiModel):  the new EmojiModel object with all fields populated
        """
        data = await self._http.request("GET", f"/applications/{self.application_id}/emojis/{emoji_id}")
        emoji = EmojiModel.from_dict(data)
        self._cache[emoji.id] = emoji # also add it to the cache
        return emoji

    def get_emoji(self, name: str) -> EmojiModel:
        """Get an emoji from this resource's cache by name.

        Args:
            name (str): name of the emoji

        Returns:
            (EmojiModel): the new EmojiModel object with all fields populated
        """
        return self._cache.get(name, EmojiModel('❓'))
