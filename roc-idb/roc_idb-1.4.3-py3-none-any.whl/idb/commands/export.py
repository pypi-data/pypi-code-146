# -*- coding: utf-8 -*-
from poppy.core.command import Command
from roc.idb.tasks import ParseSequencesTask, ExportSequencesTask

__all__ = ['Export', 'ExportSequences']


class Export(Command):
    """
    Command to set a given idb version as current
    """

    __command__ = 'idb_export'
    __command_name__ = 'export'
    __parent__ = 'idb'
    __parent_arguments__ = ['base']
    __help__ = 'Export the IDB in the requested format'


class ExportSequences(Command):
    """
    Command to set a given idb version as current
    """

    __command__ = 'idb_export_sequences'
    __command_name__ = 'sequences'
    __parent__ = 'idb_export'
    __parent_arguments__ = ['base']
    __help__ = (
        'Command to export CSV/XLS sequences using MIB files or the database'
    )

    def add_arguments(self, parser):
        # path to MIB files directory
        parser.add_argument(
            '-mib',
            '--mib-dir-path',
            help="""
            Path to MIB files directory.
            """,
            type=str,
            required=True,
        )

        # path to sequences output path
        parser.add_argument(
            '-seq',
            '--seq-dir-path',
            help="""
            Path where sequences will be written.
            """,
            type=str,
        )

    def setup_tasks(self, pipeline):
        """
        Export MIB sequences as XLS/CSV
        """
        # instantiate the task
        parse_sequences = ParseSequencesTask()
        export_sequences = ExportSequencesTask()

        # set the pipeline topology
        pipeline | (parse_sequences | export_sequences)
        pipeline.start = parse_sequences
