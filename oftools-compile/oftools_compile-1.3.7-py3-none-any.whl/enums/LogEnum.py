#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enumeration module for log messages.
"""

# Generic/Built-in modules
import enum

# Third-party modules

# Owned modules


@enum.unique
class LogMessage(enum.Enum):
    """A class used to list all log messages used in this program.
    """

    # Shared
    ABORT_SECTION = '[%s] Abort section execution: Step failed: %s'
    CP_COMMAND = '[%s] cp %s %s'
    END_SECTION = '[%s] End section: Output filename: %s'
    RETURN_CODE = 'Return code: %s'
    RUN_COMMAND = '[%s] %s'
    START_SECTION = '[%s] Start section: Input filename: %s'
    VALUE_EMPTY = 'Option empty in the %s section: Skipping option: %s'

    # Context module
    MANDATORY_ADD = 'Adding section to mandatory sections: %s'

    # DeployJob module
    COMPILE_FOUND = '[%s] Evaluate completion status: Compile section found'
    COMPILE_NOT_FOUND = '[%s] Proceed deploy job only: Compile section not found'
    COMPLETE_FOUND = '[%s] Proceed deploy job execution: Complete compile section found'
    COMPLETE_NOT_FOUND = '[%s] Abort deploy job execution: Complete compile section not found'
    END_DATASET = '[%s] End dataset option processing'
    END_DEPLOY_FILE = '[%s] End file option processing'
    END_REGION = '[%s] End region option processing'
    END_TDL = '[%s] End TDL option processing'
    FILE_ALREADY_EXISTS = '[%s] File already exists: No copy required: %s'
    START_DATASET = '[%s] Process dataset option'
    START_DEPLOY_FILE = '[%s] Process file option'
    START_REGION = '[%s] Process region option'
    START_TDL = '[%s] Process TDL option'

    # Grouping module
    AGGREGATE_LOG_FILE = '(GROUPING) Aggregate %s to group.log'

    # Main module
    ABORT_FILE = 'Aborting source file processing: %s'
    PROFILE_PATH = 'Profile path: %s'
    PROFILE_REUSE = 'Profile already used: %s: Reusing corresponding Profile Python object'
    SIGINT = 'Signal SIGINT detected'
    SIGQUIT = 'Signal SIGQUIT detected'
    SOURCE_PATH = 'Source path: %s'
    WORKING_DIRECTORY = 'Current working directory: %s'

    # Profile module
    MANDATORY_SECTIONS = 'Mandatory sections: %s'
    MANDATORY_FILTER = 'Filter function not allowed in mandatory section: %s'
    MANDATORY_NOT_FOUND = 'Mandatory section not found in profile: %s'
    PROFILE_SECTIONS = 'Profile sections: %s'
    SECTION_MANDATORY = '[%s] Execute section: Section is mandatory'
    SECTION_COMPLETE = '[%s] Skip section: Section has already been processed'

    # Report module
    BUILD_STATUS = 'BUILD %s (%fs)'
    CREATE_REPORT_FILE = '(REPORT) Create report file: %s'
    REPORT_GENERATED = '(REPORT) CSV report successfully generated: %s'
    REPORT_SUMMARY = '======== SUMMARY ================================================================='
    TOTAL_PROGRAMS = 'TOTAL      : %d'
    TOTAL_SUCCESS = 'SUCCESS    : %d'
    TOTAL_FAIL = 'FAIL       : %d'
    TOTAL_TIME = 'TOTAL TIME : %fs'

    # SetupJob module
    ADD_TIME_TO_TIME_STAMP = '[%s] Add 1 second to the time stamp: directory already exists: %s'
    CD_COMMAND = '[%s] cd %s'
    END_LOG_FILE = '[%s] End log file initialization'
    END_CLEANING = '[%s] Root working directory now clean: %s'
    END_SETUP_FILE = '[%s] End source file copy'
    END_WORKING_DIRECTORY = '[%s] End working directory creation'
    MKDIR_COMMAND = '[%s] mkdir %s'
    NOT_OLD_ENOUGH = '[%s] No directory found old enough to be deleted: Skipping option: %s'
    START_CLEANING = '[%s] Start cleaning root working directory: %s'
    START_LOG_FILE = '[%s] Initialize log file'
    START_SETUP_FILE = '[%s] Start source file copy'
    START_WORKING_DIRECTORY = '[%s] Start working directory creation'
    VALUE_BELOW_THRESHOLD = '[%s] Number of backups below threshold (%d < %d): Skipping option: %s'

    # Source module
    SOURCE_COUNT = '(SOURCE) Number of source files being compiled: %d'
    SOURCE_SKIP = '(SOURCE) Skip source: skip option enabled'
    SOURCE_TYPE = '(SOURCE) Source type specified: %s'

    # Handlers

    # ShellHandler module
    FILTER_FALSE = '[%s] Filter function %s result: False: Skipping section'
    FILTER_NONE = '[%s] No filter function: Executing section'
    FILTER_TRUE = '[%s] Filter function %s result: True: Executing section'
