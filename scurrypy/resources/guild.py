from dataclasses import dataclass
from typing import Unpack

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake
from ..core.part import serialize

from .base_resource import BaseResource

from ..bases import GuildChannelCreate

from ..api.guilds import (
    BulkGuildBanPart, 
    GuildRolePart
)
from ..api.channels import (
    GuildTextChannelPart, 
    GuildAnnouncementChannelPart, 
    GuildForumChannelPart, 
)
from ..api.image_data import ImageAssetPart
from ..api.sticker import StickerPart

from ..params import (
    EditGuildRoleParams, 
    EditGuildParams, 
    EditGuildWelcomeScreenParams, 
    EditOnboardingParams, 
    EditGuildStickerParams,
    EditGuildMemberParams
)

@dataclass
class Guild(BaseResource):
    """Represents a Discord guild resource."""
    
    id: Snowflake
    """ID of the guild."""

    # GUILD
    async def fetch(self, with_counts: bool = False) -> JsonQuery:
        """Fetch the Guild object by the given ID.

        Args:
            with_counts (bool, optional): return the approximate member and presence counts for the guild. Defaults to `False`.

        Returns:
            (JsonQuery): queried guild
        """
        data = await self.http.request_json(
            'GET', 
            f'/guilds/{self.id}', 
            params={
                'with_counts': with_counts
            }
        )

        return JsonQuery(data)

    async def edit(self, **options: Unpack[EditGuildParams]) -> JsonQuery:
        """Edit this guild.

        Fires [**Guild Update**](https://docs.discord.com/developers/events/gateway-events#guild-update).

        Args:
            options (EditGuildParams): guild with fields to edit

        Returns:
            (JsonQuery): edited guild
        """
        data = await self.http.request_json(
            'PATCH',
            f'/guilds/{self.id}', 
            data=serialize(dict(options)) # nested objects in EditGuildParams
        )

        return JsonQuery(data)

    # --- CHANNELS ---
    async def fetch_channels(self) -> JsonQuery:
        """Fetch this guild's channels.

        !!! note
            Does not include threads!

        Returns:
            (JsonQuery): queried list of the guild's channels
        """
        data = await self.http.request_list('GET', f'guilds/{self.id}/channels')

        return JsonQuery(data)
    
    async def fetch_active_threads(self) -> JsonQuery:
        """Fetch all active threads in a guild (private and public).

        !!! note
            Threads are ordered by their ID in descending order.

        Returns:
            (JsonQuery): active guild threads
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/threads/active')

        return JsonQuery(data)

    async def create_channel(self, channel: GuildChannelCreate) -> JsonQuery:
        """Create a channel in this guild.
        
        Fires [**Channel Create**](https://docs.discord.com/developers/events/gateway-events#channel-create).

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS`

        Args:
            channel (GuildChannelCreate): the guild channel to create

        Returns:
            (JsonQuery): created channel
        """
        assert isinstance(channel, (GuildTextChannelPart, GuildAnnouncementChannelPart, GuildForumChannelPart))

        data = await self.http.request_json(
            'POST', 
            f'/guilds/{self.id}/channels', 
            data=channel.to_dict()
        )

        return JsonQuery(data)

    # --- GUILD MEMBERS ---
    async def fetch_member(self, user_id: Snowflake) -> JsonQuery:
        """Fetch a member in this guild.

        Args:
            user_id (Snowflake): user ID of the member to fetch

        Returns:
            (JsonQuery): queried guild member
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/members/{user_id}')

        return JsonQuery(data)

    async def fetch_members(self, limit: int = 1, after: Snowflake | None = None) -> JsonQuery:
        """Fetch guild members in this guild.

        !!! warning "Important"
            Requires the `GUILD_MEMBERS` privileged intent!

        Args:
            limit (int, optional): Max number of members to return. Range 1 - 1000 (inclusive). Default `1`.
            after (Snowflake, optional): highest user ID in previous page

        Returns:
            (JsonQuery): queried list of guild members
        """
        data = await self.http.request_list(
            'GET', 
            f'/guilds/{self.id}/members', 
            params={
                "limit": limit, 
                "after": after
            }
        )

        return JsonQuery(data)

    async def add_member_role(self, user_id: Snowflake, role_id: Snowflake) -> None:
        """Append a role to a guild member of this guild.

        Fires [**Guild Member Update**](https://docs.discord.com/developers/events/gateway-events#guild-member-update).

        !!! important "Permissions"
            Requires `MANAGE_ROLES`
        
        Args:
            user_id (Snowflake): ID of the member for the role
            role_id (Snowflake): ID of the role to append
        """
        await self.http.request('PUT', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')
    
    async def remove_member_role(self, user_id: Snowflake, role_id: Snowflake) -> None:
        """Remove a role from a guild member of this guild.

        Fires [**Guild Member Update**](https://docs.discord.com/developers/events/gateway-events#guild-member-update).

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            user_id (Snowflake): ID of the member with the role
            role_id (Snowflake): ID of the role to remove
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')

    async def search_members(self, query: str, limit: int = 1) -> JsonQuery:
        """Fetch guild members whose username or nickname starts with the provided query.

        Args:
            query (str): query string to match against
            limit (int, optional): Max number of members to return. Max `1000`. Defaults to `1`.

        Returns:
            (JsonQuery): queried list of guild members
        """
        data = await self.http.request_list(
            'GET', 
            f'guild/{self.id}/members/search',
            params={
                'query': query,
                'limit': limit
            }
        )

        return JsonQuery(data)

    async def edit_member(self, user_id: Snowflake, **options: Unpack[EditGuildMemberParams]) -> JsonQuery:
        """Edit a guild member's attributes.

        Fires [**Guild Member Update**](https://docs.discord.com/developers/events/gateway-events#guild-member-update).

        Args:
            user_id (Snowflake): ID of the member to edit

        Returns:
            (JsonQuery): edited guid member
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/guilds/{self.id}/members/{user_id}', 
            data=dict(options)
        )

        return JsonQuery(data)

    async def remove_member(self, user_id: Snowflake) -> None:
        """Remove a member from this guild.

        Fires [**Guild Member Remove**](https://docs.discord.com/developers/events/gateway-events#guild-member-remove).

        !!! important "Permissions"
            Requires `KICK_MEMBERS`

        Args:
            user_id (Snowflake): ID of the user to kick
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/members/{user_id}')

    # --- BANS ---
    async def fetch_ban(self, user_id: Snowflake) -> JsonQuery:
        """Fetch a guild ban for the given user ID.

        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        Args:
            user_id (Snowflake): ID of the user to fetch

        Returns:
            (JsonQuery): queried ban
        """
        data = await self.http.request_json('GET', f'/guild/{self.id}/bans/{user_id}')

        return JsonQuery(data)

    async def fetch_bans(self, limit: int = 1000, before: Snowflake | None = None, after: Snowflake | None = None) -> JsonQuery:
        """Fetch bans in this guild.

        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        !!! note
            If `before` and `after` are provided, only `before` is respected.

        Args:
            limit (int, optional): max number of users to return. Defaults to `1000`.
            before (Snowflake, optional): fetch users before this ID
            after (Snowflake, optional): fetch users after this ID

        Returns:
            (JsonQuery): queried list of guild bans in ascending order by user ID
        """
        data = await self.http.request_list(
            'GET',
            f'/guilds/{self.id}/bans',
            params={
                'limit': limit,
                'before': before,
                'after': after
            }
        )

        return JsonQuery(data)

    async def create_ban(self, user_id: Snowflake, delete_message_seconds: int = 0) -> None:
        """Create a guild ban and optionally delete messages sent by the banned user.

        Fires [**Guild Ban Add**](https://docs.discord.com/developers/events/gateway-events#guild-member-add).
        
        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        Args:
            user_id (Snowflake): ID of the user to ban
            delete_message_seconds (int, optional): seconds back to delete messages. Range `0` to `604800` (7 days). Defaults to `0`.
        """
        await self.http.request(
            'PUT',
            f'/guilds/{self.id}/bans/{user_id}',
            params={
                'delete_message_seconds': delete_message_seconds
            }
        )

    async def remove_ban(self, user_id: Snowflake) -> None:
        """Remove the ban for a user.

        Fires [**Guild Ban Remove**](https://docs.discord.com/developers/events/gateway-events#guild-ban-remove).

        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        Args:
            user_id (Snowflake): ID of the user in which to remove the ban
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/bans/{user_id}')

    async def bulk_create_ban(self, bulk_ban: BulkGuildBanPart) -> JsonQuery:
        """Create guild bans and optionally delete messages sent by the banned users.

        !!! important "Permissions"
            Requires `BAN_MEMBERS` and `MANAGE_GUILD`

        Args:
            bulk_ban (BulkGuildBanPart): bulk ban to create
            
        Returns:
            (JsonQuery): bulk ban response
        """
        data = await self.http.request_json(
            'POST', 
            f'/guilds/{self.id}/bulk-ban', 
            data=bulk_ban.to_dict()
        )

        return JsonQuery(data)

    # --- ROLES ---
    async def fetch_role_member_counts(self) -> JsonQuery:
        """Fetch a map of role IDs to number of members with the role.

        !!! note
            Does not include `@everyone` role.

        Returns:
            (JsonQuery): map of role IDs to member count
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/roles/member-counts')

        return JsonQuery(data)

    async def fetch_role(self, role_id: Snowflake) -> JsonQuery:
        """Fetch a role in this guild.

        Args:
            role_id (Snowflake): ID of the role to fetch

        Returns:
            (JsonQuery): queried guild role
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/roles/{role_id}')
        
        return JsonQuery(data)
    
    async def fetch_roles(self) -> JsonQuery:
        """Fetch all roles in this guild.

        Returns:
            (JsonQuery): queried list of guild roles
        """
        data = await self.http.request_list('GET', f'/guilds/{self.id}/roles')
        
        return JsonQuery(data)

    async def create_role(self, role: GuildRolePart) -> JsonQuery:
        """Create a role in this guild.

        Fires [**Role Create**](https://docs.discord.com/developers/events/gateway-events#guild-role-create).

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            role (GuildRolePart): fields to create a role

        Returns:
            (JsonQuery): created role
        """
        data = await self.http.request_json(
            'POST', 
            f'/guilds/{self.id}/roles', 
            data=role.to_dict()
        )

        return JsonQuery(data)

    async def edit_role(self, role_id: Snowflake, **options: Unpack[EditGuildRoleParams]) -> JsonQuery:
        """Edit a role in this guild.

        Fires [**Role Update**](https://docs.discord.com/developers/events/gateway-events#guild-role-update).

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            role_id (Snowflake): ID of role to edit
            options (EditGuildRoleParams): role with fields to edit

        Returns:
            (JsonQuery): edited role
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/guilds/{self.id}/roles/{role_id}', 
            data=serialize(dict(options)) # nested objects in EditGuildRoleParamsts
        )

        return JsonQuery(data)

    async def delete_role(self, role_id: Snowflake) -> None:
        """Delete a role in this guild.
        
        Fires [**Role Delete**](https://docs.discord.com/developers/events/gateway-events#guild-role-delete).

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            role_id (Snowflake): ID of role to delete
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/roles/{role_id}')

    # --- INVITES ---
    async def fetch_invites(self) -> JsonQuery:
        """Fetch this guild's invites with no metadata.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` or `VIEW_AUDIT_LOG`
        
        !!! note
            Invite metadata is only include with `MANAGE_GUILD` permission.

        Returns:
            (JsonQuery): queried list of invites
        """
        data = await self.http.request_list('GET', f'/guild/{self.id}/invites')

        return JsonQuery(data)

    async def fetch_invites_with_metadata(self) -> JsonQuery:
        """Fetch this guild's invites with metadata.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` and `MANAGE_GUILD` or `VIEW_AUDIT_LOG`

        Returns:
            (JsonQuery): queried list of invites with metadata
        """
        data = await self.http.request_list('GET', f'/guild/{self.id}/invites')

        return JsonQuery(data)

    # --- INTEGRATIONS ---
    async def fetch_integrations(self) -> JsonQuery:
        """Fetch this guild's integrations.

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Returns:
            (JsonQuery): queried integrations
        """
        data = await self.http.request_list('GET', f'/guild/{self.id}/integrations')

        return JsonQuery(data)

    async def delete_integration(self, integration_id: Snowflake) -> None:
        """Delete the attached integration object for this guild.

        Fires [**Integration Update**](https://docs.discord.com/developers/events/gateway-events#integration-update) 
        and [**Integration Delete**](https://docs.discord.com/developers/events/gateway-events#integration-delete).

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            integration_id (Snowflake): ID of the integration to delete
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/integrations/{integration_id}')

    # --- WELCOME SCREEN ---
    async def fetch_welcome_screen(self) -> JsonQuery:
        """Fetch the welcome screen for this guild.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` if welcome screen is not enabled

        Returns:
            (JsonQuery): queried welcome screen
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/welcome-screen')

        return JsonQuery(data)

    async def edit_welcome_screen(self, **options: Unpack[EditGuildWelcomeScreenParams]) -> JsonQuery:
        """Edit this guild's welcome screen.
        May fire [**Guild Update**](https://docs.discord.com/developers/events/gateway-events#guild-update).

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            options (EditGuildWelcomeScreen): fields to edit

        Returns:
            (JsonQuery): edited welcome screen
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/guilds/{self.id}/welcome-screen', 
            data=serialize(dict(options)) # nested objects in EditGuildWelcomeScreenParams
        )

        return JsonQuery(data)

    # --- ONBOARDING ---
    async def fetch_onboarding(self) -> JsonQuery:
        """Fetch this guild's onboarding flow.

        Returns:
            (JsonQuery): queried onboarding flow
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/onboarding')

        return JsonQuery(data)

    async def edit_onboarding(self, **options: Unpack[EditOnboardingParams]) -> JsonQuery:
        """Modifies this guild's onboarding flow.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` and `MANAGE_ROLES`

        !!! note
            Must be at least **7** Default Channels and at least **5** allow sending message to the @everyone role.
            Constraints depend on the new `mode`.

        Args:
            options (EditOnboardingParams): onboarding field to edit

        Returns:
            (JsonQuery): edited onboarding flow
        """            
        data = await self.http.request_json(
            'PUT',
            f'/guilds/{self.id}/onboarding',
            params=serialize(dict(options)) # nested objects in EditOnboardingParams
        )
        return JsonQuery(data)

    # --- STICKERS ---
    async def fetch_sticker(self, sticker_id: Snowflake) -> JsonQuery:
        """Fetch a sticker from this guild.

        !!! note
            Includes the `user` field if the bot has
            `CREATE_GUILD_EXPRESSIONS` or `MANAGE_GUILD_EXPRESSIONS`

        Args:
            sticker_id (Snowflake): ID of the sticker to fetch

        Returns:
            (JsonQuery): queried sticker
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/stickers/{sticker_id}')

        return JsonQuery(data)

    async def fetch_stickers(self) -> JsonQuery:
        """Fetch this guild's stickers.

        !!! note
            Includes the `user` field if the bot has
            `CREATE_GUILD_EXPRESSIONS` or `MANAGE_GUILD_EXPRESSIONS`

        Returns:
            (JsonQuery): queried guild stickers
        """
        data = await self.http.request_list('GET', f'/guilds/{self.id}/stickers')

        return JsonQuery(data)

    async def create_sticker(self, sticker: StickerPart, file: ImageAssetPart) -> JsonQuery:
        """Add a sticker to this guild.

        Fires [**Guild Stickers Update**](https://docs.discord.com/developers/events/gateway-events#guild-stickers-update).

        !!! important "Permissions"
            Requires `CREATE_GUILD_EXPRESSIONS`

        Args:
            sticker (GuildStickerPart): sticker to create
            file (ImageAssetPart): the sticker file to upload
                !!! note
                    Accepted file types: PNG, APNG, GIF, Lottie JSON file.
                !!! note
                    Animated stickers are restricted to a max of 5 seconds.
                !!! note
                    Lottie stickers are only usable if the guild has `VERIFIED` or `PARTNERED` guild feature.

        Returns:
            (JsonQuery): created sticker
        """
        data = await self.http.request_json(
            'POST', f'/guilds/{self.id}/stickers', 
            data=file.to_dict(),
            assets=sticker.to_dict()
        )
    
        return JsonQuery(data)

    async def edit_sticker(self, sticker_id: Snowflake, **options: Unpack[EditGuildStickerParams]) -> JsonQuery:
        """Edit a sticker from this guild.

        Fires [**Guild Stickers Update**](https://docs.discord.com/developers/events/gateway-events#guild-stickers-update).

        !!! important "Permissions"
            Requires `CREATE_GUILD_EXPRESSIONS` or `MANAGE_GUILD_EXPRESSIONS` if created by the bot.
            
            Requires `MANAGE_GUILD_EXPRESSIONS` if not created by the bot.

        Args:
            sticker_id (Snowflake): ID of the sticker to delete
            options (EditGuildStickerParams): fields to edit

        Returns:
            (JsonQuery): edited sticker
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/guilds/{self.id}/stickers/{sticker_id}', 
            data=dict(options)
        )

        return JsonQuery(data)

    async def delete_sticker(self, sticker_id: Snowflake) -> None:
        """Delete a sticker from this guild.

        Fires [**Guild Stickers Update**](https://docs.discord.com/developers/events/gateway-events#guild-stickers-update).

        !!! important "Permissions"
            Requires `CREATE_GUILD_EXPRESSIONS` or `MANAGE_GUILD_EXPRESSIONS` if created by the bot.
            
            Requires `MANAGE_GUILD_EXPRESSIONS` if not created by the bot.

        Args:
            sticker_id (Snowflake): ID of the sticker to delete
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/stickers/{sticker_id}')
