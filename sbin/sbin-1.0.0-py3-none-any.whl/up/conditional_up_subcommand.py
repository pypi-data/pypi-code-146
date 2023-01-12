from bin.models.bin_base_model import BinBaseModel
from bin.models.str_command import StrCommand
from bin.process.process import Process
from bin.up.up_subcommand import UpResult, UpSubcommand


class ConditionalUpSubcommand(BinBaseModel, UpSubcommand):
    name: str
    run_cmd: StrCommand
    unless_cmd: StrCommand

    def run(self, process: Process) -> UpResult:
        if process.run(self.unless_cmd, capture_output=True).has_succeeded():
            return UpResult.succeeded(self.name).with_details("already up")

        if process.run(self.run_cmd).has_failed():
            return UpResult.failed(self.name).with_details(f"Command '{self.run_cmd}' failed")

        if process.run(self.unless_cmd, capture_output=True).has_failed():
            return UpResult.failed(self.name).with_details(
                f"Command '{self.run_cmd}' ran but failed to fix '{self.unless_cmd}'"
            )

        return UpResult.succeeded(self.name)
