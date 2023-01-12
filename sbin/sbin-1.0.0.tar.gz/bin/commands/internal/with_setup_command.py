from typing import List

from bin.commands.command import Command
from bin.models.bin_base_model import BinBaseModel
from bin.process.helpable import Helpable
from bin.process.process import Process


class WithSetupCommand(BinBaseModel, Command):
    setup_cmds: List[Command]
    main_cmd: Command

    def _run(self, process: Process, args: List[str]) -> Process:
        for command in self.setup_cmds:
            process = command.run(process, [])

        return self.main_cmd.run(process, args)

    def _get_short_description(self) -> str:
        return self.main_cmd._get_short_description()

    def _get_help(self) -> Helpable:
        return self.main_cmd._get_help()
