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
