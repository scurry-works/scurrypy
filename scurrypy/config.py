import sys
import importlib.metadata

try:
    __version__ = importlib.metadata.version("scurrypy")
except importlib.metadata.PackageNotFoundError:
    # Fallback for development/editable installs
    __version__ = "0.0.0-dev"

__title__ = "scurrypy"
__url__ = "https://github.com/scurry-works/scurrypy"

USER_AGENT = (
    f"DiscordBot ({__url__}, {__version__}) "
    f"{__title__}/{__version__} "
    f"Python/{sys.version_info.major}.{sys.version_info.minor}"
)

GATEWAY_PROPERTIES = {
    "$os": sys.platform,
    "$browser": __title__,
    "$device": __title__
}

# silence internals by default
import logging

logging.getLogger('websockets').setLevel(logging.WARNING)
logging.getLogger('aiohttp').setLevel(logging.WARNING)
logging.getLogger('asyncio').setLevel(logging.WARNING)

def version() -> str:
    """Reports this package's version."""
    from importlib import metadata

    return metadata.version("scurrypy")
