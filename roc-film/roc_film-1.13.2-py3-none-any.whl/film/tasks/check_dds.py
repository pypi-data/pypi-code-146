#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Contains task to check for SolO MOC DDS files.
"""
import os
from glob import glob

from edds_process.response import \
    count_packets

from poppy.core.task import Task
from poppy.core.logger import logger
from poppy.core.target import FileTarget

__all__ = ['CheckDds']


class CheckDds(Task):
    """
    Task to check and load every SolO MOC DDS XML files found into
    a given input directory or list of files.
    """
    plugin_name = 'roc.film'
    name = 'check_dds'

    def add_targets(self):
        self.add_output(identifier='dds_xml_files', many=True,
                        target_class=FileTarget)

    def run(self):

        # Get optional filters from input keywords
        no_tmraw = self.pipeline.get('no_tmraw', default=False)
        no_tcreport = self.pipeline.get('no_tcreport', default=False)

        if no_tmraw and no_tcreport:
            logger.warning('"no-tmraw" and "no-tcreport" input keywords cannot be both '
                           'set to True')
            self.pipeline.exit()

        # Get input directory containing DDS file(s)
        input_dir = self.pipeline.get('input_dir')
        if input_dir:
            self.dds_xml_list = glob(os.path.join(input_dir, '*.xml'))
        elif self.pipeline.get('dds_files'):
            self.dds_xml_list = self.pipeline.get('dds_files')
        else:
            logger.warning(
                'No valid input argument passed to the CheckDds Task')
            self.pipeline.exit()

        # Filtering input DDS files
        self.dds_xml_list = self.filtering_dds(self.dds_xml_list,
                                               no_tcreport=no_tcreport,
                                               no_tmraw=no_tmraw)

        # Check if no DDS file
        self.dds_xml_num = len(self.dds_xml_list)
        if self.dds_xml_num == 0:
            self.dds_packet_num_list = []
            self.dds_packet_num = 0
            logger.warning(f'No input DDS file found')
        else:
            logger.debug('Getting total number of packets...')
            self.dds_packet_num_list = [count_packets(current_dds)
                                        for current_dds in self.dds_xml_list]
            self.dds_packet_num = sum(self.dds_packet_num_list)
            logger.info(f'{self.dds_xml_num} DDS file(s) with {self.dds_packet_num} packets loaded')

        self.outputs['dds_xml_files'].filepath = self.dds_xml_list

    @staticmethod
    def filtering_dds(dds_xml_list,
                      no_tmraw=False,
                      no_tcreport=False):
        """
        Filter input DDS files.

        :param input_dir: Input directory containing
        :return: List of DDS XML files found in input directory
        """

        output_list = []

        # Filtering input DDS file(s)
        for current_file in dds_xml_list:
            file_pattern = os.path.splitext(
                os.path.basename(current_file))[0].lower()
            if 'tmraw' in file_pattern and not no_tmraw:
                output_list.append(current_file)
                logger.debug(f'{current_file} added to the list')
            elif 'tcreport' in file_pattern and not no_tcreport:
                output_list.append(current_file)
                logger.debug(f'{current_file} added to the list')

        return output_list

    def loop_generator(self, loop):

        # Get pipeline
        pipeline = loop.pipeline

        # Get list of dds XML files
        dds_xml_list = loop.inputs['dds_xml_files'].filepath
        if dds_xml_list is None or len(dds_xml_list) == 0:
            logger.info('No input DDS file for loop')
            return

        # Loop over each DDS file in the list
        for i, dds_file_target in enumerate(loop.inputs['dds_xml_files']):

            # pass DDS to first task in the pipeline workflow loop
            dds_file_target.link('dds_xml')

            yield
