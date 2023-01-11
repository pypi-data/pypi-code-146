import re
from pathlib import Path

from click.testing import CliRunner
import gl_parser.cli.convert_commmands
from gl_parser.enums import ExitCode


def test_convert_file_not_found():
    file = './file.xlsx'
    runner = CliRunner()
    result = runner.invoke(gl_parser.cli.convert_commmands.convert, ['-f', file])
    results = result.output.split('\n')
    assert result.exit_code == ExitCode.INVALID_PATH
    assert len(results) == 2
    assert results[0] == 'File file.xlsx does not exist.'
    # help_result = runner.invoke(cli_commands.main, ['--help'])


def test_convert_file(fixtures_folder):
    regexp = re.compile(r"^Successfully\sconverted\sfile\sto\s(?P<filename>.+\.xlsx)$")
    small_excel = str(fixtures_folder / 'general_ledger_small.xlsx')
    runner = CliRunner()
    result = runner.invoke(gl_parser.cli.convert_commmands.convert, ['-f', small_excel])
    results = result.output.split('\n')
    assert result.exit_code == 0
    assert len(results) == 3
    match = regexp.match(results[1])
    assert match is not None
    output_file = Path(match.group('filename'))
    assert output_file.exists()
    output_file.unlink()
