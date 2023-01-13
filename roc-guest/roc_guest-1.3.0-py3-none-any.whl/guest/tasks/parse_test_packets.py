#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUEST plugin tasks to parse RPW TM/TC packet binary data."""

import sys
import uuid

try:
    from poppy.core.logger import logger
    from poppy.core.task import Task
    from poppy.core.target import PyObjectTarget
except Exception:
    sys.exit('POPPy framework seems to not be installed properly!')

# Import external Tasks, classes and methods (if any)
try:
    from roc.rpl.packet_parser import PacketParser
    from roc.rpl.time import Time
    from roc.rpl.constants import VALID_PACKET
except Exception:
    logger.exception('RPL plugin modules cannot be imported!')

__all__ = ['ParseTestPackets']


class ParseTestPackets(Task):
    """
    Parse RPW packet binaries in input Test class instance.
    Return Test class instance with unpacked RPW data
    """

    plugin_name = 'roc.guest'
    name = 'parse_test_packets'

    def add_targets(self):

        self.add_input(target_class=PyObjectTarget,
                       identifier='raw_data')
        self.add_output(target_class=PyObjectTarget,
                        identifier='raw_data')

    def setup_inputs(self):

        # Initialize Time instance
        self.time_instance = Time()

        # Pass input arguments for the Time instance
        self.time_instance.no_spice = self.pipeline.get(
            'no_spice', default=True)

        # Get IDB inputs
        self.idb_version = self.pipeline.get('idb_version', default=[None])[0]
        self.idb_source = self.pipeline.get('idb_source', default=[None])[0]

        # Get test data object
        self.test_data = self.inputs['raw_data'].value

        # Initialize PacketParser instance
        self.PacketParser = PacketParser

        # Get start_time/end_time
        self.start_time = self.pipeline.get('start_time', default=[None])[0]
        self.end_time = self.pipeline.get('end_time', default=[None])[0]

    def run(self):

        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = self.job_uuid[:8]
        logger.info(f'Task {self.job_id} is starting')
        try:
            # Initialize task inputs
            self.setup_inputs()
        except Exception:
            logger.exception(f'Initializing inputs has failed for task {self.job_id}!')
            self.pipeline.exit()
            return

        # Parse RPW packets for the current test
        try:
            packet_count = len(self.test_data.packet_list)
            logger.info(f'Extracting {packet_count} RPW packets '
                        f'from {self.test_data.file_path}...    [{self.job_id}]')
            parser = self._parse_packet(self.test_data.packet_list)
        except Exception:
            logger.exception(f'Parsing RPW packets from {self.test_data.file_path} has failed!    [{self.job_id}]')
        else:
            # Get only valid packets
            valid_packets = self.PacketParser.packet_status(
                parser.parsed_packets,
                status=VALID_PACKET)
            n_valid = len(valid_packets)

            # Get only invalid packets
            invalid_packets = self.PacketParser.packet_status(
                parser.parsed_packets,
                status=VALID_PACKET, invert=True)
            n_invalid = len(invalid_packets)

            if n_invalid > 0:
                logger.error(f'{n_invalid} invalid TM/TC packets '
                             f'found in {self.test_data.file_path}!    [{self.job_id}]')

            # Check if valid packets are found
            if n_valid == 0:
                logger.info(f'No valid TM/TC packet '
                            f'found in {self.test_data.file_path}    [{self.job_id}]')
            else:
                logger.info(f'{n_valid} valid TM/TC packets '
                            f'found in {self.test_data.file_path}    [{self.job_id}]')

            # Fill raw_data packet list
            self.test_data.packet_parser = parser

        self.outputs['raw_data'].value = self.test_data

    def _parse_packet(self, packet_list):
        """
        Analyze input packets.

        :param packet_list:
        :return:
        """

        parser = None

        # Initialize packet_parser
        parser = self.PacketParser(
            idb_version=self.idb_version,
            idb_source=self.idb_source,
            time=self.time_instance,
        )

        # connect to add exception when packet analysis is bad
        parser.extract_error.connect(self.exception)

        # Analyse input RPW TM/TC packets
        parser.parse_packets(packet_list,
                             start_time=self.start_time,
                             end_time=self.end_time,
                             valid_only=False)

        return parser
