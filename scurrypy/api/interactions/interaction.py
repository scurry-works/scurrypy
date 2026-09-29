from ...core.model import DataModel, datamodel
from ...core.snowflake import Snowflake
from ...core.types import (
    PresentModelField, 
    OmittableModelField, 
    ScurrypyStr, 
    ScurrypyBool
)

from ...enums.permissions import Permissions
from ...enums.interaction import InteractionCallbackType, InteractionType

from ..channels.channel import ChannelModel
from ..guilds.guild import GuildModel
from ..messages.message import MessageModel

from ..user import GuildMemberModel

@datamodel
class InteractionCallbackDataModel(DataModel):
    """Represents the interaction callback object."""

    id: PresentModelField[Snowflake]
    """ID of the interaction."""

    type: PresentModelField[InteractionCallbackType]
    """Type of interaction."""

    activity_instance_id: OmittableModelField[ScurrypyStr]
    """Instance ID of activity if an activity was launched or joined."""

    response_message_id: OmittableModelField[Snowflake]
    """ID of the message created by the interaction."""

    response_message_loading: OmittableModelField[ScurrypyBool]
    """If the interaction is in a loading state."""

    response_message_ephemeral: OmittableModelField[ScurrypyBool]
    """If the interaction is ephemeral."""

@datamodel
class InteractionCallbackModel(DataModel):
    """Represents the interaction callback response object."""

    interaction: PresentModelField[InteractionCallbackDataModel]
    """The interaction object associated with the interaction response."""

@datamodel
class InteractionModel(DataModel):
    """Represents the interaction model."""

    type: PresentModelField[InteractionType]
    """Type of interaction."""

    id: PresentModelField[Snowflake]
    """ID of interaction."""

    token: PresentModelField[ScurrypyStr]
    """token of interaction."""

    application_id: PresentModelField[Snowflake]
    """ID of the application that owns the interaction."""

    app_permissions: PresentModelField[Permissions]
    """Bitwise set of permissions pertaining to the location of the interaction. [`INT_LIMIT`]"""

    member: OmittableModelField[GuildMemberModel]
    """Guild member invoking the interaction."""

    message: OmittableModelField[MessageModel]
    """Message associated with interaction (components or modals)."""

    guild_id: OmittableModelField[Snowflake]
    """ID of guild the interaction was invoked (if invoked in a guild)."""

    guild: OmittableModelField[GuildModel]
    """Partial guild object of the guild the interaction was invoked (if invoked in a guild)."""

    channel_id: OmittableModelField[Snowflake]
    """ID of the channel where the interaction was sent."""

    channel: OmittableModelField[ChannelModel]
    """Partial channel object the interaction was invoked."""
