from dataclasses import dataclass

from .base_resource import BaseResource

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake

@dataclass
class Sticker(BaseResource):
    """Represents a Sticker resource."""

    async def fetch(self, sticker_id: Snowflake) -> JsonQuery:
        """Fetch a sticker.
        
        Args:
            sticker_id (Snowflake): ID of the sticker to fetch

        Returns:
            (JsonQuery): queried sticker
        """
        data = await self.http.request_json('GET', f'/stickers/{sticker_id}')

        return JsonQuery(data)

    async def fetch_sticker_pack(self, pack_id: Snowflake) -> JsonQuery:
        """Fetch a sticker pack.

        Args:
            pack_id (Snowflake): ID of the pack to fetch

        Returns:
            (JsonQuery): queried sticker pack
        """
        data = await self.http.request_json('GET', f'/sticker-packs/{pack_id}')

        return JsonQuery(data)

    async def fetch_sticker_packs(self) -> JsonQuery:
        """Fetch available sticker packs.

        Raises:
            (MissingField): no sticker packs field

        Returns:
            (JsonQuery): queried list of sticker packs.
        """
        data = await self.http.request_json('GET', '/sticker-packs')

        return JsonQuery(data)
