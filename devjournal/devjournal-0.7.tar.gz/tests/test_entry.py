from datetime import datetime

from pytest import CaptureFixture

from devjournal.entry import Entry, print_ids_and_entries


def _strip_rows(string: str) -> str:
    return "\n".join(line.strip() for line in string.splitlines())


def test_print_ids_and_entries(capsys: CaptureFixture):
    print_ids_and_entries(
        [
            (1, Entry(datetime(2021, 12, 26, 22, 55, 10), "hello world")),
            (2, Entry(datetime(2022, 11, 27, 23, 56, 11), "goodbye world")),
        ]
    )
    expected = """1 │ 2021-12-26 22:55:10 │ hello world
2 │ 2022-11-27 23:56:11 │ goodbye world
"""

    assert _strip_rows(capsys.readouterr().out) == _strip_rows(expected)
