from scurrypy import Client, JsonQuery
from scurrypy.core import Snowflake, MissingField
from scurrypy.resources import (
    Interaction, 
    Message, 
    Channel, 
    Guild
)

class InteractionContext(Interaction):
    """Useful interaction event info."""

    def __init__(self, bot: Client, event: JsonQuery):
        id: Snowflake = event.get('id', t=Snowflake).value
        token: str = event.get('token').value
        super().__init__(bot.http, id, token)
        self.bot = bot
        self.event = event
        self.data = event.get('data')

    @property
    def user(self) -> JsonQuery | None:
        """The invoking user."""
        user = self.event.get('member.user').value
        if user is None:
            return None
        return JsonQuery(user)

    @property
    def member(self) -> JsonQuery | None:
        """The invoking user's member."""
        member = self.event.get('member').value
        if member is None:
            return None
        return JsonQuery(member)
    
    @property
    def channel(self) -> Channel | None:
        """Channel resource of the interaction."""
        channel_id = self.event.get('channel_id', t=Snowflake).value
        if channel_id is None:
            raise MissingField("This event has no associated channel ID.")
        return self.bot.channel(channel_id)
    
    @property
    def guild(self) -> Guild:
        """Guild resource of the interaction."""
        guild_id = self.event.get('guild_id', t=Snowflake).value
        if not guild_id:
            raise MissingField("This event has no associated guild ID.")
        
        return self.bot.guild(guild_id)

    @property
    def message(self) -> Message:
        """Message resource of the interaction."""
        msg = self.event.get('message').value
        if msg is None:
            raise MissingField("This event has no associated message.")

        msg_id: Snowflake = JsonQuery(msg).get('id', t=Snowflake).value

        channel_id: Snowflake = self.event.get('channel_id', t=Snowflake).value

        if not channel_id:
            raise MissingField("This event has no associated channel ID.")

        return self.bot.message(channel_id, msg_id)
