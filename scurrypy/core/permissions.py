from typing import TypedDict, Unpack

class PermissionsFlagParams(TypedDict, total=False):
    """Role/User permission selection parameters.
    !!! important
        Param name MUST match the permission it represents! 
        For example, "KICK_MEMBERS" is "kick_members".
    """
    create_instant_invite: bool
    kick_members: bool
    ban_members: bool
    administrator: bool
    manage_channels: bool
    manage_guild: bool
    add_reactions: bool
    view_channel: bool
    send_messages: bool
    manage_messages: bool
    embed_links: bool
    attach_files: bool
    read_message_history: bool
    use_external_emojis: bool
    manage_roles: bool
    use_application_commands: bool
    manage_threads: bool
    create_public_threads: bool
    create_private_threads: bool
    send_messages_in_threads: bool
    moderate_members: bool
    send_polls: bool
    pin_messages: bool
    bypass_slowmode: bool

class Permissions:
    """Guild/User permission flags.
    
    !!! note
        Not all permissions are listed. Permissions not listed are not yet supported.
    """

    CREATE_INSTANT_INVITE = 1 << 0
    """Allows creation of instant invites."""

    KICK_MEMBERS = 1 << 1
    """Allows kicking members."""

    BAN_MEMBERS = 1 << 2
    """Allows banning members."""

    ADMINISTRATOR = 1 << 3
    """Allows all permissions and bypasses channel permission overwrites."""

    MANAGE_CHANNELS = 1 << 4
    """Allows management and editing of channels"""

    MANAGE_GUILD = 1 << 5
    """Allows management and editing of the guild."""

    ADD_REACTIONS = 1 << 6
    """Allows for adding new reactions to messages. 
        !!! warning 
            This permission does not apply to reacting with an existing reaction on a message.
    """

    VIEW_CHANNEL = 1 << 10
    """Allows guild members to view a channel, which includes reading messages in text channels and joining voice channels."""

    SEND_MESSAGES = 1 << 11
    """Allows for sending messages in a channel and creating threads in a forum. 
        !!! warning
            Does not allow sending messages in threads.
    """

    MANAGE_MESSAGES = 1 << 13
    """Allows for deletion of other users messages."""

    EMBED_LINKS = 1 << 14
    """Links sent by users with this permission will be auto-embedded."""

    ATTACH_FILES = 1 << 15
    """Allows for uploading images and files."""

    READ_MESSAGE_HISTORY = 1 << 16
    """Allows for reading of message history."""

    USE_EXTERNAL_EMOJIS = 1 << 18
    """Allows the usage of custom emojis from other servers."""

    MANAGE_ROLES = 1 << 28
    """Allows management and editing of roles."""

    USE_APPLICATION_COMMANDS = 1 << 31
    """Allows members to use application commands, including slash commands and context menu commands."""

    MANAGE_THREADS = 1 << 34
    """Allows for deleting and archiving threads, and viewing all private threads."""

    CREATE_PUBLIC_THREADS = 1 << 35
    """Allows for creating public and announcement threads."""

    CREATE_PRIVATE_THREADS = 1 << 36
    """Allows for creating private threads."""

    SEND_MESSAGES_IN_THREADS = 1 << 38
    """Allows for sending messages in threads."""
    
    MODERATE_MEMBERS = 1 << 40
    """Allows for timing out users to prevent them from sending or reacting to messages in chat and threads, and from speaking in voice and stage channels."""

    SEND_POLLS = 1 << 49
    """Allows sending polls."""
    
    PIN_MESSAGES = 1 << 51
    """Allows pinning and unpinning messages."""

    BYPASS_SLOWMODE = 1 << 52
    """Allows bypassing slowmode restrictions."""

    @staticmethod
    def set(**flags: Unpack[PermissionsFlagParams]):
        """Set permissions. See [`Permission`][scurrypy.core.permissions.Permissions].

        Args:
            **flags (Unpack[PermissionsFlagParams]): permissions to set

        Raises:
            (ValueError): invalid flag

        Returns:
            (int): combined permissions field
        """

        perms = 0
        for k, v in flags.items():
            if v:
                try:
                    perms |= getattr(Permissions, k.upper())
                except AttributeError:
                    raise ValueError(f"Unknown intent flag: '{k}'")
        
        return perms

    @staticmethod
    def has(permissions: int, permission: int):
        """Checks if a permission bit is toggled.

        Args:
            permissions (int): permissions integer
            permission (int): permission bit to check

        Returns:
            (bool): if permission bit is toggled
        """
        return (permissions & permission) == permission
