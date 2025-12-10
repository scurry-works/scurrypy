from ..addon import Addon
from ...client import Client

from ...models import *
from ...events import *

class RoleCacheAddon(Addon):
    """Defines caching guild roles and lookup."""

    def __init__(self, client: Client):
        self.bot = client

        self.roles: dict[int, dict[int, RoleModel]] = {} # stores OBJECTS
        self.role_index: dict[int, RoleModel] = {} # stores REFERENCES

        client.addons.add(self)

    def setup(self):
        self.bot.add_startup_hook(self.on_startup)

    def on_startup(self):
        self.bot.add_event_listener('GUILD_CREATE', self.on_guild_create)
        self.bot.add_event_listener('GUILD_DELETE', self.on_guild_delete)

        self.bot.add_event_listener('ROLE_CREATE', self.on_role_create)
        self.bot.add_event_listener('ROLE_UPDATE', self.on_role_update)
        self.bot.add_event_listener('ROLE_DELETE', self.on_role_delete)

    def on_guild_create(self, event: GuildCreateEvent):
        """Append new guild roles to cache. Also add roles to index.

        Args:
            event (GuildCreateEvent): the GUILD_CREATE event
        """
        guild_dict = self.roles.setdefault(event.id, {})

        for role in event.roles:
            guild_dict[role.id] = role
            self.role_index[role.id] = role

    def on_guild_delete(self, event: GuildDeleteEvent):
        """Remove guild roles from cache. Also remove roles from index

        Args:
            event (GuildDeleteEvent): the GUILD_DELETE event
        """
        removed_roles = self.roles.pop(event.id, {})

        for role in removed_roles.values():
            self.role_index.pop(role.id, None)

    def on_role_create(self, event: RoleCreateEvent):
        """Append role to guild key. Also append role to index.

        Args:
            event (RoleCreateEvent): the ROLE_CREATE event
        """
        model = RoleModel.from_dict(event.raw)
        guild_dict = self.roles.setdefault(event.guild_id, {})

        guild_dict[event.role.id] = model
        self.role_index[event.role.id] = model

    def on_role_update(self, event: RoleUpdateEvent):
        """Replace role in guild key. Also replace role in index.

        Args:
            event (RoleUpdateEvent): the ROLE_UPDATE event
        """
        model = RoleModel.from_dict(event.raw)
        guild_dict = self.roles.setdefault(event.guild_id, {})

        guild_dict[event.role.id] = model
        self.role_index[event.role.id] = model

    def on_role_delete(self, event: RoleDeleteEvent):
        """Remove role from guild key. Also remove role from index.

        Args:
            event (RoleDeleteEvent): the ROLE_DELETE event
        """
        model = self.role_index.pop(event.role_id, None)
        if model:
            self.roles.get(event.guild_id, {}).pop(event.role_id, None)

    def get_role(self, role_id: int):
        """Get a role from the cache.

        Args:
            role_id (int): ID of the role

        Returns:
            (RoleModel | None): the role object if found else None
        """
        return self.role_index.get(role_id)

    def put(self, guild_id: int, role: RoleModel):
        """Put a new role into the cache.

        Args:
            guild_id (int): guild ID of the role
            role (RoleModel): the role object
        """
        guild_dict = self.roles.setdefault(guild_id, {})
        guild_dict[role.id] = role
        self.role_index[role.id] = role
