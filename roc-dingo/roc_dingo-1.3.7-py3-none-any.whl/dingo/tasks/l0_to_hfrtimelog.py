#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

import h5py
from sqlalchemy import and_, null
import pandas as pd
import numpy as np

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import FileTarget

from roc.rpl.packet_structure.data import Data

from roc.dingo.models.data import HfrTimeLog
from roc.dingo.tasks import get_l0_files, load_param
from roc.dingo.tools import glob_paths, valid_time, query_db, get_columns, load_spice, insert_in_db
from roc.dingo.constants import PIPELINE_DATABASE, TIME_DAILY_STRFORMAT, TRYOUTS, TIME_WAIT_SEC, SQL_LIMIT, \
    TIME_ISO_STRFORMAT, HFR_SCIENCE_PACKETS

__all__ = ['L0ToHfrTimeLog']


class L0ToHfrTimeLog(Task):
    """
    Insert HFR data in input L0 files into the
    in pipeline.hfr_time_log table in ROC database
    See https://gitlab.obspm.fr/ROC/RCS/THR_CALBAR/-/issues/76 for details
    about why this task is needed
    """
    plugin_name = 'roc.dingo'
    name = 'l0_to_hfrtimelog'

    def add_targets(self):
        self.add_input(identifier='rpw_l0_files',
                       many=True,
                       filepath=get_l0_files,
                       target_class=FileTarget)

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):

        # get the input l0 files
        self.l0_files = glob_paths(self.inputs['rpw_l0_files'].filepath)

        # Get start_time input value
        self.start_time = valid_time(self.pipeline.get(
            'start_time', default=[None])[0],
                                     format=TIME_DAILY_STRFORMAT)

        # Get end_time input value
        self.end_time = valid_time(self.pipeline.get(
            'end_time', default=[None])[0],
                                   format=TIME_DAILY_STRFORMAT)

        # get a database session, table model and table columns (except primary key)
        self.session = Connector.manager[PIPELINE_DATABASE].session
        self.model = HfrTimeLog
        self.columns = get_columns(self.model, remove=['id'])

        # Get tryouts from pipeline properties
        self.tryouts = self.pipeline.get(
            'tryouts', default=[TRYOUTS], create=True)[0]

        # Get wait from pipeline properties
        self.wait = self.pipeline.get(
            'wait', default=[TIME_WAIT_SEC], create=True)[0]

        # Retrieve --limit keyword value
        self.limit = self.pipeline.get('limit',
                                       default=[SQL_LIMIT],
                                       )[0]

        # Get or create failed_files list from pipeline properties
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get or create processed_files list from pipeline properties
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)

        # Load spice_manager class
        self.spice = load_spice()

        # Define query filters for existing data in database
        self.filters = []
        if self.start_time:
            self.filters.append(self.model.acq_time >= str(self.start_time))
        if self.end_time:
            self.filters.append(self.model.acq_time < str(self.end_time))

    def run(self):
        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = f'L0ToHfrTimeLog-{self.job_uuid[:8]}'
        logger.info(f'Task {self.job_id} is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(
                f'Initializing inputs has failed for {self.job_id}!')
            self.pipeline.exit()
            return

        n_l0_files = len(self.l0_files)
        logger.info(f'{n_l0_files} RPW L0 files to process')
        if n_l0_files == 0:
            return

        # Loops over each input RPW L0 file
        inserted_count = 0
        updated_count = 0
        failed_count = 0
        for i, current_l0_file in enumerate(self.l0_files):
            logger.info(f'Processing {current_l0_file}    ({n_l0_files - i - 1} remaining)')

            try:
                with h5py.File(current_l0_file, 'r') as l0:
                    # Check if the SCLK SPICE kernel used to compute TM utc times in the input L0 file
                    # is older or newer than the l0 file date (if kernel is older, then it means that utc times are computed
                    # with predictive time coefficients. In this case, the utc times are not stored in the database
                    # in order to avoid confusion)
                    current_l0_datetime = datetime.strptime(l0.attrs['Datetime'][:8],
                                                            TIME_DAILY_STRFORMAT,
                                                            )
                    # Skip file if outside of the [start_time, end_time] time range
                    # (if any)
                    if self.start_time and self.start_time.date() > current_l0_datetime.date():
                        logger.info(f'{current_l0_file} older than {self.start_time.date()}, skip it')
                        continue
                    if self.end_time and self.end_time.date() < current_l0_datetime.date():
                        logger.info(f'{current_l0_file} newer than {self.end_time.date()}, skip it')
                        continue

                    # Retrieving L0 start/end times
                    self.l0_start_time = datetime.strptime(
                        l0.attrs['TIME_MIN'], TIME_ISO_STRFORMAT)
                    self.l0_end_time = datetime.strptime(
                        l0.attrs['TIME_MAX'], TIME_ISO_STRFORMAT)

                    # Retrieve existing data from pipeline.hfr_time_log table before each L0 file processing
                    # (Database content may change between two L0 file processes)
                    logger.debug(f'Getting existing hfr_time_log data between {self.start_time} and {self.end_time}')
                    # Return existing data as a pandas.DataFrame object
                    table_data = query_db(self.session, self.model,
                                          filters=(and_(*self.filters) if self.filters else None),
                                          tryouts=self.tryouts,
                                          wait=self.wait,
                                          limit=self.limit,
                                          )
                    n_existing = table_data.shape[0]
                    # If data have been found in the database, then building and adding a new "coarse_fine" variable.
                    # This variable will be used to handle and compare times in the data
                    # (more simple than with [coarse, fine] vectors)
                    if n_existing > 0:
                        table_data['coarse_fine'] = table_data.apply(
                            lambda x: self.merge_coarse_fine(x['coarse_time'], x['fine_time'])
                            , axis=1)
                    else:
                        logger.info(
                            f'No existing hfr_time_log data found in database between {self.start_time} and {self.end_time}')

                    # Loop over TM packets in L0 file
                    for packet_name in l0['TM'].keys():

                        # Only process science TM packets from HFR
                        if packet_name not in HFR_SCIENCE_PACKETS:
                            continue

                        # Get packet header
                        packet_header = load_param(l0['TM'][packet_name][
                                                       'packet_header'])
                        # Get packet data field header
                        data_field_header = load_param(l0['TM'][packet_name][
                                                           'data_field_header'])
                        # Get packet data
                        packet_data = load_param(l0['TM'][packet_name]['source_data'])

                        # Concatenate packet headers and data dataframes
                        packet_df = pd.concat(
                            [packet_header, data_field_header, packet_data], axis=1)

                        # Add packet creation UTC time
                        packet_df['utc_time'] = l0['TM'][packet_name]['utc_time'][()]

                        # Get number of packets
                        n_packet = packet_df.shape[0]

                        logger.info(
                            f'{n_packet} {packet_name} packets retrieved from {current_l0_file}')

                        # Get mode
                        if 'NORMAL' in packet_name:
                            self.mode = 0
                        elif 'BURST' in packet_name:
                            self.mode = 1
                        elif 'CALIBRATION' in packet_name:
                            self.mode = 2
                        else:
                            raise ValueError(f'Unknown HFR mode for {packet_name} in {current_l0_file}')

                        # Convert PA_THR_ACQUISITION_TIME values into unique integers
                        # (To be comparable with "coarse_fine" variable in database table_data)
                        packet_df['coarse_fine'] = packet_df['PA_THR_ACQUISITION_TIME'].apply(
                            lambda x: self.merge_coarse_fine(x[0], x[1])
                        )

                        # Do the same for packet creation time
                        packet_df['packet_time'] = packet_df['time'].apply(
                            lambda x: self.merge_coarse_fine(x[0], x[1])
                        )

                        # Extract values of delta times for HF1 and HF2 for each packet
                        # Only for NORMAL and BURST packets
                        if self.mode != 2:
                            try:
                                packet_df['delta_time1'], packet_df['delta_time2'] = zip(*packet_df.apply(
                                    self.extract_deltatime,
                                    axis=1
                                ))
                            except:
                                logger.exception(
                                    f'Extraction delta_time values from {packet_name} in {current_l0_file} has failed!')
                                self.failed_files.append(current_l0_file)
                                break

                        # Get list of unique PA_THR_ACQUISITION_TIME values
                        unique_coarse_fine = packet_df['coarse_fine'].unique()
                        n_entry = unique_coarse_fine.shape[0]
                        logger.info(
                            f'{n_entry} {packet_name} entries to insert into hfr_time_log table for {current_l0_file}')
                        for i in range(n_entry):
                            # Get subset of packet data for current acquisition time
                            current_indices = packet_df.index[unique_coarse_fine[i] == packet_df['coarse_fine']]
                            current_df = packet_df.iloc[current_indices].reset_index(drop=True)

                            # Fill new database entry dictionary
                            current_entry = {}
                            current_entry['coarse_time'] = int(current_df['PA_THR_ACQUISITION_TIME'][0][0])
                            current_entry['fine_time'] = int(current_df['PA_THR_ACQUISITION_TIME'][0][1])
                            current_entry['acq_time'] = self.spice.cuc2datetime(
                                current_entry['coarse_time'], current_entry['fine_time'])
                            current_entry['mode'] = self.mode

                            if self.mode != 2:
                                # For delta_time1 and delta_time2 columns, make sure to concatenate all values
                                # Save delta_time1 and delta_time2 as (JSONB format) dictionaries
                                # with packet creation times as keywords
                                # and delta_time1 and delta_time2 block values as values
                                current_entry['delta_time1'] = {}
                                current_entry['delta_time2'] = {}
                                for j in range(current_df.shape[0]):
                                    current_entry['delta_time1'][str(int(current_df['packet_time'][j]))] = \
                                    current_df['delta_time1'][j].astype(int).tolist()
                                    current_entry['delta_time2'][str(int(current_df['packet_time'][j]))] = \
                                    current_df['delta_time2'][j].astype(int).tolist()

                            # Check if data for current acquisition time already in the database
                            try:
                                current_table_df = table_data[unique_coarse_fine[i] == table_data['coarse_fine']]
                                current_table_df.reset_index(inplace=True)
                            except:
                                logger.debug(
                                    f'No {packet_name} entry found in the hfr_time_log table for {current_entry["acq_time"]}')
                                data_to_insert = current_entry
                            else:
                                # if data found, then merge data before inserting
                                data_to_insert = self.merge_data(current_entry, current_table_df)

                                if data_to_insert is None:
                                    logger.info(
                                        f'No new {packet_name} data to insert in hfr_time_log table for {current_entry["acq_time"]}')
                                    continue
                                elif self.mode != 2:
                                    # Sort delta_time dictionaries by ascending packet creation times
                                    data_to_insert['delta_time1'] = dict(sorted(data_to_insert['delta_time1'].items()))
                                    data_to_insert['delta_time2'] = dict(sorted(data_to_insert['delta_time2'].items()))

                            # define columns to check for update
                            update_fields_kwargs = {key: val
                                                    for key, val in data_to_insert.items()
                                                    if key not in ['delta_time1', 'delta_time2']}

                            # Insert entry in the hfr_time_log table
                            insert_status = insert_in_db(self.session, self.model, data_to_insert,
                                                         update_fields=data_to_insert,
                                                         update_fields_kwargs=update_fields_kwargs,
                                                         tryouts=self.tryouts,
                                                         wait=self.wait,
                                                         )
                            if insert_status < 0:
                                logger.error(f'Inserting {update_fields_kwargs} in pipeline.hfr_time_log table '
                                             f'has failed for task {self.job_id}')
                                failed_count += 1
                            elif insert_status > 1:
                                logger.info(f'{update_fields_kwargs} updated in hfr_time_log')
                                updated_count += 1
                            else:
                                logger.debug(
                                    f'{update_fields_kwargs} inserted into hfr_time_log table for task {self.job_id}')
                                inserted_count += 1

            except:
                self.failed_files.append(current_l0_file)
                logger.exception(f'Cannot process {current_l0_file} in task {self.job_id}!')
                break

        logger.info(f'{inserted_count} new entries inserted into hfr_time_log table')
        if updated_count > 0:
            logger.info(f'{updated_count} entries updated in hfr_time_log table')
        if failed_count > 0:
            logger.error(f'hfr_time_log table insertion has failed for {failed_count} entries')

        logger.info(f'Task {self.job_id} has ended')

    def merge_data(self, current_entry, current_table_df):
        """
        Merge properly l0 file data for current acquisition time
        with data already found in the hfr_time_log table.

        :param current_entry: dictionary with entry to insert for current acq. time
        :param current_table_df: pandas DataFrame with existing
                                 hfr_time_log table data for current acq. time
        :return: new dictionary with merged data. NoneType if no new data to merge
        """
        # No merge for CALIBRATION mode
        if current_entry['mode'] == 2:
            return current_entry

        # if no data in database for current entry, then return as is
        if current_table_df.shape[0] == 0:
            logger.debug(f'No delta time values to merge for {current_entry["acq_time"]}')
            return current_entry

        # Get delta_time1 and delta_time2 from table data
        table_delta_time1 = current_table_df['delta_time1'][0]
        table_delta_time2 = current_table_df['delta_time2'][0]
        # Check if current_entry already saved in database
        if (all(k in table_delta_time1 for k in current_entry['delta_time1'].keys()) and
            all(k in table_delta_time2 for k in current_entry['delta_time2'].keys())):
            # If already saved, then return None
            return None

        # Else merge delta_time dictionaries from database and l0 file for current acquisition time
        merged_delta_time1 = {**table_delta_time1, **current_entry['delta_time1']}
        merged_delta_time2 = {**table_delta_time2, **current_entry['delta_time2']}

        # Update current entry with new delta times values
        current_entry['delta_time1'] = merged_delta_time1
        current_entry['delta_time2'] = merged_delta_time2

        return current_entry

    def merge_coarse_fine(self, coarse, fine):
        """
        return input coarse and fine parts of CCSDS CUC time
        as an unique integer

        :param coarse: coarse part of CUC time
        :param fine: fine part of CUC time
        :return: resulting unique integer
        """
        return int(coarse * 100000 + fine)

    def extract_deltatime(self, packet_data):
        """
        Extract HF1 / HF2 delta time values from input HFR binary data blocks.
        Only works with TM_THR_SCIENCE_NORMAL_HFR and TM_THR_SCIENCE_BURST_HFR packets

        :param packet_data: pandas.DataFrame storing packet data
        :return: tuple containing delta time values for HF1 and HF2 bands
        """
        # size of the number of unsigned int
        size = packet_data["PA_THR_HFR_DATA_CNT"]

        # Define block counter parameter name
        # (depends of the mode)
        if self.mode == 0:
            cnt_param = f'PA_THR_N_BLOCK_CNT'
        else:
            cnt_param = f'PA_THR_B_BLOCK_CNT'

        # number of blocks
        nblocks = packet_data[cnt_param]

        # transform the data into byte array
        # store because of the garbage collector removing reference while
        # processing in cython
        byte = np.array(packet_data[
                            "PA_THR_HFR_DATA"
                        ][:size], dtype=np.uint16).byteswap().newbyteorder().tobytes()
        data = Data(byte, len(byte))

        # init offset
        offset = 0

        # init output values
        delta_time1 = np.empty(nblocks, dtype=np.uint32)
        delta_time2 = np.empty(nblocks, dtype=np.uint32)

        # loop over blocks
        for j in range(nblocks):

            # Skip command control, rpw status and temperatures bits
            offset += 8

            # read hfr setup
            hfr_setup_cmd = self._hfr_setup(data, offset)
            offset += 2

            # Skip input setup bits
            offset += 2

            # read hfr sweep setup
            hfr_sweep_cmd = self._hfr_sweep_setup(data, offset)
            n1 = hfr_sweep_cmd[2]
            n2 = hfr_sweep_cmd[0]
            offset += 4

            # read do analysis command
            offset += 1
            do_analysis_cmd = self._do_analysis(data, offset)
            offset += 1

            # read delta times
            deltas = self._delta_times(data, offset)
            delta_time1[j] = deltas[0]
            delta_time2[j] = deltas[1]
            offset += 8

            # initialize bit count
            bit_count = 0

            # Count bands size
            bit_count = self._get_band_size(
                do_analysis_cmd[4],
                hfr_setup_cmd[3],
                hfr_setup_cmd[2],
                n1,
                n2,
                bit_count,
            )
            bit_count = self._get_band_size(
                do_analysis_cmd[3],
                hfr_setup_cmd[3],
                hfr_setup_cmd[2],
                n1,
                n2,
                bit_count,
            )

            # compute the new offset for the block
            offset += bit_count // 8

            # align
            if offset % 2 != 0:
                offset += 1

        return delta_time1, delta_time2

    def _delta_times(self, data, start):
        """
        Read delta times command.
        """

        hf1 = data.u32p(start, 0, 32)
        hf2 = data.u32p(start + 4, 0, 32)

        return hf1, hf2

    def _get_band_size(self, ch, band1, band2, n1, n2, bit_count):
        """
        Get HFR bands total bit size.
        """

        # if channel is activated
        if ch == 1:
            # read the first band
            if band1 == 1:
                bit_count += 12 * n1

            # second band
            if band2 == 1:
                bit_count += 12 * n2

        return bit_count

    def _hfr_setup(self, data, start):
        """
        Return tuple of values from the HFR setup command.
        """
        tmp = start + 1

        # read parameters
        av = data.u8p(tmp, 6, 2)
        hf1 = data.u8p(tmp, 5, 1)
        hf2 = data.u8p(tmp, 4, 1)
        initial_frequency = data.u16p(start, 3, 9)
        sw = data.u8p(start, 2, 1)

        return sw, initial_frequency, hf2, hf1, av

    def _hfr_sweep_setup(self, data, start):
        """
        Return tuple of values from the HFR sweep setup command.
        """

        # read parameters
        hf1_size = data.u8p(start + 3, 4, 4)
        hf1_number = data.u16p(start + 2, 3, 9)
        hf2_size = data.u8p(start + 1, 7, 4)
        hf2_number = data.u16p(start, 6, 9)

        return hf2_number, hf2_size, hf1_number, hf1_size

    def _do_analysis(self, data, start):
        """
        Return tuple of values from the DoAnalysis command.
        """

        # read parameters
        ch1 = data.u8p(start, 7, 1)
        ch2 = data.u8p(start, 6, 1)
        eos = data.u8p(start, 5, 1)
        mod = data.u8p(start, 4, 1)
        it = data.u8p(start, 0, 4)

        return it, mod, eos, ch2, ch1
