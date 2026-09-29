from scurrypy import Client, Addon
from scurrypy.enums import EventType
from scurrypy.core import Snowflake, DiscordError
from scurrypy.api.guilds import GuildRoleModel
from scurrypy.events import (
    GuildCreateEvent, 
    GuildDeleteEvent, 
    RoleCreateEvent, 
    RoleUpdateEvent, 
    RoleDeleteEvent
)

class GuildRoleCacheAddon(Addon):
    """Defines caching guild roles and lookup."""

    def __init__(self, client: Client):
        self.bot = client

        self.roles: dict[Snowflake, dict[Snowflake, GuildRoleModel]] = {} # stores OBJECTS
        self.role_index: dict[Snowflake, GuildRoleModel] = {} # stores REFERENCES

        client.add_event_listener(EventType.GUILD_CREATE, self.on_guild_create)
        client.add_event_listener(EventType.GUILD_DELETE, self.on_guild_delete)

        client.add_event_listener(EventType.ROLE_CREATE, self.on_role_create)
        client.add_event_listener(EventType.ROLE_UPDATE, self.on_role_update)
        client.add_event_listener(EventType.ROLE_DELETE, self.on_role_delete)

    async def on_guild_create(self, event: GuildCreateEvent) -> None:
        """Append new guild roles to cache. Also add roles to index.

        Args:
            event (GuildCreateEvent): the GUILD_CREATE event
        """
        guild_dict = self.roles.setdefault(event.id, {})

        for role in event.roles:
            guild_dict[role.id] = role
            self.role_index[role.id] = role

    async def on_guild_delete(self, event: GuildDeleteEvent) -> None:
        """Remove guild roles from cache. Also remove roles from index

        Args:
            event (GuildDeleteEvent): the GUILD_DELETE event
        """
        removed_roles = self.roles.pop(event.id, {})

        for role in removed_roles.values():
            self.role_index.pop(role.id, None)

    async def on_role_create(self, event: RoleCreateEvent) -> None:
        """Append role to guild key. Also append role to index.

        Args:
            event (RoleCreateEvent): the ROLE_CREATE event
        """
        model = GuildRoleModel.from_dict(event.raw)
        guild_dict = self.roles.setdefault(event.guild_id, {})

        guild_dict[event.role.id] = model
        self.role_index[event.role.id] = model

    async def on_role_update(self, event: RoleUpdateEvent) -> None:
        """Replace role in guild key. Also replace role in index.

        Args:
            event (RoleUpdateEvent): the ROLE_UPDATE event
        """
        model = GuildRoleModel.from_dict(event.raw)
        guild_dict = self.roles.setdefault(event.guild_id, {})

        guild_dict[event.role.id] = model
        self.role_index[event.role.id] = model

    async def on_role_delete(self, event: RoleDeleteEvent) -> None:
        """Remove role from guild key. Also remove role from index.

        Args:
            event (RoleDeleteEvent): the ROLE_DELETE event
        """
        model = self.role_index.pop(event.role_id, None)
        if model:
            self.roles.get(event.guild_id, {}).pop(event.role_id, None)
    
    async def get_role(self, guild_id: Snowflake, role_id: Snowflake) -> GuildRoleModel | None:
        """Fetch a guild role. If not found, request and store it.

        Args:
            guild_id (Snowflake): guild ID of role
            role_id (Snowflake): role ID of guild

        Returns:
            (GuildRoleModel | None): hydrated role object or None if fetch failed
        """
        role = self.role_index.get(role_id)
        if role:
            return role
        
        try:
            role = await self.bot.guild(guild_id).fetch_role(role_id)
        except DiscordError:
            return None
        
        self.put(guild_id, role)
        return role

    def put(self, guild_id: Snowflake, role: GuildRoleModel) -> None:
        """Put a new role into the cache.

        Args:
            guild_id (Snowflake): guild ID of the role
            role (GuildRoleModel): the role object
        """
        guild_dict = self.roles.setdefault(guild_id, {})
        guild_dict[role.id] = role
        self.role_index[role.id] = role
