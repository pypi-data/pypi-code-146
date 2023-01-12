from unittest.mock import mock_open, patch

from chalk.gitignore.gitignore_parser import parse_gitignore


def test_simple():
    matches = _parse_gitignore_string(("__pycache__/\n" "*.py[cod]"), fake_base_dir="/home/michael")
    assert not matches("/home/michael/main.py")
    assert matches("/home/michael/main.pyc")
    assert matches("/home/michael/dir/main.pyc")
    assert matches("/home/michael/__pycache__")


def test_wildcard():
    matches = _parse_gitignore_string("hello.*", fake_base_dir="/home/michael")
    assert matches("/home/michael/hello.txt")
    assert matches("/home/michael/hello.foobar/")
    assert matches("/home/michael/dir/hello.txt")
    assert matches("/home/michael/hello.")
    assert not matches("/home/michael/hello")
    assert not matches("/home/michael/helloX")


def test_anchored_wildcard():
    matches = _parse_gitignore_string("/hello.*", fake_base_dir="/home/michael")
    assert matches("/home/michael/hello.txt")
    assert matches("/home/michael/hello.c")
    assert not matches("/home/michael/a/hello.java")


def test_trailingspaces():
    matches = _parse_gitignore_string(
        (
            "ignoretrailingspace \n"
            "notignoredspace\\ \n"
            "partiallyignoredspace\\  \n"
            "partiallyignoredspace2 \\  \n"
            "notignoredmultiplespace\\ \\ \\ "
        ),
        fake_base_dir="/home/michael",
    )
    assert matches("/home/michael/ignoretrailingspace")
    assert not matches("/home/michael/ignoretrailingspace ")
    assert matches("/home/michael/partiallyignoredspace ")
    assert not matches("/home/michael/partiallyignoredspace  ")
    assert not matches("/home/michael/partiallyignoredspace")
    assert matches("/home/michael/partiallyignoredspace2  ")
    assert not matches("/home/michael/partiallyignoredspace2   ")
    assert not matches("/home/michael/partiallyignoredspace2 ")
    assert not matches("/home/michael/partiallyignoredspace2")
    assert matches("/home/michael/notignoredspace ")
    assert not matches("/home/michael/notignoredspace")
    assert matches("/home/michael/notignoredmultiplespace   ")
    assert not matches("/home/michael/notignoredmultiplespace")


def test_comment():
    matches = _parse_gitignore_string(
        "somematch\n#realcomment\nothermatch\n\\#imnocomment", fake_base_dir="/home/michael"
    )
    assert matches("/home/michael/somematch")
    assert not matches("/home/michael/#realcomment")
    assert matches("/home/michael/othermatch")
    assert matches("/home/michael/#imnocomment")


def test_ignore_directory():
    matches = _parse_gitignore_string(".venv/", fake_base_dir="/home/michael")
    assert matches("/home/michael/.venv")
    assert matches("/home/michael/.venv/folder")
    assert matches("/home/michael/.venv/file.txt")


def test_ignore_directory_asterisk():
    matches = _parse_gitignore_string(".venv/*", fake_base_dir="/home/michael")
    assert not matches("/home/michael/.venv")
    assert matches("/home/michael/.venv/folder")
    assert matches("/home/michael/.venv/file.txt")


def test_negation():
    matches = _parse_gitignore_string(
        """
*.ignore
!keep.ignore
            """,
        fake_base_dir="/home/michael",
    )
    assert matches("/home/michael/trash.ignore")
    assert not matches("/home/michael/keep.ignore")
    assert matches("/home/michael/waste.ignore")


def test_double_asterisks():
    matches = _parse_gitignore_string("foo/**/Bar", fake_base_dir="/home/michael")
    assert matches("/home/michael/foo/hello/Bar")
    assert matches("/home/michael/foo/world/Bar")
    assert matches("/home/michael/foo/Bar")


def test_single_asterisk():
    matches = _parse_gitignore_string("*", fake_base_dir="/home/michael")
    assert matches("/home/michael/file.txt")
    assert matches("/home/michael/directory")
    assert matches("/home/michael/directory-trailing/")


def _parse_gitignore_string(data: str, fake_base_dir: str):
    with patch("builtins.open", mock_open(read_data=data)):
        success = parse_gitignore(f"{fake_base_dir}/.gitignore", fake_base_dir)
        return success
