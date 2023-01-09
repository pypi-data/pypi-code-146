#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of click_logging_config.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import copy
import logging
import pathlib
import typing

import click

from click_logging_config._click import LoggingConfiguration, logging_parameters
from click_logging_config._logging import FileLogging, LoggingState
from tests.ci.support.click_runner import click_runner  # noqa: F401


class TestLoggingParameters:
    def test_logging_option(self, capsys, click_runner):
        """Using a logging option."""
        this_context: typing.Optional[click.Context] = None
        user_default_attributes = {
            "enable_console_logging": False,
            "enable_file_logging": False,
            "file_logging": {
                "log_file_path": pathlib.Path("some_file.log"),
                "log_level": logging.DEBUG,
                "file_rotation_size_megabytes": 5,
                "max_rotation_backup_files": 50,
            },
        }
        expected_attributes = {
            "enable_console_logging": True,
            "enable_file_logging": False,
            "file_logging": {
                "log_file_path": pathlib.Path("some_file.log"),
                "log_level": logging.DEBUG,
                "file_rotation_size_megabytes": 5,
                "max_rotation_backup_files": 50,
            },
        }
        expected = LoggingConfiguration.parse_obj(expected_attributes)

        @click.command()
        @click.option(
            "--parm",
            default="a value",
            type=str,
        )
        @logging_parameters(
            LoggingConfiguration.parse_obj(user_default_attributes)
        )
        def mock_main(
            parm: str,
        ):
            nonlocal this_context
            this_context = click.get_current_context()

            assert parm == "a value"

        result = click_runner.invoke(mock_main, ["--log-console-enable"])

        assert result.exit_code == 0

        this_state = this_context.obj["logging_state"]
        assert (
            this_state.configuration.file_logging.log_file_path
            == expected.file_logging.log_file_path
        )
        assert this_state.configuration.log_level == expected.log_level
        assert (
            this_state.configuration.enable_file_logging
            is expected.enable_file_logging
        )
        assert (
            this_state.configuration.enable_console_logging
            is expected.enable_console_logging
        )

    def test_no_user_ctx(self, capsys, click_runner):
        """User does not use ``@click.pass_context decorator``.

        Logging parameters continues to be able to consume click context.
        """
        this_context: typing.Optional[click.Context] = None
        expected = LoggingConfiguration.parse_obj(
            {
                "enable_console_logging": False,
                "enable_file_logging": False,
                "file_logging": FileLogging.parse_obj(
                    {
                        "log_file_path": pathlib.Path("some_file.log"),
                        "log_level": logging.DEBUG,
                        "file_rotation_size_megabytes": 5,
                        "max_rotation_backup_files": 50,
                    },
                ),
            },
        )

        @click.command()
        @click.option(
            "--mock-p",
            default="a value",
            type=str,
        )
        @logging_parameters(expected)
        def mock_main(
            mock_p: str,
        ):
            nonlocal this_context
            this_context = copy.deepcopy(click.get_current_context())

            assert mock_p == "mp"

        result = click_runner.invoke(mock_main, ["--mock-p", "mp"])

        assert result.exit_code == 0

        this_state = this_context.obj["logging_state"]
        assert (
            this_state.configuration.file_logging.log_file_path
            == expected.file_logging.log_file_path
        )
        assert this_state.configuration.log_level == expected.log_level
        assert (
            this_state.configuration.enable_file_logging
            is expected.enable_file_logging
        )
        assert (
            this_state.configuration.enable_console_logging
            is expected.enable_console_logging
        )

    def test_user_ctx(self, capsys, click_runner, mocker):
        """User uses ``@click.pass_context decorator``.

        The user consumption of click context does not interfere with
        logging parameters context.
        """
        this_context: typing.Optional[click.Context] = None
        expected = LoggingConfiguration.parse_obj(
            {
                "enable_console_logging": False,
                "enable_file_logging": False,
                "file_logging": FileLogging.parse_obj(
                    {
                        "log_file_path": pathlib.Path("some_file.log"),
                        "log_level": logging.DEBUG,
                        "file_rotation_size_megabytes": 5,
                        "max_rotation_backup_files": 50,
                    }
                ),
            }
        )

        @click.command()
        @click.pass_context
        @click.option(
            "--mock-p",
            default="a value",
            type=str,
        )
        @logging_parameters(expected)
        def mock_main(
            ctx: click.Context,
            mock_p: str,
        ):
            nonlocal this_context
            this_context = copy.deepcopy(ctx)

            assert mock_p == "mp"

        result = click_runner.invoke(mock_main, ["--mock-p", "mp"])

        assert result.exit_code == 0

        this_state = this_context.obj["logging_state"]
        assert (
            this_state.configuration.file_logging.log_file_path
            == expected.file_logging.log_file_path
        )
        assert this_state.configuration.log_level == expected.log_level
        assert (
            this_state.configuration.enable_file_logging
            is expected.enable_file_logging
        )
        assert (
            this_state.configuration.enable_console_logging
            is expected.enable_console_logging
        )
