from dataclasses import dataclass

from .base_resource import BaseResource

from ..models.emoji import EmojiModel

from ..parts.image_data import ImageData

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
    
    async def create(self, emoji_name: str, image: ImageData):
        """Add an emoji to the bot emoji repository.

        Args:
            emoji_name (str): name of the emoji
            image (ImageData): image data of the emoji

        Returns:
            (EmojiModel): the new Emoji object
        """
        content = {
            'name': emoji_name,
            'image': image.uri
        }

        data = await self._http.request(
            'POST', 
            f'/applications/{self.application_id}/emojis',
            data=content
        )
    
        return EmojiModel.from_dict(data)
    
    async def modify(self, emoji_id: int, new_name: str):
        """Modify an emoji in the bot repository.

        !!! note
            `name` is the only field that can be edited, so no object is passed.

        Args:
            emoji_id (int): ID of the emoji to modify
            new_name (str): new name for the emoji

        Returns:
            (EmojiModel): the updated emoji
        """
        data = await self._http.request(
            'PATCH', 
            f'/applications/{self.application_id}/emojis/{emoji_id}', 
            data={'name': new_name}
        )

        return EmojiModel.from_dict(data)

    async def delete(self, emoji_id: int):
        """Deletes an emoji from the bot repository.

        Args:
            emoji_id (int): ID of the emoji to remove
        """
        await self._http.request('DELETE', f'/applications/{self.application_id}/emojis/{emoji_id}')
