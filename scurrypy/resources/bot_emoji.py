from dataclasses import dataclass

from .base_resource import BaseResource

from ..models.emoji import EmojiModel

@dataclass
class BotEmoji(BaseResource):
    """Represents a Discord Bot Emoji."""

    application_id: int
    """Application ID of the emojis."""

    async def fetch(self, emoji_id: int):
        """Fetch an emoji from the bot repository.

        Args:
            emoji_id (int): emoji ID

        Returns:
            (EmojiModel): the Emoji object
        """
        data = await self._http.request("GET", f"/applications/{self.application_id}/emojis/{emoji_id}")

        return EmojiModel.from_dict(data)
    
    async def fetch_all(self):
        """Fetch all emojis from the bot repository.

        Returns:
            (list[EmojiModel]): queried bot emojis
        """
        data = await self._http.request("GET", f"/applications/{self.application_id}/emojis")

        emojis = data.get("items")

        return [EmojiModel.from_dict(emoji) for emoji in emojis]
