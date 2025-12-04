## __<center> ScurryPy </center>__

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)

A lightweight, fully readable Discord API framework built to accommodate everything from basic bots to custom frameworks.

While ScurryPy powers many squirrel-related shenanigans, it works just as well for game bots, interactive components, and educational projects.

## Philosophy

ScurryPy is built on a simple idea: clarity over magic.

* Every operation should be traceable.
* No hidden behavior or side effects.
* Explicit design over clever abstractions.
* If you can’t explain a function in 3–6 steps, simplify it.
* Legacy features can be removed or replaced without rewriting the library.
* Models = pure data
* Resources = HTTP logic
* Nothing mixes responsibilities.

ScurryPy is not discord.py, hikari, disnake, or any other framework.
ScurryPy is built from scratch.
It is a true Discord API wrapper built on predictable, modern Python principles.

## Features
* Easy to extend and build frameworks on top
* Lightweight core (<1000 lines)
* Command, and event handling
* Unix shell-style wildcards for component routing
* Declarative style using decorators
* Supports both legacy and new features
* Respects Discord's rate limits
* No `__future__` hacks to avoid circular import
* Capable of sharding

## Getting Started

*Note: This section also appears in the documentation, but here are complete examples ready to use with your bot credentials.*

### Installation

To install the ScurryPy package, run:

```bash
pip install scurrypy
```

> **About the Following Examples**:
    These examples are built using [EasyBot](https://scurry-works.github.io/scurrypy/addons/easy_bot), an extension of ScurryPy designed with pre-packaged convenience!

## Minimal Slash Command

The following demonstrates building and responding to a slash command.

```py
import scurrypy 
from scurrypy.addons.easy_bot import EasyBot

client = EasyBot(token=TOKEN, application_id=APP_ID)

@client.slash_command("hello", "Say hello", guild_ids=GUILD_ID) # specify guild ID for guild command
async def hello(bot, interaction: scurrypy.Interaction):
    await interaction.respond("Hello!")

client.run()
```

## Minimal Prefix Command (Legacy)

The following demonstrates building and responding to a message prefix command.

```py
import scurrypy 
from scurrypy.addons.easy_bot import EasyBot

client = EasyBot(token=TOKEN, application_id=APP_ID, prefix="!")

@client.prefix("ping")
async def ping_cmd(bot, message: scurrypy.Message):
    await message.send("Pong!")

client.run()
```

## Building on Top of ScurryPy

ScurryPy is designed to be easy to extend with your own abstractions.
See [Addons](https://scurry-works.github.io/scurrypy/addons) documentation for details!

## Like What You See?
Explore the full [documentation](https://scurry-works.github.io/scurrypy) for more examples, guides, and API reference.
