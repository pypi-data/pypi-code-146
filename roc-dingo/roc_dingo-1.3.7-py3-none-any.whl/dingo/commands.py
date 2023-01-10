#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from poppy.core.tools.poppy_argparse import argparse
from poppy.core.command import Command

from roc.dingo.constants import PIPELINE_TABLES, TRYOUTS, \
    TIME_WAIT_SEC, DATA_VERSION, \
    ROC_DATA_ROOT, FILE_LEVEL_LIST, ROC_SPICE_KERNEL_ROOT, SQL_LIMIT, \
    IDB_SOURCE, WORKERS, SOAR_TAP_URL, \
    ROC_DELIVERED_ROOT, ROC_PUBLIC_DATA_ROOT
from roc.dingo.tasks.clear import ClearRocDb
from roc.dingo.tasks.efecs_to_db import EfecsToDb
from roc.dingo.tasks.event_to_db import EventToDb

from roc.dingo.tasks import \
    LogFileToDb, ParseFileTree, CheckFileInDb, UpdateParentsInDb, \
    StoreDelivered, StorePublicFilename, CheckSOARDataAvailability, \
    SearchForUpdate
from roc.dingo.tasks.l0_to_hfrtimelog import L0ToHfrTimeLog
from roc.dingo.tasks.solohk_to_db import SoloHkToDb
from roc.dingo.tasks.db_to_solohk import DbToSoloHk
from roc.dingo.tasks.update_utc_time import UpdateUtcTime
from roc.dingo.tools import valid_data_version, valid_time, valid_date

from roc.dingo.tasks import \
    ExportToJson, L0ToDb, MoveFailedFiles, MoveProcessedFiles

__all__ = []


class DingoCommands(Command):
    """
    Manage the commands relative to the DINGO module.
    """
    __command__ = 'dingo'
    __command_name__ = 'dingo'
    __parent__ = 'master'
    __help__ = """
        Commands relative to the DINGO module, responsible for getting,
        parsing and store de-commuted packets into the ROC database.
    """

    def add_arguments(self, parser):
        """
        Add input arguments common to all the Dingo plugin.

        :param parser: high-level pipeline parser
        :return:
        """

        # If passed as an argument, then generate a temporary file
        # in the output folder
        # To indicate that output file production is in progress
        # lock file is automatically deleted at the end.
        parser.add_argument(
            '--lock-file',
            help='Name of the lock temporary file.',
            default=None,
        )

        # specify the IDB version to use
        parser.add_argument(
            '--idb-version',
            help='IDB version to use.',
            default=[None],
            nargs=1,
        )

        # specify the IDB source to use
        parser.add_argument(
            '--idb-source',
            help='IDB source to use (MIB, SRDB or PALISADE).',
            default=[IDB_SOURCE],
            nargs=1,
        )

        # specify the SOLO SCLK SPICE kernel
        # (required to compute UTC time from OBT time)
        parser.add_argument(
            '--sclk',
            help='Path of SOLO SPICE SCLK kernel file '
                 '(required to compute UTC time from OBT time).',
            default=[None],
            nargs=1,
        )

        # specify the SOLO SPICE LSK kernel
        # (required to compute UTC time from OBT time)
        parser.add_argument(
            '--lsk',
            help='Path of SOLO SPICE LSK kernel '
                 '(required to compute UTC time from OBT time).',
            default=[None],
            nargs=1,
        )

        # Specify the value of the Data_version attribute (and filename)
        parser.add_argument(
            '-v',
            '--data-version',
            nargs=1,
            help='Define the data version value for output files. ',
            type=valid_data_version,
            default=[DATA_VERSION],
        )

        parser.add_argument(
            '-t',
            '--tryouts',
            nargs=1,
            help='Max. number of database query tryouts. ',
            type=int,
            default=[TRYOUTS],
        )

        parser.add_argument(
            '-w',
            '--wait',
            nargs=1,
            help='Time in seconds to wait between two tryouts. ',
            type=int,
            default=[TIME_WAIT_SEC],
        )

        parser.add_argument(
            '-P',
            '--processed-files-dir',
            nargs=1,
            type=str,
            help='Directory where well processed files must be moved'
        )

        parser.add_argument(
            '-F',
            '--failed-files-dir',
            nargs=1,
            type=str,
            help='Directory where failed files must be moved'
        )

        parser.add_argument(
            '--no-move',
            action='store_true',
            default=False,
            help='If passed, skip processed/failed file moving')

        parser.add_argument(
            '-s',
            '--start-time',
            nargs=1, type=str,
            help='Filter database query/insert by start time. ',
            default=[None])

        parser.add_argument(
            '-e',
            '--end-time',
            nargs=1, type=str,
            help='Filter database query/insert by end time. ',
            default=[None])

        parser.add_argument(
            '-l',
            '--limit',
            nargs=1,
            help='Limit of returned rows when querying database. ',
            type=int,
            default=[SQL_LIMIT],
        )

        parser.add_argument(
            '-d',
            '--date-list',
            nargs='+',
            type=valid_date,
            default=[],
            help='List of dates to process (format is YYYYMMDD)')

        parser.add_argument(
            '--to-queue',
            action='store_true',
            default=False,
            help='If passed, add new datasets in the data queue')

        parser.add_argument(
            '--from-queue',
            action='store_true',
            default=False,
            help='If passed, process datasets found in the data queue')

        parser.add_argument(
            '--clean-queue',
            action='store_true',
            default=False,
            help='If passed, clean data queue from already processed datasets')

        parser.add_argument(
            '-W',
            '--workers',
            type=int,
            nargs=1,
            default=[WORKERS],
            help='Number of workers to run in parallel '
                 '(only for multiprocessing tasks)')


class L0ToDbCommand(Command):
    """
    Command to import some packet data from RPW L0 files into the
    ROC database.
    """
    __command__ = 'dingo_l0_to_db'
    __command_name__ = 'l0_to_db'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to import some packet data from RPW L0 files
        into the ROC database.
    """

    def add_arguments(self, parser):
        # path to input RPW L0 file(s)
        parser.add_argument(
            '-l0', '--rpw-l0-files',
            help="""
             Input RPW L0 file(s) to import into the ROC database.
             """,
            nargs='+',
            type=str,
            required=True,
        )
        parser.add_argument(
            '-i', '--include',
            nargs='+',
            type=str,
            default=[],
            help='List of packets to include (by palisade_id)',
        )
        parser.add_argument(
            '-x', '--exclude',
            nargs='+',
            type=str,
            default=[],
            help='List of packets to ignore (by palisade_id)',
        )
        parser.add_argument(
            '-T', '--exclude-tm-apid',
            nargs='+',
            type=int,
            default=[],
            help='List of TM packets to exclude (by apid)',
        )
        parser.add_argument(
            '-C', '--exclude-tc-apid',
            nargs='+',
            type=int,
            default=[],
            help='List of TC packets to exclude (by apid)',
        )
        parser.add_argument(
            '--param-only',
            action='store_true',
            default=False,
            help='Insert packet parameters only. '
                 '(i.e., no insertion in tm_log/tc_log tables)'
        )

    def setup_tasks(self, pipeline):
        """
        Run workflow of tasks .
        """

        # Set start task
        start = L0ToDb()
        end = L0ToDb()

        #  Build workflow of tasks
        pipeline | start

        # define the start/end task of the pipeline
        pipeline.start = start
        pipeline.end = end

class L0ToHfrTimeLogCommand(Command):
    """
    Command to import RPW L0 files into the
    pipeline.hfr_time_log table in ROC database.
    """
    __command__ = 'dingo_l0_to_hfrtimelog'
    __command_name__ = 'l0_to_hfrtimelog'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
         Command to import RPW L0 files into the
         pipeline.hfr_time_log table in ROC database.
    """

    def add_arguments(self, parser):
        # path to input RPW L0 file(s)
        parser.add_argument(
            '-l0', '--rpw-l0-files',
            help="""
             Input RPW L0 file(s) to process.
             """,
            nargs='+',
            type=str,
            required=True,
        )

    def setup_tasks(self, pipeline):
        """
        Run workflow of tasks .
        """

        # Set start task
        start = L0ToHfrTimeLog()
        end = L0ToHfrTimeLog()

        #  Build workflow of tasks
        pipeline | start

        # define the start/end task of the pipeline
        pipeline.start = start
        pipeline.end = end


class EventToDbCommand(Command):
    """
    Command to import some SOLO/RPW-related event data into the ROC database.
    These events are used to fill the QUALITY_BITMASK zVariable in RPW L1 CDF
    """
    __command__ = 'dingo_event_to_db'
    __command_name__ = 'event_to_db'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to import some SOLO/RPW-related event data
        into the ROC database.
    """

    def add_arguments(self, parser):
        pass

    def setup_tasks(self, pipeline):
        """
        Run workflow of tasks .
        """

        # Set start task
        start = EventToDb()

        #  Build workflow of tasks
        pipeline | start

        # define the start/end task of the pipeline
        pipeline.start = start


class DbToJsonCommand(Command):
    """
    Command to export ROC pipeline database content in a JSON format file.
    """
    __command__ = 'dingo_db_to_json'
    __command_name__ = 'db_to_json'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to export the content of the ROC pipeline database
        in a JSON file.
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '-o', '--output-json',
            help="""
                 Name of the output JSON format file.
                 """,
            type=str,
            default=None,
        )

        parser.add_argument(
            '-t', '--tables',
            help=f"""
                 Name of table(s) to export.
                 Possible values: {','.join(list(PIPELINE_TABLES.keys()))}
                 """,
            nargs='+',
            default=list(PIPELINE_TABLES.keys()),
        )

        parser.add_argument(
            '-t', '--tables',
            help=f"""
                 Name of table(s) to export.
                 Possible values: {','.join(list(PIPELINE_TABLES.keys()))}
                 """,
            nargs='+',
            default=list(PIPELINE_TABLES.keys()),
        )

        parser.add_argument(
            '-C', '--creation-time',
            action='store_true',
            help='Filter time by creation time instead of insertion time '
                 '(only for packet_log and file_log tables'
        )

    def setup_tasks(self, pipeline):
        """
        Export table entries in the ROC pipeline database into JSON file.
        """
        # the task
        start = ExportToJson()

        # build the pipeline workflow for the command
        pipeline | start
        pipeline.start = start


class ClearRocDbCommand(Command):
    """
    Command to clear the content of the ROC pipeline database.
    (Delete pipeline.packet_log and pipeline.file_log tables only)
    """
    __command__ = 'dingo_clear_rocdb'
    __command_name__ = 'clear_rocdb'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to clear content of the pipeline
        in the ROC database.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '-t', '--tables',
            help=f"""
                 Name of table(s) to delete.
                 Possible values: {','.join(list(PIPELINE_TABLES.keys()))}
                 """,
            nargs='+',
            default=list(PIPELINE_TABLES.keys()),
        )

        parser.add_argument(
            '--force',
            help="""
                Force deletion (i.e., no confirmation step)
                """,
            action='store_true',
            default=False,
        )

    def setup_tasks(self, pipeline):
        """
        Clear of table entries in the ROC pipeline database.
        """

        # the task
        clear_rocdb = ClearRocDb()

        # build the pipeline workflow for the command
        pipeline | clear_rocdb
        pipeline.start = clear_rocdb


class LogFileToDbCommand(Command):
    """
    Command to log files from the ROC filetree into the ROC pipeline database
    """
    __command__ = 'dingo_logfile_to_rocdb'
    __command_name__ = 'logfile_to_rocdb'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to log files from the ROC filetree
        into the ROC pipeline database.
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '-r', '--root',
            help="""
                 relative path to the ROC filetree root
                 """,
            default=ROC_DATA_ROOT,
            type=valid_data_path_type,
        )

        # for this command, SK is not authorized
        levels = list(FILE_LEVEL_LIST)
        levels.remove('SK')

        parser.add_argument(
            '-l', '--level',
            help=f"""
                 comma-separated list of levels to include in the parsing
                 e.g L1,L2 or HK,L0,BIA
                 Default values: {','.join(list(levels))}
                 """,
            nargs='+',
            choices=list(levels),
            default=list(levels),
        )

        parser.add_argument(
            '-d', '--date',
            help="""
                 date to include in the parsing (yyyy or yyyy/mm or yyyy/mm/dd)
                 e.g 2020 or 2020/07 or 2020/07/02
                 """,
            default=None,
        )

        parser.add_argument(
            '-f', '--force',
            help="""
                 Force the update of the database
                 """,
            action='store_true',
            default=False,
        )

        parser.add_argument(
            '-nf', '--no-former-versions',
            help="""
                 Exclude files from the directories "former_versions"
                 """,
            action='store_true',
            default=False,
        )

    def setup_tasks(self, pipeline):
        """
        Synchronise the ROC file tree content into the ROC database
        """

        # the tasks
        parse_file_tree = ParseFileTree()
        log_file_to_db = LogFileToDb()
        check_file_in_db = CheckFileInDb()

        # build the pipeline workflow for the command
        pipeline | parse_file_tree | check_file_in_db | log_file_to_db

        # define the start points of the pipeline
        pipeline.start = parse_file_tree
        pipeline.end = log_file_to_db


class UpdateLogFileCommand(Command):
    """
    Search for files to be updated in file file_log table
    Their column to_update is set to True
    Update these files (set to_update=False)
    """
    __command__ = 'dingo_update_filelog'
    __command_name__ = 'update_filelog'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Search for files to be updated in file file_log table
        and update them
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '-r', '--root',
            help="""
                 relative path to the ROC filetree root
                 """,
            default=ROC_DATA_ROOT,
            type=valid_data_path_type,
        )

    def setup_tasks(self, pipeline):
        """
        Update the requested files (to_update = True in db)
        """

        # the tasks
        search_for_update = SearchForUpdate()
        log_file_to_db = LogFileToDb()

        # build the pipeline workflow for the command
        pipeline | search_for_update | log_file_to_db

        # define the start points of the pipeline
        pipeline.start = search_for_update
        pipeline.end = log_file_to_db


class LogSpiceKernelsToDbCommand(Command):
    """
    Command to log files from the ROC filetree into the ROC pipeline database
    """
    __command__ = 'dingo_logsk_to_rocdb'
    __command_name__ = 'logsk_to_rocdb'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to log spice kernel files from the ROC filetree
        into the ROC pipeline database.
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '-r', '--root',
            help="""
                 relative path to the ROC filetree root
                 """,
            type=valid_data_path_type,
            default=ROC_SPICE_KERNEL_ROOT
        )

        parser.add_argument(
            '-l', '--level',
            help="""
                 level to include in the parsing
                 Only one value possible : SK
                 """,
            nargs='+',
            choices=['SK'],
            default=['SK'],
        )

        parser.add_argument(
            '-f', '--force',
            help="""
                 Force the update of the database
                 """,
            action='store_true',
            default=False,
        )

        parser.add_argument(
            '-nf', '--no-former-versions',
            help="""
                 Exclude files from the directories "former_versions"
                 """,
            action='store_true',
            default=False,
        )

    def setup_tasks(self, pipeline):
        """
        Synchronise the ROC file tree content into the ROC database
        """

        # the tasks
        parse_file_tree = ParseFileTree()
        log_file_to_db = LogFileToDb()
        check_file_in_db = CheckFileInDb()

        # build the pipeline workflow for the command
        pipeline | parse_file_tree | check_file_in_db | log_file_to_db

        # define the start points of the pipeline
        pipeline.start = parse_file_tree
        pipeline.end = log_file_to_db


class UpdateMissingParentsDbCommand(Command):
    """
    Command to log files from the ROC filetree into the ROC pipeline database
    """
    __command__ = 'dingo_update_missing_parents_in_db'
    __command_name__ = 'update_missing_parents_in_db'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to update files into the ROC pipeline database.
        Only handles files with the error_log Missing Parents.
    """

    def add_arguments(self, parser):
        pass

    def setup_tasks(self, pipeline):
        """
        Synchronise the ROC file tree content into the ROC database
        """

        # the tasks
        update_parents_in_db = UpdateParentsInDb()

        # build the pipeline workflow for the command
        pipeline | update_parents_in_db

        # define the start points of the pipeline
        pipeline.start = update_parents_in_db
        pipeline.end = update_parents_in_db


class StoreDeliveredCommand(Command):
    """
    Command to store into file_log files that have been delivered by GFTS
    """
    __command__ = 'dingo_store_delivered'
    __command_name__ = 'store_delivered'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to store into file_log files that have been delivered by GFTS.
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '--delivered',
            help="""
                 relative path to the ROC delivered directory
                 """,
            type=valid_data_path_type,
            default=ROC_DELIVERED_ROOT
        )

        parser.add_argument(
            '--public',
            help="""
                 relative path to the ROC delivered directory
                 """,
            type=valid_data_path_type,
            default=ROC_PUBLIC_DATA_ROOT
        )

        parser.add_argument(
            '--remove_files',
            help="""
                 If set shadow delivered files will be removed
                 """,
            action='store_true',
            default=False,
        )

    def setup_tasks(self, pipeline):
        """
        Synchronise the ROC file tree content into the ROC database
        """

        # the tasks
        store_public = StorePublicFilename()
        store_delivered = StoreDelivered()

        # build the pipeline workflow for the command
        pipeline | store_public | store_delivered

        # define the start points of the pipeline
        pipeline.start = store_public
        pipeline.end = store_delivered


class CheckSOARDataAvailabilityCommand(Command):
    """
    Query and report RPW data availability in Solar Orbiter Archive (SOAR)
    at ESAC.
    https://gitlab.obspm.fr/ROC/Pipelines/RODP/-/blob/develop/scripts/report_rpw_soar_data_availability.py  # noqa: E501
    """
    __command__ = 'dingo_check_soar'
    __command_name__ = 'check_soar'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Check if delivered files are available in SOAR.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            default=SOAR_TAP_URL,
            help='URL of the SOAR TAP service. '
            f'{SOAR_TAP_URL}'
        )

    def setup_tasks(self, pipeline):
        """
        Check if delivered files are available in SOAR
        """

        # the tasks
        check_soar = CheckSOARDataAvailability()

        # build the pipeline workflow for the command
        pipeline | check_soar

        # define the start points of the pipeline
        pipeline.start = check_soar
        pipeline.end = check_soar


def valid_data_path_type(arg):
    """ Type function for argparse - an accessible path not empty """

    # check is accessible
    ret = os.access(arg, os.R_OK)
    if not ret:
        raise argparse.ArgumentTypeError(
            'Argument must be a valid and readable data path')

    # check if not empty
    listdir = os.listdir(arg)
    if len(listdir) == 0:
        raise argparse.ArgumentTypeError(
            'Argument data path must contain data. Directory is empty.')

    return arg


class SoloHkToDbCommand(Command):
    """
    Command to import Solo HK EDDS data into the ROC database.
    """
    __command__ = 'dingo_solohk_to_db'
    __command_name__ = 'solohk_to_db'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to import Solo HK EDDS data into the ROC database.
    """

    def add_arguments(self, parser):
        # path to input RPW L0 file(s)
        parser.add_argument(
            '-f', '--solo-hk-files',
            help="""
             Input SOLO HK EDDS XML file(s) to import into the ROC database.
             """,
            nargs='+',
            type=str,
            required=True,
        )

    def setup_tasks(self, pipeline):
        """
        Insert SOLO HK EDDS Data into the ROC database
        """

        # Task
        start_task = SoloHkToDb()
        end_task = MoveFailedFiles()

        # build the pipeline workflow for the command
        pipeline | start_task | MoveProcessedFiles() | end_task

        # define the start points of the pipeline
        pipeline.start = start_task
        pipeline.end = end_task


class DbToSoloHkCmd(Command):
    """
    Command to export Solo HK EDDS data saved in the ROC database
    into a output XML file.
    Format of the output XML file is close to the Parameter EDDS response XML.
    """
    __command__ = 'dingo_db_to_solohk'
    __command_name__ = 'db_to_solohk'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to export Solo HK EDDS data saved in the ROC database
        into a output XML file.
    """

    def add_arguments(self, parser):
        pass

    def setup_tasks(self, pipeline):
        """
        Export SOLO HK EDDS Data into an output XML file
        """

        # Task
        start_task = DbToSoloHk()
        end_task = MoveFailedFiles()

        # build the pipeline workflow for the command
        pipeline | start_task | end_task

        # define the start points of the pipeline
        pipeline.start = start_task
        pipeline.end = end_task


class EfecsToDbCommand(Command):
    """
    Command to import EFECS data into the ROC database.
    """
    __command__ = 'dingo_efecs_to_db'
    __command_name__ = 'efecs_to_db'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to import Solo EFECS data into the ROC database.
    """

    def add_arguments(self, parser):
        # path to input RPW L0 file(s)
        parser.add_argument(
            '-f', '--efecs-files',
            help="""
             Input SOLO EFECS XML file(s) to import into the ROC database.
             """,
            nargs='+',
            type=str,
            required=True,
        )

    def setup_tasks(self, pipeline):
        """
        Insert SOLO HK EFECS Data into the ROC database
        """

        # Task
        start_task = EfecsToDb()

        # build the pipeline workflow for the command
        pipeline | start_task

        # define the start points of the pipeline
        pipeline.start = start_task


class UpdateUtcTimeCommand(Command):
    """
    Command to update utc_time values in the ROC database.
    """
    __command__ = 'dingo_update_utc_time'
    __command_name__ = 'update_utc_time'
    __parent__ = 'dingo'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to update utc_time values in the ROC database.
    """

    def add_arguments(self, parser):
        pass

    def setup_tasks(self, pipeline):
        """
        Update utc_time values in the ROC database
        """

        # Task
        start_task = UpdateUtcTime()

        # build the pipeline workflow for the command
        pipeline | start_task

        # define the start points of the pipeline
        pipeline.start = start_task
