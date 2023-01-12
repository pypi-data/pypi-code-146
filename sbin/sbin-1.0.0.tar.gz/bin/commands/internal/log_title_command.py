from typing import List

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.models.bin_base_model import BinBaseModel
from bin.process.emoji import Emoji
from bin.process.helpable import Helpable
from bin.process.process import Process


class _BoxChars:
    NORTH_WEST = "┏"
    NORTH = "━"
    NORTH_EAST = "┓"
    EAST = "┃"
    SOUTH_EAST = "┛"
    SOUTH = "━"
    SOUTH_WEST = "┗"
    WEST = "┃"


TITLE_COLS = 6


class LogTitleCommand(BinBaseModel, Command):
    title: str

    @classmethod
    def venv(cls) -> "LogTitleCommand":
        return cls(title=f"Virtual environment {Emoji.HOME}")

    @classmethod
    def requirements(cls) -> "LogTitleCommand":
        return cls(title=f"Requirements {Emoji.NOTE}")

    @classmethod
    def up(cls) -> "LogTitleCommand":
        return cls(title=f"Up {Emoji.PLANE_UP}")

    @classmethod
    def down(cls) -> "LogTitleCommand":
        return cls(title=f"Down {Emoji.PLANE_DOWN}")

    def _run(self, process: Process, args: List[str]) -> Process:
        length = len(self.title) + TITLE_COLS
        text_format = f"{{:^{length}}}"
        text = text_format.format(self.title)
        title = ""
        # length + 1 here is needed because of the emojis in the title
        title += _BoxChars.NORTH_WEST + (length + 1) * _BoxChars.NORTH + _BoxChars.NORTH_EAST + "\n"
        title += _BoxChars.WEST + text + _BoxChars.EAST + "\n"
        title += _BoxChars.SOUTH_WEST + (length + 1) * _BoxChars.SOUTH + _BoxChars.SOUTH_EAST

        process.log_title(title)
        return process

    def _get_short_description(self) -> str:
        return "inner step, never triggered"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self("inner step, never triggered")
