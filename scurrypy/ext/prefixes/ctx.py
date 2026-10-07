from scurrypy import Client, JsonQuery
from scurrypy.core import Snowflake, MissingField
from scurrypy.resources import Channel, Guild, Message

class PrefixCommandContext(Channel):
    """Useful message prefix event info."""

    def __init__(self, bot: Client, event: JsonQuery, args: list[str]) -> None:

        channel_id: Snowflake = event.get('channel_id', t=Snowflake).value
        super().__init__(bot.http, channel_id)

        self.bot = bot
        self.event = event
        self.args = args

    @property
    def author(self) -> JsonQuery:
        """Author of the prefix command."""
        return self.event.get('author')

    @property
    def guild(self) -> Guild:
        """Guild resource of the prefix command."""
        guild_id: Snowflake = self.event.get('guild_id', t=Snowflake).value

        if guild_id is None:
            raise MissingField("This event has no associated guild ID.")
        
        return self.bot.guild(guild_id)

    @property
    def channel(self) -> Channel:
        """Channel resource of the prefix command."""
        channel_id: Snowflake = self.event.get('channel_id', t=Snowflake).value

        return self.bot.channel(channel_id)

    @property
    def message(self) -> Message:
        """Message resource of the prefix command."""
        id: Snowflake = self.event.get('id', t=Snowflake).value
        channel_id: Snowflake = self.event.get('channel_id', t=Snowflake).value

        return self.bot.message(channel_id, id)
