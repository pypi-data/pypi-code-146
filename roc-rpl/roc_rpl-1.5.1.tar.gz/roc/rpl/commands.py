#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from roc.idb.constants import IDB_SOURCE

from roc.rpl import SCOS_HEADER_BYTES
from roc.rpl.tasks import IdentifyPackets, ParsePackets
from roc.rpl.tasks.packets_to_json import PacketsToJson

try:
    from poppy.core.command import Command
    from poppy.core.logger import logger
except:
    print('POPPy framework is not installed!')

__all__ = ['RPL']


class RPL(Command):
    """
    A command to do the decommutation of a test log file in the XML format.
    """
    __command__ = 'rpl'
    __command_name__ = 'rpl'
    __parent__ = 'master'
    __parent_arguments__ = ['base']
    __help__ = (
        'Commands relative to the decommutation of packets with help ' +
        'of PacketParser library'
    )
    def add_arguments(self, parser):
        """
        Add input arguments common to all the RPL plugin.

        :param parser: high-level pipeline parser
        :return:
        """

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
            help='IDB source to use: SRDB, PALISADE or MIB.',
            default=[IDB_SOURCE],
            nargs=1,
        )

        # Remove SCOS2000 header in the binary packet
        parser.add_argument(
            '--scos-header',
            nargs=1,
            type=int,
            default=[SCOS_HEADER_BYTES],
            help='Length (in bytes) of SCOS2000 header to be removed'
                 ' from the TM packet in the DDS file.'
                 f' (Default value is {SCOS_HEADER_BYTES} bytes.)',
        )

class PacketsToJsonCommand(Command):
    """
    Command to parse and write RPW packets data into a JSON format file.

    input binary data must be passed as hexadecimal strings.
    IDB must be available in the database.
    """
    __command__ = 'rpl_pkt_to_json'
    __command_name__ = 'pkt_to_json'
    __parent__ = 'rpl'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to parse and save RPW packets data into a JSON format file.
    """

    def add_arguments(self, parser):

        # packet binary data
        parser.add_argument(
            '-b', '--binary',
            help="""
             Packet binary data (hexadecimal).
             """,
            type=str,
            nargs='+',
            required=True,
        )

        # Output file path
        parser.add_argument(
            '-j', '--output-json-file',
            help=f'If passed, save packet data in a output JSON file.',
            type=str,
            nargs=1,
            default=[None],
        )

        # Header only
        parser.add_argument(
            '-H', '--header-only',
            action='store_true',
            default=False,
            help='Return packet header information only'
        )

        # Only return valid packets
        parser.add_argument(
            '-V', '--valid-only',
            action='store_true',
            default=False,
            help='Return valid packets only'
        )

        # Only return valid packets
        parser.add_argument(
            '-P', '--print',
            action='store_true',
            default=False,
            help='Return results in stdin'
        )

        # Overwrite existing file
        parser.add_argument(
            '-O', '--overwrite',
            action='store_true',
            default=False,
            help='Overwrite existing JSON file'
        )

    def setup_tasks(self, pipeline):
        """
        Execute the command.
        """

        if pipeline.args.header_only:
            start = IdentifyPackets()
        else:
            start = ParsePackets()

        pipeline | start | PacketsToJson()

        # define the start points of the pipeline
        pipeline.start = start
