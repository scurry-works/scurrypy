from dataclasses import dataclass
from typing import Unpack

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake

from .base_resource import BaseResource

from ..api import ApplicationEmojiPart, GuildEmojiPart

from ..params import EditApplicationEmojiParams, EditGuildEmojiParams

@dataclass
class ApplicationEmoji(BaseResource):
    """Represents a Discord bot emoji resource."""

    application_id: Snowflake
    """Application ID of the emojis."""

    async def fetch(self, emoji_id: Snowflake) -> JsonQuery:
        """Fetch an emoji from the bot repository.

        Args:
            emoji_id (Snowflake): emoji ID

        Returns:
            (JsonQuery): queried emoji
        """
        data = await self.http.request_json("GET", f"/applications/{self.application_id}/emojis/{emoji_id}")

        return JsonQuery(data)
    
    async def fetch_all(self) -> JsonQuery:
        """Fetch all emojis from the bot repository.

        Returns:
            (JsonQuery): queried list of bot emojis
        """
        data = await self.http.request_json("GET", f"/applications/{self.application_id}/emojis")
        
        return JsonQuery(data)
    
    async def create(self, emoji: ApplicationEmojiPart) -> JsonQuery:
        """Add an emoji to the bot emoji repository.

        Args:
            emoji (ApplicationEmojiPart): bot emoji fields

        Returns:
            (JsonQuery): new emoji
        """
        data = await self.http.request_json(
            'POST', 
            f'/applications/{self.application_id}/emojis',
            data=emoji.to_dict()
        )
    
        return JsonQuery(data)
    
    async def edit(self, emoji_id: Snowflake, **options: Unpack[EditApplicationEmojiParams]) -> JsonQuery:
        """Edit an emoji in the bot repository.

        Args:
            emoji_id (Snowflake): ID of the emoji
            options (EditBotEmojiParams): fields to edit the emoji

        Returns:
            (JsonQuery): updated emoji
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/applications/{self.application_id}/emojis/{emoji_id}', 
            data=dict(options)
        )

        return JsonQuery(data)

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

    async def fetch(self, emoji_id: Snowflake) -> JsonQuery:
        """Fetch an emoji from this guild.

        Args:
            emoji_id (Snowflake): emoji ID

        Returns:
            (JsonQuery): queried guild emoji
        """
        data = await self.http.request_json("GET", f"/guilds/{self.guild_id}/emojis/{emoji_id}")

        return JsonQuery(data)
    
    async def fetch_all(self) -> JsonQuery:
        """Fetch all emojis from this guild.

        Returns:
            (JsonQuery): queried list of guild emojis
        """
        data = await self.http.request_list("GET", f"/guilds/{self.guild_id}/emojis")

        return JsonQuery(data)

    async def create(self, emoji: GuildEmojiPart) -> JsonQuery:
        """Create a new emoji for this guild.
        Fires [**Guild Emojis Update**](https://docs.discord.com/developers/events/gateway-events#guild-emojis-update).

        Args:
            emoji (GuildEmojiPart): fields for creating a guild emoji

        Returns:
            (JsonQuery): new emoji
        """
        data = await self.http.request_json(
            'POST', 
            f'/guilds/{self.guild_id}/emojis', 
            data=emoji.to_dict()
        )

        return JsonQuery(data)
    
    async def edit(self, emoji_id: Snowflake, **options: Unpack[EditGuildEmojiParams]) -> JsonQuery:
        """Edit a guild emoji in this guild.
        Fires [**Guild Emojis Update**](https://docs.discord.com/developers/events/gateway-events#guild-emojis-update).

        Args:
            emoji_id (Snowflake): ID of the emoji to edit
            options (EditGuildEmojiParams): params for editing a guild's emoji

        Returns:
            (JsonQuery): updated emoji
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/guilds/{self.guild_id}/emojis/{emoji_id}', 
            data=dict(options)
        )

        return JsonQuery(data)

    async def delete(self, emoji_id: Snowflake) -> None:
        """Delete an emoji from this guild.
        Fires [**Guild Emojis Update**](https://docs.discord.com/developers/events/gateway-events#guild-emojis-update).

        !!! important "Permissions"
            * `CREATE_GUILD_EXPRESSIONS` → required if created by the current user (or `MANAGE_GUILD_EXPRESSIONS`)
            * `MANAGE_GUILD_EXPRESSIONS` → required for other emojis

        Args:
            emoji_id (Snowflake): ID of the emoji
        """
        await self.http.request('DELETE', f'/guilds/{self.guild_id}/emojis/{emoji_id}')
