from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from rich import print
from rich.table import Table

from devjournal.constants import datetime_from_filename, entries_directory

TIME_FORMAT_FOR_PRINTING = "%Y-%m-%d %H:%M:%S"


@dataclass
class Entry:
    datetime: datetime
    text: str

    @classmethod
    def from_path(cls, path: Path):
        return cls(datetime_from_filename(path.name), path.read_text())


def get_entry_path(id_: int):
    paths = list(entries_directory().glob("*.txt"))
    return paths[id_ - 1]


def get_ids_and_entries() -> list[tuple[int, Entry]]:
    paths = entries_directory().glob("*.txt")
    return [(i, Entry.from_path(path)) for i, path in enumerate(paths, 1)]


def print_ids_and_entries(ids_and_entries: list[tuple[int, Entry]]):
    table = Table(show_header=False, show_edge=False, highlight=True)
    for i, entry in ids_and_entries:
        time = entry.datetime.strftime(TIME_FORMAT_FOR_PRINTING)
        table.add_row(str(i), time, entry.text)
    print(table)
