from dataclasses import dataclass
from typing import Unpack

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake
from ..core.part import serialize

from .base_resource import BaseResource

from ..api.automod import AutoModerationRulePart

from ..params import AutoModerationRuleParams

@dataclass
class AutoModeration(BaseResource):
    """Represents an auto moderation resource."""

    guild_id: Snowflake
    """Guild ID of the auto moderation."""

    async def fetch_all(self) -> JsonQuery:
        """Fetch all of the guild's auto moderation rules.

        Returns:
            (JsonQuery): list of guild's auto moderation rules
        """
        data = await self.http.request_list('GET', f'/guilds/{self.guild_id}/auto-moderation/rules')

        return JsonQuery(data)

    async def fetch(self, rule_id: Snowflake) -> JsonQuery:
        """Fetch a guild's auto moderation rule.

        Args:
            rule_id (Snowflake): ID of the moderation rule

        Returns:
            (JsonQuery): queried moderation rule
        """
        data = await self.http.request_json('GET', f'/guilds/{self.guild_id}/auto-moderation/rules/{rule_id}')

        return JsonQuery(data)

    async def create(self, rule: AutoModerationRulePart) -> JsonQuery:
        """Create an auto moderation rule.
        Fires [**Auto Moderation Rule Create**](https://docs.discord.com/developers/events/gateway-events#auto-moderation-rule-create).

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            rule (AutoModerationRulePart): auto moderation rule to create

        Returns:
            (JsonQuery): created auto moderation rule
        """
        data = await self.http.request_json(
            'POST', 
            f'/guilds/{self.guild_id}/auto-moderation/rules', 
            data=rule.to_dict()
        )

        return JsonQuery(data)

    async def edit(self, rule_id: Snowflake, **options: Unpack[AutoModerationRuleParams]) -> JsonQuery:
        """Edit an auto moderation rule.
        Fires [**Auto Moderation Rule Update**](https://docs.discord.com/developers/events/gateway-events#auto-moderation-rule-update).

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            rule_id (Snowflake): ID of the moderation rule

        Returns:
            (JsonQuery): edited auto moderation rule
        """
        data = await self.http.request_json(
            'PATCH', 
            f'/guilds/{self.guild_id}/auto-moderation/rules/{rule_id}', 
            data=serialize(dict(options)) # nested objects in AutoModerationRuleParams
        )

        return JsonQuery(data)

    async def delete(self, rule_id: Snowflake) -> None:
        """Delete an auto moderation rule.
        Fires [**Auto Moderation Rule Delete**](https://docs.discord.com/developers/events/gateway-events#auto-moderation-rule-delete).

        Args:
            rule_id (Snowflake): ID of the moderation rule
        """
        await self.http.request('DELETE', f'/guilds/{self.guild_id}/auto-moderation/rules/{rule_id}')
