from .enum_types import DiscordFlags

class GuildMemberFlags(DiscordFlags):
    """Represents flags associated with a guild member."""

    DID_REJOIN = 1 << 0
    """Member has left and rejoined the guild."""

    COMPLETED_ONBOARDING = 1 << 1
    """Member has completed onboarding."""

    BYPASSES_VERIFICATION = 1 << 2
    """Member is exempt from guild verification requirements."""

    STARTED_ONBOARDING = 1 << 3
    """Member has started onboarding."""

    STARTED_HOME_ACTIONS = 1 << 5
    """Member has started Server Guide new member actions."""

    COMPLETED_HOME_ACTIONS = 1 << 6
    """Member has completed Server Guide new member actions."""

class UserFlags(DiscordFlags):
    """Represents flags associated with a user."""

    STAFF = 1 << 0
    """Discord Employee."""

    PARTNER = 1 << 1
    """Partnered Server Owner."""

    HYPERSQUAD = 1 << 2
    """HypeSquad Events Member."""

    BUG_HUNTER_LEVEL_1 = 1 << 3
    """Bug Hunter Level 1."""

    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    """House Bravery Member."""
    
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    """House Brilliance Member."""

    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    """House Balance Member."""

    PREMIUM_EARLY_SUPPORTER = 1 << 9
    """Early Nitro Supporter."""

    BUG_HUNTER_LEVEL_2 = 1 << 14
    """Bug Hunter Level 2."""

    VERIFIED_BOT = 1 << 16
    """Verified Bot."""

    VERIFIED_DEVELOPER = 1 << 17
    """Early Verified Bot Developer."""

    CERTIFIED_MODERATOR = 1 << 18
    """Moderator Programs Alumni."""

    BOT_HTTP_INTERACTIONS = 1 << 19
    """Bot uses only HTTP interactions and is shown in the online member list."""
