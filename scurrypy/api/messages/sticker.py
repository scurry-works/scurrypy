from dataclasses import dataclass

from ...core.model import DataModel, datamodel
from ...core.snowflake import Snowflake
from ...core.types import (
    PresentModelField, 
    OmittableModelField, 
    PresentNullableModelField, 
    RequiredPartField,
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool
)

from ...enums.guild import StickerType, StickerFormatType

from ..user import UserModel

@datamodel
class StickerModel(DataModel):
    """Represents the sticker object."""

    id: PresentModelField[Snowflake]
    """ID of the sticker."""

    pack_id: OmittableModelField[Snowflake]
    """ID of the pack the sticker is from (if standard)."""

    name: PresentModelField[ScurrypyStr]
    """Name of the sticker."""

    description: PresentNullableModelField[ScurrypyStr]
    """Description of the sticker."""

    tags: PresentModelField[ScurrypyStr]
    """Autocomplete/suggestion tags for the sticker."""

    type: PresentModelField[StickerType]
    """Type of sticker."""

    format_type: PresentModelField[StickerFormatType]
    """Type of sticker format."""

    available: OmittableModelField[ScurrypyBool]
    """Whether this guild sticker can be used.
    
    !!! note
        May be `False` due to loss of Server Boosts
    """

    guild_id: OmittableModelField[Snowflake]
    """ID of the guild that owns this sticker."""
    
    user: OmittableModelField[UserModel]
    """The user that uploaded the guild sticker."""

    sort_type: OmittableModelField[ScurrypyInt]
    """The standard sticker's sort order within its pack."""

@datamodel
class StickerItemModel(DataModel):
    """Represents a minimal sticker item."""
    
    id: PresentModelField[Snowflake]
    """ID of the sticker."""

    name: PresentModelField[ScurrypyStr]
    """Name of the sticker."""

    format_type: PresentModelField[StickerFormatType]
    """Type of sticker format."""

@datamodel
class StickerPackModel(DataModel):
    """Represents a pack of standard stickers."""

    id: PresentModelField[Snowflake]
    """ID of the sticker pack."""

    stickers: PresentModelField[list[StickerModel]]
    """The stickers in the pack."""

    name: PresentModelField[ScurrypyStr]
    """Name of the sticker pack."""

    sku_id: PresentModelField[Snowflake]
    """ID of the pack's SKU."""

    cover_sticker_id: OmittableModelField[Snowflake]
    """ID of a sticker in the pack which is shown as the pack's icon."""

    description: PresentModelField[ScurrypyStr]
    """Description of the sticker pack."""

    banner_asset_id: OmittableModelField[Snowflake]
    """ID of the sticker pack's banner image."""

@dataclass
class StickerPart(DataModel):
    """Represents fields for creating a sticker."""

    name: RequiredPartField[str] = None
    """Name of the sticker."""

    description: RequiredPartField[str] = None
    """Description of the sticker."""

    tags: RequiredPartField[str] = None
    """Autocomplete/suggestion tags for the sticker."""
