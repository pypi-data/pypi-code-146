import shutil
import subprocess
from typing import Dict, List, Optional

from bin.process.helpable import Helpable
from bin.process.io.console_io import ConsoleIo
from bin.process.io.io import Io
from bin.process.io.mute_io import MuteIo
from bin.process.process_result import ProcessResult


class Process:
    def __init__(
        self,
        *,
        io: Optional[Io] = None,
        env: Optional[Dict[str, str]] = None,
        venv: Optional[str] = None,
    ) -> None:
        self.__io = io or ConsoleIo()
        self.__env = env or {}
        self.__venv = venv

    def run(self, cmd: str, args: Optional[List[str]] = None, *, capture_output: bool = False) -> ProcessResult:
        to_run = self._to_full_command(cmd, args or [])
        proc = subprocess.run(to_run, shell=True, env=self.__env, capture_output=capture_output)

        return ProcessResult(
            exit_code=proc.returncode, stdout=(proc.stdout or b"").decode(), stderr=(proc.stderr or b"").decode()
        )

    def mute_logs(self) -> "Process":
        return Process(io=MuteIo(), env=self.__env, venv=self.__venv)

    def unmute_logs(self) -> "Process":
        return Process(io=ConsoleIo(), env=self.__env, venv=self.__venv)

    def with_venv(self, venv: str) -> "Process":
        return Process(io=self.__io, env=self.__env, venv=venv)

    def apply_env(self, env: Dict[str, str]) -> "Process":
        return Process(io=self.__io, env={**self.__env, **env}, venv=self.__venv)

    def log(self, text: str) -> None:
        self.__io.text(text)

    def log_title(self, text: str) -> None:
        self.__io.title(text)

    def log_success(self, text: str) -> None:
        self.__io.success(text)

    def log_error(self, text: str) -> None:
        self.__io.error(text)

    def log_warning(self, text: str) -> None:
        self.__io.warning(text)

    def log_help(self, helpable: Helpable) -> None:
        term_cols, _ = shutil.get_terminal_size()
        help_message = helpable.format_help(term_cols)

        self.__io.text(help_message)

    def _to_full_command(self, cmd: str, args: List[str]) -> str:
        full_cmd = f"{cmd}{self._args_as_str(args)}"
        if self.__venv is not None:
            full_cmd = f"{self.__venv} && {full_cmd}"

        return full_cmd

    def _args_as_str(self, args: List[str]) -> str:
        as_str = subprocess.list2cmdline(args)

        return f" {as_str}" if len(as_str) > 0 else ""
