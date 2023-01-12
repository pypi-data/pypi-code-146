class CommandParseError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CommandNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("command not found")


class CommandFailedError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @classmethod
    def must_run_without_args(cls, what: str) -> "CommandFailedError":
        return cls(f"{what}: must run without arguments")

    @classmethod
    def command_failed(cls, what: str) -> "CommandFailedError":
        return cls(f"{what}: command failed")

    @classmethod
    def failed_with_reason(cls, what: str, reason: str) -> "CommandFailedError":
        return cls(f"{what}: command failed, {reason}")
