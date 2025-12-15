## <center> ScurryPy </center>

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)
[![Discord](https://img.shields.io/discord/905167903224123473?style=plastic&logo=discord&logoColor=ffffff&color=5865F2)](https://discord.gg/D4SdHxcujM)

ScurryPy is a lightweight, modern Discord API wrapper powering all kinds of squirrel-related shenanigans, from tiny bots to full custom frameworks.

## Philosophy

ScurryPy is built on a one idea:
✨*clarity over magic* ✨

* Every operation is explicit
* No hidden behavior or black boxes
* Components do *one* job and do it predictably

ScurryPy is not discord.py, hikari, disnake, or any existing framework.
ScurryPy is a minimal, transparent, and modern wrapper around Discord's REST and Gateway API, built completely from scratch.

If you want to understand your bot rather than fight it, you're in the right place.

## Framework Features

The following are baked into ScurryPy:

* Lightweight core (<1000 lines)
* Proper rate limit handling
* Automatic session + gateway reconnection logic
* Automatic sharding
* Predictable event models and resource classes

Addons and user code never need to reimplement these.

ScurryPy exposes clean primitives. What you build on top is entirely up to you, from bots to full frameworks.

## ScurryKit

Looking for a higher-level experience similar to discord.py, hikari, or nextcord?
Check out [ScurryKit](https://github.com/scurry-works/scurry-kit), a batteries-included framework built on top of ScurryPy.

## Installation

Install ScurryPy with pip:

```bash
pip install scurrypy
```

## Like What You See?

Explore the full [documentation](https://scurry-works.github.io/scurrypy) for more examples, guides, and API reference.
