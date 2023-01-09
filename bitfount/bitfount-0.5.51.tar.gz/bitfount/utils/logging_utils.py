"""Utilities for logging and warning messages functionality."""
from contextlib import contextmanager
from datetime import datetime
import logging
from pathlib import Path
import re
import sys
from typing import Final, Generator, List, Optional, Union
import warnings

from bitfount.config import BITFOUNT_LOG_TO_FILE, BITFOUNT_LOGS_DIR

# Timestamp when this module is read in. Guarantees that any file-loggers will refer
# to the same file.
_log_file_time: Final = datetime.now().strftime("%Y-%m-%d-%H%M%S")


@contextmanager
def filter_stderr(to_filter: Union[str, re.Pattern]) -> Generator[None, None, None]:
    """Filter stderr messages emitted within this context manager.

    Will remove any messages where the start matches the filter pattern whilst allowing
    any other messages to go through.

    Args:
        to_filter: Regex pattern to match the start of messages to be filtered.
    """
    # Compile regex pattern if not already done
    reg_to_filter: re.Pattern[str]
    if isinstance(to_filter, str):
        reg_to_filter = re.compile(to_filter)
    else:
        reg_to_filter = to_filter

    # Store previous stderr.write() method
    _stderr_write = sys.stderr.write

    def _write(s: str) -> int:
        """Override write() method of stderr."""
        if reg_to_filter.match(s):
            # Do nothing, write 0 bytes
            return 0
        else:
            return _stderr_write(s)

    # mypy_reason: mypy is overzealous with functions being assigned to instance
    #              methods as it cannot easily determine the type of the callable
    #              between bound and unbound. "type: ignore" is the recommended
    #              workaround.
    #              See: https://github.com/python/mypy/issues/2427
    try:
        sys.stderr.write = _write  # type: ignore[assignment] # Reason: see comment
        yield
    finally:
        # Need to ensure that anything written to stderr during this time is flushed
        # out as otherwise may not be printed until the stderr.write is reset
        sys.stderr.flush()
        # Reset stderr.write() method
        sys.stderr.write = _stderr_write  # type: ignore[assignment] # Reason: see comment # noqa: B950


def _get_bitfount_logdir(subdir_name: Optional[str] = None) -> Path:
    """Get the directory that Bitfount logs should be written to.

    This will be BITFOUNT_LOGS_DIR unless subdir_name is specified in which case
    it will be that subdirectory within BITFOUNT_LOGS_DIR.
    """
    # Establish log directory and create it if it doesn't exist
    parent_logfile_dir = BITFOUNT_LOGS_DIR

    if subdir_name:
        logfile_dir = parent_logfile_dir / subdir_name
    else:
        logfile_dir = parent_logfile_dir

    logfile_dir.mkdir(parents=True, exist_ok=True)
    return logfile_dir


def _get_bitfount_log_file_handler(
    log_file_subdir_name: Optional[str] = None,
) -> logging.FileHandler:
    """Get a FileHandler pre-configured for Bitfount style.

    Will create the log file in BITFOUNT_LOGS_DIR unless log_file_subdir_name is
    specified in which case it will be created in that subdirectory within
    BITFOUNT_LOGS_DIR.

    Log-level will be DEBUG.
    """
    logfile_dir = _get_bitfount_logdir(log_file_subdir_name)

    # Set file logging configuration
    file_handler = logging.FileHandler(f"{logfile_dir}/{_log_file_time}.log")
    file_log_formatter = logging.Formatter(
        "%(asctime)s:"
        " %(threadName)s:"
        " [%(levelname)-8s]"
        " %(name)s:%(filename)s:%(lineno)d:"
        " %(message)s"
    )
    file_handler.setFormatter(file_log_formatter)
    file_handler.setLevel(logging.DEBUG)

    return file_handler


def _configure_logging() -> None:
    """Configure logging and third-party loggers to adhere to Bitfount style."""
    # Set up logging to capture any `warnings` module issues raised.
    logging.captureWarnings(True)

    # Handle pytorch_lightning loggers if pytorch_lightning is enabled
    try:
        # Need to import here to guarantee that the pytorch_lightning logger is
        # set up before we override it.
        import pytorch_lightning  # noqa: F401

        # Change level to WARNING and above, ensure only sent to file, not to
        # stream, ensure not propagated beyond this logger.
        pytorch_logger = logging.getLogger("pytorch_lightning")
        pytorch_logger.setLevel(logging.WARNING)
        pytorch_logger.handlers = []
        pytorch_logger.addHandler(_get_bitfount_log_file_handler())
        pytorch_logger.propagate = False

        # Filter out warnings related to IterableDataset (as not an issue for us
        # as we guarantee only one worker); should only be processed once, not
        # per-batch.
        warnings.filterwarnings(
            action="once",
            message=r"Your `IterableDataset` has `__len__` defined.",
            category=UserWarning,
            module="pytorch_lightning.utilities",
        )

        # Filter out warnings from pytorch_lightning, redirecting them to file only.
        # Other warnings are printed to stderr AND logged to file.
        # Avoid propagating to the root logger.
        warnings_logger = logging.getLogger("py.warnings")
        warnings_logger.propagate = False

        non_lightning_warning_handler = logging.StreamHandler(sys.stderr)
        non_lightning_warning_handler.addFilter(is_not_pytorch_lightning_warning)
        warnings_logger.addHandler(non_lightning_warning_handler)

        all_warnings_handler = _get_bitfount_log_file_handler()
        warnings_logger.addHandler(all_warnings_handler)
    except ImportError:
        pass


def setup_loggers(
    loggers: List[logging.Logger], log_file_dir_name: Optional[str] = None
) -> List[logging.Logger]:
    """Set up loggers with console and file handlers.

    Creates a logfile in 'logs' directory with the current date and time and outputs all
    logs at the "DEBUG" level. Also outputs logs to stdout at the "INFO" level. A common
    scenario is to attach handlers only to the root logger, and to let propagation take
    care of the rest.

    Args:
        loggers: The logger(s) to set up
        log_file_dir_name: Creates a subdirectory inside BITFOUNT_LOGS_DIR
            if provided. Defaults to None.

    Returns:
        A list of updated logger(s).
    """
    handlers: List[logging.Handler] = []

    # If logging to file is enabled, create appropriate FileHandler
    if BITFOUNT_LOG_TO_FILE:
        file_handler = _get_bitfount_log_file_handler(log_file_dir_name)
        handlers.append(file_handler)

    # Set console logging configuration
    console_handler = logging.StreamHandler(sys.stdout)
    console_log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s]: %(message)s", datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_log_formatter)
    console_handler.setLevel(logging.INFO)
    handlers.append(console_handler)

    # Cannot use `logger` as iter-variable as shadows outer name.
    for i_logger in loggers:
        # Clear any existing handler/filter configuration
        i_logger.handlers = []
        i_logger.filters = []

        # Set base level to DEBUG and ensure messages are not duplicated
        i_logger.setLevel(logging.DEBUG)
        i_logger.propagate = False

        # Add handlers to loggers
        for handler in handlers:
            i_logger.addHandler(handler)

    return loggers


# PyTorch-Lightning-related utilities
def is_not_pytorch_lightning_warning(record: logging.LogRecord) -> int:
    """Returns 0 if is a warning generated by PyTorch Lightning, 1 otherwise."""
    msg: str = record.getMessage()

    # warnings generates a log message of form "<file_path>:<line_no> ..." so should
    # be able to only filter on lightning mentions in file path.
    file_path: str = msg.split(":", maxsplit=1)[0]
    if "pytorch_lightning" in file_path:
        return 0  # i.e. should not be logged
    else:
        return 1  # i.e. should be logged
