from .addon import Addon
from ..core.error import DiscordError
from ..client import Client
from ..events.message_events import MessageCreateEvent

class PrefixAddon(Addon):
    """Addon that implements automatic registering and decorating prefix commands."""

    def __init__(self, client: Client, prefix: str):
        """
        Args:
            client (Client): the Client object
            prefix (str): message prefix for commands
        """
        self.bot = client

        self.logger = client.logger

        self._prefix = prefix

        self._commands = {}
        """Maps prefix command names to handler."""
        
        client.addons.add(self)

    def setup(self):
        """Sets up the addon with the client."""

        self.bot.addons.add_event_listener("MESSAGE_CREATE", self.dispatch)

    def register(self, name: str):
        """Register a prefix command.

        Args:
            name (str): name of the command
                !!! warning "Important"
                    Prefix commands are CASE-INSENSITIVE.
        """
        def decorator(func):
            self._commands[name.lower()] = func
        return decorator

    async def dispatch(self, event: MessageCreateEvent):
        """Dispatch event to user-defined handler.
            Ignore bot responding to self and messages without the desired prefix.

        Args:
            event (MessageCreateEvent): message create event object
        """
        if not event.content:
            self.logger.log_warn("No message content.")
            return
        
        # ignore bot responding to itself
        if event.author.id == self.bot.application_id:
            return
        
        has_prefix = event.content.lower().startswith(self._prefix.lower())

        # ignore messages without prefix
        if not has_prefix:
            return
        
        command, *args = event.content[len(self._prefix):].strip().lower().split()
        handler = self._commands.get(command)

        # warn if this command doesnt have a known handler
        if not handler:
            self.logger.log_warn(f"Prefix Event '{command}' not found.")
            return

        # now prefix info can be confidently set
        try:
            res = self.bot.message(event.channel_id, event.id, context=event)
            await handler(self.bot, res)
            
            self.logger.log_info(f"Prefix Event '{command}' acknowledged with args: {list(args) or 'No args'}")
        except DiscordError as e:
            self.logger.log_error(f"Error in prefix command '{command}': {e}")        
        except Exception as e:
            self.logger.log_error(f"Unhandled error in prefix command '{command}': {e}")
