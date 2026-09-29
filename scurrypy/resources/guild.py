from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..core.snowflake import Snowflake
from ..core.serialization import serialize
from ..core.types import JSON

from ..bases.channel import GuildChannelCreate

from ..api.guilds import (
    GuildModel, 
    BulkGuildBanPart, 
    GuildBanModel, 
    BulkGuildBanModel, 
    GuildWelcomeScreenModel, 
    GuildOnboadingModel, 
    GuildRolePart, 
    GuildRoleModel
)
from ..api.channels import (
    ChannelModel, 
    GuildTextChannelPart, 
    GuildAnnouncementChannelPart, 
    GuildForumChannelPart, 
    ActiveThreadsModel
)
from ..api.messages import StickerModel, StickerPart
from ..api.invite import InviteModel, InviteWithMetadataModel
from ..api.integration import IntegrationModel
from ..api.user import GuildMemberModel
from ..api.image_data import ImageAssetPart

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
    """Represents a Discord guild."""
    
    id: Snowflake
    """ID of the guild."""

    # GUILD
    async def fetch(self, with_counts: bool = False) -> GuildModel:
        """Fetch the Guild object by the given ID.

        Args:
            with_counts (bool, optional): return the approximate member and presence counts for the guild. Defaults to `False`.

        Returns:
            (GuildModel): queried guild
        """
        params = {'with_counts': with_counts}

        data = await self.http.request_json('GET', f'/guilds/{self.id}', params=params)

        return GuildModel.from_dict(data)

    async def edit(self, **options: Unpack[EditGuildParams]) -> GuildModel:
        """Edit this guild.
        Fires [`GuildUpdateEvent`][scurrypy.events.guild_events.GuildUpdateEvent].

        Args:
            options (EditGuildParams): guild with fields to edit

        Returns:
            (GuildModel): edited guild
        """
        opts = serialize(dict(options)) # nested objects in EditGuildParams

        data = await self.http.request_json('PATCH', f'/guilds/{self.id}', data=opts)

        return GuildModel.from_dict(data)

    # --- CHANNELS ---
    async def fetch_channels(self) -> list[ChannelModel]:
        """Fetch this guild's channels.

        !!! note
            Does not include threads!

        Returns:
            (list[ChannelModel]): queried list of the guild's channels
        """
        data = await self.http.request_list('GET', f'guilds/{self.id}/channels')

        return [ChannelModel.from_dict(channel) for channel in data]
    
    async def fetch_active_threads(self) -> ActiveThreadsModel:
        """Fetch all active threads in a guild (private and public).

        !!! note
            Threads are ordered by their ID in descending order.

        Returns:
            (ActiveThreadsModel): active guild threads
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/threads/active')

        return ActiveThreadsModel.from_dict(data)

    async def create_channel(self, channel: GuildChannelCreate) -> ChannelModel:
        """Create a channel in this guild.
        Fires [`ChannelCreateEvent`][scurrypy.events.channel_events.ChannelCreateEvent].

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS`

        Args:
            channel (GuildChannelCreate): the guild channel to create

        Returns:
            (ChannelModel): created channel
        """
        assert isinstance(channel, (GuildTextChannelPart, GuildAnnouncementChannelPart, GuildForumChannelPart))
        data = await self.http.request_json('POST', f'/guilds/{self.id}/channels', data=channel.to_dict())

        return ChannelModel.from_dict(data)

    # --- GUILD MEMBERS ---
    async def fetch_member(self, user_id: Snowflake) -> GuildMemberModel:
        """Fetch a member in this guild.

        Args:
            user_id (Snowflake): user ID of the member to fetch

        Returns:
            (GuildMemberModel): queried guild member
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/members/{user_id}')

        return GuildMemberModel.from_dict(data)

    async def fetch_members(self, limit: int = 1, after: Snowflake | None = None) -> list[GuildMemberModel]:
        """Fetch guild members in this guild.

        !!! warning "Important"
            Requires the `GUILD_MEMBERS` privileged intent!

        Args:
            limit (int, optional): Max number of members to return. Range 1 - 1000 (inclusive). Default `1`.
            after (Snowflake, optional): highest user ID in previous page

        Returns:
            (list[GuildMemberModel]): queried list of guild members
        """
        params = {
            "limit": limit, 
            "after": after
        }

        data = await self.http.request_list('GET', f'/guilds/{self.id}/members', params=params)

        return [GuildMemberModel.from_dict(member) for member in data]

    async def add_member_role(self, user_id: Snowflake, role_id: Snowflake) -> None:
        """Append a role to a guild member of this guild.
        Fires [`GuildMemberUpdateEvent`][scurrypy.events.user_events.GuildMemberUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_ROLES`
        
        Args:
            user_id (Snowflake): ID of the member for the role
            role_id (Snowflake): ID of the role to append
        """
        await self.http.request('PUT', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')
    
    async def remove_member_role(self, user_id: Snowflake, role_id: Snowflake) -> None:
        """Remove a role from a guild member of this guild.
        Fires [`GuildMemberUpdateEvent`][scurrypy.events.user_events.GuildMemberUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            user_id (Snowflake): ID of the member with the role
            role_id (Snowflake): ID of the role to remove
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')

    async def search_members(self, query: str, limit: int = 1) -> list[GuildMemberModel]:
        """Fetch guild members whose username or nickname starts with the provided query.

        Args:
            query (str): query string to match against
            limit (int, optional): Max number of members to return. Max `1000`. Defaults to `1`.

        Returns:
            list[GuildMemberModel]: queried list of guild members
        """
        data = await self.http.request_list(
            'GET', 
            f'guild/{self.id}/members/search',
            params={
                'query': query,
                'limit': limit
            }
        )

        return [GuildMemberModel.from_dict(m) for m in data]

    async def edit_member(self, user_id: Snowflake, **options: Unpack[EditGuildMemberParams]) -> GuildMemberModel:
        """Edit a guild member's attributes.
        Fires [`GuildMemberUpdateEvent`][scurrypy.events.user_events.GuildMemberUpdateEvent].

        Args:
            user_id (Snowflake): ID of the member to edit

        Returns:
            (GuildMemberModel): edited guid member
        """
        opts = dict(options)

        data = await self.http.request_json('PATCH', f'/guilds/{self.id}/members/{user_id}', data=opts)

        return GuildMemberModel.from_dict(data)

    async def remove_member(self, user_id: Snowflake) -> None:
        """Remove a member from this guild.
        Fires [`GuildMemberRemoveEvent`][scurrypy.events.user_events.GuildMemberRemoveEvent].

        !!! important "Permissions"
            Requires `KICK_MEMBERS`

        Args:
            user_id (Snowflake): ID of the user to kick
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/members/{user_id}')

    # --- BANS ---
    async def fetch_ban(self, user_id: Snowflake) -> GuildBanModel:
        """Fetch a guild ban for the given user ID.

        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        Args:
            user_id (Snowflake): ID of the user to fetch

        Returns:
            (GuildBan): queried ban
        """
        data = await self.http.request_json('GET', f'/guild/{self.id}/bans/{user_id}')

        return GuildBanModel.from_dict(data)

    async def fetch_bans(self, limit: int = 1000, before: Snowflake | None = None, after: Snowflake | None = None) -> list[GuildBanModel]:
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
            (list[GuildBan]): queried list of guild bans in ascending order by user ID
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

        return [GuildBanModel.from_dict(i) for i in data]

    async def create_ban(self, user_id: Snowflake, delete_message_seconds: int = 0) -> None:
        """Create a guild ban and optionally delete messages sent by the banned user.
        Fires [`GuildBanAddEvent`][scurrypy.events.guild_events.GuildBanAddEvent].
        
        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        Args:
            user_id (Snowflake): ID of the user to ban
            delete_message_seconds (int, optional): seconds back to delete messages. Range `0` to `604800` (7 days). Defaults to `0`.
        """
        await self.http.request(
            'PUT',
            f'/guilds/{self.id}/bans/{user_id}',
            params={'delete_message_seconds': delete_message_seconds}
        )

    async def remove_ban(self, user_id: Snowflake) -> None:
        """Remove the ban for a user.
        Fires [`GuildBanRemoveEvent`][scurrypy.events.guild_events.GuildBanRemoveEvent].

        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        Args:
            user_id (Snowflake): ID of the user in which to remove the ban
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/bans/{user_id}')

    async def bulk_create_ban(self, bulk_ban: BulkGuildBanPart) -> BulkGuildBanModel:
        """Create guild bans and optionally delete messages sent by the banned users.

        !!! important "Permissions"
            Requires `BAN_MEMBERS` and `MANAGE_GUILD`

        Args:
            bulk_ban (BulkGuildBanPart): bulk ban to create
            
        Returns:
            (BulkGuildBanModel): bulk ban response
        """
        data = await self.http.request_json('POST', f'/guilds/{self.id}/bulk-ban', data=bulk_ban.to_dict())

        return BulkGuildBanModel.from_dict(data)

    # --- ROLES ---
    async def fetch_role_member_counts(self) -> JSON:
        """Fetch a map of role IDs to number of members with the role.

        !!! note
            Does not include `@everyone` role.

        Returns:
            (JSON): map of role IDs to member count
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/roles/member-counts')

        assert isinstance(data, dict)
        return data

    async def fetch_role(self, role_id: Snowflake) -> GuildRoleModel:
        """Fetch a role in this guild.

        Args:
            role_id (Snowflake): ID of the role to fetch

        Returns:
            (GuildRoleModel): queried guild role
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/roles/{role_id}')
        
        return GuildRoleModel.from_dict(data)
    
    async def fetch_roles(self) -> list[GuildRoleModel]:
        """Fetch all roles in this guild.

        Returns:
            (list[GuildRoleModel]): queried list of guild roles
        """
        data = await self.http.request_list('GET', f'/guilds/{self.id}/roles')
        
        return [GuildRoleModel.from_dict(role) for role in data]

    async def create_role(self, role: GuildRolePart) -> GuildRoleModel:
        """Create a role in this guild.
        Fires [`RoleCreateEvent`][scurrypy.events.role_events.RoleCreateEvent].

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            role (GuildRolePart): fields to create a role

        Returns:
            (GuildRoleModel): created role
        """
        data = await self.http.request_json('POST', f'/guilds/{self.id}/roles', data=role.to_dict())

        return GuildRoleModel.from_dict(data)

    async def edit_role(self, role_id: Snowflake, **options: Unpack[EditGuildRoleParams]) -> GuildRoleModel:
        """Edit a role in this guild.
        Fires [`RoleUpdateEvent`][scurrypy.events.role_events.RoleUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            role_id (Snowflake): ID of role to edit
            options (EditGuildRoleParams): role with fields to edit

        Returns:
            (GuildRoleModel): edited role
        """
        opts = serialize(dict(options)) # nested objects in EditGuildRoleParams

        data = await self.http.request_json('PATCH', f'/guilds/{self.id}/roles/{role_id}', data=opts)

        return GuildRoleModel.from_dict(data)

    async def delete_role(self, role_id: Snowflake) -> None:
        """Delete a role in this guild.
        Fires [`RoleDeleteEvent`][scurrypy.events.role_events.RoleDeleteEvent].

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            role_id (Snowflake): ID of role to delete
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/roles/{role_id}')

    # --- INVITES ---
    async def fetch_invites(self) -> list[InviteModel]:
        """Fetch this guild's invites with no metadata.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` or `VIEW_AUDIT_LOG`
        
        !!! note
            Invite metadata is only include with `MANAGE_GUILD` permission.

        Returns:
            (list[InviteModel]): queried list of invites
        """
        data = await self.http.request_list('GET', f'/guild/{self.id}/invites')

        return [InviteModel.from_dict(i) for i in data]

    async def fetch_invites_with_metadata(self) -> list[InviteWithMetadataModel]:
        """Fetch this guild's invites with metadata.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` and `MANAGE_GUILD` or `VIEW_AUDIT_LOG`

        Returns:
            (list[InviteModel]): queried list of invites with metadata
        """
        data = await self.http.request_list('GET', f'/guild/{self.id}/invites')

        return [InviteWithMetadataModel.from_dict(i) for i in data]

    # --- INTEGRATIONS ---
    async def fetch_integrations(self) -> list[IntegrationModel]:
        """Fetch this guild's integrations.

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Returns:
            (list[IntegrationModel]): queried integrations
        """
        data = await self.http.request_list('GET', f'/guild/{self.id}/integrations')

        return [IntegrationModel.from_dict(i) for i in data]

    async def delete_integration(self, integration_id: Snowflake) -> None:
        """Delete the attached integration object for this guild.
        Fires [`GuildIntegrationUpdateEvent`][scurrypy.events.integration_events.GuildIntegrationUpdateEvent] 
        and [`GuildIntegrationDeleteEvent`][scurrypy.events.integration_events.GuildIntegrationDeleteEvent].

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            integration_id (Snowflake): ID of the integration to delete
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/integrations/{integration_id}')

    # --- WELCOME SCREEN ---
    async def fetch_welcome_screen(self) -> GuildWelcomeScreenModel:
        """Fetch the welcome screen for this guild.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` if welcome screen is not enabled

        Returns:
            (GuildWelcomeScreenModel): queried welcome screen
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/welcome-screen')

        return GuildWelcomeScreenModel.from_dict(data)

    async def edit_welcome_screen(self, **options: Unpack[EditGuildWelcomeScreenParams]) -> GuildWelcomeScreenModel:
        """Edit this guild's welcome screen.
        May fire [`GuildUpdateEvent`][scurrypy.events.guild_events.GuildUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            options (EditGuildWelcomeScreen): fields to edit

        Returns:
            (GuildWelcomeScreenModel): edited welcome screen
        """
        opts = serialize(dict(options)) # nested objects in EditGuildWelcomeScreenParams

        data = await self.http.request_json('PATCH', f'/guilds/{self.id}/welcome-screen', data=opts)

        return GuildWelcomeScreenModel.from_dict(data)

    # --- ONBOARDING ---
    async def fetch_onboarding(self) -> GuildOnboadingModel:
        """Fetch this guild's onboarding flow.

        Returns:
            (GuildOnboadingModel): queried onboarding flow
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/onboarding')

        return GuildOnboadingModel.from_dict(data)

    async def edit_onboarding(self, **options: Unpack[EditOnboardingParams]) -> GuildOnboadingModel:
        """Modifies this guild's onboarding flow.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` and `MANAGE_ROLES`

        !!! note
            Must be at least **7** Default Channels and at least **5** allow sending message to the @everyone role.
            Constraints depend on the new `mode`.

        Args:
            options (EditOnboardingParams): onboarding field to edit

        Returns:
            (GuildOnboadingModel): edited onboarding flow
        """
        opts = serialize(dict(options)) # nested objects in EditOnboardingParams
            
        data = await self.http.request_json(
            'PUT',
            f'/guilds/{self.id}/onboarding',
            params=opts
        )
        return GuildOnboadingModel.from_dict(data)

    # --- STICKERS ---
    async def fetch_sticker(self, sticker_id: Snowflake) -> StickerModel:
        """Fetch a sticker from this guild.

        !!! note
            Includes the `user` field if the bot has
            `CREATE_GUILD_EXPRESSIONS` or `MANAGE_GUILD_EXPRESSIONS`

        Args:
            sticker_id (Snowflake): ID of the sticker to fetch

        Returns:
            (StickerModel): queried sticker
        """
        data = await self.http.request_json('GET', f'/guilds/{self.id}/stickers/{sticker_id}')

        return StickerModel.from_dict(data)

    async def fetch_stickers(self) -> list[StickerModel]:
        """Fetch this guild's stickers.

        !!! note
            Includes the `user` field if the bot has
            `CREATE_GUILD_EXPRESSIONS` or `MANAGE_GUILD_EXPRESSIONS`

        Returns:
            list[StickerModel]: queried guild stickers
        """
        data = await self.http.request_list('GET', f'/guilds/{self.id}/stickers')

        return [StickerModel.from_dict(i) for i in data]

    async def create_sticker(self, sticker: StickerPart, file: ImageAssetPart) -> StickerModel:
        """Add a sticker to this guild.
        Fires [`GuildStickersUpdateEvent`][scurrypy.events.guild_events.GuildStickersUpdateEvent].

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
            (StickerModel): created sticker
        """
        data = await self.http.request_json(
            'POST', f'/guilds/{self.id}/stickers', 
            data=file.to_dict(),
            assets=sticker.to_dict()
        )
    
        return StickerModel.from_dict(data)

    async def edit_sticker(self, sticker_id: Snowflake, **options: Unpack[EditGuildStickerParams]) -> StickerModel:
        """Edit a sticker from this guild.
        Fires [`GuildStickersUpdateEvent`][scurrypy.events.guild_events.GuildStickersUpdateEvent].

        !!! important "Permissions"
            Requires `CREATE_GUILD_EXPRESSIONS` or `MANAGE_GUILD_EXPRESSIONS` if created by the bot.
            
            Requires `MANAGE_GUILD_EXPRESSIONS` if not created by the bot.

        Args:
            sticker_id (Snowflake): ID of the sticker to delete
            options (EditGuildStickerParams): fields to edit
        """
        opts = dict(options)

        data = await self.http.request_json('PATCH', f'/guilds/{self.id}/stickers/{sticker_id}', data=opts)

        return StickerModel.from_dict(data)

    async def delete_sticker(self, sticker_id: Snowflake) -> None:
        """Delete a sticker from this guild.
        Fires [`GuildStickersUpdateEvent`][scurrypy.events.guild_events.GuildStickersUpdateEvent].

        !!! important "Permissions"
            Requires `CREATE_GUILD_EXPRESSIONS` or `MANAGE_GUILD_EXPRESSIONS` if created by the bot.
            
            Requires `MANAGE_GUILD_EXPRESSIONS` if not created by the bot.

        Args:
            sticker_id (Snowflake): ID of the sticker to delete
        """
        await self.http.request('DELETE', f'/guilds/{self.id}/stickers/{sticker_id}')
