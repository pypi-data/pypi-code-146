from typing import Callable, Dict, Type, TypeVar

from pydantic import ValidationError

from bin.commands.command import Command
from bin.commands.errors import CommandFailedError, CommandNotFound, CommandParseError
from bin.env.errors import EnvProvisionError
from bin.process.process import Process

ExitCode = int
T = TypeVar("T", bound=Exception)
KeyType = Type[T]
OnErrorCallback = Callable[[T, Command, Process], ExitCode]


class ErrorHandler:
    def __init__(self) -> None:
        self.__handlers: Dict[KeyType, OnErrorCallback] = {}  # type: ignore

    def register(self, error: KeyType, callback: OnErrorCallback) -> None:  # type: ignore
        self.__handlers[error] = callback

    def handle(self, exc: T, cmd: Command, process: Process) -> ExitCode:
        if type(exc) in self.__handlers:
            return self.__handlers[type(exc)](exc, cmd, process)

        if Exception in self.__handlers:
            return self.__handlers[Exception](exc, cmd, process)

        return 1


def get_error_handler() -> ErrorHandler:
    handler = ErrorHandler()
    handler.register(CommandParseError, __command_parse_error)
    handler.register(ValidationError, __validation_error)
    handler.register(EnvProvisionError, __env_provision_error)
    handler.register(CommandNotFound, __command_not_found)
    handler.register(CommandFailedError, __command_failed)
    handler.register(Exception, __exception)

    return handler


def __command_parse_error(exc: CommandParseError, _: Command, process: Process) -> int:
    return __log_exception(process, str(exc), "invalid bin file")


def __validation_error(_: ValidationError, __: Command, process: Process) -> int:
    process.log_error("error: invalid bin file (exit code 1)")

    return 1


def __env_provision_error(exc: EnvProvisionError, __: Command, process: Process) -> int:
    return __log_exception(process, str(exc), "env loading failed")


def __command_not_found(exc: CommandNotFound, cmd: Command, process: Process) -> int:
    try:
        cmd.run(process, ["--help"])
        process.log_error(f"\nerror: {str(exc)} (exit code 1)")
    except Exception:
        process.log_error(f"error: {str(exc)}\n\nunexpected error happened when running --help (exit code 1)")

    return 1


def __command_failed(exc: CommandFailedError, _: Command, process: Process) -> int:
    return __log_exception(process, str(exc), "command failed")


def __exception(exc: Exception, _: Command, process: Process) -> int:
    return __log_exception(process, str(exc), "unhandled error")


def __log_exception(process: Process, details: str, error_message: str, exit_code: int = 1) -> int:
    process.log(details)
    process.log_error(f"\nerror: {error_message} (exit code {exit_code})")

    return exit_code
