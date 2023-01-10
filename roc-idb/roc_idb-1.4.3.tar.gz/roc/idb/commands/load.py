#!/usr/bin/env python
# -*- coding: utf-8 -*-

from poppy.core.command import Command
from roc.idb.tasks import (
    LoadTask,
    LoadSequencesTask,
    LoadPalisadeMetadataTask,
    ParseSequencesTask,
)

__all__ = ['Load', 'LoadIdb', 'LoadSequences']


class Load(Command):
    """
    Command to set a given idb version as current
    """

    __command__ = 'idb_load'
    __command_name__ = 'load'
    __parent__ = 'idb'
    __parent_arguments__ = ['base']
    __help__ = 'Load the IDB from files'


class LoadIdb(Command):
    """
    Command to load the information of the IDB into the ROC database.
    """

    __command__ = 'idb_load_idb'
    __command_name__ = 'idb'
    __parent__ = 'idb_load'
    __parent_arguments__ = ['base']
    __help__ = (
        'Load the IDB packets, parameters and transfer functions from files'
    )

    def add_arguments(self, parser):
        # path to XML file of the IDB
        parser.add_argument(
            '-i',
            '--idb-path',
            help="""
            Path to the IDB directory (e.g. 'V4.3.3/IDB/').
            """,
            type=str,
            required=True,
        )

        # idb source
        parser.add_argument(
            '-t',
            '--idb-source',
            help="""
            IDB type: SRDB or PALISADE or MIB (default: %(default)s).
            """,
            type=str,
            default='MIB',
            required=True,
        )
        # path to the mapping of parameters and packets to the SRDB
        parser.add_argument(
            '-m',
            '--mapping',
            help="""
            Path to the XML file containing the mapping of parameters and
            packets to the SRDB.
            """,
            type=str,
            required=True,
        )

    def setup_tasks(self, pipeline):
        """
        Load the information from the IDB in the given XML files and set them
        into the ROC database.
        """

        load_task = LoadTask()

        # set the pipeline for this situation
        pipeline | load_task
        pipeline.start = load_task


class LoadPalisadeMetadata(Command):
    """
    Command to load the PALISADE metadata into the ROC database.
    """

    __command__ = 'idb_load_palisade_metadata'
    __command_name__ = 'palisade_metadata'
    __parent__ = 'idb_load'
    __parent_arguments__ = ['base']
    __help__ = 'Load the PALISADE metadata from XML files'

    def add_arguments(self, parser):
        # path to XML file of the IDB
        parser.add_argument(
            'idb_path',
            help="""
            Path to the PALISADE IDB directory (e.g. 'V4.3.3/IDB/').
            """,
            type=str,
        )

    def setup_tasks(self, pipeline):
        """
        Load the information from the IDB in the given XML files and set them
        into the ROC database.
        """

        load_metadata_task = LoadPalisadeMetadataTask()

        # set the pipeline for this situation
        pipeline | load_metadata_task
        pipeline.start = load_metadata_task


class LoadSequences(Command):
    """
    Command to load MIB sequences into the ROC database.
    """

    __command__ = 'idb_load_sequences'
    __command_name__ = 'sequences'
    __parent__ = 'idb_load'
    __parent_arguments__ = ['base']
    __help__ = 'Command to load MIB sequences into the MUSIC database'

    def add_arguments(self, parser):
        # path to MIB files directory
        parser.add_argument(
            'mib_dir_path',
            help="""
            Path to MIB files directory.
            """,
            type=str,
        )

    def setup_tasks(self, pipeline):
        """
        Load MIB sequences into the MUSIC database
        """
        # instantiate the task
        parse_sequences = ParseSequencesTask()
        load_sequences = LoadSequencesTask()

        # set the pipeline topology
        pipeline | (parse_sequences | load_sequences)
        pipeline.start = parse_sequences
