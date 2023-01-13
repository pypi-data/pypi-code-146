import logging
from pathlib import Path

from . import vars


def create_logfile(log_file_list: list[str], path: str):
    """Create a log files in the given directory"""
    for log_file in log_file_list:
        try:
            file = open(path + "/" + log_file, "r")
            file.close()
        except IOError:
            file = open(path + "/" + log_file, "w")
            file.close()


def validate_logger_level(level):
    if level not in list(logging._nameToLevel.keys()):
        raise ValueError("Invalid logger level: {}".format(level))
    return getattr(logging, level)


# check .env value
LEVEL = validate_logger_level(vars.LOGGER_LEVEL)

logging.basicConfig(level=LEVEL)
# Then we can define the child logger instance
logger: logging.Logger = logging.getLogger("broker-logger")
# Paths
current_directory = Path(__file__).resolve().parent
log_folder = current_directory.joinpath("logfiles")

# check if the directory exists, and create it if it doesn't
if not log_folder.exists():
    Path(log_folder).mkdir()
    create_logfile(
        path=str(log_folder),
        log_file_list=["critical.log", "error.log", "info.log", "debug.log"],
    )

critical_log_file_path = log_folder.joinpath("critical.log")
error_log_file_path = log_folder.joinpath("error.log")
info_log_file_path = log_folder.joinpath("info.log")
debug_log_file_path = log_folder.joinpath("debug.log")


# Handlers
format_handler = logging.Formatter("[%(asctime)s] [%(levelname)s] -> %(message)s")

critical_log_handler = logging.FileHandler(critical_log_file_path)
critical_log_handler.setLevel(logging.CRITICAL)
critical_log_handler.setFormatter(format_handler)

info_log_handler = logging.FileHandler(info_log_file_path)
info_log_handler.setLevel(logging.INFO)
info_log_handler.setFormatter(format_handler)

debug_log_handler = logging.FileHandler(debug_log_file_path)
debug_log_handler.setLevel(logging.DEBUG)
debug_log_handler.setFormatter(format_handler)


warning_log_handler = logging.FileHandler(error_log_file_path)
warning_log_handler.setLevel(logging.WARNING)
warning_log_handler.setFormatter(format_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(format_handler)

# Adding the handlers
logger.addHandler(stream_handler)
logger.addHandler(critical_log_handler)
logger.addHandler(warning_log_handler)
logger.addHandler(debug_log_handler)
logger.addHandler(info_log_handler)
