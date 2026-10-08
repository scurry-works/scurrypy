from scurrypy import JsonQuery
from scurrypy.core.snowflake import Snowflake

BASE_DISCORD_CDN = "https://cdn.discordapp.com/"

class Cdn:
    """Constructs URLs for Discord CDN assets."""

    @staticmethod
    def guild_icon(guild: JsonQuery) -> str | None:
        """Format the CDN endpoint for a guild icon.

        Args:
            guild (JsonQuery): guild object

        Returns:
            (str | None): CDN endpoint if guild icon exists
                else `None`
        """
        guild_id: Snowflake = guild.get("id", t=Snowflake).value
        icon: str | None = guild.get("icon").value

        if icon is None:
            return None

        if icon.startswith("a_"):
            return (
                f"{BASE_DISCORD_CDN}"
                f"icons/{guild_id}/{icon}.webp?animated=true"
            )

        return (
            f"{BASE_DISCORD_CDN}"
            f"icons/{guild_id}/{icon}.png"
        )

    @staticmethod
    def guild_splash(guild: JsonQuery) -> str | None:
        """Format the CDN endpoint for a guild splash.

        Args:
            guild (JsonQuery): guild object

        Returns:
            (str | None): CDN endpoint if guild splash exists
                else `None`
        """
        guild_id: Snowflake = guild.get("id", t=Snowflake).value
        splash: str | None = guild.get("splash").value

        if splash is None:
            return None

        return (
            f"{BASE_DISCORD_CDN}"
            f"splashes/{guild_id}/{splash}.png"
        )

    @staticmethod
    def guild_discovery_splash(guild: JsonQuery) -> str | None:
        """Format the CDN endpoint for a guild discovery splash.

        Args:
            guild (JsonQuery): guild object

        Returns:
            (str | None): CDN endpoint if guild discovery splash exists
                else `None`
        """
        guild_id: Snowflake = guild.get("id", t=Snowflake).value
        discovery_splash: str | None = guild.get("discovery_splash").value

        if discovery_splash is None:
            return None

        return (
            f"{BASE_DISCORD_CDN}"
            f"discovery-splashes/{guild_id}/{discovery_splash}.png"
        )

    @staticmethod
    def guild_banner(guild: JsonQuery) -> str | None:
        """Format the CDN endpoint for a guild banner.

        Args:
            guild (JsonQuery): guild object

        Returns:
            (str | None): CDN endpoint if guild banner exists
                else `None`
        """
        guild_id: Snowflake = guild.get("id", t=Snowflake).value
        banner: str | None = guild.get("banner").value

        if banner is None:
            return None

        if banner.startswith("a_"):
            return (
                f"{BASE_DISCORD_CDN}"
                f"banners/{guild_id}/{banner}.webp?animated=true"
            )

        return (
            f"{BASE_DISCORD_CDN}"
            f"banners/{guild_id}/{banner}.png"
        )

    @staticmethod
    def user_banner(user: JsonQuery) -> str | None:
        """Format the CDN endpoint for a user banner.

        Args:
            user (JsonQuery): user object

        Returns:
            (str | None): CDN endpoint if user banner exists
                else `None`
        """
        user_id: Snowflake = user.get("id", t=Snowflake).value
        banner: str | None = user.get("banner").value

        if banner is None:
            return None

        if banner.startswith("a_"):
            return (
                f"{BASE_DISCORD_CDN}"
                f"banners/{user_id}/{banner}.webp?animated=true"
            )

        return (
            f"{BASE_DISCORD_CDN}"
            f"banners/{user_id}/{banner}.png"
        )

    @staticmethod
    def guild_member_avatar(guild_id: Snowflake, member: JsonQuery) -> str | None:
        """Format the CDN endpoint for a guild member avatar.

        Args:
            guild_id (Snowflake): ID of guild member is in
            member (JsonQuery): member object

        Returns:
            (str | None): CDN endpoint if guild member avatar exists
                else `None`
        """
        user_id: Snowflake = member.get("user.id", t=Snowflake).value
        avatar: str | None = member.get("avatar").value

        if avatar is None:
            return None

        return (
            f"{BASE_DISCORD_CDN}"
            f"guilds/{guild_id}/users/{user_id}/avatars/{avatar}.png"
        )

    @staticmethod
    def guild_member_banner(guild_id: Snowflake, member: JsonQuery) -> str | None:
        """Format the CDN endpoint for a guild member banner.

        Args:
            guild_id (Snowflake): ID of guild member is in
            member (JsonQuery): member object

        Returns:
            (str | None): CDN endpoint if guild member banner exists
                else `None`
        """
        user_id: Snowflake = member.get("user.id", t=Snowflake).value
        banner: str | None = member.get("banner").value

        if banner is None:
            return None

        if banner.startswith("a_"):
            return (
                f"{BASE_DISCORD_CDN}"
                f"guilds/{guild_id}/users/{user_id}/banners/{banner}.webp?animated=true"
            )

        return (
            f"{BASE_DISCORD_CDN}"
            f"guilds/{guild_id}/users/{user_id}/banners/{banner}.png"
        )

    @staticmethod
    def guild_role_icon(role: JsonQuery) -> str | None:
        """Format the CDN endpoint for a guild role icon.

        Args:
            role (JsonQuery): role object

        Returns:
            (str | None): CDN endpoint if guild role icon exists
                else `None`
        """
        role_id: Snowflake = role.get('id', t=Snowflake).value
        icon: str | None = role.get('icon').value

        if icon is None:
            return None

        return (
            f"{BASE_DISCORD_CDN}"
            f"role-icons/{role_id}/{icon}.png"
        )

    @staticmethod
    def user_avatar(user: JsonQuery) -> str | None:
        """Format the CDN endpoint for a user avatar.

        Args:
            user (JsonQuery): user object

        Returns:
            (str | None): CDN endpoint if user avatar exists
                else `None`
        """
        user_id: Snowflake = user.get("id", t=Snowflake).value
        avatar: str | None = user.get("avatar").value

        if avatar is None:
            return None

        if avatar.startswith("a_"):
            return (
                f"{BASE_DISCORD_CDN}"
                f"avatars/{user_id}/{avatar}.webp?animated=true"
            )

        return (
            f"{BASE_DISCORD_CDN}"
            f"avatars/{user_id}/{avatar}.png"
        )

    @staticmethod
    def user_avatar_decoration(user: JsonQuery) -> str | None:
        """Format the CDN endpoint for a user avatar decoration.

        Args:
            user (JsonQuery): user object

        Returns:
            (str | None): CDN endpoint if user avatar decoration exists
                else `None`
        """
        avatar_decoration: str | None = user.get("avatar_decoration_data.asset").value

        if avatar_decoration is None:
            return None

        return (
            f"{BASE_DISCORD_CDN}"
            f"avatar-decoration-presets/{avatar_decoration}.png"
        )

    @staticmethod
    def application_icon(application: JsonQuery) -> str | None:
        app_id: Snowflake = application.get("id", t=Snowflake).value
        icon: str | None = application.get("icon").value

        if icon is None:
            return None

        return (
            f"{BASE_DISCORD_CDN}"
            f"app-icons/{app_id}/{icon}.png"
        )

    @staticmethod
    def application_cover(application: JsonQuery) -> str | None:
        app_id: Snowflake = application.get("id", t=Snowflake).value
        cover_image: str | None = application.get("cover_image").value

        if cover_image is None:
            return None

        return (
            f"{BASE_DISCORD_CDN}"
            f"app-icons/{app_id}/{cover_image}.png"
        )
