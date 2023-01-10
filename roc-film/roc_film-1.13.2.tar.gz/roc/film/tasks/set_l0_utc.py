#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains task to set the utc_time values of L0 TM/TC packets."""


import os
import shutil
from datetime import datetime

import h5py
from poppy.core.logger import logger
from poppy.core.target import FileTarget
from poppy.core.task import Task
from roc.rpl import Time

from roc.film import TIME_ISO_STRFORMAT
from roc.film.tools.file_helpers import get_output_dir
from roc.film.tools.l0 import L0

__all__ = ['SetL0Utc']

class SetL0Utc(Task):
    """
    Set the UTC times of the input L0 file using SolO SPICE kernels.
    """
    plugin_name = 'roc.film'
    name = 'set_l0_utc'

    def add_targets(self):
        self.add_input(target_class=FileTarget,
                       identifier='l0_file',
                       filepath=self.get_l0_file())
        self.add_output(target_class=FileTarget,
                        identifier='l0_file')

    def get_l0_file(self):
        return self.pipeline.get('l0_file', default=[None])[0]

    def setup_inputs(self):
        self.l0_file = self.inputs['l0_file'].filepath
        if not os.path.isfile(self.l0_file):
            logger.error(f'Input file {self.l0_file} not found!')
            return False

        # Get time instance
        self.time = Time()

        # Pass input arguments for the Time instance
        self.time.kernel_date = self.pipeline.get(
            'kernel_date', default=None, args=True)
        self.time.predictive = self.pipeline.get(
            'predictive', default=True, args=True)
        self.time.no_spice = self.pipeline.get(
            'no_spice', default=False, args=True)

        # Get/create list of well processed L0 files
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

        return True

    def run(self):

        # Load/Initialize task inputs
        if not self.setup_inputs():
            return

        # Make a copy of the input L0 file
        l0_copy = os.path.join(self.output_dir,
                               os.path.basename(self.l0_file))
        shutil.copyfile(self.l0_file, l0_copy)

        if not self._set_utc_time(l0_copy):
            logger.info(f'{self.l0_file} does not need to be updated '
                        f'(delete copy in {self.output_dir})')
            os.remove(l0_copy)
        else:
            logger.debug('Make sure to have sorted/unique utc time values')
            L0.order_by_utc(l0_copy, unique=True, update_time_minmax=True)
            logger.info(f'{l0_copy} updated')

    def _set_utc_time(self, l0_file):

        # Flag to indicate if the L0 file content has been changed at the end
        # (or if the L0 already uses the latest SPICE kernels to compute time).
        # If has_changed = False, then do not need to update the L0, if True then
        # a new L0 file with updated UTC times will be created
        has_changed = False

        # SPICE SCLK kernel name prefix
        sclk_prefix = 'solo_ANC_soc-sclk'

        # Get loaded SPICE kernels
        loaded_kernel_list = self.time.spice.kall()
        if not loaded_kernel_list:
            logger.warning('No SPICE kernel loaded, exiting')
            return has_changed
        else:
            # Keep only SCLK kernels
            loaded_sclk_list = [kfile
                                for kfile in loaded_kernel_list.keys()
                                if sclk_prefix in kfile]
            loaded_sclk_num = len(loaded_sclk_list)
            if loaded_sclk_num == 0:
                logger.warning('No SPICE SCLK kernel loaded, exiting')
                return has_changed
            else:
                # Get loaded SCLK (latest)
                loaded_sclk = os.path.basename(loaded_sclk_list[-1])

        # Open L0 file
        with h5py.File(l0_file, 'a') as l0:

            # Check if utc time values need to be updated
            # To achieve it, re-compute UTC times with loaded kernels
            # and compare with current values in the L0
            cat = 'TM'
            if cat in l0.keys():
                # Loop over each TM packet in L0
                for packet_name in l0[cat].keys():
                    # Get packet UTC times
                    utc_time = [datetime.strptime(current_time[:-4] + 'Z', TIME_ISO_STRFORMAT)
                                for current_time in l0[cat][packet_name]['utc_time'][()]]

                    # Compute UTC times with current SPICE kernels from
                    # array of time in packet data_field_header
                    new_utc_time = self.time.obt_to_utc((l0[cat][packet_name]
                                                         ['data_field_header']['time'][()])[:, :2],
                                                        to_datetime=True)
                    try:
                        # Compare current L0 utc time values with new ones
                        assert utc_time == new_utc_time
                    except AssertionError:
                        # If not equal, then update L0 UTC Times with loaded
                        # SCLK kernel
                        l0[cat][packet_name]['utc_time'][...] = new_utc_time
                        logger.debug(f'UTC time values updated for '
                                     f'{packet_name} in {l0_file}')
                        has_changed = True
                    else:
                        logger.debug(f'Same UTC time values found for '
                                     f'{packet_name} in {l0_file}')

            # If UTC times have been updated, set the new SCLK filename
            # in the SPICE_KERNELS attribute
            if has_changed:
                l0.attrs['SPICE_KERNELS'] = loaded_sclk

        return has_changed
