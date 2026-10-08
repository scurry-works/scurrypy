from scurrypy.core.snowflake import Snowflake

class Mention:
    """Mention an object in a message."""

    @staticmethod
    def user(user_id: Snowflake) -> str:
        """Mention a user.

        Args:
            user_id (Snowflake): ID of the user

        Returns:
            (str): formatted user mention
        """
        return f"<@{user_id}>"

    @staticmethod
    def channel(channel_id: Snowflake) -> str:
        """Mention a channel

        Args:
            channel_id (Snowflake): ID of the channel

        Returns:
            (str): formatted channel mention
        """
        return f"<#{channel_id}>"

    @staticmethod
    def role(role_id: Snowflake) -> str:
        """Mention a role

        Args:
            role_id (Snowflake): ID of the role

        Returns:
            (str): formatted role mention
        """
        return f"<@&{role_id}>"

    @staticmethod
    def slash_command(command_name: str, command_id: Snowflake) -> str:
        """Mention a slash command.

        Args:
            command_name (str): name of the command
            command_id (Snowflake): ID of the command

        Returns:
            (str): formatted slash command mention
        """
        return f"</{command_name}:{command_id}>"

    @staticmethod
    def subcommand(command_name: str, subcommand_name: str, command_id: Snowflake) -> str:
        """Mention a subcommand.

        Args:
            command_name (str): name of the command
            subcommand_name (str): name of the subcommand
            command_id (Snowflake): ID of the command

        Returns:
            (str): formatted subcommand mention
        """
        return f"</{command_name} {subcommand_name}:{command_id}>"

    @staticmethod
    def subcommand_group(command_name: str, subcommand_group_name: str, subcommand_name: str, command_id: Snowflake) -> str:
        """Mention a subcommand group.

        Args:
            command_name (str): name of the command
            subcommand_group_name (str): name of the command group
            subcommand_name (str): name of the subcommand
            command_id (Snowflake): ID of the command

        Returns:
            (str): formatted subcommand group mention
        """
        return f"</{command_name} {subcommand_group_name} {subcommand_name}:{command_id}>"
