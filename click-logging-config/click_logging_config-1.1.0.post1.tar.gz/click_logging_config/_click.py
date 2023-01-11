#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of click_logging_config.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import copy
import functools
import logging
import pathlib
import typing

import click
from click.decorators import FC

from ._default_values import VALID_LOG_LEVELS
from ._logging import LoggingConfiguration, LoggingState
from ._version import __version__

log = logging.getLogger(__name__)

LOG_STATE_KEY = "logging_state"


def logging_parameters(
    default_configuration: typing.Optional[LoggingConfiguration] = None,
) -> typing.Union[typing.Callable[..., typing.Any], click.Command]:
    """Define a set of logging configuration options to a ``click`` command.

    Args:
        default_configuration: User defined logging default configuration.

    Returns:
        The decorator function object.
    """
    resolved_configuration: LoggingConfiguration
    if not default_configuration:
        resolved_configuration = LoggingConfiguration()
    else:
        resolved_configuration = typing.cast(
            LoggingConfiguration, default_configuration
        )

    def decorator(f: FC) -> FC:
        @click.option(
            "--log-console-enable/--log-console-disable",
            "enable_console_log",
            default=resolved_configuration.enable_console_logging,
            help="Enable or disable console logging.",
            is_flag=True,
            show_default=True,
        )
        @click.option(
            "--log-console-json-enable/--log-console-json-disable",
            "enable_console_json",
            default=resolved_configuration.console_logging.json_enabled,
            help="Enable or disable console JSON logging.",
            is_flag=True,
            show_default=True,
        )
        @click.option(
            "--log-file-enable/--log-file-disable",
            "enable_file_log",
            default=resolved_configuration.enable_file_logging,
            help="Enable or disable file logging.",
            is_flag=True,
            show_default=True,
        )
        @click.option(
            "--log-file-json-enable/--log-file-json-disable",
            "enable_file_json",
            default=resolved_configuration.file_logging.json_enabled,
            help="Enable or disable file JSON logging.",
            is_flag=True,
            show_default=True,
        )
        @click.option(
            "--log-file",
            "log_file",
            default=resolved_configuration.file_logging.log_file_path,
            help="The log file to write to.",
            is_eager=True,
            show_default=True,
            type=click.Path(
                dir_okay=False,
                exists=False,
                file_okay=True,
                path_type=pathlib.Path,
                writable=True,
                readable=True,
            ),
        )
        @click.option(
            "--log-level",
            "log_level",
            default=resolved_configuration.log_level,
            help="Select logging level to apply to all enabled log sinks.",
            show_default=True,
            type=click.Choice(VALID_LOG_LEVELS, case_sensitive=False),
        )
        def wrapper(
            *args: typing.Any,
            enable_console_log: bool,
            enable_console_json: bool,
            enable_file_log: bool,
            enable_file_json: bool,
            log_file: pathlib.Path,
            log_level: str,
            **kwargs: typing.Any,
        ) -> typing.Any:
            ctx = click.get_current_context()
            this_object = ctx.ensure_object(dict)
            if LOG_STATE_KEY not in this_object:
                this_configuration = copy.deepcopy(resolved_configuration)
                this_configuration.enable_console_logging = enable_console_log
                this_configuration.console_logging.json_enabled = (
                    enable_console_json
                )
                this_configuration.enable_file_logging = enable_file_log
                this_configuration.file_logging.json_enabled = enable_file_json
                this_configuration.file_logging.log_file_path = log_file
                this_configuration.log_level = log_level

                this_object[LOG_STATE_KEY] = LoggingState(this_configuration)
                log.info(f"Click logging config version, {__version__}")
            elif not isinstance(this_object, dict):
                raise RuntimeError(
                    "Unable to define logging state since click context.obj is "
                    "not a dictionary"
                )

            return ctx.invoke(
                f,
                *args,
                **kwargs,
            )

        return functools.update_wrapper(typing.cast(FC, wrapper), f)

    return decorator
