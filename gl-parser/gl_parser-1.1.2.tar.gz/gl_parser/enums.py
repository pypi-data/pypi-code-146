from enum import Enum


class ExitCode(int, Enum):
    CANNOT_OVERWRITE = 500
    INVALID_CONFIGURATION = 600
    INVALID_PATH = 650
    UNEXPECTED_ERROR = 700


class ErrorCode(int, Enum):
    UNKNOWN = 5
    INVALID_SOURCE_FILE = 100
    INVALID_OUTPUT_FOLDER = 105
