from dataclasses import dataclass
from typing import Unpack

from ..core.json_query import JsonQuery
from ..core.snowflake import Snowflake
from ..core.part import serialize

from .base_resource import BaseResource

from ..enums import InteractionContextType

from ..api.commands import (
    SlashCommandPart, 
    UserCommandPart, 
    MessageCommandPart,
    SlashCommandFamilyPart,
)

from ..params.command import EditGlobalCommandParams, EditGuildCommandParams

type AnyCommand = SlashCommandPart | UserCommandPart | MessageCommandPart | SlashCommandFamilyPart

@dataclass
class GlobalCommand(BaseResource):
    """Represents a global command resource."""

    application_id: Snowflake
    """Application ID of the commands."""

    async def fetch(self, command_id: Snowflake) -> JsonQuery:
        """Fetches a command object.

        Args:
            command_id (int): ID of the command to fetch

        Returns:
            (ApplicationCommandModel): queried application command
        """
        data = await self.http.request_json('GET', f"/applications/{self.application_id}/commands/{command_id}")

        return JsonQuery(data)
    
    async def fetch_all(self) -> JsonQuery:
        """Fetches ALL global commands.

        Returns:
            (JsonQuery): queried list of application commands
        """
        data = await self.http.request_list('GET', f"applications/{self.application_id}/commands")

        return JsonQuery(data)

    async def create(self, command: AnyCommand, contexts: list[InteractionContextType] | None = None) -> JsonQuery:
        """Add a command to the client.

        !!! danger
            Creating a command with the same name as an existing command in the same scope will overwrite the old command.

        Args:
            command (AnyCommand): command to register
            contexts (list[InteractionContextType], optional): where the command can be used

        Returns:
            (JsonQuery): created command
        """
        payload = command.to_dict()

        assert isinstance(payload, dict)
        
        if contexts is not None:
            payload['contexts'] = contexts

        data = await self.http.request_json(
            'POST', 
            f"applications/{self.application_id}/commands", 
            data=payload
        )

        return JsonQuery(data)

    async def edit(self, command_id: Snowflake, **options: Unpack[EditGlobalCommandParams]) -> JsonQuery:
        """Edit a command.

        Args:
            command_id (Snowflake): ID of command to edit
            options (EditGlobalCommandParams): command fields to edit

        Returns:
            (JsonQuery): updated application command
        """
        data = await self.http.request_json(
            'PATCH', 
            f"applications/{self.application_id}/commands/{command_id}", 
            data=serialize(dict(options)) # nested objects in EditGlobalCommandParams
        )

        return JsonQuery(data)

    async def delete(self, command_id: Snowflake) -> None:
        """Delete a command.

        Args:
            command_id (Snowflake): ID of the command to delete
        """
        await self.http.request('DELETE', f"applications/{self.application_id}/commands/{command_id}")

    async def bulk_overwrite(self, commands: list[AnyCommand]) -> JsonQuery:
        """Takes a list of application commands, overwriting existing commands list for this application. 
        
        !!! warning
            Commands that do not already exist will count toward daily application command create limits.

        !!! danger
            This will overwrite all types of application commands: slash commands, user commands, and message commands.

        Args:
            commands (list[AnyCommand]): commands to register

        Returns:
            (JsonQuery): created application commands
        """
        data = await self.http.request_list(
            'PUT', 
            f"applications/{self.application_id}/commands", 
            data=[cmd.to_dict() for cmd in commands]
        )

        return JsonQuery(data)


@dataclass
class GuildCommand(BaseResource):
    """Represents a guild command."""

    application_id: Snowflake
    """Application ID of the commands."""

    guild_id: Snowflake
    "Guild ID of command."

    async def fetch(self, command_id: Snowflake) -> JsonQuery:
        """Fetches the command object.

        Args:
            command_id (int): ID of command to fetch

        Returns:
            (JsonQuery): queried application command
        """
        data = await self.http.request_json('GET', f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{command_id}")

        return JsonQuery(data)
    
    async def fetch_all(self) -> JsonQuery:
        """Fetches ALL guild commands.

        Returns:
            (JsonQuery): queried list of application commands
        """
        data = await self.http.request_list('GET', f"applications/{self.application_id}/guilds/{self.guild_id}/commands" )

        return JsonQuery(data)

    async def create(self, command: AnyCommand) -> JsonQuery:
        """Add a command to the client.

        !!! danger
            Creating a command with the same name as an existing command in the same scope will overwrite the old command.

        Args:
            command (AnyCommand): command to register

        Returns:
            (JsonQuery): created command
        """
        data = await self.http.request_json(
            'POST', 
            f"applications/{self.application_id}/guilds/{self.guild_id}/commands", 
            data=command.to_dict()
        )

        return JsonQuery(data)

    async def edit(self, command_id: Snowflake, **options: Unpack[EditGuildCommandParams]) -> JsonQuery:
        """Edit a command.

        Args:
            command_id (Snowflake): ID of command to edit
            options (EditGuildCommandParams): command fields to edit

        Returns:
            (JsonQuery): updated application command
        """
        data = await self.http.request_json(
            'PATCH', 
            f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{command_id}", 
            data=serialize(dict(options)) # nested objects in EditGuildCommandParams
        )

        return JsonQuery(data)

    async def delete(self, command_id: Snowflake) -> None:
        """Delete a command.

        Args:
            command_id (Snowflake): ID of command to delete
        """
        await self.http.request('DELETE', f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{command_id}")

    async def bulk_overwrite(self, commands: list[AnyCommand]) -> JsonQuery:
        """Takes a list of application commands, overwriting existing commands list for this guild. 
        
        !!! warning
            Commands that do not already exist will count toward daily application command create limits.

        !!! danger
            This will overwrite all types of application commands: slash commands, user commands, and message commands.

        Args:
            commands (list[AnyCommand]): commands to register

        Returns:
            (JsonQuery): created application commands
        """
        data = await self.http.request_list(
            'PUT', 
            f"applications/{self.application_id}/guilds/{self.guild_id}/commands", 
            data=[cmd.to_dict() for cmd in commands]
        )

        return JsonQuery(data)
