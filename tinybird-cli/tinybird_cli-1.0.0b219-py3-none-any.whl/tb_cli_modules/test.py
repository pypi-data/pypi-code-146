
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import glob
import click
from tinybird.feedback_manager import FeedbackManager
from typing import Any, Dict, List

from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import coro, create_tb_client
from tinybird.tb_cli_modules.tinyunit.tinyunit import generate_file, parse_file, run_test_file, test_run_summary


@cli.group()
@click.pass_context
def test(ctx):
    '''Test commands'''


@test.command(name="run", help="Run the test suite, a file, or a test.")
@click.argument('file', nargs=-1)
@click.option('-v', is_flag=True, default=False, help='Enable verbose (show results)', type=bool)
@click.option('--fail', 'only_fail', is_flag=True, default=False, help='Show only failed/error tests', type=bool)
@click.pass_context
@coro
async def test_run(ctx: click.Context, file, v, only_fail):
    test_file_results: Dict[str, Dict[str, Dict[str, Any]]] = {}

    try:
        tb_client = create_tb_client(ctx)
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))
        raise e

    file_list: List[str] = file if len(file) > 0 else glob.glob("./tests/*.yaml")
    for test_file in file_list:
        try:
            test_result = await run_test_file(tb_client, test_file)
            test_file_results[test_file] = test_result
        except Exception as e:
            click.echo(FeedbackManager.error_running_test(file=test_file))
            if v:
                click.echo(FeedbackManager.error_exception(error=e))
    if len(test_file_results) <= 0:
        click.echo(FeedbackManager.error_no_test_results())
    else:
        test_run_summary(test_file_results, only_fail=only_fail, verbose_level=int(v))


@test.command(name="init", help="Initialize a file list with a simple test suite.")
@click.argument('file', nargs=-1)
@click.option('--force', is_flag=True, default=False, help="Override existing files")
@click.pass_context
@coro
async def test_init(ctx: click.Context, file, force):
    if len(file) == 0:
        file = ("tests/default.yaml",)

    for f in file:
        generate_file(f, overwrite=force)


@test.command(name="parse", help="Read the contents of a test file list.")
@click.argument('files', nargs=-1)
@click.pass_context
@coro
async def test_parse(ctx: click.Context, files):
    for f in files:
        click.echo(f"\nFile: {f}")
        for test in parse_file(f):
            click.echo(test)
