from dataclasses import dataclass

from ...core.part import Part
from ...core.snowflake import Snowflake
from ...core.types import (
    RequiredPartField, 
    OptionalPartField, 
    RequiredNullablePartField
)

from ...enums import PromptType

@dataclass
class OnboardingPromptOptionPart(Part):
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
class OnboardingPromptPart(Part):
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
