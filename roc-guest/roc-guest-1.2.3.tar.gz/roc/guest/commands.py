#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GUEST plugin commands
"""

import os
import os.path as osp
import argparse


from poppy.core.command import Command

from roc.guest.tools import valid_time, valid_single_file
from roc.guest.constants import SCOS_HEADER_BYTES
from roc.guest.tasks import \
    xml_to_test, txt_to_test, \
    test_to_xml, test_to_txt, \
    mebdb_to_test, test_to_mebdb, \
    raw_to_tmraw, raw_to_tcreport
from roc.guest.tasks import L0ToTest, TestToL0
from roc.guest.tasks.rocdb import clear_test

__all__ = []


class GuestCommands(Command):
    """
    Manage the commands relative to the roc.guest module.
    """
    __command__ = 'guest'
    __command_name__ = 'guest'
    __parent__ = 'master'
    __parent_arguments__ = ['base']
    __help__ = """
        Commands relative to the roc.guest module.
    """

    def add_arguments(self, parser):
        # Option to filter test log data by testname pattern
        parser.add_argument(
            '-p', '--pattern',
            nargs=1,
            help="""
            Testname filter pattern.
            """,
            type=str,
        )

        # Option to set a lower time interval limit
        parser.add_argument(
            '--start-time',
            help="""
            Minimum of the date/time interval to export [YYYY-mm-ddTHH:MM:SS].
            """,
            default=None,
            type=valid_time,
        )

        # Option to set a upper time interval limit
        parser.add_argument(
            '--end-time',
            help="""
            Maximum of the date/time interval to export [YYYY-mm-ddTHH:MM:SS].
            """,
            default=None,
            type=valid_time,
        )

        # Optional argument to only process "Terminated" Test
        parser.add_argument(
            '-T', '--terminated',
            help="""
            Only process terminated tests
            """,
            action='store_true',
        )

        # specify the IDB version to use
        parser.add_argument(
            '--idb-version',
            help='IDB version to use.',
            nargs=1,
            default=None,
        )

        # specify the IDB source to use
        parser.add_argument(
            '--idb-source',
            help='IDB source to use (MIB, SRDB or PALISADE).',
            nargs=1,
            default=None,
        )

        # Provide output test name
        parser.add_argument(
            '--out-test-name',
            type=str,
            help='Output test name.',
        )

        # Provide output test description
        parser.add_argument(
            '--out-test-descr',
            type=str,
            help='Output test description.',
        )

        # Remove SCOS2000 header in the binary packet
        parser.add_argument(
            '--scos-header', nargs=1,
            type=int, default=[None],
            help='Remove the '
                 'SCOS2000 header in the packet(s).'
                 ' (Value for MOC DDS should be {0} bytes.)'.format(SCOS_HEADER_BYTES)
        )

        # no-spice keyword to force not use of SPICE kernels
        parser.add_argument(
            '--no-spice', action='store_true',
            default=False,
            help='If False, then use SPICE kernels to compute time (SPICE_KERNEL_PATH env. variable must be defined)'
        )


class MebDbToXmlCommand(Command):
    """
     Command to extract test log data from a MEB GSE database and convert it into XML files (one file per test).
     """
    __command__ = 'guest_mebdb_to_xml'
    __command_name__ = 'mebdb_to_xml'
    __parent__ = 'guest'
    __parent_arguments__ = ['base']
    __help__ = """
         Command to export test log data from a MEB GSE database (one XML file per test).
     """

    def setup_tasks(self, pipeline):
        # starting point of the pipeline
        start = mebdb_to_test()

        # task starting the loop
        end = test_to_xml()

        # create the tasks workflow
        pipeline | start | end

        # define the start points of the pipeline
        pipeline.start = start
        pipeline.end = end

        # create a loop
        pipeline.loop(start, end, start.generator)


class XmlToMebDbCommand(Command):
    __command__ = 'guest_xml_to_mebdb'
    __command_name__ = 'xml_to_mebdb'
    __parent__ = 'guest'
    __parent_arguments__ = ['base']
    __help__ = 'Command to import a given test log XML into a MEB GSE database.'

    def add_arguments(self, parser):
        parser.add_argument(
            'test_log_xml',
            nargs=1,
            type=str,
            default=None,
            help='Input test log XML file to import'
        )

    def setup_tasks(self, pipeline):
        # Parse input file, then import data inside MEB GSE database
        start = xml_to_test()
        end = test_to_mebdb()

        # set the pipeline workflow
        pipeline | start | end

        # define the start points of the pipeline
        pipeline.start = start



class TxtToXmlCommand(Command):
    """
    Manage command to convert an input ADS GSE text format file
    into a MEB GSE XML test log file.
    """
    __command__ = 'guest_txt_to_xml'
    __command_name__ = 'txt_to_xml'
    __parent__ = 'guest'
    __parent_arguments__ = ['base']
    __help__ = """
        Manage command to convert an input ADS GSE text format file
    into a MEB GSE XML test log file.
    """

    def add_arguments(self, parser):
        # add lstable argument
        #        LSTableMixin.add_arguments(parser)

        # path to input ADS file
        parser.add_argument(
            'ads_gse_txt',
            help="""
            The input ADS GSE text format file to convert.
            """,
            type=valid_single_file,
        )

        # path to input ADS file
        parser.add_argument(
            '--output-file',
            help="""
            The output test log XML file.
            """,
            type=str,
            default=None,
        )

        # Remove header in bytes from the binary packets
        parser.add_argument(
            '--remove-header',
            help='Remove a header (in bytes) from the binary packet(s)',
            type=int,
            default=None,
        )

    def setup_tasks(self, pipeline):
        # Import task
        from roc.rpl.tasks import IdentifyPackets as identify_packets

        # Define start/end tasks
        start = txt_to_test()

        # Create topology
        pipeline | start | identify_packets() | test_to_xml()

        # define the start points of the pipeline
        pipeline.start = start


class XmlToDdsCommand(Command):
    """
    Command to convert an input MEB GSE test log XML format file
    into MOC DDS TmRaw and/or TcReport XML file(s).
    """
    __command__ = 'guest_xml_to_dds'
    __command_name__ = 'xml_to_dds'
    __parent__ = 'guest'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to convert an input MEB GSE test log XML format file
        into MOC DDS TmRaw and/or TcReport XML file(s).
    """

    def add_arguments(self, parser):
        # add lstable argument
        #        LSTableMixin.add_arguments(parser)

        # path to input ADS file
        parser.add_argument(
            'test_log_xml',
            help="""
            The input MEB GSE Test log XML format file to convert.
            """,
            type=valid_single_file,
        )

        # Remove header in bytes from the binary packets
        parser.add_argument(
            '--scos-header-size',
            help='Bytes length of the dummy SCOS header to add in the DDS binary packet(s)',
            type=int,
            default=None,
        )

        # Name of the output DDS tmraw xml file
        parser.add_argument(
            '--output-tmraw-xml',
            help='Name of the output DDS tmraw xml file',
            type=str,
        )

        # Name of the output DDS tcreport xml file
        parser.add_argument(
            '--output-tcreport-xml',
            help='Name of the output DDS tcreport xml file',
            type=str,
        )

    def setup_tasks(self, pipeline):
        # Import task
        from roc.rpl.tasks import IdentifyPackets as identify_packets

        # Define start task
        start = xml_to_test()

        # Create topology
        pipeline | start | identify_packets() | raw_to_tmraw() | raw_to_tcreport()

        # define the start point of the pipeline
        pipeline.start = start


class XmlToTxtCommand(Command):
    """
    Manage command to convert an input MEB GSE text log XML file into
    a ADS GSE text format file.
    """
    __command__ = 'guest_xml_to_txt'
    __command_name__ = 'xml_to_txt'
    __parent__ = 'guest'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to convert an input MEB GSE text log XML file into
    a ADS GSE text format file.
    """

    def add_arguments(self, parser):
        # add lstable argument
        #        LSTableMixin.add_arguments(parser)

        # path to input ADS file
        parser.add_argument(
            'test_log_xml',
            help="""
            The input MEB GSE test log XML file to convert.
            """,
            type=valid_single_file,
        )

        # path to input ADS file
        parser.add_argument(
            '--output-file',
            help="""
            The output ADS text file.
            """,
            type=str, default=None,
        )

    def setup_tasks(self, pipeline):
        start = xml_to_test()
        end = test_to_txt()

        # Create topology
        pipeline | start | end

        # define the start points of the pipeline
        pipeline.start = start


class ClearDbCommand(Command):
    """
    Manage command to clear a given test
    inside the ROC database,
    providing the test name and uuid.
    """
    __command__ = 'guest_clear'
    __command_name__ = 'clear'
    __parent__ = 'guest'
    __parent_arguments__ = ['guest']
    __help__ = """
    Command to clear a test inside the ROC database.
    """

    def add_arguments(self, parser):
        # the name of the test
        parser.add_argument(
            '--test-name',
            nargs=1,
            help="""
            The name of the test to remove.
            """,
            type=str,
            default=[None],
        )

        # the UUID
        parser.add_argument(
            '--test-uuid',
            nargs=1,
            help="""
            The UUID of the test to remove.
            """,
            type=str,
            default=[None],
        )

        # Clear all tests
        parser.add_argument(
            '--clear-all',
            help="""
            Clear all tests in the ROC database (USE WITH CAUTION!).
            """,
            action='store_true',
        )

    def setup_tasks(self, pipeline):
        # starting task
        start = clear_test()

        # Set test terminated status off
        pipeline.properties.test_terminated = False

        # Set input arguments
        pipeline.properties.test_name = pipeline.properties.test_name[0]
        pipeline.properties.test_uuid = pipeline.properties.test_uuid[0]

        # create the tasks and their dependencies
        pipeline | start

        # define the start points of the pipeline
        pipeline.start = start


class ClearDbFromXmlCommand(Command):
    """
    Manage command to clear a given test
    inside the ROC database,
    providing the test log XML file.
    """
    __command__ = 'guest_clear_xml'
    __command_name__ = 'clear_from_xml'
    __parent__ = 'guest'
    __parent_arguments__ = ['base']
    __help__ = """
    Command to clear a test inside the ROC database from
    its test log XML file.
    """

    def add_arguments(self, parser):
        # the name of the test
        parser.add_argument(
            'test_log_xml',
            help="""
            The XML file the test to remove.
            """,
            type=str,
        )

    def setup_tasks(self, pipeline):
        # starting task
        start = xml_to_test()
        end = clear_test()

        # Set test terminated status off
        pipeline.properties.test_terminated = False

        # create the tasks and their dependencies
        pipeline | start | end

        # define the start points of the pipeline
        pipeline.start = start

class L0ToXmlCommand(Command):
    __command__ = 'guest_l0_to_xml'
    __command_name__ = 'l0_to_xml'
    __parent__ = 'guest'
    __parent_arguments__ = ['base']
    __help__ = 'Command to convert a given RPW L0 hd5 file into a MEB GSE test log XML file'

    def add_arguments(self, parser):
        parser.add_argument(
            'l0_file',
            type=str,
            nargs=1,
            help='Input RPW L0 hd5 file to convert'
        )

        parser.add_argument('--test-log-xml',
                            nargs=1,
                            default=None,
                            type=str,
                            help='Full path of the output test log XML file'
                            )

    def setup_tasks(self, pipeline):
        # Parse input file, then convert it into output test log XML
        start = L0ToTest()
        end = test_to_xml()

        # set the pipeline workflow
        pipeline | start | end

        # define the start points of the pipeline
        pipeline.start = start

class FromXmlCommand(Command):
    __command__ = 'guest_testlog_to_l0'
    __command_name__ = 'testlog_to_l0'
    __parent__ = 'guest'
    __parent_arguments__ = ['base']
    __help__ = 'Command to generate RPW L0 files from a given input MEB GSE test log XML file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-log-xml',
            required=True,
            type=str,
            nargs=1,
            help='Input RPW MEB GSE test log XML file to process'
        )

    def setup_tasks(self, pipeline):
        # Import task from other plugin
        from roc.rpl.tasks import ParsePackets

        # Parse input file, then convert it into output test log XML
        start = xml_to_test()
        end = TestToL0()

        # set the pipeline workflow
        pipeline | start | ParsePackets() | end

        # define the start points of the pipeline
        pipeline.start = start
