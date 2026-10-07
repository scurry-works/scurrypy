from typing import cast

from scurrypy import JsonQuery
from scurrypy.enums import CommandOptionType
from scurrypy.core.exceptions import OptionNotFound

from ..interactions.ctx import InteractionContext

class CommandContext(InteractionContext):
    pass

type CommandOptionValue = int | float | bool | str
"""Possible types in which a command option value can be converted."""

def convert_option_value(option: JsonQuery) -> CommandOptionValue:
    """Converts the option's value based on the option's type.

    Args:
        option (JsonQuery): command option

    Returns:
        (CommandOptionValue): converted command option value
    """
    opt_type: CommandOptionType = option.get('type', t=CommandOptionType).value
    opt_value: str = option.get('value').value

    if opt_type in [
        CommandOptionType.INTEGER,
        CommandOptionType.USER,
        CommandOptionType.CHANNEL,
        CommandOptionType.ROLE,
        CommandOptionType.ATTACHMENT
    ]:
        return int(opt_value)
    
    if opt_type == CommandOptionType.NUMBER:
        return float(opt_value)
    
    if opt_type == CommandOptionType.BOOLEAN:
        return opt_value.lower() == 'true'
    
    return opt_value

class ApplicationCommandContext(CommandContext):
    event: JsonQuery

    def get_option(self, option_name: str) -> CommandOptionValue | None:
        """Get a command option input value by name converted to its appropriate type.

        Args:
            option_name (str): name of option

        Raises:
            OptionNotFound: command option not found

        Returns:
            (CommandOptionValue | None): converted command input value or None
                if no command options are present
        """
        options = self.event.get('data.options').value

        if options is None:
            return None

        selected = JsonQuery(options[0])
        selected_type: CommandOptionType = selected.get('type', t=CommandOptionType).value

        if selected_type == CommandOptionType.SUB_COMMAND_GROUP:
            command_options = selected.get('options.0.options').value

        elif selected_type == CommandOptionType.SUB_COMMAND:
            command_options = selected.get('options').value

        else:
            command_options = options

        if not command_options:
            return None

        for option in command_options:
            opt = JsonQuery(option)
            name: str = opt.get('name').value

            if name == option_name:
                return convert_option_value(option)

        raise OptionNotFound(f"Option name '{option_name}' not found")

class AutocompleteApplicationCommandContext(CommandContext):
    event: JsonQuery

    def get_focused_value(self) -> str | None:
        """Get the next focused value in options.

        Returns:
            (str | None): next focused value or None if no values are focused or no options are present
        """
        options = self.event.get('data.options').value

        if options is None:
            return None

        next_focused = next(
            (
                o 
                for o in options 
                if JsonQuery(o).get('focused', t=bool).value is True
            ), 
            None)

        return JsonQuery(next_focused).get('value').value if next_focused is not None else None
