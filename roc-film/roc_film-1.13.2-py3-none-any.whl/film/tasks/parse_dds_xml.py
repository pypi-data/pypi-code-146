#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Contains task to parse SolO MOC DDS XML files.
"""

import os

from poppy.core.task import Task
from poppy.core.logger import logger
from poppy.core.target import FileTarget, PyObjectTarget

from edds_process.response import xml_to_dict

__all__ = ['ParseDdsXml']

class ParseDdsXml(Task):
    """
    Task to parse an input DDS TmRaw XML file
    and return content as a dictionary.
    """
    plugin_name = 'roc.film'
    name = 'parse_dds_xml'

    def add_targets(self):
        self.add_input(identifier='dds_xml',
                       filepath=self.get_dds_xml(),
                       target_class=FileTarget)
        self.add_output(identifier='dds_data',
                        target_class=PyObjectTarget)

    def get_dds_xml(self):
        return self.pipeline.get('dds_xml', default=[])

    def setup_inputs(self):

        # Get input DDS XML file
        dds_file = None
        try:
            dds_file = self.inputs['dds_xml'].filepath
            if not os.path.isfile(dds_file):
                raise FileNotFoundError
        except:
            logger.exception(f"Cannot load input DDS XML file '{dds_file}'")
            return False
        else:
            self.dds_file = dds_file

        # Get/create list of well processed DDS files
        self.processed_dds_files = self.pipeline.get(
            'processed_dds_files', default=[], create=True)
        # Get/create list of failed DDS files
        self.failed_dds_files = self.pipeline.get(
            'failed_dds_files', default=[], create=True)

        return True

    def run(self):

        if not self.setup_inputs():
            return

        try:
            logger.info(f'Parsing {self.dds_file}...')
            dds_data = xml_to_dict(self.dds_file)
        except:
            logger.exception(f"Cannot parse input DDS XML file '{self.dds_file}'")
            self.failed_dds_files.append(self.dds_file)
            return
        else:
            self.outputs['dds_data'].value = dds_data
            self.processed_dds_files.append(self.dds_file)
