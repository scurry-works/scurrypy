from typing import TypedDict

class GuildTemplateParams(TypedDict, total=False):
    """Parameters for editing a guild template."""

    name: str
    """Name of the template."""

    description: str | None
    """Description of the template."""
