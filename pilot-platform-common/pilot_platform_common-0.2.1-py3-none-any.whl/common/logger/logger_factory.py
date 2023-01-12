import logging
import os
import sys
from logging import Formatter
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional

from common.logger.formatter import get_formatter


class LoggerFactory:
    """Init format and location of log file."""

    def __init__(
        self,
        name: str,
        formatter: Optional[Formatter] = None,
        logs_path: Optional[Path] = None,
        level_default: Optional[int] = 10,
        level_file: Optional[int] = 10,
        level_stdout: Optional[int] = 10,
        level_stderr: Optional[int] = 40,
    ) -> None:
        self.name = name
        self.level_default = level_default
        self.level_file = level_file
        self.level_stdout = level_stdout
        self.level_stderr = level_stderr

        if formatter is None:
            formatter = get_formatter()
        self.formatter = formatter

        if logs_path is None:
            logs_path = Path('./logs')
        self.logs_path = logs_path

        self.log_file_path = os.fspath(self.logs_path / f'{self.name}.log')

        Path(self.logs_path).mkdir(exist_ok=True)

    def get_logger(self) -> Logger:
        """Return instance of logger with multiple handlers."""

        logger = logging.getLogger(self.name)
        logger.setLevel(self.level_default)

        if not logger.handlers:
            # File Handler
            handler = TimedRotatingFileHandler(self.log_file_path, when='D', interval=1, backupCount=2)
            handler.setFormatter(self.formatter)
            handler.setLevel(self.level_file)
            # Standard Out Handler
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(self.formatter)
            stdout_handler.setLevel(self.level_stdout)
            # Standard Err Handler
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setFormatter(self.formatter)
            stderr_handler.setLevel(self.level_stderr)
            # Register handlers
            logger.addHandler(handler)
            logger.addHandler(stdout_handler)
            logger.addHandler(stderr_handler)

        return logger
