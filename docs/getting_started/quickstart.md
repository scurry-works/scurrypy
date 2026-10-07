# Examples
---

The following examples use the `scurrypy.ext` module. 

## Basic Event
---
Demonstrates responding to the `READY` event.

```py
# --- Core library imports ---
from scurrypy import Client, JsonQuery
from scurrypy.enums import EventType

from scurrypy.ext.events import EventsAddon

# --- Setup bot and addons ---
client = Client(token=TOKEN)
events = EventsAddon(client)

# --- Register events ---
@events.listen(EventType.READY)
async def on_ready(bot: Client, event: JsonQuery):
    username: str = event.get('user.username').value
    print(f"{username} is online!")

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
from scurrypy import Client, Intents

from scurrypy.ext.prefixes import PrefixAddon, PrefixCommandContext

# --- Setup bot and addons ---
client = Client(token=TOKEN, intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT)
prefixes = PrefixAddon(client, APP_ID, '!')

# --- Register events ---
@prefixes.listen('ping')
async def on_ping(ctx: PrefixCommandContext):
    await ctx.send("Pong!")

# --- Run the bot ---
client.run()
```

## Basic Slash Command
---
Demonstrates registering and responding to a slash command interaction.

```py
# --- Core library imports ---
from scurrypy import Client

from scurrypy.ext.commands import CommandsAddon, ApplicationCommandContext

# --- Setup bot and addons ---
client = Client(token=TOKEN)
commands = CommandsAddon(client, APP_ID)

# --- Register events ---
@commands.slash_command('greet', 'Greet the bot!', guild_ids=[GUILD_ID])
async def on_greet(ctx: ApplicationCommandContext):
    await ctx.respond("Hello!")

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
from scurrypy import Client
from scurrypy.enums import ButtonStyle
from scurrypy.api.components import ActionRow, Button
from scurrypy.api.messages import MessagePart

from scurrypy.ext.commands import CommandsAddon, ApplicationCommandContext
from scurrypy.ext.components import ComponentsAddon, MessageComponentContext

# --- Setup bot and addons ---
client = Client(token=TOKEN)
commands = CommandsAddon(client, APP_ID)
components = ComponentsAddon(client)

# --- Register events ---
@commands.slash_command('button_demo', 'Button demo!', guild_ids=[GUILD_ID])
async def handle_command(ctx: ApplicationCommandContext):
    await ctx.respond(
        MessagePart(
            content='Press the button!',
            components=[
                ActionRow([
                    Button(ButtonStyle.PRIMARY, 'btn_demo', 'Press me!')
                ])
            ]
        )
    )

@components.button('btn_demo')
async def handle_button(ctx: MessageComponentContext):
    await ctx.update(content="You pressed the button!", components=[])

# --- Run the bot ---
client.run()
```

## Stateful Bot
---
Demonstrates grouping state and behavior using a class-based addon.

```py
# --- Core library imports ---
from scurrypy import Client

from scurrypy.ext.commands import CommandsAddon, ApplicationCommandContext

# --- Setup bot and addons ---
client = Client(token=TOKEN)
commands = CommandsAddon(client, APP_ID)

user_points = {}

import asyncio
dict_lock = asyncio.Lock()

# --- Register events ---
@commands.slash_command("points", "Check your points", guild_ids=[GUILD_ID])
async def points(ctx: ApplicationCommandContext):
    user_id = ctx.user.get('id', t=int).value
    async with dict_lock:
        pts = user_points.get(user_id, 0)

    await ctx.respond(f"You have {pts} points!")

@commands.slash_command("addpoints", "Give points", guild_ids=[GUILD_ID])
async def addpoints(ctx: ApplicationCommandContext):
    user_id = ctx.user.get('id', t=int).value
    async with dict_lock:
        user_points[user_id] = user_points.get(user_id, 0) + 1

    await ctx.respond("Point added!")

# --- Run the bot ---
client.run()
```

## Handling Command Errors
---
Demonstrates handling invalid user input inside a prefix command.

!!! tip
    By default, ScurryPy catches unhandled command errors and logs a traceback. 
    The bot will not crash.

```py
# --- Core library imports ---
from scurrypy import Client, Intents
from scurrypy.ext.prefixes import PrefixAddon, PrefixCommandContext

# --- Setup bot and addons ---
client = Client(token=TOKEN, intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT)
prefixes = PrefixAddon(client, APP_ID, '!')

# --- Register events ---
@prefixes.listen('divide')
async def divide(ctx: PrefixCommandContext):
    try:
        a = int(ctx.args[0])
        b = int(ctx.args[1])
        await ctx.send(f"{a}/{b} = {a/b:.2f}")
    except ZeroDivisionError:
        await ctx.send("The second value cannot be zero!")
    except IndexError:
        await ctx.send("This command requires 2 numbers! Try `!divide 6 3`")
    except ValueError:
        await ctx.send("Command args must be integers!")

# --- Run the bot ---
client.run()
```

## Role Restricted Command
---
Demonstrates a command needing a certain role to use.

```py
# --- Core library imports ---
from scurrypy import Client
from scurrypy.ext.commands import CommandsAddon, ApplicationCommandContext

# Set EXCLUSIVE_ROLE_ID to ID of role in which command is available.
EXCLUSIVE_ROLE_ID = 0

# --- Setup bot and addons ---
client = Client(token=TOKEN)
commands = CommandsAddon(client, APP_ID)

# --- Register events ---
@commands.slash_command('exclusive', 'Only certain roles can use this command!', guild_ids=[GUILD_ID])
async def on_exclusive(ctx: ApplicationCommandContext):
    member_roles = ctx.member.get('roles', t=list[int]).value

    if not EXCLUSIVE_ROLE_ID in member_roles:
        await ctx.respond(f"You need the <@&{EXCLUSIVE_ROLE_ID}> role to use this command!", ephemeral=True)
        return

    # ephemeral because its a secret!
    await ctx.respond("Welsh Myth Secret: Corgis were once ridden by fairies and elves!", ephemeral=True)

# --- Run the bot ---
client.run()
```

## Background Task
---
ScurryPy uses standard `asyncio` tasks for background jobs.

```py
# --- Core library imports ---
from scurrypy import Client

# --- Setup bot ---
client = Client(token=TOKEN)

import asyncio

# --- Register events ---
async def my_task():
    while True:
        print("Running background task...")
        await asyncio.sleep(5)

async def start_my_task():
    asyncio.create_task(my_task())

client.add_startup_hook(start_my_task)

# --- Run the bot ---
client.run()
```

## Modals
---
Demonstrates submitting feedback with the modal.

```py
# --- Core library imports ---
from scurrypy import Client
from scurrypy.enums import TextInputStyle
from scurrypy.api.components import Label, TextInput, ModalPart

from scurrypy.ext.commands import CommandsAddon, ApplicationCommandContext
from scurrypy.ext.components import ComponentsAddon, ComponentModalContext

# --- Setup bot and addons ---
client = Client(token=TOKEN)
commands = CommandsAddon(client, APP_ID, False)
components = ComponentsAddon(client)

# --- Register events ---
@components.modal("feedback_modal")
async def on_feedback(ctx: ComponentModalContext):
    feedback = ctx.get_modal_value("feedback_input")
    await ctx.respond(f"Thanks for your feedback:\n{feedback}", ephemeral=True)

@commands.slash_command("feedback", "Send feedback", guild_ids=[GUILD_ID])
async def feedback(ctx: ApplicationCommandContext):

    feedback_input = Label(
        label="Your feedback",
        component=TextInput(
            custom_id="feedback_input",
            style=TextInputStyle.PARAGRAPH,
            placeholder="Type something...",
            required=True
        )
    )

    modal = ModalPart(
        title="Feedback Form",
        custom_id="feedback_modal",
        components=[feedback_input]
    )

    await ctx.respond_modal(modal)

# --- Run the bot ---
client.run()
```

## More Examples...
---

Want more control?
Check out [core examples](core_examples.md).

Want more customization? 
Check out using [Addons](addons.md).

Ready for a challenge?
Check out [advanced patterns](advanced.md).
