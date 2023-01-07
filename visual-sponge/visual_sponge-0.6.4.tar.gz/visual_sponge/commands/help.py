from .. import MACROS
from ..commands import __all__ as all_commands

def HELP(command=None):
    if command is None:
        return f"""{MACROS.localization("HelpHelpHint")} {all_commands}"""
    if command in all_commands:
        return MACROS.localization("CommandHelp" + command.capitalize())
    raise ValueError(f"{command} is not a name of available commands")
