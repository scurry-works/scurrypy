from dataclasses import dataclass

from .base_resource import BaseResource

from ..models.emoji import EmojiModel

@dataclass
class GuildEmoji(BaseResource):
    """Represents a Discord Guild Emoji."""

    guild_id: int
    """Guild ID of the emojis."""

    async def fetch(self, emoji_id: int):
        """Fetch an emoji from a guild.

        Args:
            emoji_id (int): emoji ID

        Returns:
            (EmojiModel): the Emoji object
        """
        data = await self._http.request("GET", f"/guilds/{self.guild_id}/emojis/{emoji_id}")

        return EmojiModel.from_dict(data)
    
    async def fetch_all(self):
        """Fetch all emojis from a guild.

        Returns:
            (list[EmojiModel]): queried guild emojis
        """
        data = await self._http.request("GET", f"/guilds/{self.guild_id}/emojis")

        return [EmojiModel.from_dict(emoji) for emoji in data]
