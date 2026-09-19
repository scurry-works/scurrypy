<div align='center'>

## ScurryPy

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)
[![Discord](https://img.shields.io/discord/905167903224123473?style=plastic&logo=discord&logoColor=ffffff&color=5865F2)](https://discord.gg/D4SdHxcujM)

<img
src="assets/banner.png"
width="450"
alt="Fire-breathing squirrel"
/>

✨ **Clarity over magic**: build a bot that lasts ✨

</div>

> **Development Note:** ScurryPy remains actively maintained, with ongoing updates and improvements.

## Features

* Lightweight core
* Strictly typed
* Rate limit handling
* Automatic session & gateway management
* Automatic sharding
* Predictable event models and resource classes

Your focus is building what you want instead of fighting a framework.

ScurryPy is a stability-first Discord runtime built around explicit API coverage and strict scope boundaries to minimize long-term breakage.

## Installation

Install ScurryPy with pip:

```bash
pip install scurrypy
```

## Examples

The following examples are quick drop-in starters if you wish to try ScurryPy.

> [!TIP]
> It is recommended to use a `.env` file for bot tokens. More details about using a `.env` file [here](https://scurry-works.github.io/scurrypy/getting_started/start_here/).

### Slash Command

```python
# Set TOKEN, APP_ID (bot user ID), and GUILD_ID (for guild command)

# --- Core library imports ---
from scurrypy import Client

from scurrypy.ext.commands import CommandsAddon, ApplicationCommandContext

# --- Setup bot ---
client = Client(token=TOKEN)
commands = CommandsAddon(client, APP_ID)

@commands.slash_command('greet', 'Greet the bot!', guild_ids=[GUILD_ID])
async def on_greet(ctx: ApplicationCommandContext):
    await ctx.respond("Hello!")

# --- Run the bot ---
client.run()
```

### Prefix Command (Legacy)

```python
# Set TOKEN and APP_ID (bot user ID)

# --- Core library imports ---
from scurrypy import Client, Intents

from scurrypy.ext.prefixes import PrefixAddon, PrefixCommandContext

client = Client(token=TOKEN, intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT)
prefixes = PrefixAddon(client, APP_ID, '!')

# --- Setup bot ---
@prefixes.listen('ping')
async def on_ping(ctx: PrefixCommandContext):
    await ctx.send("Pong!")

# --- Run the bot ---
client.run()
```

## Dependencies

ScurryPy has exactly 3 required dependencies:
- aiohttp (HTTP client)
- websockets (Gateway connection)  
- aiofiles (Async file operations)

These dependencies are automatically installed with ScurryPy's pip package.

## Learn More

Explore the full [documentation](https://scurry-works.github.io/scurrypy) for more examples, guides, and API reference.

See the [manifesto](https://scurry-works.github.io/scurrypy/manifesto) section for details!

**Got some questions?**
Check out the [FAQ](https://scurry-works.github.io/scurrypy/faq) page for commonly asked questions!

**Looking for changes?** 
See the [Changelog](https://github.com/scurry-works/scurrypy/blob/main/CHANGELOG.md).
