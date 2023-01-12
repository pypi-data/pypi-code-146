from typing import Optional

from bin.models.bin_base_model import BinBaseModel
from bin.models.str_command import StrCommand
from bin.process.process import Process
from bin.requirements.requirement import Requirement


class ShellRequirement(BinBaseModel, Requirement):
    name: str
    met_if_cmd: StrCommand
    help: Optional[str]

    def is_met(self, process: Process) -> bool:
        return process.run(self.met_if_cmd, capture_output=True).has_succeeded()

    def get_name(self) -> str:
        return self.name

    def get_help(self) -> Optional[str]:
        return self.help
