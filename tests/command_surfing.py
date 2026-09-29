
# --- Isolate ApplicationCommandContext ---
from scurrypy.api.interactions import ApplicationCommandDataModel
from typing import cast

from scurrypy.enums import CommandOptionType
from scurrypy.core.exceptions import OptionNotFound
from scurrypy.api.interactions import (
    ApplicationCommandDataModel, 
    ApplicationCommandOptionDataModel,
    ApplicationSubcommandGroupDataModel,
    ApplicationSubcommandDataModel
)

type CommandOptionValue = int | float | bool | str

def convert_option_value(option: ApplicationCommandOptionDataModel) -> CommandOptionValue:
    """Converts the option's value based on the option's type.

    Args:
        option (ApplicationCommandOptionDataModel): command option

    Returns:
        (CommandOptionValue): converted command option value
    """
    if option.type in [
        CommandOptionType.INTEGER,
        CommandOptionType.USER,
        CommandOptionType.CHANNEL,
        CommandOptionType.ROLE,
        CommandOptionType.ATTACHMENT
    ]:
        return int(option.value)
    
    if option.type == CommandOptionType.NUMBER:
        return float(option.value)
    
    if option.type == CommandOptionType.BOOLEAN:
        return option.value.lower() == 'true'
    
    return option.value

from dataclasses import dataclass

@dataclass
class ApplicationCommandContext:
    data: ApplicationCommandDataModel

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
        options = self.data.options

        if not options:
            return None

        selected = options[0]

        if isinstance(selected, ApplicationSubcommandGroupDataModel):
            command_options = selected.options[0].options

        elif isinstance(selected, ApplicationSubcommandDataModel):
            command_options = selected.options

        else:
            command_options = cast( # guaranteed to be a list of ApplicationCommandOptionDataModel
                list[ApplicationCommandOptionDataModel],
                options
            )

        if not command_options:
            return None

        for option in command_options:
            if option.name == option_name:
                return convert_option_value(option)

        raise OptionNotFound(f"Option name '{option_name}' not found")

# --- TEST 1: SUBCOMMAND ---
data = {
    'id': '123',
    'name': 'user',
    'type': '1',
    'resolved': {},
    "options": [
        {
            "type": '1',
            "name": "set",
            "options": [
                {
                    "type": '3',
                    "name": "name",
                    "value": "Squirrel"
                }
            ]
        }
    ]
}

a = ApplicationCommandContext(ApplicationCommandDataModel.from_dict(data))

assert a.get_option('name') == 'Squirrel'

# --- TEST 2: SUBCOMMAND GROUP ---

data_b = {
    'id': '123',
    'name': 'user',
    'type': '1',
    'resolved': {},
    "options": [
        {
            "type": 2,
            "name": "user",
            "options": [
                {
                    "type": 1,
                    "name": "set",
                    "options": [
                        {
                            "type": 3,
                            "name": "name",
                            "value": "Squirrel"
                        }
                    ]
                }
            ]
        }
    ]
}

b = ApplicationCommandContext(ApplicationCommandDataModel.from_dict(data_b))

assert b.get_option('name') == 'Squirrel'

# --- TEST 3: SLASH COMMAND ---

data_c = {
    'id': '123',
    'name': 'echo',
    'type': '1',
    'resolved': {},
    'options': [
        {
            'type': '3',
            'name': 'message',
            'value': 'Hello!'
        }
    ]
}

c = ApplicationCommandContext(ApplicationCommandDataModel.from_dict(data_c))

assert c.get_option('message') == 'Hello!'

# --- TEST 3.B: OptionNotFound ---

try:
    c.get_option('nope')
except OptionNotFound:
    pass
else:
    raise AssertionError("Expected OptionNotFound")
