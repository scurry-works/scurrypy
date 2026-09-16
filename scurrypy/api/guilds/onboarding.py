from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import PresentModelField, OmittableModelField, PresentNullableModelField, RequiredPartField, OptionalPartField, RequiredNullablePartField

from ...enums.guild import OnboardingMode, PromptType

from ..emoji import EmojiModel

@dataclass
class OnboardingPromptOptionModel(DataModel):
    """Represents a guild's prompt option for onboarding."""

    id: PresentModelField[Snowflake]
    """ID of the prompt option."""

    channel_ids: PresentModelField[list[Snowflake]]
    """Channel IDs a member is added to when selected."""

    role_ids: PresentModelField[list[Snowflake]]
    """Role IDs a member is given when selected."""

    emoji: OmittableModelField[EmojiModel]
    """Emoji for the option."""

    emoji_id: OmittableModelField[Snowflake]
    """ID for the emoji of the option."""

    emoji_name: OmittableModelField[str]
    """Name for the emoji of the option."""

    emoji_animated: OmittableModelField[bool]
    """Whether the emoji of the option is animated."""

    title: PresentModelField[str]
    """Title of the option."""

    description: PresentNullableModelField[str]
    """Description of the option."""

@dataclass
class OnboardingPromptModel(DataModel):
    """Represents a guild's prompt for onboarding."""

    id: PresentModelField[Snowflake]
    """ID of the prompt."""

    type: PresentModelField[PromptType]
    """Type of prompt."""

    options: PresentModelField[list[OnboardingPromptOptionModel]]
    """Options available with the prompt."""

    title: PresentModelField[str]
    """Title of the prompt."""

    single_select: PresentModelField[bool]
    """Whether users are limited to selecting one option."""

    required: PresentModelField[bool]
    """Whether the prompt is required for completing the onboarding process."""

    in_onboarding: PresentModelField[bool]
    """Whether the prompt is present in the onboarding flow."""

@dataclass
class GuildOnboadingModel(DataModel):
    """Represents a guild's onboarding flow."""

    guild_id: PresentModelField[Snowflake]
    """ID of the guild for onboarding."""

    prompts: PresentModelField[list[OnboardingPromptModel]]
    """Prompts shown during onboarding."""

    default_channel_ids: PresentModelField[list[Snowflake]]
    """Channel IDs members are opted into by default."""

    enabled: PresentModelField[bool]
    """Whether onboarding is enabled for the guild."""

    mode: PresentModelField[OnboardingMode]
    """Current mode of onboarding."""

@dataclass
class OnboardingPromptOptionPart(DataModel):
    """Represents fields for creating an onboarding prompt option."""

    id: RequiredPartField[Snowflake] = None
    """ID of the prompt option."""

    channel_ids: RequiredPartField[list[Snowflake]] = None
    """IDs for channels a member is added to when the option is selected."""

    role_ids: RequiredPartField[list[Snowflake]] = None
    """IDs for roles assigned to a member when the option is selected."""

    emoji_id: OptionalPartField[Snowflake] = None
    """Emoji ID of the option."""

    emoji_name: OptionalPartField[str] = None
    """Emoji name of the option."""

    emoji_animated: OptionalPartField[bool] = None
    """Whether the emoji is animated."""

    title: RequiredPartField[str] = None
    """Title of the option."""

    description: RequiredNullablePartField[str] = None
    """Description of the option."""

@dataclass
class OnboardingPromptPart(DataModel):
    """Represents fields for creating an onboarding prompt."""

    id: RequiredPartField[Snowflake] = None
    """ID of the prompt"""

    type: RequiredPartField[PromptType] = None
    """Type of prompt."""

    options: RequiredPartField[list[OnboardingPromptOptionPart]] = None
    """Options available with the prompt."""

    title: RequiredPartField[str] = None
    """Title of the prompt."""

    single_select: RequiredPartField[bool] = None
    """Whether the users are limited to selecting one option."""

    required: RequiredPartField[bool] = None
    """Whether the prompt is required to complete the onboarding flow."""
