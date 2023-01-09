#  Copyright (c) 2020 Russell Smiley
#
#  This file is part of click_logging_config.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.

"""Default values."""

import pathlib

DEFAULT_RELEASE_ID = "0.0.0"

DEFAULT_CONSOLE_JSON_ENABLED = False
DEFAULT_CONSOLE_LOGGING_ENABLED = False

DEFAULT_FILE_JSON_ENABLED = True
DEFAULT_FILE_LOGGING_ENABLED = True
DEFAULT_FILE_ROTATION_BACKUPS = 10
DEFAULT_FILE_ROTATION_SIZE_MB = 1

DEFAULT_LOG_FILE = pathlib.Path("this.log")
DEFAULT_LOG_FORMAT = "%(asctime)s::%(levelname)s::%(name)s::%(message)s"
DEFAULT_LOG_LEVEL = "warning"

VALID_LOG_LEVELS = ["critical", "error", "warning", "info", "debug", "notset"]
