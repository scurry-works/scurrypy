from ...core.model import datamodel
from ...core.snowflake import Snowflake
from ...core.types import OmittableModelField, OmittableNullableModelField, ScurrypyStr

from ..user import UserModel

from .channel import ChannelModel

@datamodel
class DMChannelModel(ChannelModel):
    """Represents a DM channel."""

    recipients: OmittableModelField[list[UserModel]]
    """Recipients of the DM."""

    icon: OmittableNullableModelField[ScurrypyStr]
    """Icon hash of the group DM."""

    owner_id: OmittableModelField[Snowflake]
    """ID of the creator of the group DM."""

    application_id: OmittableNullableModelField[Snowflake]
    """ID of the application that created the DM."""
