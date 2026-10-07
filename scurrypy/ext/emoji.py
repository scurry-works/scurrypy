from urllib.parse import quote

from scurrypy import JsonQuery
from scurrypy.core.snowflake import Snowflake

class EmojiInfo:
    def __init__(self, query: JsonQuery):
        self.name: str = query.get('name').value
        self.id: Snowflake = query.get('id', t=Snowflake).value
        self.is_animated: bool = query.get('animated', t=bool).value

    @property
    def mention(self) -> str | None:
        """Mention this emoji in a message."""
        # no emoji
        if self.name is None:
            return None
        # unicode emoji
        if self.id is None:
            return self.name
        # animated emoji
        if self.is_animated:
            return f"<a:{self.name}:{self.id}>"
        
        return f"<:{self.name}:{self.id}>"
    
    @property
    def api_code(self) -> str | None:
        """API code for this emoji (URL-safe)."""
        if self.name is None:
            return None
        # unicode emoji
        if self.id is None:
            return quote(self.name)
        # custom emoji
        if self.is_animated:
            return quote(f"a:{self.name}:{self.id}")
        
        return quote(f"{self.name}:{self.id}")

    @property
    def url(self) -> str | None:
        """Full qualifying link for this emoji."""
        if self.id is None:
            return None
        
        ext = 'gif' if self.is_animated else 'png'

        return f"https://cdn.discordapp.com/emojis/{self.id}.{ext}"
