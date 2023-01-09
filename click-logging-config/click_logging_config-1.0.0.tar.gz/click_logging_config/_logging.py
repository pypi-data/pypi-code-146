#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of click_logging_config.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.

"""Logging configuration and state."""

import logging.handlers
import pathlib
import typing

import json_log_formatter  # type: ignore
import pendulum
import pydantic
import pytz

from ._default_values import (
    DEFAULT_CONSOLE_JSON_ENABLED,
    DEFAULT_CONSOLE_LOGGING_ENABLED,
    DEFAULT_FILE_JSON_ENABLED,
    DEFAULT_FILE_LOGGING_ENABLED,
    DEFAULT_FILE_ROTATION_BACKUPS,
    DEFAULT_FILE_ROTATION_SIZE_MB,
    DEFAULT_LOG_FILE,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_LEVEL,
)


class ConsoleLogging(pydantic.BaseModel):
    """Console log configuration parameters."""

    json_enabled: bool = DEFAULT_CONSOLE_JSON_ENABLED


class FileLogging(pydantic.BaseModel):
    """Log file configuration parameters.

    In this context file logs are *always* rotated - the rotation just might be
    at a relatively large file size. As a best practice, not rotating log files
    is considered not particularly useful.
    """

    json_enabled: bool = DEFAULT_FILE_JSON_ENABLED
    log_file_path: pathlib.Path = DEFAULT_LOG_FILE
    file_rotation_size_megabytes: int = DEFAULT_FILE_ROTATION_SIZE_MB
    max_rotation_backup_files: int = DEFAULT_FILE_ROTATION_BACKUPS


class LoggingConfiguration(pydantic.BaseModel):
    """Logging configuration data."""

    log_level: str = DEFAULT_LOG_LEVEL

    enable_console_logging: bool = DEFAULT_CONSOLE_LOGGING_ENABLED
    console_logging: ConsoleLogging = ConsoleLogging()

    enable_file_logging: bool = DEFAULT_FILE_LOGGING_ENABLED
    file_logging: FileLogging = FileLogging()


U = typing.TypeVar("U", bound="Iso8601Formatter")


class Iso8601Formatter(logging.Formatter):
    """Custom formatter with ISO-8601 timestamps."""

    converter: typing.Callable[
        ..., pendulum.DateTime
    ] = pendulum.from_timestamp  # type: ignore [assignment]

    def formatTime(
        self: U,
        record: logging.LogRecord,
        datefmt: typing.Optional[str] = None,
        timezone: typing.Optional[str] = None,
    ) -> str:
        """Generate formatted time."""
        if timezone:
            v = Iso8601Formatter.converter(
                record.created,
                tz=pytz.timezone(timezone),
            ).isoformat()
        else:
            v = Iso8601Formatter.converter(
                record.created,
            ).isoformat()

        return v


T = typing.TypeVar("T", bound="LoggingState")


class LoggingState:
    """Logging configuration parameters."""

    configuration: LoggingConfiguration
    _console_handler: typing.Optional[logging.StreamHandler]
    _rotation_handler: typing.Optional[logging.handlers.RotatingFileHandler]

    def __init__(
        self: T,
        logging_configuration: LoggingConfiguration,
    ) -> None:
        """Construct ``LoggingState`` object.

        Args:
            logging_configuration: Logging configuration to be applied.
        """
        self.configuration = logging_configuration
        self._console_handler = None
        self._rotation_handler = None

        self.set_logging_state()

    def set_logging_state(self: T) -> None:
        """Apply the logging state from configuration."""
        root_logger = logging.getLogger()
        self.__set_log_level(root_logger)
        self.__set_file_logging(root_logger)
        self.__set_console_logging(root_logger)

    def __level_value(self: T) -> int:
        """Convert log level text to a ``logging`` framework integer."""
        return getattr(logging, self.configuration.log_level.upper())

    def __set_file_logging(self: T, root_logger: logging.Logger) -> None:
        """Enable or disable file logging.

        Args:
            root_logger: Root logger to modify.
        """
        if self.configuration.enable_file_logging:
            # No change if a rotation handler already exists.
            if not self._rotation_handler:
                this_handler = logging.handlers.RotatingFileHandler(
                    str(self.configuration.file_logging.log_file_path),
                    backupCount=(
                        self.configuration.file_logging.max_rotation_backup_files  # noqa: E501
                    ),
                    maxBytes=(  # noqa: E501
                        self.configuration.file_logging.file_rotation_size_megabytes  # noqa: E501
                        * (1024**2)
                    ),
                )
                this_handler.setLevel(self.__level_value())
                if self.configuration.file_logging.json_enabled:
                    this_handler.setFormatter(
                        json_log_formatter.VerboseJSONFormatter()
                    )
                else:
                    this_handler.setFormatter(
                        Iso8601Formatter(fmt=DEFAULT_LOG_FORMAT)
                    )

                self._rotation_handler = this_handler

                root_logger.addHandler(self._rotation_handler)
        elif self._rotation_handler:
            self._rotation_handler.flush()
            self._rotation_handler.close()
            root_logger.removeHandler(self._rotation_handler)
            self._rotation_handler = None
        # else self._rotation_handler is None and not self.enable_file_logging
        # so do nothing

    def __set_console_logging(self: T, root_logger: logging.Logger) -> None:
        """Enable or disable console logging.

        Args:
            root_logger: Root logger to modify.
        """
        # def remove_stream_handlers() -> None:
        #     nonlocal root_logger
        #     for this_handler in root_logger.handlers:
        #         if type(this_handler) == logging.StreamHandler:
        #             root_logger.removeHandler(this_handler)

        # Have to remove ALL stream handlers to fully disable console
        # logging.
        # remove_stream_handlers()
        if self.configuration.enable_console_logging:
            self._console_handler = logging.StreamHandler()
            self._console_handler.setLevel(self.__level_value())
            if self.configuration.console_logging.json_enabled:
                self._console_handler.setFormatter(
                    json_log_formatter.VerboseJSONFormatter()
                )
            else:
                self._console_handler.setFormatter(
                    Iso8601Formatter(fmt=DEFAULT_LOG_FORMAT)
                )

            root_logger.addHandler(self._console_handler)
        elif self._console_handler:
            self._console_handler.flush()
            self._console_handler.close()
            root_logger.removeHandler(self._console_handler)
            self._console_handler = None
        # else self._console_handler is None and not
        # self.enable_console_logging so do nothing

    def __set_log_level(self: T, root_logger: logging.Logger) -> None:
        """Set log level on any existing handlers.

        Args:
            root_logger: Root logger to modify.
        """
        for this_handler in root_logger.handlers:
            this_handler.setLevel(self.__level_value())
        # Ensure that the logging level propagates to any subsequently created
        # handlers by setting the root logger level as well.
        root_logger.setLevel(self.__level_value())
