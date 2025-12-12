# scurrypy

from .client import Client

__all__ = [
    # top-level modules
    "Client"
]

# imports listed  __all__ libs
from .events import *
from .parts import *
from .resources import *
from .models import *
from .core import *
