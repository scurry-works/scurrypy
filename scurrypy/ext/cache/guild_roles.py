from scurrypy import Client, Addon, JsonQuery
from scurrypy.enums import EventType
from scurrypy.core import Snowflake, DiscordError

class GuildRoleCacheAddon(Addon):
    """Defines caching guild roles and lookup."""

    def __init__(self, client: Client):
        self.bot = client

        self.roles: dict[Snowflake, dict[Snowflake, JsonQuery]] = {} # stores OBJECTS
        self.role_index: dict[Snowflake, JsonQuery] = {} # stores REFERENCES

        client.add_event_listener(EventType.GUILD_CREATE, self.on_guild_create)
        client.add_event_listener(EventType.GUILD_DELETE, self.on_guild_delete)

        client.add_event_listener(EventType.ROLE_CREATE, self.on_role_create)
        client.add_event_listener(EventType.ROLE_UPDATE, self.on_role_update)
        client.add_event_listener(EventType.ROLE_DELETE, self.on_role_delete)

    async def on_guild_create(self, event: JsonQuery) -> None:
        """Append new guild roles to cache. Also add roles to index.

        Args:
            event (JsonQuery): the GUILD_CREATE event
        """
        id: Snowflake = event.get('id', t=Snowflake).value
        guild_dict = self.roles.setdefault(id, {})

        for role in event.get('roles').value:
            r = JsonQuery(role)
            role_id: Snowflake = r.get('id', t=Snowflake).value
            guild_dict[role_id] = r
            self.role_index[role_id] = r

    async def on_guild_delete(self, event: JsonQuery) -> None:
        """Remove guild roles from cache. Also remove roles from index

        Args:
            event (JsonQuery): the GUILD_DELETE event
        """
        id: Snowflake = event.get('id', t=Snowflake).value
        removed_roles = self.roles.pop(id, {})

        for role in removed_roles.values():
            role_id: Snowflake = role.get('id', t=Snowflake).value
            self.role_index.pop(role_id, None)

    async def on_role_create(self, event: JsonQuery) -> None:
        """Append role to guild key. Also append role to index.

        Args:
            event (JsonQuery): the ROLE_CREATE event
        """
        guild_id: Snowflake = event.get('guild_id', t=Snowflake).value
        guild_dict = self.roles.setdefault(guild_id, {})

        role_id: Snowflake = event.get('role.id', t=Snowflake).value
        guild_dict[role_id] = event
        self.role_index[role_id] = event

    async def on_role_update(self, event: JsonQuery) -> None:
        """Replace role in guild key. Also replace role in index.

        Args:
            event (JsonQuery): the ROLE_UPDATE event
        """
        guild_id: Snowflake = event.get('guild_id', t=Snowflake).value
        guild_dict = self.roles.setdefault(guild_id, {})

        role_id: Snowflake = event.get('role.id', t=Snowflake).value
        guild_dict[role_id] = event
        self.role_index[role_id] = event

    async def on_role_delete(self, event: JsonQuery) -> None:
        """Remove role from guild key. Also remove role from index.

        Args:
            event (JsonQuery): the ROLE_DELETE event
        """
        guild_id: Snowflake = event.get('guild_id', t=Snowflake).value
        role_id: Snowflake = event.get('role_id', t=Snowflake).value

        data = self.role_index.pop(role_id, None)
        if data is not None:
            self.roles.get(guild_id, {}).pop(role_id, None)
    
    async def get_role(self, guild_id: Snowflake, role_id: Snowflake) -> JsonQuery | None:
        """Fetch a guild role. If not found, request and store it.

        Args:
            guild_id (Snowflake): guild ID of role
            role_id (Snowflake): role ID of guild

        Returns:
            (JsonQuery | None): role object or None if fetch failed
        """
        role = self.role_index.get(role_id)
        if role is not None:
            return role
        
        try:
            role = await self.bot.guild(guild_id).fetch_role(role_id)
        except DiscordError:
            return None
        
        self.put(guild_id, role)
        return role

    def put(self, guild_id: Snowflake, role: JsonQuery) -> None:
        """Put a new role into the cache.

        Args:
            guild_id (Snowflake): guild ID of the role
            role (JsonQuery): the role object
        """
        guild_dict = self.roles.setdefault(guild_id, {})

        role_id: Snowflake = role.get('id', t=Snowflake).value
        guild_dict[role_id] = role
        self.role_index[role_id] = role
