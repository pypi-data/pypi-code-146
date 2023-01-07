from typer.testing import CliRunner

from devjournal.__main__ import app

runner = CliRunner()


def test_text_is_added_to_entry_file(mock_devjournal_dir, mock_popen):
    mock_popen("hello world")
    runner.invoke(app, ["add"], catch_exceptions=False)

    mock_popen("goodbye world")
    runner.invoke(app, ["amend"], catch_exceptions=False)

    entry_files = list(mock_devjournal_dir.glob("entries/*"))
    assert "goodbye world" in entry_files[0].read_text()
