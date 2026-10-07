# Core Examples
---

This section details examples using ScurryPy without `scurrypy.ext`.

!!! important
    These examples assume you have ScurryPy set up.

    If you've missed this part, it is recommended to start [here](start_here.md).

## Basic Event
---
Demonstrates responding to the `READY` event.

```py
# --- Core library imports ---
from scurrypy import Client, JsonQuery
from scurrypy.enums import EventType

# --- Setup bot ---
client = Client(token=TOKEN)

async def on_ready(event: JsonQuery):
    name: str = event.get('user.username').value
    print(f"{name} is online!")

client.add_event_listener(EventType.READY, on_ready)

# --- Run the bot ---
client.run()

```

## Basic Prefix Command
---
Demonstrates registering and responding to a prefix command.

!!! warning "Legacy"
    While prefix commands are supported, they are deemed a legacy feature.

    Discord encourages using interactions. See the next example.

```py
# --- Core library imports ---
from scurrypy import Client, Intents, JsonQuery
from scurrypy.enums import EventType

client = Client(token=TOKEN, intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT)

# --- Setup bot ---
async def on_ping(event: JsonQuery):

    content: str = event.get('content').value

    if not content:
        return

    if not content.startswith('!ping'):
        return

    event_id: int = event.get('channel_id', t=int).value

    await client.channel(event_id).send("Pong!")

client.add_event_listener(EventType.MESSAGE_CREATE, on_ping)

# --- Run the bot ---
client.run()
```

## Basic Slash Command
---
Demonstrates registering and responding to a slash command interaction.

```py
# --- Core library imports ---
from scurrypy import Client, JsonQuery
from scurrypy.api.commands import SlashCommandPart
from scurrypy.enums import EventType, InteractionType

# --- Setup bot ---
client = Client(token=TOKEN)

async def register_commands():
    """Register slash commands on startup (before READY)."""
    await client.guild_command(APP_ID, GUILD_ID).create(
        SlashCommandPart("greet", "Greet the bot!")
    )

client.add_startup_hook(register_commands)

async def on_greet(event: JsonQuery):
    """Respond to /greet"""

    interaction_type: InteractionType = event.get('type', t=InteractionType).value

    if interaction_type != InteractionType.APPLICATION_COMMAND:
        return # ignore non-command interactions

    name: str = event.get('data.name').value

    if name != "greet":
        return

    event_id = event.get('id', t=int).value
    event_token = event.get('token').value
    await client.interaction(event_id, event_token).respond("Hello!")

client.add_event_listener(EventType.INTERACTION_CREATE, on_greet)

# --- Run the bot ---
client.run()
```

!!! tip "About guild commands"
    **Guild commands** appear instantly when registered to a guild.
    
    **Global commands** can take up to 1 hour to propagate.


## Component Interactions
---
Demonstrates building and responding to a button interaction.

```py
# --- Core library imports ---
from scurrypy import Client, JsonQuery

from scurrypy.api.commands import SlashCommandPart
from scurrypy.api.components import ActionRow, Button
from scurrypy.api.messages import MessagePart

from scurrypy.resources import Interaction
from scurrypy.enums import EventType, ButtonStyle, InteractionType

# --- Setup bot ---
client = Client(token=TOKEN)

async def register_commands():
    """Register slash commands on startup (before READY)."""
    await client.guild_command(APP_ID, GUILD_ID).create(
        SlashCommandPart('button_demo', 'A command with a button!')
    )

client.add_startup_hook(register_commands)

async def handle_command(interaction: Interaction, event: JsonQuery):
    """Handle button_demo slash command."""

    name: str = event.get('data.name').value

    if name != 'button_demo':
        return

    await interaction.respond(
        MessagePart(
            content='Press the button!',
            components=[
                ActionRow([
                    Button(ButtonStyle.PRIMARY, 'btn_demo', 'Press me!')
                ])
            ]
        )
    )

async def handle_button(interaction: Interaction, event: JsonQuery):
    """Handle btn demo custom ID."""

    custom_id: str = event.get('data.custom_id').value

    if custom_id != 'btn_demo':
        return

    await interaction.update(content="You pressed the button!", components=[])

async def dispatch(event: JsonQuery):
    """InteractionEvent is automatically resolved into a concrete interaction type."""

    event_id = event.get('id', t=int).value
    event_token = event.get('token').value

    interaction = client.interaction(event_id, event_token)
    interaction_type = event.get('type', t=InteractionType).value

    if interaction_type == InteractionType.APPLICATION_COMMAND:
        await handle_command(interaction, event)
    elif interaction_type == InteractionType.MESSAGE_COMPONENT:
        await handle_button(interaction, event)

client.add_event_listener(EventType.INTERACTION_CREATE, dispatch)

# --- Run the bot ---
client.run()
```

!!! tip "Need to Refresh Your Commands?"
    Consider deleting your old commands before registering new ones:
    ```py
    async def refresh_commands():
        commands = await client.command(APP_ID, GUILD_ID).fetch_all()

        for cmd in commands:
            await client.command(APP_ID, GUILD_ID, cmd.id).delete()
        
        # then create your new commands
    
    client.add_startup_hook(refresh_commands)
    ...
    ```
    If you are using `scurrypy.ext`, this should be done for you.

## Stateful Bot
---
Demonstrates grouping state and behavior using a class-based addon.

```py
# --- Core library imports ---
from scurrypy import Client, JsonQuery
from scurrypy.api.commands import SlashCommandPart
from scurrypy.enums import EventType, InteractionType

import asyncio

class StatefulBot:
    def __init__(self, client: Client):
        self.bot = client

        # user registry
        self.user_points = {}
        self.dict_lock = asyncio.Lock()

        # commands registry
        self.commands = {
            'points': self.on_points,
            'addpoints': self.on_add_points
        }

        # hook up addon to client
        client.add_startup_hook(self.register_commands)
        client.add_event_listener(EventType.INTERACTION_CREATE, self.dispatch)

    async def register_commands(self):
        """Register slash commands on startup (before READY)."""
        bot_commands = self.bot.guild_command(APP_ID, GUILD_ID)
        commands = [
            SlashCommandPart('points', 'Check your points'),
            SlashCommandPart('addpoints', 'Give points')
        ]

        for cmd in commands:
            await bot_commands.create(cmd)

    async def on_points(self, event: JsonQuery):
        """Get points for the invoking user."""

        user_id: int = event.get('member.user.id', t=int).value

        async with self.dict_lock:
            pts = self.user_points.get(user_id, 0)

        event_id = event.get('id', t=int).value
        event_token = event.get('token').value

        await self.bot.interaction(event_id, event_token).respond(f"You have {pts} points!")

    async def on_add_points(self, event: JsonQuery):
        """Add points for the invoking user."""

        user_id: int = event.get('member.user.id', t=int).value

        async with self.dict_lock:
            self.user_points[user_id] = self.user_points.get(user_id, 0) + 1

        event_id = event.get('id', t=int).value
        event_token = event.get('token').value

        await self.bot.interaction(event_id, event_token).respond("Point added!")

    async def dispatch(self, event: JsonQuery):
        """Main entry point for commands."""

        interaction_type = event.get('type').transform(InteractionType).value

        if interaction_type != InteractionType.APPLICATION_COMMAND:
            return # ignore non-command interactions

        name: str = event.get('data.name').value

        handler = self.commands.get(name)

        event_id = event.get('id', t=int).value
        event_token = event.get('token').value

        if not handler:
            await self.bot.interaction(event_id, event_token).respond(f"No command named '{name}'!")
            return

        await handler(event)

client = Client(token=TOKEN)

# attach addon to client
StatefulBot(client)

# --- Run the bot ---
client.run()
```
