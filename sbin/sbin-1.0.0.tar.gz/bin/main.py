import os
import subprocess
import sys
from pathlib import Path
from typing import List

import colorama

from bin.bin import Bin
from bin.commands.command import Command
from bin.commands.internal.factory import InternalCommandFactory
from bin.error_handler import ErrorHandler, get_error_handler
from bin.process.emoji import Emoji
from bin.process.process import Process


class Main:
    def __init__(self, error_handler: ErrorHandler, process: Process, cwd: Path, args: List[str]) -> None:
        self.__error_handler = error_handler
        self.__process = process
        self.__cwd = cwd
        self.__args = args

    @classmethod
    def init(cls) -> "Main":
        error_handler = get_error_handler()
        cwd = Path(".")
        process = Process(env=dict(os.environ))
        return cls(error_handler, process, cwd, sys.argv[1:])

    def run(self) -> int:
        self.__log_user_command()
        cmd: Command = InternalCommandFactory.noop()
        try:
            cmd = Bin.make_command(self.__cwd)
            cmd.run(self.__process, self.__args)
            return 0
        except Exception as e:
            return self.__error_handler.handle(e, cmd, self.__process.unmute_logs())

    def __log_user_command(self) -> None:
        args = subprocess.list2cmdline(self.__args)
        self.__process.log_title(f"  {Emoji.BIN}  bin {args}\n")


def main() -> None:
    __enable_color_schemas_across_os()

    exit_code = Main.init().run()
    sys.exit(exit_code)


def __enable_color_schemas_across_os() -> None:
    colorama.init(autoreset=True)
