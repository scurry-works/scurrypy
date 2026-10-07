from dataclasses import dataclass
from typing import Unpack

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake

from .base_resource import BaseResource

from ..params import GuildTemplateParams

from ..api import GuildTemplatePart

@dataclass
class GuildTemplate(BaseResource):
    """Represents a guild template resource."""
    
    async def fetch(self, template_code: str) -> JsonQuery:
        """Fetch a guild template.

        Args:
            template_code (str): code of guild template to fetch

        Returns:
            (JsonQuery): queried guild template
        """
        data = await self.http.request_json('GET', f'/guilds/templates/{template_code}')

        return JsonQuery(data)

    async def fetch_guild(self, guild_id: Snowflake) -> JsonQuery:
        """Fetch all of a guild's templates.

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            guild_id (Snowflake): ID of guild to fetch guild templates

        Returns:
            (list[GuildTemplateModel]): queried list of guild templates
        """
        data = await self.http.request_list('GET', f'/guilds/{guild_id}/templates')

        return JsonQuery(data)

    async def create(self, guild_id: Snowflake, template: GuildTemplatePart) -> JsonQuery:
        """Create a template for a guild.

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            guild_id (Snowflake): guild ID of which the guild template will belong
            template (GuildTemplatePart): guild template to create

        Returns:
            (GuildTemplateModel): created guild template
        """
        data = await self.http.request_json(
            'POST', 
            f'/guilds/{guild_id}/templates', 
            data=template.to_dict()
        )

        return JsonQuery(data)

    async def sync(self, guild_id: Snowflake, template_code: str) -> JsonQuery:
        """Syncs the guild template to a guild's current state.

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            guild_id (Snowflake): guild ID of which to sync the guild template
            template_code (str): code of guild template to sync

        Returns:
            (JsonQuery): synced guild template
        """
        data = await self.http.request_json('PUT', f'/guilds/{guild_id}/templates/{template_code}')

        return JsonQuery(data)

    async def edit(self, 
        guild_id: Snowflake, 
        template_code: str, 
        **options: Unpack[GuildTemplateParams]
    ) -> JsonQuery:
        """Edit a guild template.

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            guild_id (Snowflake): guild ID of the guild template to edit
            template_code (str): code of the guild template to edit

        Returns:
            (JsonQuery): edited guild template
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/guilds/{guild_id}/templates/{template_code}',
            params=dict(options)
        )

        return JsonQuery(data)

    async def delete(self, guild_id: Snowflake, template_code: str) -> None:
        """Delete a guild template

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            guild_id (Snowflake): guild ID of the guild template to delete
            template_code (str): code of the guild template to delete
        """
        await self.http.request('DELETE', f'/guilds/{guild_id}/templates/{template_code}')
