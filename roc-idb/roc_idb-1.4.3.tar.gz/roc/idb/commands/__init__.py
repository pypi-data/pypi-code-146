#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from datetime import datetime

from poppy.core.command import Command
from poppy.core.logger import logger

from roc.idb.constants import (
    TIME_ARG_STRFORMAT,
    VALIDITY_MIN,
    VALIDITY_MAX,
    IDB_SOURCE, IDB_INSTALL_DIR,
    TIMEOUT, MIB_GITLAB_TOKEN,
    IDB_SVN_USER, IDB_SVN_PASSWORD
)
from roc.idb.tasks import (
    LoadTask, LoadIdbDump,
    InstallIdbTask,
    SetCurrentTask,
    SetTrangeTask,
)
from roc.idb.tasks.clear_release import ClearIdbReleaseTask

from .export import Export, ExportSequences
from .list import List, ListReleases
from .load import Load, LoadIdb, LoadSequences

__all__ = [
    'Idb',
    'Install',
    'SetCurrent',
    'Load',
    'LoadIdb',
    'LoadIdbDumpCommand',
    'LoadSequences',
    'List',
    'ListReleases',
    'SetTrangeTask',
]

from ..tools.valid import valid_mib_version


class Idb(Command):
    """
    Parent command of the IDB commands.
    """

    __command__ = 'idb'
    __command_name__ = 'idb'
    __parent__ = 'master'
    __parent_arguments__ = ['base']
    __help__ = 'Commands used to manage the IDB'

    def add_arguments(self, parser):
        """
        Add input arguments common to all the IDB plugin.

        :param parser: high-level pipeline parser
        :return:
        """

        parser.add_argument('-t', '--access-token',
                            type=str,
                            default=[MIB_GITLAB_TOKEN],
                            nargs=1,
                            help='Gitlab access token')
        parser.add_argument(
            '-T', '--timeout',
            help='Process timeout in seconds',
            type=int,
            nargs=1,
            default=[TIMEOUT],
        )

        parser.add_argument(
            '--force',
            action='store_true',
            default=False,
            help='Force IDB source files downloading (even if local files are already found)'
        )

class Install(Command):
    """
    Command to load the information of the IDB into the ROC database.
    """

    __command__ = 'idb_install'
    __command_name__ = 'install'
    __parent__ = 'idb'
    __parent_arguments__ = ['base']
    __help__ = 'Install the requested IDB in the given directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--idb-source',
            help="""
            IDB type: SRDB or PALISADE or MIB (default: %(default)s).
            """,
            choices=['MIB', 'SRDB', 'PALISADE'],
            default='MIB',
        )

        parser.add_argument(
            '-i',
            '--install-dir',
            help="""
            Path to the install directory (e.g. 'lib/idb/').
            """,
            type=str,
            default=None,
        )

        parser.add_argument(
            '-v',
            '--idb-version',
            help="""
            IDB version
            """,
            type=str,
            required=True,
        )

        parser.add_argument(
            '-l',
            '--load',
            help='load the IDB information into the ROC database',
            action='store_true',
        )

        parser.add_argument(
            '--validity-min',
            help=f"""
            Validity start time.
            Default value is {VALIDITY_MIN.strftime(TIME_ARG_STRFORMAT)}
            """,
            type=valid_time,
            default=VALIDITY_MIN.strftime(TIME_ARG_STRFORMAT),
        )

        parser.add_argument(
            '--validity-max',
            help=f"""
            Validity end time.
            Default value is {VALIDITY_MAX.strftime(TIME_ARG_STRFORMAT)}
            """,
            type=valid_time,
            default=VALIDITY_MAX.strftime(TIME_ARG_STRFORMAT),
        )

        parser.add_argument(
            '--current',
            action='store_true',
            default=False,
            help='Flag loaded IDB as "current" version to use'
        )

        parser.add_argument(
            '--svn-user',
            help='Username to login RPW IDB SVN repo',
            type=str,
            default=[IDB_SVN_USER],
            nargs=1,
        )

        parser.add_argument(
            '--svn-password',
            help='Password to login RPW IDB SVN repo',
            type=str,
            default=[IDB_SVN_PASSWORD],
            nargs=1,
        )

    def setup_tasks(self, pipeline):
        """
        Load the information from the IDB in the given XML files and set them
        into the ROC database.
        """
        from poppy.core.conf import settings

        # get pipeline args
        args = pipeline.args

        if not args.install_dir:
            # by default, install the idb in the lib folder of the pipeline
            args.install_dir = os.path.join(
                settings.ROOT_DIRECTORY, 'lib', 'idb'
            )

        # instantiate the install task
        install_task = InstallIdbTask()

        if args.load:

            # update args
            if args.idb_source in ['PALISADE', 'SRDB']:
                # PALISADE case
                idb_dir_name = (
                    args.idb_version
                    if args.idb_version.startswith('V')
                    else 'V' + args.idb_version
                )
                idb_path = os.path.join(args.install_dir, idb_dir_name)
                args.idb_path = os.path.join(idb_path, 'IDB')
                args.mapping = os.path.join(
                    args.idb_path,
                    'xml',
                    'IDB_SRDB_Mapping_Table_by_MapGen.xml',
                )

            else:
                # MIB case
                idb_dir_name = args.idb_version
                idb_path = os.path.join(args.install_dir, idb_dir_name)
                args.mapping = os.path.join(
                    idb_path, 'idb_srdb_mapping_table.xml'
                )
                args.idb_path = os.path.join(idb_path, 'data')

            # prepare the tasks
            load_task = LoadTask()
            tasks = install_task | load_task

            if args.validity_min or args.validity_max:
                tasks = tasks | SetTrangeTask()

            if args.current:
                tasks = tasks | SetCurrentTask()

        else:
            tasks = install_task

        pipeline | tasks

        # set the pipeline for this situation

        pipeline.start = install_task


class LoadIdbDumpCommand(Command):
    """
    Command to load IDB SQL dump file into the ROC database.
    Required psql command line tool to work.
    """

    __command__ = 'idb_load_idb_dump'
    __command_name__ = 'load_idb_dump'
    __parent__ = 'idb'
    __parent_arguments__ = ['base']
    __help__ = 'Load IDB SQL dump file into the ROC database using psql tool.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--dump-file',
            help="""
             Path of the IDB SQL dump file.
             Can be a local path or a URL.
             """,
            type=str,
            nargs=1,
            default=[None],
        )
        parser.add_argument(
            '-i',
            '--install-dir',
            help="""
            Path to the install directory.
            """,
            type=str,
            default=[IDB_INSTALL_DIR],
            nargs=1
        )
        parser.add_argument(
                            '-a', '--auth',
                            type=str,
                            default=(None, None),
                            nargs=2,
                            help='Authentication parameters (username, password)'
        )
        parser.add_argument('--pg_restore',
                            action='store_true',
                            default=False,
                            help='Use pg_restore tool instead of psql to load idb dump file.'
                                 '(Required for PostgreSQL custom-format dump.)')
        parser.add_argument('-C', '--clear-temp',
                            action='store_true',
                            default=False,
                            help='Delete temporary files, if any, at the end')
        parser.add_argument('--shell',
                            action='store_true',
                            default=False,
                            help='Use "shell=True/False" option in subprocess.call()')

    def setup_tasks(self, pipeline):
        pass

        load_idb_dump = LoadIdbDump()

        # Define pipeline workflow
        pipeline | load_idb_dump

        # set the pipeline first task
        pipeline.start = load_idb_dump

class ClearRelease(Command):
    """
    Command to clear a given IDB release from the database
    """

    __command__ = 'clear_release'
    __command_name__ = 'clear_release'
    __parent__ = 'idb'
    __parent_arguments__ = ['base']
    __help__ = (
        'Command to clear a given IDB release from the database '
        '(palisade_metadata table entries and IDB source files will not be deleted)'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'idb_version',
            help="""
            IDB version of the release to delete
            """,
            type=str,
        )

        parser.add_argument(
            '-s',
            '--idb-source',
            help="""
            IDB source of the release to delete
            """,
            type=str,
            default=None,
            required=True,
        )

        parser.add_argument(
            '--force',
            help="""
            Force deletion of the release (i.e., no interactive process)
            """,
            action='store_true',
            default=False,
        )

    def setup_tasks(self, pipeline):
        """
        Clear of a given IDB.
        """

        # the task
        clear_idb = ClearIdbReleaseTask()

        # build the pipeline workflow for the command
        pipeline | clear_idb
        pipeline.start = clear_idb


class SetCurrent(Command):
    """
    Command to set a given idb version as current
    """

    __command__ = 'set_current'
    __command_name__ = 'set_current'
    __parent__ = 'idb'
    __parent_arguments__ = ['base']
    __help__ = 'Command to set a given idb version as current'

    def add_arguments(self, parser):
        parser.add_argument(
            'idb_version',
            help="""
            IDB version of the release to set as current
            """,
            type=str,
        )

        parser.add_argument(
            '--idb-source',
            help="""
            IDB source (MIB, SRDB or PALISADE)
            """,
            type=str,
            default=None,
        )

    def setup_tasks(self, pipeline):
        """
        Load the information from the IDB in the given XML files and set them
        into the ROC database.
        """

        # the task
        set_current = SetCurrentTask()

        # set the pipeline for this situation
        pipeline | set_current
        pipeline.start = set_current


class SetTimeRange(Command):
    """
    Command to set the validity time range of a given idb
    """

    __command__ = 'set_trange'
    __command_name__ = 'set_trange'
    __parent__ = 'idb'
    __parent_arguments__ = ['base']
    __help__ = 'Command to set the validity time range of a given idb'

    def add_arguments(self, parser):
        parser.add_argument(
            'idb_version',
            help="""
            IDB version of the release to set
            """,
            type=str,
        )

        parser.add_argument(
            '-s',
            '--idb-source',
            help="""
            IDB source
            """,
            type=str,
            default='MIB',
        )

        parser.add_argument(
            '--validity-min',
            help=f'Validity start time. '
            f'Valid format is "YYYY-MM-DDTHH:MM:SS".',
            type=valid_time,
        )

        parser.add_argument(
            '--validity-max',
            help=f'Validity end time. '
            f'Valid format is "YYYY-MM-DDTHH:MM:SS".',
            type=valid_time,
        )

    def setup_tasks(self, pipeline):
        """
        Set validity time range of a given IDB.
        """

        # the task
        set_trange = SetTrangeTask()

        # set the pipeline for this situation
        pipeline | set_trange
        pipeline.start = set_trange


class GetLatestIdb(Command):
    """
    Command to get the latest release of a given IDB source
    """

    __command__ = 'get_latest'
    __command_name__ = 'get_latest'
    __parent__ = 'idb'
    __parent_arguments__ = ['base']
    __help__ = 'Command to get the latest release of a given IDB source'

    def add_arguments(self, parser):
        parser.add_argument(
            'idb_source',
            help=f"""
            IDB source. Default is {IDB_SOURCE}.
            """,
            type=str,
            default=IDB_SOURCE,
        )

    def setup_tasks(self, pipeline):
        """
        Setup tasks workflow for command.
        """

        idb_source = pipeline.args.idb_source.upper()
        latest_idb = SetCurrentTask.get_latest_idb(idb_source)
        logger.info(
            f'Latest version "{latest_idb.idb_version}" found for IDB "{latest_idb.idb_source}"'
        )
        logger.info(
            f'Valid between "{latest_idb.validity_min}" and "{latest_idb.validity_max}"'
        )
        if idb_source == 'MIB':
            logger.info(f'MIB Version is "{latest_idb.mib_version}"')

        # TODO - Add a way to avoid ERROR message
        #       "The pipeline is not linked to an entry point task, and cannot be run."


def valid_time(t, format=TIME_ARG_STRFORMAT):
    """
    Validate input datetime string format.

    :param t: input datetime string
    :param format: expected datetime string format
    :return: datetime object with input datetime info
    """
    if t:
        try:
            return datetime.strptime(t, format)
        except ValueError:
            msg = f"Not a valid date: '{t}'!"
            logger.error(msg)
            raise argparse.ArgumentTypeError
