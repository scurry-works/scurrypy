from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..core.snowflake import Snowflake

from ..api.emoji import EmojiModel, ApplicationEmojiPart, GuildEmojiPart

from ..params.emoji import EditApplicationEmojiParams, EditGuildEmojiParams

@dataclass
class ApplicationEmoji(BaseResource):
    """Represents a Discord Bot Emoji."""

    application_id: Snowflake
    """Application ID of the emojis."""

    async def fetch(self, emoji_id: Snowflake) -> EmojiModel:
        """Fetch an emoji from the bot repository.

        Args:
            emoji_id (Snowflake): emoji ID

        Returns:
            (EmojiModel): queried emoji
        """
        data = await self.http.request_json("GET", f"/applications/{self.application_id}/emojis/{emoji_id}")

        return EmojiModel.from_dict(data)
    
    async def fetch_all(self) -> list[EmojiModel]:
        """Fetch all emojis from the bot repository.

        Returns:
            (list[EmojiModel]): queried list of bot emojis
        """
        data = await self.http.request_json("GET", f"/applications/{self.application_id}/emojis")
        emojis = data.get("items")
        
        assert isinstance(emojis, list)
        return [EmojiModel.from_dict(emoji) for emoji in emojis]
    
    async def create(self, emoji: ApplicationEmojiPart) -> EmojiModel:
        """Add an emoji to the bot emoji repository.

        Args:
            emoji (ApplicationEmojiPart): bot emoji fields

        Returns:
            (EmojiModel): new emoji
        """
        data = await self.http.request_json(
            'POST', 
            f'/applications/{self.application_id}/emojis',
            data=emoji.to_dict()
        )
    
        return EmojiModel.from_dict(data)
    
    async def edit(self, emoji_id: Snowflake, **options: Unpack[EditApplicationEmojiParams]) -> EmojiModel:
        """Edit an emoji in the bot repository.

        Args:
            emoji_id (Snowflake): ID of the emoji
            options (EditBotEmojiParams): fields to edit the emoji

        Returns:
            (EmojiModel): updated emoji
        """
        opts = dict(options)

        data = await self.http.request_json(
            'PATCH', 
            f'/applications/{self.application_id}/emojis/{emoji_id}', 
            data=opts
        )

        return EmojiModel.from_dict(data)

    async def delete(self, emoji_id: Snowflake) -> None:
        """Deletes an emoji from the bot repository.

        Args:
            emoji_id (int): ID of the emoji to remove
        """
        await self.http.request('DELETE', f'/applications/{self.application_id}/emojis/{emoji_id}')

@dataclass
class GuildEmoji(BaseResource):
    """Represents a Discord Guild Emoji."""

    guild_id: Snowflake
    """Guild ID of the emojis."""

    async def fetch(self, emoji_id: Snowflake) -> EmojiModel:
        """Fetch an emoji from this guild.

        Args:
            emoji_id (Snowflake): emoji ID

        Returns:
            (EmojiModel): queried guild emoji
        """
        data = await self.http.request_json("GET", f"/guilds/{self.guild_id}/emojis/{emoji_id}")

        return EmojiModel.from_dict(data)
    
    async def fetch_all(self) -> list[EmojiModel]:
        """Fetch all emojis from this guild.

        Returns:
            (list[EmojiModel]): queried list of guild emojis
        """
        data = await self.http.request_list("GET", f"/guilds/{self.guild_id}/emojis")

        return [EmojiModel.from_dict(emoji) for emoji in data]

    async def create(self, emoji: GuildEmojiPart) -> EmojiModel:
        """Create a new emoji for this guild.
        Fires [`GuildEmojisUpdateEvent`][scurrypy.events.guild_events.GuildEmojisUpdateEvent].

        Args:
            emoji (GuildEmojiPart): fields for creating a guild emoji

        Returns:
            (EmojiModel): new emoji
        """
        data = await self.http.request_json(
            'POST', 
            f'/guilds/{self.guild_id}/emojis', 
            data=emoji.to_dict()
        )

        return EmojiModel.from_dict(data)
    
    async def edit(self, emoji_id: Snowflake, **options: Unpack[EditGuildEmojiParams]) -> EmojiModel:
        """Edit a guild emoji in this guild.
        Fires [`GuildEmojisUpdateEvent`][scurrypy.events.guild_events.GuildEmojisUpdateEvent].

        Args:
            emoji_id (Snowflake): ID of the emoji to edit
            options (EditGuildEmojiParams): params for editing a guild's emoji

        Returns:
            (EmojiModel): updated emoji
        """
        opts = dict(options)

        data = await self.http.request_json(
            'PATCH', 
            f'/guilds/{self.guild_id}/emojis/{emoji_id}', 
            data=opts
        )

        return EmojiModel.from_dict(data)

    async def delete(self, emoji_id: Snowflake) -> None:
        """Delete an emoji from this guild.
        Fires [`GuildEmojisUpdateEvent`][scurrypy.events.guild_events.GuildEmojisUpdateEvent].

        !!! important "Permissions"
            * `CREATE_GUILD_EXPRESSIONS` → required if created by the current user (or `MANAGE_GUILD_EXPRESSIONS`)
            * `MANAGE_GUILD_EXPRESSIONS` → required for other emojis

        Args:
            emoji_id (Snowflake): ID of the emoji
        """
        await self.http.request('DELETE', f'/guilds/{self.guild_id}/emojis/{emoji_id}')
