from dataclasses import dataclass

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake

from .base_resource import BaseResource

from ..enums import AuditLogEventType

@dataclass
class AuditLog(BaseResource):
    """Represents an audit log resource."""

    async def fetch(self, 
        guild_id: Snowflake,
        user_id: Snowflake | None = None,
        action_type: AuditLogEventType | None = None,
        before: Snowflake | None = None,
        after: Snowflake | None = None,
        limit: int = 50
    ) -> JsonQuery:
        """Fetch an audit log.

        !!! important "Permissions"
            Requires `VIEW_AUDIT_LOG`

        Args:
            guild_id (Snowflake): ID of guild in which the audit log belongs
            user_id (Snowflake, optional): entries from a specific user ID
            action_type (AuditLogEventType, optional): entries for a specific audit log event
            before (Snowflake, optional): entries with ID less than a specific audit log entry ID
            after (Snowflake, optional): entries with ID greater than a specific audit log entry ID
            limit (int, optional): Maximum number of entries. Defaults to 50. Range 1 - 100.

        Returns:
            (JsonQuery): queried audit log
        """
        data = await self.http.request_json(
            'GET',
            f'/guilds/{guild_id}/audit-logs',
            params={
                'user_id': user_id,
                'action_type': action_type,
                'before': before,
                'after': after,
                'limit': limit
            }
        )

        return JsonQuery(data)
