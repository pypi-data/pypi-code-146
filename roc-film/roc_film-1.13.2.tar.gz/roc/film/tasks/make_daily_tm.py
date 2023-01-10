#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Contains task to generate SolO/RPW TmRaw DDS XML daily files.
"""

import os

from edds_process.response import make_tmraw_xml
from poppy.core.logger import logger
from poppy.core.target import FileTarget
from poppy.core.task import Task

from roc.film import DATA_VERSION, TIME_DAILY_STRFORMAT, TMRAW_PREFIX_BASENAME
from roc.film.tools.file_helpers import get_output_dir
from roc.film.tools import valid_data_version

__all__ = ['MakeDailyTm']

class MakeDailyTm(Task):
    """
    Task to write daily XML files containing RPW DDS TmRaw data.
    """
    plugin_name = 'roc.film'
    name = 'make_daily_tm'

    def add_targets(self):
        self.add_output(identifier='daily_tm_xml', many=True,
                        target_class=FileTarget)

    def setup_inputs(self):

        # Get data_version input keyword (can be used to force version of
        # output file)
        self.data_version = valid_data_version(
            self.pipeline.get('data_version', default=[DATA_VERSION])[0])

        # Get/create list of well processed DDS files
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)

        # Get/create list of failed DDS files
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # If output directory not found, create it
        self.output_dir = get_output_dir(self.pipeline)
        if not os.path.isdir(self.output_dir):
            logger.debug(f'Making {self.output_dir}...')
            os.makedirs(self.output_dir)

        # Get packet cache and has new packet flag
        self.packet_cache = self.pipeline.get('packet_cache', default={})
        self.has_new_packet = self.pipeline.get('has_new_packet', default={})
        if not self.packet_cache or not self.has_new_packet:
            return False

        return True

    def run(self):

        logger.debug('Running MakeDailyTm task...')

        if not self.setup_inputs():
            logger.warning('Missing inputs for MakeDailyTm task!')
            return

        # Loop over each day in the outputs
        output_files = []
        for current_category, current_dates in self.packet_cache.items():
            for current_date, packet_data in current_dates.items():

                # Check if new packets have retrieved
                # If not, then no need to write a new output file
                if not self.has_new_packet[current_category][current_date]:
                    logger.info('No need to create new output '
                                f'{current_category} file for {current_date}')
                    continue

                # define format of data version
                data_version = f'V{int(self.data_version):02d}'

                # Build output TmRaw file basename
                packet_date_str = current_date.strftime(TIME_DAILY_STRFORMAT)
                file_basename = '_'.join([
                    TMRAW_PREFIX_BASENAME + '-' + current_category,
                    packet_date_str]
                )

                # Build full new output file basename
                file_basename = '_'.join(
                    [file_basename, data_version]) + '.xml'

                # Build output file path
                output_target_path = os.path.join(
                    self.output_dir, file_basename)

                # Build list of output packets
                output_packets = [current_packet[1]
                                  for current_packet in packet_data]

                # Write output file
                logger.info(f'Writing {len(output_packets)} TmRaw Packet elements '
                            f'into {output_target_path}...')
                try:
                    if make_tmraw_xml(output_packets, output_target_path,
                                      overwrite=True,
                                      logger=logger):
                        self.processed_files.append(output_target_path)
                        output_files.append(output_target_path)
                    else:
                        raise FileNotFoundError
                except:
                    logger.exception(f'Writing {output_target_path} has failed!')
                    self.failed_files.append(output_target_path)

        self.outputs['daily_tm_xml'].filepath = output_files
