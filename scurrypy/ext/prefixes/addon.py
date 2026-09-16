import logging

logger = logging.getLogger('scurrypy')

from scurrypy import Client, Intents
from scurrypy.bases import Addon
from scurrypy.enums import EventType
from scurrypy.core import DiscordError, Snowflake, InvalidCallbackSignature, MissingIntents
from scurrypy.events import MessageCreateEvent

from .ctx import PrefixCommandContext

from collections.abc import Callable, Awaitable
from typing import Any

type _AddonHandler[C: PrefixCommandContext] = Callable[[C], Awaitable[None]]

AddonHandler = _AddonHandler[Any]

type AddonDecorator = Callable[[AddonHandler], AddonHandler]

def _check_func_params(handler: AddonHandler) -> None:
    import inspect

    if not inspect.iscoroutinefunction(handler):
        raise InvalidCallbackSignature(f"Prefix handler '{handler.__name__}' must be async.")

    params_len = len(inspect.signature(handler).parameters)
    if params_len != 1:
        raise InvalidCallbackSignature(f"Prefix handler '{handler.__name__}' must accept exactly one parameter (ctx).")

class PrefixAddon(Addon):
    """Addon that implements automatic registering and decorating prefix commands."""

    def __init__(self, client: Client, application_id: Snowflake, prefix: str):
        """
        Args:
            client (Client): the Client object
            application_id (Snowflake): ID of the bot
            prefix (str): message prefix for commands
        """
        if not Intents.MESSAGE_CONTENT in client.intents:
            raise MissingIntents("Missing Intent.MESSAGE_CONTENT for scanning messages.")
        
        self.bot = client

        self.application_id = application_id

        self._prefix = prefix

        self._commands: dict[str, AddonHandler] = {}
        """Maps prefix command names to handler."""
        
        client.add_event_listener(EventType.MESSAGE_CREATE, self.dispatch)

    def listen(self, name: str, *, handler: AddonHandler | None = None) -> AddonDecorator | None:
        """Listen for a prefix command.

        Args:
            name (str): name of the command
                !!! warning "Important"
                    Prefix commands are CASE-INSENSITIVE.
            handler (AddonHandler, optional): callback for the command (if not a decorator)
        """
        name = name.lower()

        if handler is None:
            def decorator(func: AddonHandler) -> AddonHandler:
                _check_func_params(func)
                self._commands[name.lower()] = func
                logger.info(f"Prefix command '{self._prefix + name}' registered.")
                return func
            return decorator
        
        self._commands[name.lower()] = handler
        logger.info(f"Prefix command '{self._prefix + name}' registered.")
        return None
    
    async def dispatch(self, event: MessageCreateEvent) -> None:
        """Dispatch event to user-defined handler.
            Ignore bot responding to self and messages without the desired prefix.

        Args:
            event (MessageCreateEvent): message create event object
        """
        if not event.content:
            return # ignore empty messages
        
        if event.author.id == self.application_id:
            return # ignore bot responding to itself
        
        has_prefix = event.content.lower().startswith(self._prefix.lower())

        if not has_prefix:
            return # ignore messages without prefix
        
        command, *args = event.content[len(self._prefix):].strip().lower().split()
        handler = self._commands.get(command)

        # warn if this command doesnt have a known handler
        if not handler:
            logger.warning(f"Prefix Event '{command}' not found.")
            return

        # now prefix info can be confidently set
        try:
            ctx = PrefixCommandContext(self.bot, event, list(args))
            await handler(ctx)
            
            logger.info(f"Prefix Event '{self._prefix + command}' acknowledged with args: {ctx.args or 'No args'}")
        except DiscordError as e:
            logger.error(f"Error in prefix command '{self._prefix + command}': {e}")        
        except Exception as e:
            logger.exception(f"Unhandled error in prefix command '{self._prefix + command}': {e}")
