#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid

from roc.rpl.tasks.tools import get_raw_data

try:
    from poppy.core.logger import logger
    from poppy.core.task import Task
    from poppy.core.target import PyObjectTarget
    from poppy.core.tools.exceptions import MissingInput
    from poppy.core.db.connector import Connector
except:
    print('POPPy framework is not installed!')

from roc.rpl import VALID_PACKET, PIPELINE_DATABASE
from roc.rpl.exceptions import PacketParsingError
from roc.rpl.time import Time
from roc.rpl.packet_parser.packet_parser import PacketParser

__all__ = ['IdentifyPackets']

class IdentifyPackets(Task):
    """
    Task to perform the RPW packet identification.
    """

    plugin_name = 'roc.rpl'
    name = 'identify_packets'

    def add_targets(self):
        self.add_input(identifier='raw_data',
                       value=get_raw_data(self.pipeline),
                       target_class=PyObjectTarget)
        self.add_output(identifier='raw_data',
                        target_class=PyObjectTarget)

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):
        # Get input target raw_data value
        try:
            self.raw_data = self.inputs['raw_data'].value
        except:
            raise MissingInput('raw_data input is missing')

        # Get/create Time instance for time computation
        self.time_instance = Time()

        # Get IDB inputs
        self.idb_version = self.pipeline.get('idb_version',
                                        default=[self.raw_data['idb_version']])[0]
        self.idb_source = self.pipeline.get('idb_source',
                                       default=[self.raw_data['idb_source']])[0]
        # If idb_version not passed, try to get current IDB version from database
        if self.idb_version is None:
            from roc.idb.tools.db import get_current_idb
            session = Connector.manager[PIPELINE_DATABASE].session
            self.idb_version = get_current_idb(self.idb_source, session)

        # Pass input arguments for the Time instance
        self.time_instance.kernel_date = self.pipeline.get('kernel_date', default=None, args=True)
        self.time_instance.predictive = self.pipeline.get('predictive', default=True, args=True)
        self.time_instance.no_spice = self.pipeline.get('no_spice', default=False, args=True)

        # Initialize packet parser
        self.parser = PacketParser(
                idb_version=self.idb_version,
                idb_source=self.idb_source,
                time=self.time_instance,
            )

        # Get start-time
        self.start_time = self.pipeline.get('start_time', default=[None])[0]

        # Get end-time
        self.end_time = self.pipeline.get('end_time', default=[None])[0]

    def run(self):

        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = f'IdentifyPacket-{self.job_uuid[:8]}'
        logger.debug(f'Task {self.job_id} is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(
                f'Initializing inputs has failed for {self.job_id}!')
            self.pipeline.exit()
            return

        # connect to add exception when packet analysis is bad
        self.parser.extract_error.connect(self.exception)

        # Analyse input RPW TM/TC packets
        packet_list = self.raw_data['packet_list']
        logger.info(f'Identifying {len(packet_list)} input packets...')
        try:
            analyzed_packet_list = self.parser.identify_packets(
                                            packet_list,
                                            start_time=self.start_time,
                                            end_time=self.end_time,
                                            valid_only=False)
        except:
            raise PacketParsingError('Packet parsing has failed!')
        else:
            self.raw_data['packet_list'] = [current_packet
                                    for current_packet in analyzed_packet_list
                                    if current_packet['status'] == VALID_PACKET]
            self.raw_data['invalid_packet_list'] = [current_packet
                                    for current_packet in analyzed_packet_list
                                    if current_packet['status'] != VALID_PACKET]
            self.raw_data['packet_parser'] = self.parser

        # store the rpl instance into the properties
        self.outputs['raw_data'].value = self.raw_data
