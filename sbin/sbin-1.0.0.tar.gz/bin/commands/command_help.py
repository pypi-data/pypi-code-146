from typing import List

from bin.models.bin_base_model import BinBaseModel
from bin.process.helpable import Helpable

_PRE_CMD_SPACING = " " * 2
_DEFAULT_SPACING = " " * 4
_NAIVE_SPACING = " " * 2


class CommandSummary(BinBaseModel):
    command: str
    help: str

    def cmd_part_length(self) -> int:
        return len(f"{_PRE_CMD_SPACING}{self.command}{_DEFAULT_SPACING}")

    def longest_single_word_line_length(self) -> int:
        longest_word_length = max(len(word) for word in self.help.split(" "))
        longest_word_dummy = "x" * longest_word_length
        return len(f"{_PRE_CMD_SPACING}{self.command}{_DEFAULT_SPACING}{longest_word_dummy}\n")

    def naive_format(self) -> str:
        return f"{_PRE_CMD_SPACING}{self.command}{_NAIVE_SPACING}{self.help}\n"

    def pretty_format(self, cmd_nb_cols: int, help_nb_cols: int) -> str:
        current_line = ""
        lines = []
        for word in self.help.split(" "):
            if len(current_line) == 0:
                current_line = word
            elif len(f"{current_line} {word}") > help_nb_cols:
                lines.append(current_line)
                current_line = word
            else:
                current_line += f" {word}"

        lines.append(current_line)
        line_format = f"{{:{cmd_nb_cols}}}{{}}\n"
        text = line_format.format(f"{_PRE_CMD_SPACING}{self.command}", lines[0])
        for line in lines[1:]:
            text += line_format.format("", line)

        return text


class CommandHelp(BinBaseModel, Helpable):
    help: str
    summaries: List[CommandSummary] = []

    @staticmethod
    def only_self(self_help: str) -> "CommandHelp":
        return CommandHelp(help=self_help, summaries=[])

    def format_help(self, max_cols: int) -> str:
        message = f"usage:\n  {self.help}"
        if len(self.summaries) == 0:
            return message

        message += "\n\ncommands:\n"
        longest_cmd_length = 0
        longest_single_word_line_length = 0
        for cmd_summary in self.summaries:
            longest_cmd_length = max((cmd_summary.cmd_part_length()), longest_cmd_length)
            longest_single_word_line_length = max(
                longest_single_word_line_length, cmd_summary.longest_single_word_line_length()
            )

        if longest_single_word_line_length > max_cols:
            message += self._naive_summaries()
        else:
            message += self._pretty_summaries(longest_cmd_length, max_cols - longest_cmd_length)

        return message[:-1]

    def _naive_summaries(self) -> str:
        text = ""
        for summary in self._sorted_summaries():
            text += summary.naive_format()

        return text

    def _pretty_summaries(self, cmd_nb_cols: int, help_nb_cols: int) -> str:
        text = ""
        for summary in self._sorted_summaries():
            text += summary.pretty_format(cmd_nb_cols, help_nb_cols)

        return text

    def _sorted_summaries(self) -> List[CommandSummary]:
        return sorted(self.summaries, key=lambda el: el.command)
