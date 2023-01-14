import logging
from enum import Enum
from typing import Optional, cast

from rich.console import Console
from rich.logging import RichHandler
from rich.style import Style
from rich.theme import Theme

NAME: str = __package__ or "ishutils"


FAILURE: int = logging.ERROR + 1
RUNNING: int = logging.INFO + 1
SKIPPED: int = logging.INFO + 2
SUCCESS: int = logging.INFO + 3


class Action(Enum):
    COPY = "COPY"
    DOWNLOAD = "DOWNLOAD"
    EXTRACT = "EXTRACT"
    MOVE = "MOVE"
    RUN = "RUN"


class Status(Enum):
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"
    SKIPPED = "SKIPPED"
    SUCCESS = "SUCCESS"


class Logger(logging.Logger):
    def format_message(
        self, action: str | Action, status: str | Status, message: str
    ) -> str:
        if isinstance(action, Action):
            action = action.value
        action = str(action).ljust(8)

        if isinstance(status, Status):
            status = status.value
        status = str(status)
        style: str = f"logging.level.{status.lower()}"

        return f"[{style}]" + action + " " + message

    def failure(self, action: str | Action, message: str) -> None:
        self.log(
            level=FAILURE,
            msg=self.format_message(
                action=action, status=Status.FAILURE, message=message
            ),
            stacklevel=2,
        )

    def running(self, action: str | Action, message: str) -> None:
        self.log(
            level=RUNNING,
            msg=self.format_message(
                action=action, status=Status.RUNNING, message=message
            ),
            stacklevel=2,
        )

    def skipped(self, action: str | Action, message: str) -> None:
        self.log(
            level=SKIPPED,
            msg=self.format_message(
                action=action, status=Status.SKIPPED, message=message
            ),
            stacklevel=2,
        )

    def success(self, action: str | Action, message: str) -> None:
        self.log(
            level=SUCCESS,
            msg=self.format_message(
                action=action, status=Status.SUCCESS, message=message
            ),
            stacklevel=2,
        )


def install(
    format: str = "%(message)s",
    level: int | str = logging.NOTSET,
    console: Optional[Console] = None,
    keywords: Optional[list[str]] = [e.value + " " for e in Action],
) -> None:
    logging.addLevelName(level=FAILURE, levelName="FAILURE")
    logging.addLevelName(level=RUNNING, levelName="RUNNING")
    logging.addLevelName(level=SKIPPED, levelName="SKIPPED")
    logging.addLevelName(level=SUCCESS, levelName="SUCCESS")
    logging.setLoggerClass(Logger)
    if console is None:
        console = Console(
            theme=Theme(
                styles={
                    f"logging.level.failure": Style(color="red", bold=True),
                    f"logging.level.running": Style(color="blue", bold=True),
                    f"logging.level.success": Style(color="green", bold=True),
                    f"logging.level.skipped": Style(dim=True),
                }
            )
        )
    logging.basicConfig(
        format=format,
        level=level,
        handlers=[
            RichHandler(level=level, console=console, markup=True, keywords=keywords)
        ],
    )


def get_logger(name: Optional[str] = NAME) -> Logger:
    return cast(Logger, logging.getLogger(name=name))


if __name__ == "__main__":
    install()
    logger = get_logger()
    logger.failure(action="Action", message="Message")
    logger.running(action="Action", message="Message")
    logger.skipped(action="Action", message="Message")
    logger.success(action="Action", message="Message")
