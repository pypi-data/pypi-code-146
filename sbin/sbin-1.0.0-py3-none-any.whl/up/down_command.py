from bin.commands.command_help import CommandHelp
from bin.process.helpable import Helpable
from bin.up.up_command import UpCommand


class DownCommand(UpCommand):
    def _get_short_description(self) -> str:
        return "Cancels what the up command sets up"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self(self._get_short_description())

    def _type(self) -> str:
        return "down"
