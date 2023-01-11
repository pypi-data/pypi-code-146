import shlex
import sys
from subprocess import CalledProcessError
from typing import Mapping, Pattern, Type, Union

import click
from click import BadParameter, ClickException
from sentry_sdk import capture_exception, push_scope

from .helpers.envvar_option import get_used

ErrorPatterns = Mapping[Pattern[str], Type[Exception]]


def raise_if_match(patterns: ErrorPatterns, msg: str):
    if error := next((err for pat, err in patterns.items() if pat.search(msg)), None):
        raise error


def get_active_env_vars():
    if used := get_used():
        mapping = "\n".join([f"{k}\t--{n}={v}" for k, (n, v) in used.items()])
        envvars = "\n".join(["Active Env Vars:", mapping])
        return f"\n\n{envvars}"
    else:
        return ""


def _format_message(self, file=None):
    msg = click.style(self.message, fg="red", bold=True)
    if hasattr(self, "hints"):
        styled = [click.style(hint, fg="cyan", bold=True) for hint in self.hints]
        hint = "\n\n" + "\n\n".join([f"Hint: {hint}" for hint in styled])
    else:
        hint = ""
    return f"{msg}{hint}{get_active_env_vars()}"


BadParameter.format_message = _format_message


class CliErrorMeta(type):
    _exit_code_count = 2

    def __new__(cls, name, bases, attrs):
        cls._exit_code_count += 1
        klass = super().__new__(cls, name, bases, attrs)
        klass.exit_code = cls._exit_code_count
        return klass


class CliError(ClickException, metaclass=CliErrorMeta):
    def __init__(self, *args, report=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.report = report

    def _report(self):
        with push_scope() as scope:
            scope.level = "info"
            capture_exception()

    def show(self):
        if self.report:
            self._report()
        super().show()

    def format_message(self):
        return _format_message(self)


class CliErrorWithHint(CliError):
    def __init__(self, message, hints, **kwargs) -> None:
        self.hints = hints if isinstance(hints, list) else [hints]
        super().__init__(message, **kwargs)

    def __str__(self):
        return "\n\n".join(
            [
                self.message,
                *[f"Hint: {hint}" for hint in self.hints],
            ]
        )


class OfflineError(CliError):
    def __init__(self) -> None:
        super().__init__("You are currently offline.")


class BotoError(CliErrorWithHint):
    def __init__(self, wrapped: "ClientError", hint: str) -> None:
        message = f"An AWS error occured!\n{str(wrapped)}"
        super().__init__(message, hint)


class FailedSubprocessError(CliError):
    def __init__(self, wrapped: Union[CalledProcessError, str]):
        if isinstance(wrapped, str):
            super().__init__(wrapped)
        elif wrapped.stderr:
            super().__init__(
                "\n".join(
                    [
                        f"Cannot run {shlex.join(wrapped.cmd)}.",
                        "\nThe original error was:",
                        wrapped.stderr,
                    ]
                )
            )
        else:
            super().__init__(f"Cannot run {shlex.join(wrapped.cmd)}.")


class SuppressedError(FailedSubprocessError):
    def __init__(self, wrapped: CalledProcessError, echo=False):
        if echo:
            print(wrapped.stderr, file=sys.stderr)
        wrapped.stderr = None
        wrapped.cmd = [wrapped.cmd[0]]
        super().__init__(wrapped)

    def show(self):
        pass


class WrappedSubprocessError(FailedSubprocessError):
    def __init__(self, wrapped, hint, **kwargs) -> None:
        super().__init__(wrapped)
        messages = [
            f"Cannot run {wrapped.cmd[0]} [{wrapped.returncode}]",
            f"Hint: {hint}",
            f"\nThe original error was:",
            wrapped.stderr,
        ]
        CliError.__init__(self, "\n".join(messages), **kwargs)


class UnknownError(CliErrorWithHint):
    def __init__(self, wrapped: Exception) -> None:
        self.wrapped = wrapped
        super().__init__("An unknown error occurred", str(wrapped), report=True)

    def _report(self):
        with push_scope() as scope:
            scope.level = "info"
            capture_exception(self.wrapped)
