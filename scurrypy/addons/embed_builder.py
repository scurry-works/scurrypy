from .addon import Addon

from ..models.user import UserModel
from ..parts.embed import *

class EmbedBuilder(Addon):
    @staticmethod
    def user_author(user: UserModel):
        """Embed author builder.

        Args:
            user (UserModel): user author

        Returns:
            (EmbedAuthor): the EmbedAuthor object
        """
        if not user:
            raise ValueError("Missing user.")
        
        return EmbedAuthor(
            name=user.username,
            icon_url=f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png"
        )
    
    @staticmethod
    def timestamp():
        """Embed timestamp builder. Adheres to ISO8601 format.

        Returns:
            (str): message timestamp
        """
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def field(name: str, value: str, inline: bool = None):
        """Embed field builder.

        Args:
            name (str): field title
            value (str): field description
            inline (bool, optional): whether the field is inline (horizontal)

        Returns:
            (EmbedField): the EmbedField object
        """
        return EmbedField(name, value, inline)
    
    @staticmethod
    def footer(text: str, icon_url: str = None):
        """Embed footer builder.

        Args:
            text (str): footer text
            icon_url (str, optional): footer icon URL

        Returns:
            (EmbedFooter): the EmbedFooter object
        """
        return EmbedFooter(text, icon_url)
