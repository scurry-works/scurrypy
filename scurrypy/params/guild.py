from typing import TypedDict

from ..enums.guild import OnboardingMode

from ..api.guilds.welcome_screen import WelcomeScreenChannelPart
from ..api.guilds.onboarding import OnboardingPromptPart
from ..api.guilds.role import GuildRoleColorsPart
from ..api.image_data import ImageDataPart

class EditGuildParams(TypedDict, total=False):
    """Represents fields for editing a guild."""

    name: str
    """Guild name."""

    afk_channel_id: int
    """Channel ID for AFK channel."""

    icon: ImageDataPart
    """Data URI scheme for guild icon.
    
    !!! note
        Can be animated if guild has `ANIMATED_ICON` feature.
    """

    splash: ImageDataPart
    """Data URI scheme for guild splash if guild has `INVITE_SPLASH` feature."""

    discovery_splash: ImageDataPart
    """Data URI scheme for guild discovery if guild has `DISCOVERABLE` feature."""

    banner: ImageDataPart
    """Data URI scheme for guild banner if guild has `BANNER` feature.
    
    !!! note
        Can be animated if guild has `ANIMATED_BANNER` feature.
    """

    system_channel_id: int
    """Channel ID for receiving guild notices (e.g., boosts, user join)."""

    rules_channel_id: int
    """Channel ID for where guilds display rules."""

    public_updates_channel_id: int
    """Channel ID for receiving notices from Discord."""

    description: str
    """Description for the guild."""

    premium_progress_bar_enabled: bool
    """Whether the guild's boost progress bar should be shown."""

    safety_alerts_channel_id: int
    """Channel ID for receiving safety alerts from Discord."""

class EditGuildRoleParams(TypedDict, total=False):
    """Represents fields for editing a guild role."""

    name: str | None
    """Name of the role."""

    colors: GuildRoleColorsPart | None
    """Colors of the role."""

    hoist: bool | None
    """Whether the role is displayed separately on the sidebar."""

    icon: ImageDataPart | None
    """Icon of the role (if guild has `ROLE_ICONS` feature)."""

    permissions: int | None
    """Permission bit set. [`INT_LIMIT`]"""

    unicode_emoji: str | None
    """Unicode emoji of the role (if guilde has `ROLE_ICONS` feature)."""

    mentionable: bool | None
    """Whether the role should be mentionable."""

class EditGuildWelcomeScreenParams(TypedDict, total=False):
    """Represents fields for editing a guild welcome screen."""

    enabled: bool
    """Whether the welcome scren is enabled."""

    welcome_channels: list[WelcomeScreenChannelPart]
    """Channels linked when the welcome screen is displayed."""

    description: str
    """Guild description to show on the welcome screen."""

class EditOnboardingParams(TypedDict, total=False):
    """Represents fields for editing a guild onboarding flow."""

    prompts: list[OnboardingPromptPart]
    """Prompts shown during onboarding."""

    default_channel_ids: list[int]
    """Channel IDs that members get opted into automatically."""

    enabled: bool
    """Whether onboarding is enabled in the guild."""
    
    mode: OnboardingMode
    """Current mode of onboarding."""

class EditGuildStickerParams(TypedDict, total=False):
    """Represents fields for editing a guild sticker."""

    name: str
    """Name of the sticker."""

    description: str
    """Description of the sticker."""

    tags: str
    """Autocomplete/suggestion tags for the sticker."""
