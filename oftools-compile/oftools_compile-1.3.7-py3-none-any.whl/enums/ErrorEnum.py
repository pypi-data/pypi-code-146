#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enumeration module for error messages.
"""

# Generic/Built-in modules
import enum

# Third-party modules

# Owned modules


@enum.unique
class ErrorMessage(enum.Enum):
    """A class used to list all error messages used in this program.
    """

    # Shared
    ABORT = 'Error: Aborting program execution'

    # Context module
    KEY_FILTER = 'KeyError: Filter function must be defined before being used in a section: %s'

    # Job module
    OPTION_NOT_SUPPORTED = 'Warning: Option not supported: Skipping option in the %s section: %s'

    # Main module
    ARGUMENT = 'ArgumentError: %s'
    JOB = 'JobError: Unexpected error detected during the job creation'
    KEYBOARD_ABORT_COMPILATION = 'KeyboardInterrupt: Aborting compilation for current program: %s'
    KEYBOARD_INTERRUPT = 'KeyboardInterrupt: Execution ended by user'
    SYSTEM_NUMBER = 'NumberError: Number of profile and source are not matching: profile: %s, source: %s'

    # Profile module
    OS_ISSUE_WORKDIR = 'OSError: Issue in the %s section with the option: workdir'
    SYSTEM_MISSING_SETUP = 'MissingSectionError: Missing section in the profile: setup'
    SYSTEM_MISSING_OPTION = 'MissingOptionError: Missing option in the %s section: %s'
    VALUE_EMPTY = 'ValueError: Option empty in the %s section: %s'
    WARNING_MANDATORY = 'Warning: Skipping mandatory section: %s'

    # SetupJob module
    MISSING_BACKUP = 'MissingOptionError: "backup" option required to run housekeeping'
    VALUE_BACKUP = 'ValueError: The "backup" option value must be an integer: current = %s, expected (example) = 10'
    VALUE_HOUSEKEEPING = 'ValueError: The "housekeeping" option value must be a number of days: current = %s, expected (example) = 30d'

    # Handlers

    # FileHandler module
    ATTRIBUTE = 'AttributeError: %s'
    DUPLICATE_OPTION = 'DuplicateOptionError: %s'
    DUPLICATE_SECTION = 'DuplicateSectionError: %s'
    EXTENSION_INDEX = 'IndexError: Incorrect extension: File does not have a .%s extension: %s'
    EXTENSION_TYPE = 'TypeError: Expected .%s extension: %s'
    FILE_EXISTS = 'FileExistsError: File or directory already exists: %s'
    FILE_NOT_FOUND = 'FileNotFoundError: No such file or directory: %s'
    INDEX_EXTENSION = 'IndexError: File extension %s not found: %s'
    IS_A_DIRECTORY = 'IsADirectoryError: Is a directory: %s'
    JSON_DECODE = 'JSONDecodeError: %s'
    MISSING_SECTION_HEADER = 'MissingSectionHeaderError: %s'
    NOT_A_DIRECTORY = 'NotADirectoryError: Is not a directory: %s'
    OS_CREATION_TIMES = 'OSError: Failed to get file(s) creation time(s): %s'
    OS_COPY = 'OSError: Failed to copy: %s'
    OS_DELETE = 'OSError: Failed to delete directory: %s'
    OS_DIRECTORY_CREATION = 'OSError: Directory creation failed: %s'
    OS_DUPLICATE = 'OSError: Failed to get duplicates: %s'
    OS_MD5 = 'OSError: Failed to get file md5 checksum: %s'
    OS_READ = 'OSError: Failed to open and read file: %s'
    OS_SIZE = 'OSError: Failed to get file size: %s'
    PERMISSION = 'PermissionError: Permission denied: %s'
    PERMISSION_WRITE = 'PermissionError: Permission denied: No write access on: %s'
    SHUTIL_SAME_FILE = 'shutil.SameFileError: %s and %s are the same file'
    SYSTEM_EMPTY = 'EmptyError: File empty: %s'
    TYPE_EXTENSION = 'TypeError: Unsupported %s file extension: %s'
    VALUE = 'ValueError: %s'
    XML_SAX_PARSE = 'XML_SAXParseException: %s'

    # ShellHandler module
    CALLED_PROCESS = 'CalledProcessError: %s'
    KEY = 'KeyError: Environment variable not found: %s'
    PYODBC = 'pyodbc.Error: Generic I/O error: Connection failed: server does not exist or access denied'
    PYODBC_PROGRAMMING = 'pyodbc.ProgrammingError: Invalid SQL statement: %s'
    SYSTEM_SHELL = 'ShellError: Command does not exist: %s'
    UNICODE = 'UnicodeDecodeError: Using latin-1 instead of utf-8 to decode stdout and stderr'