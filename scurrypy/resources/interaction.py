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

@dataclass
class Interaction(BaseResource):
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
        suppress_embeds: bool = False,
        suppress_notifications: bool = False,
        is_voice_message: bool = False,
        is_components_v2 : bool = False,
        ephemeral: bool = False
    ) -> JsonQuery | None:
        """Create a message in response to an interaction.
        Fires [**Interaction Create**](https://docs.discord.com/developers/events/gateway-events#interaction-create)
        and [**Message Create**](https://docs.discord.com/developers/events/gateway-events#message-create).

        Args:
            message (str | MessagePart): content as a string or MessagePart
            with_response (bool, optional): if the interaction data should be returned. Defaults to `False`.
            suppress_embeds (bool, optional): whether to suppress embeds. Defaults to `False`.
            suppress_notifications (bool, optional): whether to suppress notifications. Defaults to `False`.
            is_voice_message (bool, optional): whether this message is a voice message. Defaults to `False`.
            is_components_v2 (bool, optional): whether V2 components are in this message. Defaults to `False`.
            ephemeral (bool, optional): whether the response is only visible to the invoking user. Defaults to `False`.

        Returns:
            (JsonQuery | None): interaction callback object (if `with_response` is toggled) else None
        """

        # normalize to MessagePart
        msg = MessagePart(content=message) if isinstance(message, str) else message

        if suppress_embeds:
            msg.flags |= MessageFlags.SUPPRESS_EMBEDS

        if suppress_notifications:
            msg.flags |= MessageFlags.SUPPRESS_NOTIFICATIONS

        if is_voice_message:
            msg.flags |= MessageFlags.IS_VOICE_MESSAGE

        if is_components_v2:
            msg.flags |= MessageFlags.IS_COMPONENTS_V2

        if ephemeral:
            msg.flags |= MessageFlags.EPHEMERAL

        data = await self.http.request(
            "POST",
            f'/interactions/{self.id}/{self.token}/callback',
            data={
                'type': InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
                'data': msg.prepare_attachments().to_dict()
            },
            files=[attachment.path for attachment in msg.attachments],
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
        suppress_embeds: bool = False,
        is_components_v2 : bool = False,
        **options: Unpack[EditMessageParams]
    ) -> None:
        """Edits the initial Interaction response.

        Args:
            suppress_embeds (bool, optional): whether to suppress embeds. Defaults to `False`.
            is_components_v2 (bool, optional): whether V2 components are in this message. Defaults to `False`.
            options (EditMessageParams): fields to edit for the message
        """
        files = None
        if options.get('attachments') is not None:
            for idx, file in enumerate(options['attachments']):
                file.id = idx
            files = [attachment.path for attachment in options['attachments']]

        options['flags'] = MessageFlags.NO_FLAGS

        if suppress_embeds:
            options['flags'] |= MessageFlags.SUPPRESS_EMBEDS

        if is_components_v2:
            options['flags'] |= MessageFlags.IS_COMPONENTS_V2

        await self.http.request(
            "POST",
            f"/interactions/{self.id}/{self.token}/callback",
            data={
                "type": InteractionCallbackType.UPDATE_MESSAGE,
                "data": serialize(dict(options)) # nested objects in EditMessageParams
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
        ephemeral: bool = False,
        suppress_embeds: bool = False,
        suppress_notifications: bool = False,
        is_components_v2: bool = False
    ) -> None:
        """Create a new message to respond to a deferred interaction.
        Fires [**Message Create**](https://docs.discord.com/developers/events/gateway-events#message-create).

        !!! important
            Apps are limited to 5 followup messages PER interaction.

        Args:
            application_id (Snowflake): ID of the application
            message (str | MessagePart): content as a string or MessagePart
            ephemeral (optional, bool): whether the followup should be ephemeral. Defaults to `False`.
            suppress_embeds (optional, bool): whether the followup's embeds should be removed. Defaults to `False`.
            suppress_notifications (bool, optional): whether to suppress notifications. Defaults to `False`.
            is_components_v2 (bool, optional): whether V2 components are in this message. Defaults to `False`.
        """
        # normalize to MessagePart
        msg = MessagePart(content=message) if isinstance(message, str) else message

        msg.flags = MessageFlags.NO_FLAGS

        if ephemeral:
            msg.flags |= MessageFlags.EPHEMERAL

        if suppress_embeds:
            msg.flags |= MessageFlags.SUPPRESS_EMBEDS

        if suppress_notifications:
            msg.flags |= MessageFlags.SUPPRESS_NOTIFICATIONS

        if is_components_v2:
            msg.flags |= MessageFlags.IS_COMPONENTS_V2

        await self.http.request(
            'POST',
            f'/webhooks/{application_id}/{self.token}',
            data=msg.prepare_attachments().to_dict(),
            files=[attachment.path for attachment in msg.attachments] if msg.attachments is not None else None
        )

    async def edit_original(
        self,
        application_id: Snowflake,
        suppress_embeds: bool = False,
        is_components_v2: bool = False,
        **options: Unpack[EditMessageParams]
    ) -> None:
        """Edits the initial Interaction response.

        !!! note
            Existing message flags are not automatically preserved. Flags are reset unless explicitly specified.

        Args:
            application_id (Snowflake): bot's user ID
            suppress_embeds (bool, optional): whether to suppress embeds. Defaults to `False`.
            is_components_v2 (bool, optional): whether V2 components are in this message. Defaults to `False`.
            options (EditMessageParams): fields to edit
        """
        files = None
        if options.get('attachments') is not None:
            for idx, file in enumerate(options['attachments']):
                file.id = idx
            files = [attachment.path for attachment in options['attachments']]

        options['flags'] = MessageFlags.NO_FLAGS

        if suppress_embeds:
            options['flags'] |= MessageFlags.SUPPRESS_EMBEDS

        if is_components_v2:
            options['flags'] |= MessageFlags.IS_COMPONENTS_V2

        await self.http.request(
            "PATCH",
            f"/webhooks/{application_id}/{self.token}/messages/@original",
            data=serialize(dict(options)), # nested objects in EditMessageParams
            files=files
        )
