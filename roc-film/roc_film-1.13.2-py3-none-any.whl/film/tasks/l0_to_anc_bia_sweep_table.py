#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains task to create the RPW ANC Bias sweep table CDF files."""

import csv
import os
import uuid
from datetime import datetime

import numpy as np
from poppy.core.logger import logger
from poppy.core import TargetFileNotSaved
from poppy.core.generic.cache import CachedProperty
from poppy.core.target import FileTarget
from poppy.core.task import Task

from roc.film import TIME_DAILY_STRFORMAT, TIME_ISO_STRFORMAT
from roc.film.constants import BIA_SWEEP_TABLE_NR
from roc.film.tools import get_datasets, unique_dict_list, sort_dict_list
from roc.film.tools.file_helpers import get_l0_files, get_output_dir, is_output_dir, get_l0_trange, generate_filepath
from roc.film.tools.l0 import L0
from roc.film.tools.metadata import set_logical_file_id

from roc.rap.tasks.bia.current import raw_to_na

__all__ = ['L0ToAncBiaSweepTable']

class L0ToAncBiaSweepTable(Task):
    """
    Task to generate ANC bias sweep table file from l0 file(s).

    For more information about the Bias sweeping, see section 'BIAS sweeping' of
    the RPW DAS User Manual (RPW-SYS-MEB-DPS-NTT-000859-LES)

    """
    plugin_name = 'roc.film'
    name = 'l0_to_anc_bia_sweep_table'

    csv_fieldnames = ['TC_EXE_UTC_TIME',
                      'BIA_SWEEP_TABLE_CUR',
                      'EEPROM_LOADING',
                      'TC_NAME',
                      'TC_EXE_STATE',
                      ]

    def add_targets(self):

        self.add_input(target_class=FileTarget,
                       identifier='l0_files',
                       many=True,
                       filepath=get_l0_files)

        self.add_output(target_class=FileTarget,
                        identifier='anc_bia_sweep_table')

    def setup_inputs(self):

        # Get products directory (folder where final output files will be
        # moved)
        self.products_dir = self.pipeline.get('products_dir',
                                              default=[None], args=True)[0]

        # Get output dir
        self.output_dir = get_output_dir(self.pipeline)
        if not is_output_dir(self.output_dir,
                             products_dir=self.products_dir):
            logger.info(f'Making {self.output_dir}')
            os.makedirs(self.output_dir)
        else:
            logger.debug(f'Output files will be '
                        f'saved into folder {self.output_dir}')

        # Get or create failed_files list from pipeline properties
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get or create processed_files list from pipeline properties
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)

        # Get or create ignored_target list from pipeline properties
        self.ignored_target = self.pipeline.get(
            'ignored_target', default=[], create=True)

        # Get overwrite argument
        self.overwrite = self.pipeline.get(
            'overwrite', default=False, args=True)

        # Get list of input l0 file(s)
        self.l0_file_list = self.inputs['l0_files'].filepath

        # Get force optional keyword
        self.force = self.pipeline.get('force', default=False, args=True)

        # Get L0 files time_min/time_max
        l0_time_min, l0_time_max = get_l0_trange(self.l0_file_list)

        # Define output file start time
        self.start_time = self.pipeline.get(
            'start_time', default=[min(l0_time_min)])[0]
        logger.debug(f'start_time value is {self.start_time}')

        # Define output file end time
        self.end_time = self.pipeline.get(
            'end_time', default=[max(l0_time_max)])[0]
        logger.debug(f'end_time value is {self.end_time}')

        # Retrieve output dataset to produce for the task (it should be one)
        self.dataset = get_datasets(self, self.name)[0]
        logger.debug(f'Produce file(s) for the following dataset: {self.dataset["name"]}')

        # Get existing data (if any)
        self.existing_file = self.pipeline.get('sweep_tables',
                                               args=True, default=[None])[0]
        if self.existing_file:
            self.existing_data = L0ToAncBiaSweepTable.parse_bia_sweep_table_file(
                self.existing_file)
        else:
            self.existing_data = []

        return True

    @CachedProperty
    def output_filepath(self):

        # Build output filename using metadata
        filename_items = {}
        filename_items[
            'File_naming_convention'] = '<Source_name>_<LEVEL>_<Descriptor>_<Datetime>_V<Data_version>'
        filename_items['Source_name'] = 'SOLO>Solar Orbiter'
        filename_items[
            'Descriptor'] = 'RPW-BIA-SWEEP-TABLE>RPW Bias sweep table report'
        filename_items['LEVEL'] = 'ANC>Ancillary data'
        filename_items['Data_version'] = self.dataset['version']

        filename_items['Datetime'] = self.start_time.strftime(
            TIME_DAILY_STRFORMAT) + '-' + self.end_time.strftime(TIME_DAILY_STRFORMAT)
        filename_items['Logical_file_id'] = set_logical_file_id(filename_items)
        return generate_filepath(self, filename_items, 'csv',
                                 output_dir=self.output_dir,
                                 overwrite=self.overwrite)

    def run(self):

        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = f'L0ToAncBiaSweepTable-{self.job_uuid[:8]}'
        logger.info(f'Task {self.job_id} is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(
                f'Initializing inputs has failed for {self.job_id}!')
            try:
                os.makedirs(os.path.join(self.output_dir, 'failed'))
            except:
                logger.error('output_dir argument is not defined!')
            self.pipeline.exit()
            return

        logger.info(f'Loading data from {len(self.l0_file_list)} L0 files '
                    f'between {self.start_time} and {self.end_time}...')

        # First retrieve sweep table data from TC load/clear in l0 files
        # List of TC utc times, tc names, tc ack states and parameters
        tc_load_sweep_list = L0.l0_to_packet_list(self.l0_file_list,
                                          include=self.dataset[
                                              'descr']['packet'],
                                          start_time=self.start_time,
                                          end_time=self.end_time,
                                          ascending=True,
                                          )

        tc_load_sweep_num = len(tc_load_sweep_list)
        if tc_load_sweep_num == 0:
            logger.warning('No sweep table TC found in the input L0 files')
            return
        else:
            logger.info(f'{tc_load_sweep_num} sweep table TCs found')

        # csv header fieldnames length
        field_num = len(self.csv_fieldnames)

        # Initialize the sweep table array with NaN values
        # (Assume here that the table is empty at the beginning)
        sweep_table = np.empty(BIA_SWEEP_TABLE_NR, dtype=np.float32)
        sweep_table[:] = np.nan

        # Loop over tc load/clear sweep list
        has_new_data = False
        for tc_load_sweep in tc_load_sweep_list:

            # Get elements from current tc load/clear sweep packet
            tc_time = tc_load_sweep['utc_time']
            tc_name = tc_load_sweep['palisade_id']
            tc_state = tc_load_sweep['tc_exe_state']
            tc_idb_version = tc_load_sweep['idb_version']
            tc_idb_source = tc_load_sweep['idb_source']

            eeprom_loading = '0'
            if tc_state != 'PASSED':
                # If failed command, the current sweep table stays unchanged
                logger.info(f'{tc_name} on {tc_time} was failed, skip it')
            elif tc_name == 'TC_DPU_CLEAR_BIAS_SWEEP':
                # if valid clear table command is found, then
                # reset the sweep table with NaN values
                sweep_table[:] = np.nan
            elif tc_name == 'TC_DPU_LOAD_BIAS_SWEEP':
                # If valid load table command is executed,
                # then update the current sweep table values

                # Get first index of the elements to change in the sweep table
                first_idx = tc_load_sweep['CP_DPU_BIA_SWEEP_FIRST_IDX']
                # Get number of elements to change in the sweep table
                step_nr = tc_load_sweep['CP_DPU_BIA_SWEEP_STEP_NR']
                # Get current values in physical units (nA)
                # of elements to change in the sweep table
                step_cur = raw_to_na(tc_load_sweep['CP_DPU_BIA_SWEEP_STEP_CUR'],
                                     idb_source=tc_idb_source,
                                     idb_version=tc_idb_version)
                eeprom_loading = str(tc_load_sweep['CP_DPU_BIA_SWEEP_EEPROM'])

                # Update the sweep table with new current values
                sweep_table[first_idx:first_idx + step_nr] = step_cur

            # Write data into output csv file
            row = [''] * field_num
            row[0] = tc_time
            row[1] = np.copy(sweep_table)
            row[2] = eeprom_loading
            row[3] = tc_name
            row[4] = tc_state  # Only write the TC execution state

            # Add row into existing data list
            row_dict = dict(zip(self.csv_fieldnames, row))
            if row_dict not in self.existing_data:
                self.existing_data.append(row_dict)
                has_new_data = True
            else:
                logger.debug(f'({row_dict}) already found in {self.existing_file}')

        if not has_new_data:
            logger.info(
                'No new data loaded: no need to generate a new output file')
            self.pipeline.exit()
            return

        # Make sure to have unique values in the list
        sorted_data = unique_dict_list(self.existing_data)

        # Re-order rows by ascending time values
        logger.debug('Re-ordering sweep table data by ascending times...')
        sorted_data = sort_dict_list(sorted_data, 'TC_EXE_UTC_TIME')

        # Write output CSV file
        output_filepath = self.output_filepath
        logger.info(f'Writing {output_filepath}...')
        try:
            with open(output_filepath, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_fieldnames,
                                        delimiter=',')
                writer.writeheader()
                for current_row in sorted_data:
                    current_row['TC_EXE_UTC_TIME'] = current_row['TC_EXE_UTC_TIME'].strftime(
                        TIME_ISO_STRFORMAT)  # Write UTC time in ISO format
                    current_row['BIA_SWEEP_TABLE_CUR'] = ';'.join([str(element)
                                                                   for element in current_row[
                        'BIA_SWEEP_TABLE_CUR']])  # Write sweep table values using ';' delimiter
                    writer.writerow(current_row)

        except:
            if output_filepath not in self.failed_files:
                self.failed_files.append(output_filepath)
            raise TargetFileNotSaved(
                'Anc Bias sweep table csv file production has failed!')

        if not os.path.isfile(output_filepath):
            if output_filepath not in self.failed_files:
                self.failed_files.append(output_filepath)
            raise FileNotFoundError(f'{output_filepath} not found')
        else:
            logger.info(f'{output_filepath} saved')
            if output_filepath not in self.processed_files:
                self.processed_files.append(output_filepath)

        self.outputs['anc_bia_sweep_table'] = output_filepath

    @staticmethod
    def parse_bia_sweep_table_file(sweep_table_file):
        """
        Parse an input bia sweep table CSV file

        :param sweep_table_file: File to parse
        :return: list of sweep tables
        """

        # Initialize output list
        sweep_table_list = []

        if not os.path.isfile(sweep_table_file):
            logger.error(f'{sweep_table_file} not found!')
        else:
            # Read file and store in output list
            with open(sweep_table_file, 'r', newline='') as csv_file:
                reader = csv.DictReader(csv_file)

                # Loop over rows
                for row in reader:
                    row['TC_EXE_UTC_TIME'] = datetime.strptime(
                        row['TC_EXE_UTC_TIME'], TIME_ISO_STRFORMAT)
                    row['BIA_SWEEP_TABLE_CUR'] = row[
                        'BIA_SWEEP_TABLE_CUR'].split(';')
                    sweep_table_list.append(row)

        return sweep_table_list

    @staticmethod
    def get_latest_sweep_table(current_time, sweep_table_list):
        """
        Get the latest sweep table for a given datetime

        :param current_time: Time for which sweep table must be returned (datetime object)
        :param sweep_table_list: list of sweep tables
        :return: row of the sweep table list
        """

        # Initialize output
        output_table = {}

        # Get size of input table list
        sweep_table_num = len(sweep_table_list)

        # Loop over time of sweep tables
        i = 0
        table_time = sweep_table_list[0]['TC_EXE_UTC_TIME']
        while True:
            # Only get sweep table for passed TC
            if (sweep_table_list[i]['TC_EXE_STATE'] == 'PASSED'):
                output_table = sweep_table_list[i]
                table_time = sweep_table_list[i]['TC_EXE_UTC_TIME']
            i += 1
            if i >= sweep_table_num:
                break
            if current_time <= sweep_table_list[i]['TC_EXE_UTC_TIME']:
                break

        return output_table
