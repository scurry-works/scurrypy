from dataclasses import dataclass
from ..core.model import DataModel
from ..core.permissions import Permissions

from typing import Optional

from .channel import ChannelModel
from .guild import GuildModel
from .guild_member import GuildMemberModel

class InteractionDataTypes:
    """Interaction data types constants."""

    SLASH_COMMAND = 1
    """The interaction is a slash command."""

    USER_COMMAND = 2
    """The interaction is attached to a user."""

    MESSAGE_COMMAND = 3
    """The interaction is attached to a message."""

class InteractionTypes:
    """Interaction types constants."""

    APPLICATION_COMMAND = 2
    """Slash command interaction."""

    MESSAGE_COMPONENT = 3
    """Message component interaction (e.g., button, select menu, etc.)."""

    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    """Application command autocompletion."""

    MODAL_SUBMIT = 5
    """Modal submit interaction."""

class InteractionCallbackTypes:
    """Interaction callback types constants."""

    PONG = 1
    """Acknowledge a Ping."""

    CHANNEL_MESSAGE_WITH_SOURCE = 4
    """Respond to an interaction with a message."""

    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    """Acknowledge an interaction and edit a response later. User sees a loading state."""

    DEFERRED_UPDATE_MESSAGE = 6
    """
        Acknowledge an interaction and edit the original message later. 
        The user does NOT see a loading state. (Components only)
    """

    UPDATE_MESSAGE = 7
    """Edit the message in which the component was attached."""

    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    """Respond to an autocomplete interaction with suggested choices."""

    MODAL = 9
    """Respond to an interaction with a popup modal (not available for MODAL_SUBMIT and PING interactions)."""

    LAUNCH_ACTIVITY = 12
    """Launch an activity associated with the app (Activities must be enabled)."""

@dataclass
class InteractionCallbackDataModel(DataModel):
    """Represents the interaction callback object."""

    id: int
    """ID of the interaction."""

    type: int
    """Type of interaction.
        See [`InteractionCallbackTypes`][scurrypy.models.interaction.InteractionCallbackTypes].
    """

    activity_instance_id: str
    """Instance ID of activity if an activity was launched or joined."""

    response_message_id: int
    """ID of the message created by the interaction."""

    response_message_loading: bool
    """If the interaction is in a loading state."""

    response_message_ephemeral: bool
    """If the interaction is ephemeral."""

@dataclass
class InteractionCallbackModel(DataModel):
    """Represents the interaction callback response object."""

    interaction: InteractionCallbackDataModel
    """The interaction object associated with the interaction response."""

@dataclass
class InteractionModel(DataModel):
    """Represents the interaction model."""

    type: int
    """Type of interaction.
        See [`InteractionTypes`][scurrypy.models.interaction.InteractionTypes].
    """

    id: int
    """ID of interaction."""

    token: str
    """token of interaction."""

    channel_id: int
    """ID of the channel where the interaction was sent."""

    application_id: int
    """ID of the application that owns the interaction."""

    app_permissions: int
    """Bitwise set of permissions pertaining to the location of the interaction. [`INT_LIMIT`]"""

    member: GuildMemberModel # guild member invoking the interaction
    """Guild member invoking the interaction."""

    locale: str
    """Invoking user's locale."""

    guild_locale: str
    """Locale of the guild the interaction was invoked (if invoked in a guild)."""

    guild_id: Optional[int]
    """ID of guild the interaction was invoked (if invoked in a guild)."""

    guild: Optional[GuildModel]
    """Partial guild object of the guild the interaction was invoked (if invoked in a guild)."""

    channel: Optional[ChannelModel]
    """Partial channel object the interaction was invoked."""

    def bot_can(self, permission_bit: int):
        """Checks `app_permissions` to see if permission bit is toggled.

        Args:
            permission_bit (int): permission bit. See [Permissions][scurrypy.core.permissions.Permissions].

        Returns:
            (bool): whether the bot has this permission
        """
        return Permissions.has(self.app_permissions, permission_bit)
