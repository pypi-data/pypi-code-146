#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of click_logging_config.
#
#  You should have received a copy of the MIT License along with click_logging_config.
#  If not, see <https://opensource.org/licenses/MIT>.
#

from click_logging_config._default_values import (
    DEFAULT_CONSOLE_JSON_ENABLED,
    DEFAULT_CONSOLE_LOGGING_ENABLED,
    DEFAULT_FILE_JSON_ENABLED,
    DEFAULT_FILE_LOGGING_ENABLED,
    DEFAULT_FILE_ROTATION_BACKUPS,
    DEFAULT_FILE_ROTATION_SIZE_MB,
    DEFAULT_LOG_FILE,
    DEFAULT_LOG_LEVEL,
)
from click_logging_config._logging import LoggingConfiguration


def test_default():
    under_test = LoggingConfiguration()

    assert under_test.enable_file_logging is DEFAULT_FILE_LOGGING_ENABLED
    assert under_test.enable_console_logging is DEFAULT_CONSOLE_LOGGING_ENABLED
    assert under_test.log_level == DEFAULT_LOG_LEVEL

    assert (
        under_test.console_logging.json_enabled is DEFAULT_CONSOLE_JSON_ENABLED
    )

    assert under_test.file_logging.json_enabled is DEFAULT_FILE_JSON_ENABLED
    assert under_test.file_logging.log_file_path == DEFAULT_LOG_FILE
    assert (
        under_test.file_logging.file_rotation_size_megabytes
        == DEFAULT_FILE_ROTATION_SIZE_MB
    )
    assert (
        under_test.file_logging.max_rotation_backup_files
        == DEFAULT_FILE_ROTATION_BACKUPS
    )
