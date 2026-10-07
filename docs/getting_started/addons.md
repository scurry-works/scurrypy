# Addon Examples
---
The following examples demonstrate the idiomatic and recommended patterns when extending ScurryPy.

!!! important "Setting Up"
    These examples assume you've already seen [Setting Up](start_here.md).

## Minimal Event Listener
---
Drop-in example demonstrating listening for the `READY` event.

```py
from scurrypy import Client, Addon, JsonQuery
from scurrypy.enums import EventType

class MyAddon(Addon):
    def __init__(self, client: Client):
        self.bot = client
        client.add_event_listener(EventType.READY, self.on_ready)

    async def on_ready(self, event: JsonQuery):
        print("Bot is ready!")

client = Client(token=TOKEN)
MyAddon(client)

client.run()
```

## Minimal Addon
---
Demonstrates addon setup. Feel free to use this as a reference!

!!! warning "ScurryPy's Contract"
    ScurryPy validates handler signatures at registration time, catching errors before your bot runs. 
    Each registration method expects specific parameters:

    * `client.add_event_listener` → `def handler(self, event)` (sync or async)
    * `client.add_startup_hook` → `def handler(self)` (sync or async)
    * `client.add_shutdown_hook` → `def handler(self)` (sync or async)
    
    If signatures don't match, ScurryPy raises an error immediately. 
    This prevents bugs from reaching production!

```py
from scurrypy import Client, Addon, JsonQuery
from scurrypy.enums import EventType

class MyAddon(Addon):
    """Your custom addon."""

    def __init__(self, client: Client):
        self.bot = client

        # register handlers - validated immediately!
        client.add_startup_hook(self.my_opening_handler)
        client.add_event_listener(EventType.EVENT, self.my_event_listener)
        client.add_shutdown_hook(self.my_closing_handler)

    def my_opening_handler(self):  # can be sync or async
        """Custom startup hooks."""

    async def my_event_listener(self, event: JsonQuery):
        """Handle your event here!"""

    def my_closing_handler(self):
        """Custom shutdown hooks."""
```

!!! tip "About Addons"
    Addons only add convenient patterns and never change the Discord API itself.
    You can optionally use [`Addon`][scurrypy.bases.addon.Addon] as a marker or typing convenience.

## Event Routing
---
Demonstrates listening to multiple events in one addon.

```py
from scurrypy import Client, Addon, JsonQuery
from scurrypy.enums import EventType

class MyAddon(Addon):
    def __init__(self, client: Client):
        self.bot = client

        client.add_event_listener(EventType.GUILD_CREATE, self.on_guild_create)
        client.add_event_listener(EventType.GUILD_DELETE, self.on_guild_delete)

        client.add_event_listener(EventType.CHANNEL_CREATE, self.on_channel_create)
        client.add_event_listener(EventType.CHANNEL_UPDATE, self.on_channel_update)
        client.add_event_listener(EventType.CHANNEL_DELETE, self.on_channel_delete)

    def on_guild_create(self, event: JsonQuery):
        """Handle something on guild create."""

    def on_guild_delete(self, event: JsonQuery):
        """Handle something on guild delete."""

    def on_channel_create(self, event: JsonQuery):
        """Handle something on channel create."""

    def on_channel_update(self, event: JsonQuery):
        """Handle something on channel update."""

    def on_channel_delete(self, event: JsonQuery):
        """Handle something on channel delete."""
```

## Upgrading Events to Resources
---
Demonstrates upgrading an interaction and message event to their respective resources for more convenient use.

```py
from scurrypy import Client, Addon, JsonQuery
from scurrypy.resources import Interaction, Channel

class ResourceFromEventAddon(Addon):
    def __init__(self, client: Client):
        self.bot = client

    def interaction(self, event: JsonQuery):
        id = event.get('id', t=int).value
        token = event.get('token').value
        return Interaction(
            http=self.bot.http,
            id=id,
            token=token,
        )

    def channel(self, event: JsonQuery):
        channel_id = event.get('channel_id', t=int).value
        return Channel(
            http=self.bot.http,
            id=channel_id,
        )
```
