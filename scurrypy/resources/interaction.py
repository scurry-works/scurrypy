from dataclasses import dataclass
from typing import Unpack

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake
from ..core.part import serialize

from .base_resource import BaseResource

from ..enums import MessageFlags, InteractionCallbackType

from ..api.messages import MessagePart
from ..api.components import ModalPart
from ..api.commands import CommandOptionChoicePart

from ..params import EditMessageParams

from .message import _EditMessageMixin

@dataclass
class Interaction(BaseResource, _EditMessageMixin):
    """Represents a Discord interaction resource."""

    id: Snowflake
    """ID of the interaction."""

    token: str
    """Continuation token for responding to the interaction."""

    async def respond(
        self, 
        message: str | MessagePart, 
        *, 
        with_response: bool = False, 
        ephemeral: bool | None = None, 
        suppress_embeds: bool | None = None
    ) -> JsonQuery | None:
        """Create a message in response to an interaction.
        Fires [**Interaction Create**](https://docs.discord.com/developers/events/gateway-events#interaction-create)
        and [**Message Create**](https://docs.discord.com/developers/events/gateway-events#message-create).

        Args:
            message (str | MessagePart): content as a string or MessagePart
            with_response (bool, optional): if the interaction data should be returned. Defaults to `False`.
            ephemeral (optional, bool): whether the response should be ephemeral
            suppress_embeds (optional, bool): whether the response's embeds should be removed

        Returns:
            (JsonQuery | None): interaction callback object (if `with_response` is toggled) else None
        """
        msg = MessagePart(content=message) if isinstance(message, str) else message

        msg.flags = MessageFlags.NO_FLAGS

        if ephemeral:
            msg.flags |= MessageFlags.EPHEMERAL

        if suppress_embeds:
            msg.flags |= MessageFlags.SUPPRESS_EMBEDS

        files = [str(f.path) for f in msg.attachments] if msg.attachments else None

        data = await self.http.request(
            'POST', 
            f'/interactions/{self.id}/{self.token}/callback', 
            data={
                'type': InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE, 
                'data': msg._prepare().to_dict()
            }, 
            files=files,
            params={
                'with_response': with_response
            }
        )

        if with_response:
            assert isinstance(data, dict)
            return JsonQuery(data)
        
        return None
        
    async def update(
        self,
        *,
        suppress_embeds: bool | None = None,
        **options: Unpack[EditMessageParams]
    ) -> None:
        """Edits the initial Interaction response.

        Args:
            options (EditMessageParams): fields to edit
            suppress_embeds (optional, bool): whether the response's embeds should be removed
        """
        files = self._prepare_attachments(dict(options))
        opts = serialize(dict(options)) # nested objects in EditMessageParams
        self._apply_suppress_embeds(opts, suppress_embeds)

        await self.http.request(
            "POST",
            f"/interactions/{self.id}/{self.token}/callback",
            data={
                "type": InteractionCallbackType.UPDATE_MESSAGE,
                "data": opts,
            },
            files=files
        )

    async def respond_modal(self, modal: ModalPart) -> None:
        """Create a modal in response to an interaction.
        Fires [**Interaction Create**](https://docs.discord.com/developers/events/gateway-events#interaction-create).

        Args:
            modal (ModalPart): modal data
        """
        await self.http.request(
            'POST', 
            f'/interactions/{self.id}/{self.token}/callback', 
            data={
                'type': InteractionCallbackType.MODAL,
                'data': modal.to_dict()
            }
        )

    async def respond_autocomplete(self, choices: list[CommandOptionChoicePart]) -> None:
        """Autocomplete a command in response to an interaction.
        Fires [**Interaction Create**](https://docs.discord.com/developers/events/gateway-events#interaction-create).

        Args:
            choices (list[CommandOptionChoicePart]): list of choices to autocomplete
        """
        await self.http.request(
            'POST',
            f'/interactions/{self.id}/{self.token}/callback',
            data={
                'type': InteractionCallbackType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT,
                'data': {
                    'choices': [choice.to_dict() for choice in choices]
                }
            }
        )

    async def defer_respond(self, ephemeral: bool | None = None) -> None:
        """Defer creating a message in response to an interaction.
        Fires [**Interaction Create**](https://docs.discord.com/developers/events/gateway-events#interaction-create).

        Args:
            ephemeral (bool, optional): whether thinking + deferred interaction response is ephemeral
        """
        await self.http.request(
            'POST',
            f'/interactions/{self.id}/{self.token}/callback',
            data={
                'type': InteractionCallbackType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
                'data': {
                    'flags': MessageFlags.EPHEMERAL if ephemeral else MessageFlags.NO_FLAGS
                }
            }
        )

    async def defer_update(self) -> None:
        """Defer updating a message in response to an interaction.
        Fires [**Interaction Create**](https://docs.discord.com/developers/events/gateway-events#interaction-create).
        """
        await self.http.request(
            'POST',
            f'/interactions/{self.id}/{self.token}/callback',
            data={
                'type': InteractionCallbackType.DEFERRED_UPDATE_MESSAGE,
            }
        )

    async def followup(
        self, 
        application_id: Snowflake, 
        message: str | MessagePart, 
        ephemeral: bool | None = None,
        suppress_embeds: bool | None = None
    ) -> None:
        """Create a new message to respond to a deferred interaction.
        Fires [**Message Create**](https://docs.discord.com/developers/events/gateway-events#message-create).

        !!! important
            Apps are limited to 5 followup messages PER interaction.

        Args:
            application_id (Snowflake): ID of the application
            message (str | MessagePart): content as a string or MessagePart
            ephemeral (optional, bool): whether the followup should be ephemeral
            suppress_embeds (optional, bool): whether the followup's embeds should be removed
        """
        if isinstance(message, str):
            message = MessagePart(content=message)

        message.flags = MessageFlags.NO_FLAGS

        if ephemeral:
            message.flags |= MessageFlags.EPHEMERAL

        if suppress_embeds:
            message.flags |= MessageFlags.SUPPRESS_EMBEDS

        await self.http.request(
            'POST',
            f'/webhooks/{application_id}/{self.token}',
            data=message._prepare().to_dict()
        )

    async def edit_original(
        self,
        application_id: Snowflake,
        *,
        suppress_embeds: bool | None = None,
        **options: Unpack[EditMessageParams]
    ) -> None:
        """Edits the initial Interaction response.

        Args:
            application_id (Snowflake): bot's user ID
            options (EditMessageParams): fields to edit
            suppress_embeds (optional, bool): whether the response's embeds should be removed
        """
        opts = serialize(dict(options)) # nested objects in EditMessageParams
        self._apply_suppress_embeds(opts, suppress_embeds)

        await self.http.request(
            "PATCH",
            f"/webhooks/{application_id}/{self.token}/messages/@original",
            data=opts,
            files=self._prepare_attachments(opts)
        )
