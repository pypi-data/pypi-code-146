from pathlib import Path

from sym.shared.cli.helpers.os import safe_create


def _assert_content(path: Path, expected: str) -> None:
    with path.open() as f:
        assert f.read() == expected


def test_safe_create(tmp_path: Path) -> None:
    foo_path = tmp_path / "foo"
    bar_path = tmp_path / "bar"
    with foo_path.open("x") as f:
        f.write("foo")

    bar_path.symlink_to("foo")
    _assert_content(bar_path, "foo")

    with safe_create(bar_path) as f:
        f.write("bar")
    _assert_content(bar_path, "bar")

    # This is, of course, what we're really testing for: that
    # foo didn't get overwritten.
    _assert_content(foo_path, "foo")
