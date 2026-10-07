# Getting Started
---

This page will help you install ScurryPy, set up your environment, and get ready to build your first bot.

## Installation
---
If you haven't already, you can install ScurryPy with pip:

```bash
pip install scurrypy
```

That's all you need. No extra dependencies.

## Setting up
---
In your main bot file, it's recommended to load your environment variables and prepare your constants:

```py
# --- Environment setup ---
import os
from dotenv import load_dotenv
load_dotenv()

# Replace with your bot token, application ID, and guild ID (optional, for guild commands)
TOKEN = os.getenv("BOT_TOKEN")
APP_ID = 0
GUILD_ID = 0
```

!!! tip
    If you use `dotenv`, you need to install it using:

    ```bash
    pip install dotenv
    ```

    Or store it anywhere you like that is not directly in your bot code.

## Logging
---
Scurrypy uses Python's standard `logging` module.

**Scurrypy does not configure logging by default.**
If you do not configure logging in your application, Scurrypy log messages will be discarded.

All loggers use the `scurrypy` namespace.

The following snippet can be used to enable logging with colored output:

!!! tip
    If you use `rich.logging`, you need to install it using:

    ```bash
    pip install rich
    ```

```py
import logging
from rich.logging import RichHandler

logger = logging.getLogger("scurrypy")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(show_path=False, rich_tracebacks=True)],
)

# normal library usage
```

You're now ready to start using ScurryPy!

## Next Steps...
---

* [Mindset](mindset.md) - ScurryPy acknowledges it operates differently from other frameworks. See this page to help conceptualize the library.
* [Examples](quickstart.md) - first steps to using ScurryPy
* [API](../api/index.md) - detailed class and method documentation
