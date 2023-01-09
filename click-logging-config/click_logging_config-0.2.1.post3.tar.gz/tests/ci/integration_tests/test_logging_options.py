#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of click_logging_parameters.
#
#  You should have received a copy of the MIT License along with click_logging_parameters.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import logging
import typing

import click
import pytest
from click.testing import CliRunner, Result

from tests.ci.support.click_runner import click_runner  # noqa: F401


def _invoke_command(
    runner, mm, arguments=[]
) -> typing.Tuple[Result, click.Context]:
    click_context: typing.Optional[click.Context] = None

    def _acquire_context(c: click.Context) -> None:
        nonlocal click_context
        click_context = c

    this_main = mm(_acquire_context)
    result = runner.invoke(this_main, arguments)

    return result, click_context


def test_default_logging(click_runner, mock_file_handler, mock_main):
    result, click_context = _invoke_command(click_runner, mock_main)

    assert result.exit_code == 0

    logging_state = click_context.obj["logging_state"]
    assert logging_state
    assert logging_state.configuration.enable_file_logging
    assert not logging_state.configuration.enable_console_logging
    assert logging_state.configuration.log_level == "warning"


def test_enable_console_logging(click_runner, mock_file_handler, mock_main):
    result, click_context = _invoke_command(
        click_runner, mock_main, ["--log-console-enable"]
    )

    assert result.exit_code == 0

    logging_state = click_context.obj["logging_state"]
    assert logging_state.configuration.enable_file_logging
    assert logging_state.configuration.enable_console_logging
    assert logging_state.configuration.log_level == "warning"


def test_enable_console_json_logging(
    click_runner, mock_file_handler, mock_main
):
    result, click_context = _invoke_command(
        click_runner,
        mock_main,
        ["--log-console-enable", "--log-console-json-enable"],
    )

    assert result.exit_code == 0

    logging_state = click_context.obj["logging_state"]
    assert logging_state.configuration.enable_console_logging
    assert logging_state.configuration.console_logging.json_enabled


def test_disable_console_json_logging(
    click_runner, mock_file_handler, mock_main
):
    result, click_context = _invoke_command(
        click_runner,
        mock_main,
        ["--log-console-enable", "--log-console-json-disable"],
    )

    assert result.exit_code == 0

    logging_state = click_context.obj["logging_state"]
    assert logging_state.configuration.enable_console_logging
    assert not logging_state.configuration.console_logging.json_enabled


def test_disable_file_logging(click_runner, mock_file_handler, mock_main):
    result, click_context = _invoke_command(
        click_runner, mock_main, ["--log-file-disable"]
    )

    assert result.exit_code == 0

    logging_state = click_context.obj["logging_state"]
    assert not logging_state.configuration.enable_file_logging
    assert not logging_state.configuration.enable_console_logging
    assert logging_state.configuration.log_level == "warning"


def test_enable_file_json_logging(click_runner, mock_file_handler, mock_main):
    result, click_context = _invoke_command(
        click_runner, mock_main, ["--log-file-enable", "--log-file-json-enable"]
    )

    assert result.exit_code == 0

    logging_state = click_context.obj["logging_state"]
    assert logging_state.configuration.enable_file_logging
    assert logging_state.configuration.file_logging.json_enabled


def test_disable_file_json_logging(click_runner, mock_file_handler, mock_main):
    result, click_context = _invoke_command(
        click_runner,
        mock_main,
        ["--log-file-enable", "--log-file-json-disable"],
    )

    assert result.exit_code == 0

    logging_state = click_context.obj["logging_state"]
    assert logging_state.configuration.enable_file_logging
    assert not logging_state.configuration.file_logging.json_enabled


def test_enable_file_logging(click_runner, mock_file_handler, mock_main):
    result, click_context = _invoke_command(
        click_runner, mock_main, ["--log-file-enable"]
    )

    assert result.exit_code == 0

    logging_state = click_context.obj["logging_state"]
    assert logging_state.configuration.enable_file_logging
    assert not logging_state.configuration.enable_console_logging
    assert logging_state.configuration.log_level == "warning"


class TestLogLevel:
    def _do_test(self, this_level: str, mm):
        click_runner = CliRunner()
        result, click_context = _invoke_command(
            click_runner, mm, ["--log-level", this_level]
        )

        if result.exit_code != 0:
            pytest.fail("Valid log level failed test, {0}".format(this_level))

        logging_state = click_context.obj["logging_state"]
        assert logging_state.configuration.log_level == this_level

    def test_critical(self, mock_file_handler, mock_main):
        self._do_test("critical", mock_main)

    def test_error(self, mock_file_handler, mock_main):
        self._do_test("error", mock_main)

    def test_warning(self, mock_file_handler, mock_main):
        self._do_test("warning", mock_main)

    def test_info(self, mock_file_handler, mock_main):
        self._do_test("info", mock_main)

    def test_debug(self, mock_file_handler, mock_main):
        self._do_test("debug", mock_main)

    def test_notset(self, mock_file_handler, mock_main):
        self._do_test("notset", mock_main)

    def test_bad_level(self, click_runner, mock_file_handler, mock_main):
        result, click_context = _invoke_command(
            click_runner, mock_main, ["--log-level", "bad_level"]
        )
        assert result.exit_code != 0

    def test_mixed_case(self, click_runner, mock_file_handler, mock_main):
        result, click_context = _invoke_command(
            click_runner, mock_main, ["--log-level", "Debug"]
        )

        assert result.exit_code == 0

        logging_state = click_context.obj["logging_state"]
        assert logging_state.configuration.log_level == "debug"

    def test_upper_case(self, click_runner, mock_file_handler, mock_main):
        result, click_context = _invoke_command(
            click_runner, mock_main, ["--log-level", "DEBUG"]
        )

        assert result.exit_code == 0

        logging_state = click_context.obj["logging_state"]
        assert logging_state.configuration.log_level == "debug"
