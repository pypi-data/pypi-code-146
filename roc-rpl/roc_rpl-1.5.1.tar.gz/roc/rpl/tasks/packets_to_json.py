#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
import json

from roc.rpl.tasks.tools import get_raw_data

try:
    from poppy.core.logger import logger
    from poppy.core.task import Task
    from poppy.core.target import PyObjectTarget, FileTarget
    from poppy.core.tools.exceptions import MissingInput
    from poppy.core.db.connector import Connector
except:
    print('POPPy framework is not installed!')

__all__ = ['PacketsToJson']


class PacketsToJson(Task):
    """
    Task to print the input RPW packets.
    """

    plugin_name = 'roc.rpl'
    name = 'packets_to_json'

    def add_targets(self):
        self.add_input(identifier='raw_data',
                       value=get_raw_data(self.pipeline),
                       target_class=PyObjectTarget)

    def setup_inputs(self):
        # Get input target raw_data value
        try:
            self.raw_data = self.inputs['raw_data'].value
        except:
            raise MissingInput('raw_data input is missing')

        # If passed, retrieve path of the output JSON file
        self.json_file = self.pipeline.get('output_json_file',
                                               default=[None])[0]

        # Retrieve input boolean keywords
        self.print = self.pipeline.get('print',
                                            default=False)
        self.overwrite = self.pipeline.get('overwrite',
                                            default=False)

    def run(self):

        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = f'PrintPacket-{self.job_uuid[:8]}'
        logger.debug(f'Task {self.job_id} is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(
                f'Initializing inputs has failed for {self.job_id}!')
            self.pipeline.exit()
            return

        # Make sure to change header/data_header objects to dictionaries
        packet_list = [None] * len(self.raw_data['packet_list'])
        for i, current_packet in enumerate(self.raw_data['packet_list']):
            packet_list[i] = current_packet
            try:
                packet_list[i]['header'] = current_packet['header'].to_dict()
                packet_list[i]['data_header'] = current_packet['data_header'].to_dict()
            except:
                logger.warning(f'header and/or data_header classes '
                               f'cannot be converted and will be removed for packet {current_packet}')
                packet_list[i].pop('header')
                packet_list[i].pop('data_header')

            if self.print:
                print(json.dumps(packet_list[i], indent=2, default=str))

        if self.json_file:
            with open(self.json_file, 'w') as out_json:
                json.dump(packet_list, out_json, indent=2, default=str)

            logger.info(f'{self.json_file} saved')
