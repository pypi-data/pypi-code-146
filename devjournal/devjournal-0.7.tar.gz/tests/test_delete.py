from typer.testing import CliRunner

from devjournal.__main__ import app

runner = CliRunner()


def test_text_is_added_to_entry_file(mock_devjournal_dir, mock_popen):
    mock_popen("hello world")
    runner.invoke(app, ["add"], catch_exceptions=False)
    runner.invoke(app, ["add"], catch_exceptions=False)
    runner.invoke(app, ["add"], catch_exceptions=False)

    result = runner.invoke(app, ["delete", "2"], catch_exceptions=False)
    assert result.exit_code == 0

    entry_paths = list(mock_devjournal_dir.glob("entries/*"))
    assert [path.read_text() for path in entry_paths] == [
        "hello world",
        "hello world",
    ]
