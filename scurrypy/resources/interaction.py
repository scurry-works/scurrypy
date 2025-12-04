from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..parts.modal import ModalPart
from ..parts.message import MessagePart, MessageFlagParams, MessageFlags
from ..parts.command import CommandOptionChoice

from ..models.interaction import InteractionCallbackModel, InteractionCallbackTypes

@dataclass
class Interaction(BaseResource):
    """Represents a Discord Interaction object."""

    id: int
    """ID of the interaction."""

    token: str
    """Continuation token for responding to the interaction."""

    async def respond(self, message: str | MessagePart, with_response: bool = False, **flags: Unpack[MessageFlagParams]):
        """Create a message in response to an interaction.

        Args:
            message (str | MessagePart): content as a string or MessagePart
            with_response (bool, optional): if the interaction data should be returned. Defaults to False.
            **flags: message flags to set. (set respective flag to True to toggle.)

        Raises:
            (TypeError): invalid `message` type

        Returns:
            (InteractionCallbackModel | None): interaction callback object (if with_response is toggled) else None
        """
        if isinstance(message, str):
            message = MessagePart(content=message).set_flags(**flags)
        elif not isinstance(message, MessagePart):
            raise TypeError(f"Interaction.respond expects type str or MessagePart, got {type(message).__name__}")
        
        content = {
            'type': InteractionCallbackTypes.CHANNEL_MESSAGE_WITH_SOURCE, 
            'data': message._prepare().to_dict()
        }
        
        data = await self._http.request(
            'POST', 
            f'/interactions/{self.id}/{self.token}/callback', 
            data=content, 
            files=[fp.path for fp in message.attachments],
            params={'with_response': with_response}
        )

        if with_response:
            return InteractionCallbackModel.from_dict(data)
        
    async def update(self, message: str | MessagePart):
        """Update a message in response to an interaction.

        Args:
            message (str | MessagePart): content as a string or MessagePart

        Raises:
            (TypeError): invalid `message` type
        """
        if isinstance(message, str):
            message = MessagePart(content=message)
        elif not isinstance(message, MessagePart):
            raise TypeError(f"Interaction.update expects type str or MessagePart, got {type(message).__name__}")
        
        content = {
            'type': InteractionCallbackTypes.UPDATE_MESSAGE, 
            'data': message._prepare().to_dict()
        }

        await self._http.request(
            'POST', 
            f'/interactions/{self.id}/{self.token}/callback', 
            data=content, 
            files=[fp.path for fp in message.attachments])

    async def respond_modal(self, modal: ModalPart):
        """Create a modal in response to an interaction.

        Args:
            modal (ModalPart): modal data

        Raises:
            (TypeError): invalid `modal` type
        """
        if not isinstance(modal, ModalPart):
            raise TypeError(f"Interaction.respond_modal expects type ModalPart, got {type(modal).__name__}")
        
        content = {
            'type': InteractionCallbackTypes.MODAL,
            'data': modal.to_dict()
        }

        await self._http.request(
            'POST', 
            f'/interactions/{self.id}/{self.token}/callback', 
            data=content)

    async def respond_autocomplete(self, choices: list[CommandOptionChoice]):
        """Autocomplete a command in response to an interaction.

        Args:
            choices (list[CommandOptionChoice]): list of choices to autocomplete
        """
        
        content = {
            'type': InteractionCallbackTypes.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT,
            'data': {
                'choices': [choice.to_dict() for choice in choices]
            }
        }

        await self._http.request(
            'POST',
            f'/interactions/{self.id}/{self.token}/callback',
            data=content
        )

    async def defer_respond(self, ephemeral: bool):
        """Defer creating a message in response to an interaction.

        Args:
            ephemeral (bool): whether thinking + deferred interaction response is ephemeral
        """

        content = {
            'type': InteractionCallbackTypes.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {
                'flags': MessageFlags.EPHEMERAL if ephemeral else 0
            }
        }

        await self._http.request(
            'POST',
            f'/interactions/{self.id}/{self.token}/callback',
            data=content
        )

    async def defer_update(self, ephemeral: bool):
        """Defer updating a message in response to an interaction.

        Args:
            ephemeral (bool): whether the deferred interaction response is ephemeral
        """

        content = {
            'type': InteractionCallbackTypes.DEFERRED_UPDATE_MESSAGE,
            'data': {
                'flags': MessageFlags.EPHEMERAL if ephemeral else 0
            }
        }

        await self._http.request(
            'POST',
            f'/interactions/{self.id}/{self.token}/callback',
            data=content
        )

    async def followup(self, application_id, message: str | MessagePart, **flags: Unpack[MessageFlagParams]):
        """Create a new message to respond to a deferred interaction.

        !!! important
            Apps are limited to 5 followup messages PER interaction.

        Args:
            application_id (int): ID of the application
            message (str | MessagePart): content as a string or MessagePart  
            **flags: message flags to set. (set respective flag to True to toggle.)

        Raises:
            (TypeError): invalid `message` type          
        """

        if isinstance(message, str):
            message = MessagePart(content=message).set_flags(**flags)
        elif not isinstance(message, MessagePart):
            raise TypeError(f"Interaction.respond expects type str or MessagePart, got {type(message).__name__}")
        
        content = message._prepare().to_dict()

        await self._http.request(
            'POST',
            f'/webhooks/{application_id}/{self.token}',
            data=content
        )

    async def edit_original(self, application_id: int, message: str | MessagePart):
        """Update the original interaction response from a deferred update interaction.

        Args:
            application_id (int): ID of the application
            message (str | MessagePart): content as a string or MessagePart

        Raises:
            (TypeError): invalid `message` type
        """

        if isinstance(message, str):
            message = MessagePart(content=message)
        elif not isinstance(message, MessagePart):
            raise TypeError(f"Interaction.respond expects type str or MessagePart, got {type(message).__name__}")
        
        content = message._prepare().to_dict()

        await self._http.request(
            'PATCH',
            f'/webhooks/{application_id}/{self.token}/messages/@original',
            data=content
        )
