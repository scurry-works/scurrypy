from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import OmittableModelField

from ..guilds.role import GuildRoleModel
from ..channels.channel import ChannelModel
from ..messages.message import MessageModel
from ..messages.attachment import AttachmentModel

from ..user import UserModel, GuildMemberModel

@dataclass
class ResolvedDataModel(DataModel):
    """Represents the resolved data object."""

    users: OmittableModelField[dict[Snowflake, UserModel]]
    """Map of user snowflakes to user objects."""

    members: OmittableModelField[dict[Snowflake, GuildMemberModel]]
    """Map of member snowflakes to partial guild member objects.

    !!! note "Missing Fields"
        `user`, `deaf`, and `mute`.
    """

    roles: OmittableModelField[dict[Snowflake, GuildRoleModel]]
    """Map of role snowflakes to role objects."""

    channels: OmittableModelField[dict[Snowflake, ChannelModel]]
    """Map of channel snowflakes to partial channel objects."""

    messages: OmittableModelField[dict[Snowflake, MessageModel]]
    """Map of message snowflakes to partial message objects."""

    attachments: OmittableModelField[dict[Snowflake, AttachmentModel]]
    """Map of attachment snowflakes to attachment objects."""
