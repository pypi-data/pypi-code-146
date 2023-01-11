#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUEST plugin tasks related to RPW L0 file handling."""
import uuid
from datetime import datetime

import sys
import os

from roc.guest.constants import DATA_VERSION, TIME_ISO_STRFORMAT
from roc.guest.tools import valid_data_version
from roc.guest.guest import Test

try:
    from poppy.core.logger import logger
    from poppy.core.db.connector import Connector
    from poppy.core.db.handlers import get_or_create_with_info
    from poppy.core.task import Task
    from poppy.core.target import FileTarget, PyObjectTarget
    from poppy.core.db.dry_runner import DryRunner
except:
    sys.exit('POPPy framework seems to not be installed properly!')

try:
    from roc.film.tasks.metadata import init_l0_meta, get_spice_kernels
    from roc.film.tasks.file_helpers import generate_filepath, get_output_dir
    from roc.film.tasks.l0 import L0
except:
    sys.exit('Dependencies are missing!')


__all__ = ['L0ToTest', 'TestToL0']

class L0ToTest(Task):
    """
    Parse input L0 and save content as a Test class instance.
    """

    plugin_name = 'roc.guest'
    name = 'l0_to_test'

    def add_targets(self):

        self.add_input(target_class=FileTarget,
                       identifier='l0_file',
                       filepath=self.get_l0_file())
        self.add_output(target_class=PyObjectTarget,
                        identifier='raw_data')

    def get_l0_file(self):
        try:
            return self.pipeline.get('l0_file', default=[None])[0]
        except:
            pass

    def run(self):

        try:
            l0_file = self.inputs['l0_file'].filepath
        except:
            logger.error('No input RPW L0 file found')
            return

        # Store input L0 data as a Test class instance into output target value
        self.outputs['raw_data'].value = Test.from_l0(l0_file)


class TestToL0(Task):
    """
    Save test class instance data into an output L0 file.
    """

    plugin_name = 'roc.guest'
    name = 'test_to_l0'

    def add_targets(self):

        self.add_input(target_class=PyObjectTarget,
                       identifier='raw_data')
        self.add_output(target_class=FileTarget,
                        identifier='l0_file')

    def setup_input(self):

        # Get/create list of well processed L0 files
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)
        # Get/create list of failed DDS files
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get test data object
        self.test_data = self.inputs['raw_data'].value
        if not self.test_data:
            logger.warning('Stopping test_to_l0 task: No input raw_data provided')
            return False
        else:
            if self.test_data.version:
                self.data_version = self.test_data.version
            else:
                self.data_version = valid_data_version(
                    self.pipeline.get('data_version', default=[DATA_VERSION])[0])

        # If output directory not found, create it
        self.output_dir = get_output_dir(self.pipeline)
        if not os.path.isdir(self.output_dir):
            logger.debug(f'Making {self.output_dir}...')
            os.makedirs(self.output_dir)

        return True

    def run(self):

        # Initialize inputs
        if not self.setup_input():
            return

        # Initialize L0 metadata
        extra_attrs = {'Data_version':self.data_version,
                       'TIME_MIN':self.test_data.date.strftime(TIME_ISO_STRFORMAT),
                       'TIME_MAX':self.test_data.terminated_date.strftime(TIME_ISO_STRFORMAT),
                       'Generation_date':datetime.utcnow().isoformat(),
                       'File_ID':str(uuid.uuid4()),
                        }
        # Attempt to add SPICE kernels in L0 metadata
        try:
            sclk_file = get_spice_kernels(time_instance=self.test_data.packet_parser.time,
                                      pattern='solo_ANC_soc-sclk')
        except:
            sclk_file = None

        if sclk_file:
            extra_attrs['SPICE_KERNELS'] = sclk_file[-1]
        else:
            logger.info('No SPICE SCLK kernel found!')

        # Initialize L0 metadata
        l0_metadata = init_l0_meta(self,
                                   extra_attrs=extra_attrs)

        # Generate L0 filepath
        l0_filepath = generate_filepath(self, l0_metadata, '.h5')

        # Write L0 file
        try:
            L0().to_hdf5(l0_filepath,
                 packet_parser=self.test_data.packet_parser,
                 metadata=l0_metadata)

        except:
            logger.exception(f'Producing {l0_filepath} has failed!')
            self.failed_files.append(l0_filepath)
        else:
            self.processed_files.append(l0_filepath)
            logger.info(f'{l0_filepath} saved')
