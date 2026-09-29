from dataclasses import dataclass

from .base_resource import BaseResource

from ..core.snowflake import Snowflake
from ..core.exceptions import MissingField

from ..api.messages import StickerModel, StickerPackModel

@dataclass
class Sticker(BaseResource):
    """Represents the Sticker resource."""

    async def fetch(self, sticker_id: Snowflake) -> StickerModel:
        """Fetch a sticker.
        
        Args:
            sticker_id (Snowflake): ID of the sticker to fetch

        Returns:
            (StickerModel): queried sticker
        """
        data = await self.http.request_json('GET', f'/stickers/{sticker_id}')

        return StickerModel.from_dict(data)

    async def fetch_sticker_pack(self, pack_id: Snowflake) -> StickerPackModel:
        """Fetch a sticker pack.

        Args:
            pack_id (Snowflake): ID of the pack to fetch

        Returns:
            (StickerPackModel): queried sticker pack
        """
        data = await self.http.request_json('GET', f'/sticker-packs/{pack_id}')

        return StickerPackModel.from_dict(data)

    async def fetch_sticker_packs(self) -> list[StickerPackModel]:
        """Fetch available sticker packs.

        Raises:
            (MissingField): no sticker packs field

        Returns:
            list[StickerPackModel]: queried list of sticker packs.
        """
        data = await self.http.request_json('GET', '/sticker-packs')

        assert isinstance(data, dict)

        stickers = data.get('sticker_packs')

        if not stickers:
            raise MissingField("No sticker packs field is present.")
        
        assert isinstance(stickers, list)
        return [StickerPackModel.from_dict(i) for i in stickers]
