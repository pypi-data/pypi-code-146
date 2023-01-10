#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to insert SOLO/RPW-related event data into the ROC database."""
import csv
import json
import os
import uuid
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from sqlalchemy import and_, or_, null

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task

from roc.dingo.models.data import EventLog, EfecsEvents, BiaSweepLog, SbmLog
from roc.dingo.constants import PIPELINE_DATABASE, TRYOUTS, TIME_WAIT_SEC, SQL_LIMIT, TF_PA_DPU_0038, TF_PA_DPU_0039, \
    IDB_SOURCE, EFECS_EVENT_LOG, TM_APID_EVENT_LOG, TC_PACKET_EVENT_LOG, HFR_FREQ_LIST_PACKETS, BIA_CURRENT_LOG_PACKETS, \
    BIA_SWEEP_TABLE_PACKETS, BIA_SWEEP_TABLE_NR, TIME_ISO_STRFORMAT, LFR_CALIB_EVENT_LOG
from roc.dingo.models.packet import TmLog, TcLog

from roc.dingo.tools import load_spice, query_db, gen_sql_filters, \
    get_columns, insert_in_db, sbm_qf_eng, \
    get_current_idb, raw_to_na, compute_hfr_list_freq

__all__ = ["EventToDb"]


class EventToDb(Task):
    """
    Insert SOLO/RPW-related event data
    (from database,  SOLO HK data)
    into the ROC database
    """
    plugin_name = 'roc.dingo'
    name = 'event_to_db'

    def add_targets(self):
        pass

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):

        # get the input files
        self.start_time = self.pipeline.get('start_time', default=[None])[0]
        self.end_time = self.pipeline.get('end_time', default=[None])[0]

        # Get SOLO SPICE kernels (SCLK and LSK)
        self.sclk_file = self.pipeline.get(
            'sclk', default=[None], create=True)[0]
        self.lsk_file = self.pipeline.get(
            'lsk', default=[None], create=True)[0]
        if not self.sclk_file or not self.lsk_file:
            raise FileNotFoundError(
                'Both sclk_file and lsk_file must be passed as inputs to run EventToDb-{self.job_sid}!')
        else:
            # Load SPICE kernels
            self.spice = load_spice(
                spice_kernels=[self.lsk_file, self.sclk_file])
        # Get tryouts from pipeline properties
        self.tryouts = self.pipeline.get(
            'tryouts', default=[TRYOUTS], create=True)[0]

        # Get wait from pipeline properties
        self.wait = self.pipeline.get(
            'wait', default=[TIME_WAIT_SEC], create=True)[0]

        # Retrieve --limit keyword value
        self.limit = self.pipeline.get('limit',
                                       default=[SQL_LIMIT],
                                       args=True)[0]

        # get a database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

        # Get idb_version/idb_source from pipeline properties
        self.idb_source = self.pipeline.get(
            'idb_source',
            default=[IDB_SOURCE],
            create=True)[0]

        self.idb_version = self.pipeline.get(
            'idb_version',
            default=[None],
            create=True)[0]

        # If idb_version not passed (is None),
        # then try to get current working version from the database
        if self.idb_version is None:
            self.idb_version = get_current_idb(
                self.idb_source,
                self.session,
                tryouts=self.tryouts,
                wait=self.wait,
            )
        if self.idb_version is None:
            raise ValueError(f'idb_version argument cannot be defined!')

        # Initialize some class attributes
        self.bia_sweep_tables = None

    def run(self):
        # Define task job ID (long and short)
        self.job_id = str(uuid.uuid4())
        self.job_sid = self.job_id[:8]
        logger.info(f'Task EventToDb-{self.job_sid} is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(f'Initializing inputs has failed for task EventToDb-{self.job_sid}!')
            self.pipeline.exit()
            return

        # Inserting TM data into event_log table
        logger.info(f'Inserting pipeline.tm_log data into pipeline.event_log for task EventToDb-{self.job_sid}')
        filters = [TmLog.apid == current_tm
                   for current_tm in TM_APID_EVENT_LOG]
        filters = or_(*filters)
        filters = and_(filters, gen_sql_filters(TmLog,
                                                start_time=self.start_time,
                                                end_time=self.end_time))
        tm_inserted, tm_failed, tm_ignored = self.to_event_log(TmLog, self.tm_to_event,
                                                               filters=filters)

        # Inserting TC data into event_log table
        logger.info(f'Inserting pipeline.tc_log data into pipeline.event_log for task EventToDb-{self.job_sid}')
        filters = [TcLog.palisade_id == current_tc
                   for current_tc in TC_PACKET_EVENT_LOG]
        filters = or_(*filters)
        filters = and_(filters, gen_sql_filters(TcLog,
                                                start_time=self.start_time,
                                                end_time=self.end_time))
        tc_inserted, tc_failed, tc_ignored = self.to_event_log(TcLog, self.tc_to_event,
                                                               filters=filters)

        # Inserting E-FECS data into event_log table
        logger.info(f'Inserting pipeline.efecs_events data into pipeline.event_log for task EventToDb-{self.job_sid}')
        filters = [EfecsEvents.name == current_efecs
                   for current_efecs in EFECS_EVENT_LOG]
        filters = or_(*filters)
        filters = and_(filters, gen_sql_filters(EfecsEvents,
                                                start_time=self.start_time,
                                                end_time=self.end_time))
        efecs_inserted, efecs_failed, efecs_ignored = self.to_event_log(
            EfecsEvents, self.efecs_to_event,
            filters=filters)

        # Inserting SBM data into event_log table
        logger.info(f'Inserting pipeline.sbm_log data into pipeline.event_log for task EventToDb-{self.job_sid}')
        sbm_inserted, sbm_failed, sbm_ignored = self.to_event_log(
            SbmLog, self.sbm_to_event)

        # Inserting TC LFR calibration data into event_log table
        # For LFR calib, get all data since the beginning of the mission
        # (To be sure to not have incomplete calibrations)
        filters = [TcLog.palisade_id == current_tc
                   for current_tc in LFR_CALIB_EVENT_LOG]
        filters = or_(*filters)
        lfrcal_inserted, lfrcal_failed, lfrcal_ignored = self.to_event_log(
            TcLog, self.lfrcalib_to_event,
            filters=filters)

        # Inserting Bias sweep table data into event_log table
        # For sweep tables get all data since the beginning of the mission
        # (To be sure to have the full table loading history)
        filters = [TcLog.palisade_id == current_tc
                   for current_tc in BIA_SWEEP_TABLE_PACKETS]
        filters = or_(*filters)
        logger.info(f'Inserting bias sweep table data (in tc_log) into pipeline.event_log for task EventToDb-{self.job_sid}')
        sweeptable_inserted, sweeptable_failed, sweeptable_ignored = self.to_event_log(
            TcLog, self.biasweeptable_to_event,
            filters=filters)

        # Inserting Bias sweep data into event_log table
        # For Bias sweep get all data since the beginning of the mission
        # (To be sure to not have incomplete sweep)
        sweep_inserted, sweep_failed, sweep_ignored = self.to_event_log(
            BiaSweepLog, self.biasweep_to_event)

        inserted = sweep_inserted + sweeptable_inserted + \
            sbm_inserted + efecs_inserted + \
            tm_inserted + tc_inserted + lfrcal_inserted
        failed = sweep_failed + sweeptable_failed + \
            sbm_failed + efecs_failed + \
            tm_failed + tc_failed + lfrcal_failed
        ignored = sweep_ignored + sweeptable_ignored + \
            sbm_ignored + efecs_ignored + \
            tm_ignored + tc_ignored + lfrcal_ignored

        logger.info(f'{inserted} events inserted')
        if failed > 0:
            logger.error(f'{failed} events failed')
        if ignored > 0:
            logger.warning(f'{ignored} events ignored')

    def efecs_to_event(self, data):
        """
        Convert input data rows from pipeline.efecs_events table
        into entries to be saved in pipeline.event_log table.

        :param data: input efecs_events data rows as a pandas.DataFrame object
        :return: pandas.DataFrame object containing Efecs events to be inserted
        """

        # Sub-method to compute end_time from start_time and duration in seconds
        # (Used by pandas.DataFrame.apply() method to get end_time)
        def get_end_time(row):
            return row.utc_time + timedelta(
                seconds=int(row.attributes["duration"]))

        # Make sure to inserted allowed EFECS events
        efecs_to_insert = pd.DataFrame()
        n_data = data.shape[0]

        # Define output event_log columns values
        efecs_to_insert['label'] = data['name']
        efecs_to_insert['start_time'] = data['utc_time']
        efecs_to_insert['is_predictive'] = [True] * n_data

        # Define end_time (if any duration. Othewise end_time=start_time)
        efecs_to_insert['end_time'] = data.apply(
            lambda row: get_end_time(row)
            if 'attributes' in row else row.utc_time,
            axis=1)

        # Set description
        efecs_to_insert['description'] = data['attributes']

        return efecs_to_insert

    def sbm_to_event(self, data):
        """
        Convert input data rows from pipeline.sbm_log table
        into entries to be saved in pipeline.event_log table.

        :param data: input sbm_log data rows as a pandas.DataFrame object
        :return: a pandas.DataFrame object containing data to be inserted
        """
        # Sub-method to compute sbm event start_time/end_time
        def get_start_end(data):
            # extract SBM algo parameters
            # (stored as a strings)
            params = [int(val)
                      for key, val in data['sbm_algo_param'].items()]
            sbm_time = data["utc_time"]
            if data["sbm_type"] == 1 and len(params) == 3:
                sbm_dt1_sbm1 = params[0]
                sbm_dt2_sbm1 = params[1]
                sbm_dt3_sbm1 = params[2]
                # Compute SBM event start, end and occurred times
                # (see SSS or DAS User manual for details)
                if sbm_dt2_sbm1 < 2 * sbm_dt1_sbm1:
                    end_time = sbm_time + timedelta(
                        seconds=sbm_dt1_sbm1)
                    start_time = end_time - timedelta(
                        seconds=sbm_dt2_sbm1)
                elif sbm_dt2_sbm1 > 2 * sbm_dt1_sbm1:
                    end_time = sbm_time + \
                        timedelta(
                            seconds=int(sbm_dt1_sbm1 + sbm_dt3_sbm1))
                    start_time = end_time - timedelta(seconds=sbm_dt2_sbm1)
                else:
                    end_time = sbm_time + timedelta(
                        seconds=sbm_dt1_sbm1)
                    start_time = end_time - timedelta(
                        seconds=sbm_dt2_sbm1)

                # Set SBM1 quality factor transfer function
                sbm_qf_tf = TF_PA_DPU_0038

            elif data["sbm_type"] == 2 and len(params) == 10:
                sbm_dt = params[0]
                # Compute start_time / end_time
                start_time = sbm_time - timedelta(
                    seconds=(sbm_dt / 2 + 1))
                end_time = sbm_time + timedelta(
                    seconds=(sbm_dt / 2 + 1))

                # Set SBM1 quality factor transfer function
                sbm_qf_tf = TF_PA_DPU_0039
            else:
                logger.error(f'Entry {data} is badly formatted, please check!')
                return None, None, None

            # Compute engineering value of quality factor
            sbm_qf = sbm_qf_eng(float(data['sbm_qf']), sbm_qf_tf,
                                idb_source=self.idb_source,
                                idb_version=self.idb_version)

            # store sbm parameters as a JSON format string
            description = {key: val
                           for key, val in data.items()
                           if key in ['cuc_time', 'selected', 'status']
                           }
            # Add Quality factor
            description['sbm_qf'] = sbm_qf

            # And SBM algo parameters
            for key, val in data['sbm_algo_param'].items():
                description[key] = int(val)

            return start_time, end_time, description

        # initialize output
        sbm_to_insert = pd.DataFrame()

        # Create label and is_predictive
        sbm_to_insert['label'] = data["sbm_type"].apply(
            lambda row: f'SBM{row} EVENT')
        sbm_to_insert['is_predictive'] = data['utc_time_is_predictive']

        # Define start_time, end_time and description
        sbm_to_insert['start_time'], \
            sbm_to_insert['end_time'], sbm_to_insert['description'] = zip(*data.apply(
                lambda row: get_start_end(row),
                axis=1))

        return sbm_to_insert

    def biasweeptable_to_event(self, data):
        """
        Extract BIAS sweep table values from input TC data

        :param data: TC packet data (as a pandas.DataFrame object)
        :return: pandas.DataFrame object containing bias sweep tables to insert
        """

        def to_na(sweep_first_idx, sweep_step_nr, sweep_step_cur,
                  sweep_table=None):

            if sweep_table is None:
                sweep_table = np.empty(BIA_SWEEP_TABLE_NR, dtype=np.float32)
                sweep_table[:] = np.nan
            # Update the sweep table with new current values
            sweep_table[sweep_first_idx: sweep_first_idx + sweep_step_nr] = raw_to_na(
                sweep_step_cur, idb_version=self.idb_version, idb_source=self.idb_source)

            # Return current table
            return sweep_table

        # Initialize output
        output_data = []

        # Initialize loop variables
        # We assume the sweep table is empty at the beginning
        sweep_table = np.empty(BIA_SWEEP_TABLE_NR, dtype=np.float32)
        sweep_table[:] = np.nan

        # Loop over each row in the input data
        for current_row in data.to_dict(orient='records'):

            # Get packet name
            packet_name = current_row['palisade_id']

            # Make sure to start with an empty description
            description = {}
            if packet_name == 'TC_DPU_CLEAR_BIAS_SWEEP':
                # if valid clear table command is found, then
                # stores NULL values
                sweep_table[:] = np.nan
                description['sweep_step_cur'] = None
                description['sweep_eeprom'] = False
            elif packet_name == 'TC_DPU_LOAD_BIAS_SWEEP':
                # If valid load table command is executed,
                # then update the current sweep table values
                sweep_table = to_na(
                    current_row['data']['CP_DPU_BIA_SWEEP_FIRST_IDX'],
                    current_row['data']['CP_DPU_BIA_SWEEP_STEP_NR'],
                    current_row['data']['CP_DPU_BIA_SWEEP_STEP_CUR'],
                    sweep_table=sweep_table
                )
                # Store sweep table values in description
                description['sweep_step_na'] = list(sweep_table.astype(str))
                # Store EEPROM loading state
                description['sweep_eeprom'] = int(current_row['data'][
                    'CP_DPU_BIA_SWEEP_EEPROM']) == 1
            else:
                continue

            # Add a new entry for the event_log table
            new_entry = {
                'label': packet_name,
                'description': description,
                'start_time': current_row['utc_time'],
                'end_time': current_row['utc_time'],
                'is_predictive': True
            }
            output_data.append(new_entry)

        # Convert list of dictionaries into list of lists
        if len(output_data) > 0:
            # Store Bias sweep table values for bias sweep events (see in
            # self.biasweep_to_event)
            self.bia_sweep_tables = pd.DataFrame.from_records(
                output_data).sort_values(by=['start_time'], ignore_index=True)

        return self.bia_sweep_tables

    def biasweep_to_event(self, data):
        """
        Convert input data rows from pipeline.bia_sweep_log table
        into entries to be saved in pipeline.event_log table.

        :param data: input bia_sweep_log data rows (passed as a pandas.DataFrame object)
        :return: a pandas.DataFrame object contains sweeps to insert
        """
        # Initialize output
        output_data = []

        # Loops over the input data to get complete bias sweeps
        sweep_start_buffer = []
        ant_index_buffer = []
        for current_row in data.to_dict(orient='records'):
            if current_row['sweep_step'] in ['START_ANT1', 'START_ANT2', 'START_ANT3']:
                current_ant_index = current_row['sweep_step'][-1]
                if current_ant_index in ant_index_buffer:
                    current_sweep_index = ant_index_buffer.index(current_ant_index)
                    # If antenna index already found in buffer, this is not expected
                    logger.error(f"START_ANT{current_ant_index} already found in antenna index buffer. "
                                 f"Bias sweep on {sweep_start_buffer[current_sweep_index]} might be incomplete!")
                    # Remove already existing bia sweep start and antenna index values
                    # from the buffers
                    del sweep_start_buffer[current_sweep_index]
                    del ant_index_buffer[current_sweep_index]

                # Add the antenna index to the antenna index buffer list
                ant_index_buffer.append(current_ant_index)
                # add the sweep start time in sweep_start_buffer list
                sweep_start_buffer.append(current_row['utc_time'])
            elif current_row['sweep_step'] in ['END_ANT1', 'END_ANT2', 'END_ANT3']:
                # The END_ANT{ant_index} should match with ones of the previous START_ANT{ant_index} in ant_index_buffer
                # If not returns a warning message and skip sweep
                current_ant_index = current_row['sweep_step'][-1]
                if current_ant_index not in ant_index_buffer:
                    logger.warning(f'{current_row} is not associated with a previous '
                                   f'START_ANT{current_ant_index} event, skip sweep'
                                    )
                    continue
                else:
                    current_sweep_index = ant_index_buffer.index(current_ant_index)
                    current_sweep_start = sweep_start_buffer[current_sweep_index]
                    # Add a new entry for the event_log table
                    new_entry = {
                        'label': f'BIA_SWEEP_ANT{current_ant_index}',
                        'description': null(),
                        'start_time': current_sweep_start,
                        'end_time': current_row['utc_time'],
                        'is_predictive': current_row['utc_time_is_predictive']
                    }

                    # Retrieve values in nA of the Bias sweep table used for
                    # the current sweep
                    if self.bia_sweep_tables is not None:
                        current_table = self.bia_sweep_tables[
                            self.bia_sweep_tables.start_time <= current_sweep_start].sort_values(by=['start_time'],
                                                                                         ascending=False,
                                                                                         ignore_index=True)
                        new_entry['description'] = {
                            'sweep_step_na': current_table.description[0]['sweep_step_na']
                        }
                    else:
                        logger.warning(f'No valid Bias sweep table values found for current bias sweep!')

                    output_data.append(new_entry)

                # Remove bia sweep start and antenna index values
                # from the buffers
                del sweep_start_buffer[current_sweep_index]
                del ant_index_buffer[current_sweep_index]
            elif current_row['sweep_step'] in ['STEP_ANT1', 'STEP_ANT2', 'STEP_ANT3']:
                # Ignore detailed bias value steps
                pass
            else:
                pass

        # Convert list of dictionaries into list of lists
        if len(output_data) > 0:
            # Store bia sweep data as pandas.DataFrame object
            sweep_to_insert = pd.DataFrame.from_records(
                output_data).sort_values(by=['start_time'], ignore_index=True)
        else:
            sweep_to_insert = pd.DataFrame()

        return sweep_to_insert

    def tm_to_event(self, data):
        """
        Convert input data rows from pipeline.tm_log table
        into entries to be saved in pipeline.event_log table.

        :param data: input tm_log data rows as a pandas.DataFrame object
        :return: pandas.DataFrame object containing tm_log rows to insert
        """
        # Initialize output
        tm_to_insert = pd.DataFrame()

        tm_to_insert['label'] = data['palisade_id']
        tm_to_insert['description'] = data['data']
        tm_to_insert['start_time'] = data['utc_time']
        tm_to_insert['end_time'] = data['utc_time']
        tm_to_insert['is_predictive'] = data['utc_time_is_predictive']

        return tm_to_insert

    def tc_to_event(self, data):
        """
        Convert input data rows from pipeline.tc_log table
        into entries to be saved in pipeline.event_log table.

        :param data: input tc_log data rows passed a pandas.DataFrame object
        :return: pandas.DataFrame object containing tc_log rows to insert
        """
        # Initialize output
        tc_to_insert = pd.DataFrame()

        # Number of input rows
        n_data = data.shape[0]

        tc_to_insert['label'] = data['palisade_id']
        tc_to_insert['start_time'] = data['utc_time']
        tc_to_insert['end_time'] = data['utc_time']
        tc_to_insert['is_predictive'] = [True] * n_data

        # Set description field
        # By default store TC data in the description
        tc_to_insert['description'] = data['data']
        # For HFR FREQ LIST TC, provide a comprehensive list of frequency values
        # in the description
        where_hfr_list = data['palisade_id'].isin(HFR_FREQ_LIST_PACKETS)
        tc_to_insert.loc[where_hfr_list, ('description')] = data.loc[where_hfr_list].apply(
            lambda row: self.extract_hfr_freq_list(
                row['palisade_id'],
                row['data'],
            ), axis=1
        )
        # For Bias current TC, provide a comprehensive value of the bias
        # current in nA
        where_bia_cur = data['palisade_id'].isin(BIA_CURRENT_LOG_PACKETS)
        tc_to_insert.loc[where_bia_cur, ('description')] = data.loc[where_bia_cur].apply(
            lambda row: self.extract_bia_current(
                row['palisade_id'],
                row['data']
            ), axis=1)

        return tc_to_insert

    def lfrcalib_to_event(self, data):
        """
        Extract LFR calibration events from input TC data

        :param data: TC packet data rows (as a pandas.DataFrame Group)
        :return: pandas.DataFrame object containing the N LFR calibration events
        """

        # Initialize the default value of output
        calib_to_insert = pd.DataFrame()

        # Initialize loop variables
        calib_list = []
        current_calib = None

        # Loop over each row in the input data
        for current_row in data.to_dict(orient='records'):

            # Get packet name
            packet_name = current_row['palisade_id']

            if packet_name == 'TC_LFR_ENABLE_CALIBRATION' and not current_calib:
                # New LFR Calibration has started
                current_calib = current_row
            elif packet_name == 'TC_LFR_DISABLE_CALIBRATION' and current_calib:
                # Current LFR calibration has ended

                # Add a new entry for the event_log table
                new_entry = {
                    'label': 'LFR CALIBRATION',
                    'description': {'description': 'LFR internal calibration'},
                    'start_time': current_calib['utc_time'],
                    'end_time': current_row['utc_time'],
                    'is_predictive': True
                }
                calib_list.append(new_entry)

                # Reset current calibration event
                current_calib = None
            elif packet_name == 'TC_LFR_ENABLE_CALIBRATION' and current_calib:
                logger.warning(f'Incomplete LFR calibration for {current_calib}!')
                current_calib = None  # Force new LFR calibration event
            elif packet_name == 'TC_LFR_DISABLE_CALIBRATION' and not current_calib:
                logger.warning(f'Encounter TC_LFR_DISABLE_CALIBRATION, but not previous TC_LFR_ENABLE_CALIBRATION found!')

        # Convert list of dictionaries into pandas.DataFrame
        if len(calib_list) > 0:
            calib_to_insert = pd.DataFrame.from_records(calib_list)

        return calib_to_insert

    def extract_hfr_freq_list(self, packet_name, packet_data):
        """
        Extract the list of HFR frequencies from input TCs
        (for HFR LIST mode)

        :param packet_name: Name of the TC (PALISADE ID)
        :param packet_data: TC data (pandas.DataFrame)
        :return: hfr_freq_list dictionary with freq_list and freq_nr
        """
        hfr_freq_list = {}

        # Get mode and HFR band from packet_name
        # (e.g., TC_THR_LOAD_BURST_PAR_2)
        tc_fields = packet_name.split('_')
        # Get first letter of the current mode (N or B)
        mode = tc_fields[3][0]
        # Get HFR band
        band = int(tc_fields[-1][0]) - 1

        # Get number of frequencies to extract
        hfr_freq_list['freq_nr'] = int(packet_data[f'SY_THR_{mode}_SET_HLS{band}_NR_FREQ'])
        # Extract list of frequencies in kHz
        hfr_freq_list['freq_list'] = [
            str(compute_hfr_list_freq(current_freq)).strip()
            for current_freq in packet_data[f'SY_THR_{mode}_SET_HLS_FREQ_HF{band}']
        ]

        return hfr_freq_list

    def extract_bia_current(self, packet_name, packet_data):
        """
        Extract BIAS current value from input TC packet data

        :param packet_name: Name of the TC packet (palisade ID)
        :param packet_data: bias current TC data as a dictionary
        :return: Bias current value in nA set on current antenna
        """
        # Define CP_BIA_SET_BIAS{i} TC name (where i = [0, 1, 2])
        param_name = 'CP_BIA_SET_BIAS{0}'.format(packet_name[-1])
        # Get Bias current value in nA for the corresponding sensor
        # (requires IDB for transfer function)
        return {param_name: float(raw_to_na(packet_data[param_name],
                                            idb_source=self.idb_source,
                                            idb_version=self.idb_version))}

    def to_event_log(self, model, func,
                     filters=None):
        """
        Generic method to insert data into the pipeline.event_log table.

        :param model: table class of data to copy into event_log table
        :param func: method to use to map data between input and output table fields
        :param filters: list of filters for database query (time range filtering will be automatically appended)

        :return: inserted, failed and ignored entry counters + input data returned from database
        """
        # Get data from pipeline table
        data = self.query_data(model, filters=filters)

        n_data = data.shape[0]
        logger.info(f'{n_data} {model.__tablename__} data to insert into event_log '
                    f'between {self.start_time} and {self.end_time} for task EventToDb-{self.job_sid} ')
        if n_data == 0:
            return 0, 0, 0

        # Convert data into entries compatible with pipeline.event_log table
        data_to_insert = func(data)
        n_entry = data_to_insert.shape[0]

        # Insert data (or update if already exist)
        inserted_count = 0
        failed_count = 0
        ignored_count = 0
        if n_entry > 0:
            # Add insertion times
            data_to_insert['insert_time'] = [datetime.today()] * n_entry
            for i, current_entry in enumerate(self.df_to_dict(data_to_insert, EventLog)):
                if current_entry['label'] in [None, null()]:
                    logger.debug(f'{current_entry} is ignored for task EventToDb-{self.job_sid}')
                    ignored_count += 0
                    continue

                # Unique constraint is only on label, start_time and end_time
                update_fields_kwargs = {
                    key: val
                    for key, val in current_entry.items()
                    if key in ['start_time',
                               'end_time',
                               'label',
                               ]
                }
                if insert_in_db(self.session, EventLog, current_entry,
                                update_fields=current_entry,
                                update_fields_kwargs=update_fields_kwargs,
                                ) < 0:
                    logger.error(f'Inserting {current_entry} in pipeline.event_log table '
                                 f'has failed for task EventToDb-{self.job_sid}')
                    failed_count += 1
                else:
                    logger.debug(f'{current_entry} inserted into pipeline.event_log table for task EventToDb-{self.job_sid}')
                    inserted_count += 1

        return inserted_count, failed_count, ignored_count

    def df_to_dict(self, data, model,
                   remove=['id']):
        """
        Convert input pandas.Dataframe containing input data
        into dictionary.
        Keep only table columns as keywords in the output dictionary.

        :param data: pandas.Dataframe containing input data
        :param model: table class
        :param remove: list of fields to remove
        :return: dictionary
        """
        columns = get_columns(model, remove=remove)
        return data[columns].to_dict('records')

    def query_data(self, model, filters=[]):
        """
        Common method to query data from database and
        to return rows as pandas.Dataframe

        :param model: Table class
        :param filters: List of filters to query
        :return: pandas.Dataframe containing query results
        """

        # If not input filters, then filter at least by time range
        if filters is None:
            filters = gen_sql_filters(model,
                                      start_time=self.start_time,
                                      end_time=self.end_time)

        # If possible, sort returned rows by increasing UTC times
        try:
            order_by = model.utc_time
        except:
            order_by = None

        results = query_db(self.session, model,
                         filters=filters,
                         order_by=order_by,
                         tryouts=self.tryouts,
                         wait=self.wait,
                         limit=self.limit,
                         )
        return results
