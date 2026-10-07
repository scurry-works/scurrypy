# Advanced Patterns and Experiments
---

This section covers features that may not be immediately obvious to power users.
Additionally, this section will showcase how customizable ScurryPy is.

## Using HTTP directly
---
ScurryPy exposes its HTTP layer via [`HttpClient`][scurrypy.core.http.HttpClient] for public consumption.
This layer handles rate limiting and still adheres to Discord's spec requirements.
This feature is useful for accessing endpoints that may not be exposed through ScurryPy's public interface.

Demonstrates using ScurryPy's HTTP client directly:

```py
from scurrypy import Client, JsonQuery
from scurrypy.enums import EventType

client = Client(token=TOKEN)

async def on_ready(event):
    data = await client.http.request_json('GET', f'/users/{APP_ID}')

    user = JsonQuery(data)

    print(user.data)

client.add_event_listener(EventType.READY, on_ready)

client.run()
```

## Command Registration
---
See the [`scurrypy.ext.commands`][scurrypy.ext.commands.addon] pattern.

## Caching
---
See the [`scurrypy.ext.cache.channels`][scurrypy.ext.cache.channels] pattern.

## Running Two Bots In One Process
---
Demonstrates running two separate bots on the same process.

```py
from scurrypy import Client, JsonQuery
from scurrypy.enums import EventType

class Bot:
    def __init__(self, token: str):
        self.bot = Client(token=token)
        self.bot.add_event_listener(EventType.READY, self.on_ready)
        self.task = asyncio.create_task(self.bot.start())

    async def on_ready(self, event: JsonQuery):
        username: str = event.get('user.username').value
        print(f"{username} is ready!")

import asyncio

async def main():
    try:
        await asyncio.gather(*(Bot(t).task for t in TOKENS))
    except asyncio.CancelledError:
        print("Bots are shutting down...")

asyncio.run(main())
```

## Integrating External Services
---
Demonstrates an example DB addon.

```py
from scurrypy import Client

import asyncpg

class PostgresDB:
    def __init__(self, client: Client, user: str, database: str, password: str):
        self.bot = client

        from urllib.parse import quote

        self.dsn = f"postgresql://{user}:{quote(password)}@localhost:5432/{database}"
        self.pool: asyncpg.Pool = None
    
        client.add_startup_hook(self.start_db)
        client.add_shutdown_hook(self.close_db)

    async def start_db(self):
        self.pool = await asyncpg.create_pool(self.dsn)
    
    async def close_db(self):
        await self.pool.close()

    async def get_connection(self) -> asyncpg.Connection:
        return await self.pool.acquire()
```

## Stress Testing
---

Curious to know how ScurryPy handles high traffic? ScurryPy can handle abuse without getting Discord angry.

This example creates `C_COUNT` channels, sends `M_COUNT` messages to each channel, and edits each message for maximum spam!

**Notice:** Not one rate limit error!

!!! danger
    This example should NOT be run in a public server.

    Consider running it in a server with just you and the bot!

```py
from scurrypy import Client, JsonQuery
from scurrypy.enums import EventType
from scurrypy.resources import Channel

import asyncio

client = Client(token=TOKEN)

M_COUNT = 30
C_COUNT = 4

async def spam_messages(channel: Channel):
    for i in range(M_COUNT):
        msg = await channel.send(f'Testing {i}!')
        msg_id = msg.get('id', t=int).value
        channel_id = msg.get('channel_id', t=int).value
        await client.message(channel_id, msg_id).edit(content='Edited!')

async def on_test(event: JsonQuery):
    for i in range(C_COUNT):
        ch = await client.guild(GUILD_ID).create_channel(...)
        channel_id = ch.get('channel_id', t=int).value
        asyncio.create_task(spam_messages(client.channel(channel_id)))

client.add_event_listener(EventType.READY, on_test)

client.run()
```
