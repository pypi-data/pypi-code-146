from pathlib import Path

from bin.bin_file.dtos.bin_file_mapper import BinFileMapper
from bin.bin_file.init_command import InitCommand
from bin.commands.command import Command
from bin.commands.internal.factory import InternalCommandFactory
from bin.custom_commands.command_tree import CommandTree


class Bin:
    @staticmethod
    def make_command(dir_path: Path) -> Command:
        if BinFileMapper.contains_bin_file(dir_path):
            return BinFileMapper.to_command(dir_path)

        return CommandTree(
            self_cmd=InternalCommandFactory.help_only(
                "Bin helps you setup your project. Use the <init> command to create an example file."
            ),
            subcommands_tree={"init": InitCommand.init(dir_path)},
        )
