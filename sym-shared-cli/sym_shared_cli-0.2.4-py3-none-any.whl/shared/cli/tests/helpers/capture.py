import os
import re
import shlex
import subprocess
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Pattern, Sequence, Tuple, Union

from _pytest.monkeypatch import MonkeyPatch
from expects import *


class ExecutedCommand:
    def __init__(
        self,
        args: Sequence[str],
        result: subprocess.CompletedProcess,
        env: Dict[str, str] = {},
    ):
        if isinstance(args, str):
            self.args = shlex.split(args)
        else:
            self.args = list(args)

        self.env = env
        self.result = result


class ExpectedCommand:
    def __init__(
        self,
        args: Sequence[str],
        *,
        env: Dict[str, str] = {},
    ):
        self.args = args
        self.env = env

    def assert_command(self, actual: ExecutedCommand) -> None:
        expect(actual.args).to(contain(*self.args))
        expect(actual.env.items()).to(contain(*self.env.items()))


def c(*args, **kwargs) -> ExpectedCommand:
    return ExpectedCommand(args, env=kwargs)


class CaptureCommand:
    def __init__(self, monkeypatch: MonkeyPatch):
        self.monkeypatch = monkeypatch
        self.commands: List[List[str]] = []
        self.executed_commands: List[ExecutedCommand] = []
        self.outputs = []
        self.matched_outputs: List[Tuple[Pattern, str, int, bool, bool]] = []
        self.allowed_calls = []
        self._run = getattr(subprocess, "run")

    def _get_output(self, args: Sequence[str]):
        command = shlex.join(args)
        for (pattern, output, exit_code, stderr, timeout) in self.matched_outputs:
            if pattern.search(command):
                if timeout:
                    raise subprocess.TimeoutExpired(command, 0, stderr=output)
                if exit_code:
                    raise subprocess.CalledProcessError(exit_code, args, stderr=output)
                elif stderr:
                    return subprocess.CompletedProcess(
                        args=args, returncode=0, stderr=output
                    )
                else:
                    return output
        if self.outputs:
            return self.outputs.pop(0)

    # This function is designed for capturing the run_subprocess decorator only.
    # It is not intended to capture subprocess.run calls generally. For example,
    # `args` has a much more constrained type than subprocess.run normally allows.
    def _run_stub(
        self, args: Sequence[str], **kwargs: Any
    ) -> subprocess.CompletedProcess:
        if isinstance(args, str):
            self.commands.append(shlex.split(args))
        else:
            self.commands.append(list(args))
        if args[0] in self.allowed_calls:
            output = self._run(args, **kwargs)
        else:
            output = self._get_output(args)
            if not isinstance(output, subprocess.CompletedProcess):
                output = subprocess.CompletedProcess(
                    args=args, returncode=0, stdout=output
                )
        env = dict(os.environ)
        self.executed_commands.append(ExecutedCommand(args, output, env))
        return output

    @contextmanager
    def __call__(self) -> Iterator["CaptureCommand"]:
        with self.monkeypatch.context() as mp:
            mp.setattr(subprocess, "run", self._run_stub)
            yield self

    def enqueue_outputs(self, *outputs: Sequence[str]) -> None:
        self.outputs.extend(outputs)

    def register_output(
        self,
        pattern: str,
        output: str,
        *,
        exit_code=0,
        stderr: bool = False,
        timeout: bool = False,
    ) -> None:
        """Stubs a subprocess matching the provided pattern and sets its output."""
        self.matched_outputs.append(
            (re.compile(pattern), output, exit_code, stderr, timeout)
        )

    def allow_call(self, binary: str) -> None:
        self.allowed_calls.append(binary)

    def assert_command(self, *commands: Union[str, Sequence[str]]) -> None:
        expect(self.commands).to(have_len(len(commands)))
        for (actual, expected) in zip(self.commands, commands):
            if isinstance(expected, Pattern):
                expect(shlex.join(actual)).to(match(expected))
            elif isinstance(expected, list):
                expect(actual).to(contain(*expected))
            else:
                expect(actual).to(equal(shlex.split(expected)))

    def assert_commands(self, commands: List[ExpectedCommand]) -> None:
        expect(self.executed_commands).to(have_len(len(commands)))
        for (actual, expected) in zip(self.executed_commands, commands):
            expected.assert_command(actual)
