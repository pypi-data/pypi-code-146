import re
from pathlib import Path
from typing import Any
from typing import Union

import click

DEBUG = False


def set_bit(value: int, bit_index: int, bit_value: bool) -> int:
    """
    Set a bit in a value to 1 or 0.

    Sets the `bit_index`th bit in `value` to 1 if `bit_value` is True, else to 0.
    """
    if bit_value:
        value |= 1 << bit_index
    else:
        value &= ~(1 << bit_index)
    return value


def bitmask_int_to_str(value: int) -> str:
    assert int(value) == value
    value = int(value)
    mask = bin(value)[2:][::-1]
    output = []
    for counter, val in enumerate(mask):
        if val == "1":
            output.append(str(counter))
    return " ".join(output) + f" ({value})"


def debug(message: Any) -> None:
    """Print a message if DEBUG is True."""
    if DEBUG:
        click.echo(str(message))


class TablePrinter:
    """A helper context manager that prints pretty tables."""

    WIDTH = 24

    def __init__(self, *columns: str) -> None:
        """Initialize the context manager and print the header."""
        self._num_columns = len(columns)
        column_str = [columns[0].ljust(self.WIDTH)] + [
            column.rjust(self.WIDTH) for column in columns[1:]
        ]

        column_str = [click.style(c, fg="cyan") for c in column_str]
        click.echo(" | ".join(column_str))
        click.echo("-|-".join([("-" * self.WIDTH)] * self._num_columns))

    @classmethod
    def print_row(cls, *columns: Any):
        """Print a single row."""
        column_str = [click.style(columns[0].ljust(cls.WIDTH), fg="green")] + [
            str(column).rjust(cls.WIDTH) for column in columns[1:]
        ]
        click.echo(" | ".join(column_str))

    def __enter__(self):
        """Enter the context manager and return the printing function."""
        return self.print_row

    def __exit__(self, type, value, traceback):
        """Print the footer."""
        click.echo("-|-".join([("-" * self.WIDTH)] * self._num_columns))


class RegexType(click.ParamType):
    name = "regex"

    def convert(self, value, param, ctx):
        try:
            return re.compile(value, re.IGNORECASE)
        except re.error as e:
            self.fail(
                "Regex error: " + str(e),
                param,
                ctx,
            )


def get_craft_name(filename: Union[str, Path], default: str) -> str:
    """Return the craft name (or a default) from the filename."""
    if not re.search(r"_\d{4}-\d\d-\d\d_\d\d-\d\d$", Path(filename).stem):
        # It's not a default filename, so we don't know what to do.
        return default
    name = Path(filename).stem[:-17]
    return name.replace("_", " ")
