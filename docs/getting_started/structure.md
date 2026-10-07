# ScurryPy Project Tree
---

This section details an exhaustive list of the project's possible and intended imports.

```py
from scurrypy import Client, Intents, Addon, JsonQuery

from scurrypy.bases import * # type markers

from scurrypy.enums import * # all enums

from scurrypy.core import * # core module (gateway, http, etc.)

from scurrypy.api import * # top level parts (object with no apparent domain)

from scurrypy.api.automod import * # auto moderation parts
from scurrypy.api.channels import * # channel parts
from scurrypy.api.commands import * # command parts 
from scurrypy.api.components import * # component parts
from scurrypy.api.guilds import * # guild parts
from scurrypy.api.messages import * # message model and parts

from scurrypy.resources import * # resources

from scurrypy.ext import * # currently convenience classes
from scurrypy.ext.cache import * # caching addons
from scurrypy.ext.commands import * # CommandsAddon and context
from scurrypy.ext.components import * # ComponentsAddon and context
from scurrypy.ext.events import * # EventsAddon
from scurrypy.ext.interactions import * # common context for interactions
from scurrypy.ext.prefixes import * # PrefixAddon and context
```
