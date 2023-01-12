from pathlib import Path
from typing import List

from bin.bin_file.bin_file_loader import BinFileLoader
from bin.bin_file.dtos.bin_file_mapper import BinFileMapper
from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.commands.errors import CommandFailedError
from bin.models.bin_base_model import BinBaseModel
from bin.process.emoji import Emoji
from bin.process.helpable import Helpable
from bin.process.process import Process


class InitCommand(BinBaseModel, Command):
    current_working_dir: Path

    @classmethod
    def init(cls, cwd: Path) -> "InitCommand":
        return cls(current_working_dir=cwd)

    def _run(self, process: Process, args: List[str]) -> Process:
        if len(args) > 0:
            raise CommandFailedError.must_run_without_args("init")

        if not self.current_working_dir.is_dir():
            raise CommandFailedError.failed_with_reason(
                "init", f"unable to initialize as '{self.current_working_dir}' is not a directory"
            )

        found_bin_file = BinFileLoader.find_any_bin_file(self.current_working_dir)
        if found_bin_file is not None:
            raise CommandFailedError.failed_with_reason("init", f"bin file already exists '{found_bin_file}'")

        bin_file_path = self.current_working_dir / BinFileLoader.DEFAULT_BIN_FILE_NAME
        bin_file_path.write_text(BinFileMapper.example_file_content())
        process.log_success(f"{Emoji.SUCCESS}  {bin_file_path} initialized!")

        return process

    def _get_short_description(self) -> str:
        return f"Initializes a {BinFileLoader.DEFAULT_BIN_FILE_NAME} file"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self(self._get_short_description())
