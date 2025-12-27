## ScurryPy

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)
[![Discord](https://img.shields.io/discord/905167903224123473?style=plastic&logo=discord&logoColor=ffffff&color=5865F2)](https://discord.gg/D4SdHxcujM)

ScurryPy is a fully extensible foundation for Discord bots and frameworks. 
Build anything from a simple bot to a complete custom framework, with the architecture entirely up to you.

> **Tip**: *Think of ScurryPy like a sandbox for Discord’s API: a reliable foundation where you control everything you build.*

## Philosophy

ScurryPy is built on one idea:
✨*clarity over magic* ✨

* Every operation is explicit
* No hidden behavior or black boxes
* Components do *one* job and do it predictably

This philosophy ensures that you can extend, compose, and control every part of your bot without hidden surprises.

If you want to understand your bot rather than fight it, you're in the right place.

## Features

The following are baked into ScurryPy:

* Lightweight core
* Rate limit handling
* Automatic session & gateway management
* Automatic sharding
* Predictable event models and resource classes

Your focus is building what you want.

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
Check out the [Migration Guide](https://scurry-works.github.io/scurrypy/migrating/) to see the difference.
