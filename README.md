<div align='center'>

## ScurryPy

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)
[![Discord](https://img.shields.io/discord/905167903224123473?style=plastic&logo=discord&logoColor=ffffff&color=5865F2)](https://discord.gg/D4SdHxcujM)

✨ **Clarity over magic**: a sandbox for Discord's API where you control everything ✨

ScurryPy is a fully extensible foundation for building bots, frameworks, and tools. You design the architecture.

</div>

## Features

The following are baked into ScurryPy:

* Lightweight core
* Rate limit handling
* Automatic session & gateway management
* Automatic sharding
* Predictable event models and resource classes

Your focus is building what you want.

## Who ScurryPy is for

ScurryPy is for developers who want full control of Discord API usage, design their own frameworks, or learn how bots work under the hood. If you want ready-made commands, consider using ScurryKit or another framework.

## Installation

Install ScurryPy with pip:

```bash
pip install scurrypy
```

## Quick Start

```python
# --- Core library imports ---
from scurrypy import Client, ReadyEvent

# --- Setup bot ---
client = Client(token=TOKEN)

async def on_ready(event: ReadyEvent):
    print("Bot is online!")

client.add_event_listener("READY", on_ready)

# --- Run the bot ---
client.run()
```

## What You Can Build

ScurryPy's clean architecture supports:
- Custom command frameworks
- Multi-bot orchestration systems
- Discord API explorers and tools
- Bots with complex state management
- Your own discord.py alternative

Check out [ScurryKit](https://github.com/scurry-works/scurry-kit) - 
a batteries-included framework built entirely on ScurryPy.

## Dependencies

ScurryPy has exactly 3 required dependencies:
- aiohttp (HTTP client)
- websockets (Gateway connection)  
- aiofiles (Async file operations)

That's it. No bloat, no surprises, no supply-chain concerns.
These dependencies are automatically installed with ScurryPy's pip package.

## Like What You See?

Explore the full [documentation](https://scurry-works.github.io/scurrypy) for more examples, guides, and API reference.

**Switching from discord.py?** 
Check out the [Migration Guide](https://scurry-works.github.io/scurrypy/migrating) to see the difference.

**Got some questions?**
Check out the [FAQ](https://scurry-works.github.io/scurrypy/faq) page for commonly asked questions!
