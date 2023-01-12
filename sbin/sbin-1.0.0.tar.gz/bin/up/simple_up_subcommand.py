from bin.models.bin_base_model import BinBaseModel
from bin.models.str_command import StrCommand
from bin.process.process import Process
from bin.up.up_subcommand import UpResult, UpSubcommand


class SimpleUpSubcommand(BinBaseModel, UpSubcommand):
    name: str
    run_cmd: StrCommand

    def run(self, process: Process) -> UpResult:
        result = process.run(self.run_cmd)

        return UpResult.from_process_result(self.name, result)
