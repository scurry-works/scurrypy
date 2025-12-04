from .addon import Addon

from ..parts.components import *

class ComponentBuilder(Addon):

    @staticmethod
    def _basic_button(style: int, custom_id: str, label: str = None, emoji: str | EmojiModel = None, disabled: bool = False):
        if emoji:
            if isinstance(emoji, str):
                emoji = EmojiModel(name=emoji)
            elif not isinstance(emoji, EmojiModel):
                raise TypeError(f"EasyBot.primary expects type str or EmojiModel, got {type(emoji).__name__}")
        
        return Button(
            style=style,
            custom_id=custom_id,
            label=label,
            emoji=emoji ,
            disabled=disabled
        )
    
    @staticmethod
    def primary(custom_id: str, label: str = None, emoji: str | EmojiModel = None, disabled: bool = False):
        """Builds a primary button

        Args:
            custom_id (str): unique button identifier
            label (str, optional): user-facing label
            emoji (str | EmojiModel, optional): emoji icon as str or EmojiModel if custom
            disabled (bool, optional): Whether the button should be disabled. Defaults to False.

        Returns:
            (Button): the button object
        """
        return ComponentBuilder._basic_button(ButtonStyles.PRIMARY, custom_id, label, emoji, disabled)
    
    @staticmethod
    def secondary(custom_id: str, label: str = None, emoji: str | EmojiModel = None, disabled: bool = False):
        """Builds a secondary button

        Args:
            custom_id (str): unique button identifier
            label (str, optional): user-facing label
            emoji (str | EmojiModel, optional): emoji icon as str or EmojiModel if custom
            disabled (bool, optional): Whether the button should be disabled. Defaults to False.

        Returns:
            (Button): the button object
        """
        return ComponentBuilder._basic_button(ButtonStyles.SECONDARY, custom_id, label, emoji, disabled)
    
    @staticmethod
    def success(custom_id: str, label: str = None, emoji: str | EmojiModel = None, disabled: bool = False):
        """Builds a success button

        Args:
            custom_id (str): unique button identifier
            label (str, optional): user-facing label
            emoji (str | EmojiModel, optional): emoji icon as str or EmojiModel if custom
            disabled (bool, optional): Whether the button should be disabled. Defaults to False.

        Returns:
            (Button): the button object
        """
        return ComponentBuilder._basic_button(ButtonStyles.SUCCESS, custom_id, label, emoji, disabled)
    
    @staticmethod
    def danger(custom_id: str, label: str = None, emoji: str | EmojiModel = None, disabled: bool = False):
        """Builds a danger button

        Args:
            custom_id (str): unique button identifier
            label (str, optional): user-facing label
            emoji (str | EmojiModel, optional): emoji icon as str or EmojiModel if custom
            disabled (bool, optional): Whether the button should be disabled. Defaults to False.

        Returns:
            (Button): the button object
        """
        return ComponentBuilder._basic_button(ButtonStyles.DANGER, custom_id, label, emoji, disabled)
    
    @staticmethod
    def link(url: str, label: str = None, emoji: str | EmojiModel = None, disabled: bool = False):
        """Builds a link button

        Args:
            url (str): button URL to open
            label (str, optional): user-facing label
            emoji (str | EmojiModel, optional): emoji icon as str or EmojiModel if custom
            disabled (bool, optional): Whether the button should be disabled. Defaults to False.

        Returns:
            (Button): the button object
        """
        btn = ComponentBuilder._basic_button(ButtonStyles.LINK, label, emoji, disabled)
        btn.url = url
        return btn
    
    @staticmethod
    def row(components: list[ActionRowChild]):
        """Shorthand for action row.

        Args:
            components (list[ActionRowChild]): the action row objects.

        Returns:
            (ActionRowPart): the action row object
        """
        if not isinstance(components, list):
            components = [components]

        return ActionRowPart(components)
    
    @staticmethod
    def option(
        label: str,
        value: str,
        description: str = None,
        emoji: EmojiModel | str = None,
        default: bool = False
    ):
        """Builds a string menu select option.

        Args:
            label (str): user-facing label
            value (str): unique identifier
            description (str, optional): option descriptor
            emoji (EmojiModel | str, optional): emoji icon as str or EmojiModel if custom
            default (bool, optional): Whether this value should be the default if none is selected. Defaults to False.

        Raises:
            (TypeError): invalid `emoji` type

        Returns:
            (SelectOption): the SelectOption object
        """
        if emoji:
            if isinstance(emoji, str):
                emoji = EmojiModel(name=emoji)
            elif not isinstance(emoji, EmojiModel):
                raise TypeError(f"EasyBot.primary expects type str or EmojiModel, got {type(emoji).__name__}")
        
        return SelectOption(
            label=label,
            value=value,
            description=description,
            emoji=emoji,
            default=default
        )
    
    @staticmethod
    def short_text(
        custom_id: str,
        required: bool = True,
        placeholder: str | None = None,
        min_length: int | None = None,
        max_length: int | None = None
    ):
        """Builds a TextInput with `TextInputStyles.SHORT` style.

        Args:
            custom_id (str): unique identifier
            required (bool, optional): Whether this field is required. Defaults to True.
            placeholder (str | None, optional): default text if nothing is entered
            min_length (int | None, optional): minimum input length
            max_length (int | None, optional): maximum input length

        Returns:
            (TextInput): the TextInput object
        """
        return TextInput(
            style=TextInputStyles.SHORT,
            custom_id=custom_id,
            required=required,
            placeholder=placeholder,
            min_length=min_length,
            max_length=max_length
        )

    @staticmethod
    def long_text(
        custom_id: str,
        required: bool = True,
        placeholder: str | None = None,
        min_length: int | None = None,
        max_length: int | None = None
    ):
        """Builds a TextInput with `TextInputStyles.PARAGRAPH` style.

        Args:
            custom_id (str): unique identifier
            required (bool, optional): Whether this field is required. Defaults to True.
            placeholder (str | None, optional): default text if nothing is entered
            min_length (int | None, optional): minimum input length
            max_length (int | None, optional): maximum input length

        Returns:
            (TextInput): the TextInput object
        """
        return TextInput(
            style=TextInputStyles.PARAGRAPH,
            custom_id=custom_id,
            required=required,
            placeholder=placeholder,
            min_length=min_length,
            max_length=max_length
        )

    @staticmethod
    def role_value(id: int):
        """Builds a default role value.

        Args:
            id (int): role ID

        Returns:
            (DefaultValue): the DefaultValue object
        """
        return DefaultValue(
            id=id,
            type='role'
        )

    @staticmethod
    def user_value(id: int):
        """Builds a default user value.

        Args:
            id (int): user ID

        Returns:
            (DefaultValue): the DefaultValue object
        """
        return DefaultValue(
            id=id,
            type='user'
        )
    
    @staticmethod
    def channel_value(id: int):
        """Builds a default channel value.

        Args:
            id (int): channel ID

        Returns:
            (DefaultValue): the DefaultValue object
        """
        return DefaultValue(
            id=id,
            type='channel'
        )
