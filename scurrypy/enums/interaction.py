from .enum_types import DiscordTypes

class InteractionDataType(DiscordTypes):
    """Interaction data types constants."""

    SLASH_COMMAND = 1
    """The interaction is a slash command."""

    USER_COMMAND = 2
    """The interaction is attached to a user."""

    MESSAGE_COMMAND = 3
    """The interaction is attached to a message."""

class InteractionType(DiscordTypes):
    """Interaction types constants."""

    PING = 1
    """Handshake for utilizing webhook-based interactions"""

    APPLICATION_COMMAND = 2
    """Slash command interaction."""

    MESSAGE_COMPONENT = 3
    """Message component interaction (e.g., button, select menu, etc.)."""

    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    """Application command autocompletion."""

    MODAL_SUBMIT = 5
    """Modal submit interaction."""

class InteractionCallbackType(DiscordTypes):
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
