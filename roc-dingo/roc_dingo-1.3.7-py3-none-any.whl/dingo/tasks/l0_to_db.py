#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to insert RPW L0 data into the ROC database."""
from datetime import datetime, timedelta
import json
import concurrent.futures

import pandas as pd
import scipy.sparse as sparse
import h5py
import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, null

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import FileTarget

from roc.dingo.models.data import SbmLog, LfrKcoeffDump, BiaSweepLog, HfrTimeLog
from roc.dingo.models.packet import TmLog, TcLog
from roc.dingo.tools import get_packet_sha, compute_apid, load_spice, \
    query_db, is_sclk_uptodate, get_columns, get_current_idb, \
    bulk_insert, glob_paths, valid_time
from roc.dingo.constants import PIPELINE_DATABASE, \
    TIME_DAILY_STRFORMAT, TRYOUTS, TIME_WAIT_SEC, SQL_LIMIT, PIPELINE_TABLES, \
    SBM_ALGO_PARAM_LIST, LFR_KCOEFF_PARAM_NR, \
    SBM_LOG_PACKETS, LFR_KCOEFF_DUMP_PACKETS, \
    TIME_ISO_STRFORMAT, PACKET_TYPE, TC_ACK_ALLOWED_STATUS, IDB_SOURCE, WORKERS, \
    BIA_SWEEP_LOG_PACKETS, CIWT0130TM, \
    NAIF_SOLO_ID, PACKET_DATA_GROUP, EVENT_TM_APID, TC_ACK_APID, HK_TM_APID, HFR_SCIENCE_PACKETS

__all__ = ["L0ToDb", "get_l0_files", "load_param"]


class L0ToDb(Task):
    """
    Insert content of input L0 files into the
    in ROC database
    """
    plugin_name = 'roc.dingo'
    name = 'l0_to_db'

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

        # Get include/exclude optional inputs
        self.include = self.pipeline.get(
            'include', default=[], create=True)
        self.exclude = self.pipeline.get(
            'exclude', default=[], create=True)

        # Retrieve --exclude-tm-apid, --exclude-tc-apid
        self.exclude_tm_apid = self.pipeline.get('exclude_tm_apid',
                                                 default=[],
                                                 args=True)
        self.exclude_tc_apid = self.pipeline.get('exclude_tc_apid',
                                                 default=[],
                                                 args=True)

        # Get or create failed_files list from pipeline properties
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get or create processed_files list from pipeline properties
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)

        # get a database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

        # Get tryouts from pipeline properties
        self.tryouts = self.pipeline.get(
            'tryouts', default=[TRYOUTS], create=True)[0]

        # Get wait from pipeline properties
        self.wait = self.pipeline.get(
            'wait', default=[TIME_WAIT_SEC], create=True)[0]

        # Get number of workers to run in parallel
        self.workers = self.pipeline.get(
            'workers', default=[WORKERS], create=True)[0]

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

        # Get SOLO SPICE kernels (SCLK and LSK)
        self.sclk_file = self.pipeline.get(
            'sclk', default=[], create=True)[0]
        self.lsk_file = self.pipeline.get(
            'lsk', default=[None], create=True)[0]
        if not self.sclk_file or not self.lsk_file:
            raise FileNotFoundError(
                'Both sclk_file and lsk_file must be passed as inputs to run L0ToDb!')
        else:
            # Load SPICE with input kernels
            self.spice = load_spice(
                spice_kernels=[self.lsk_file,
                               self.sclk_file]
            )

        # Retrieve --limit keyword value
        self.limit = self.pipeline.get('limit',
                                       default=[SQL_LIMIT],
                                       )[0]

        # Get --param-only optional keyword
        self.param_only = self.pipeline.get('param_only',
                                       default=False,
                                        )
        if self.param_only:
            logger.warning(f'Disable data insertion in tm_log/tc_log table')

        # Initialize data insertion counters
        self.inserted_count = 0

    def run(self):
        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = f'L0ToDb-{self.job_uuid[:8]}'
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

        # Loop over each L0 file in the input list
        for i, current_l0_file in enumerate(self.l0_files):
            logger.info(f'Processing {current_l0_file}    ({n_l0_files - i - 1} remaining)')
            self.current_l0_file = current_l0_file
            self.insert_time = datetime.today()
            # Open file
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
                    try:
                        self.is_predictive_time = not is_sclk_uptodate(
                            current_l0_datetime + timedelta(days=1), l0.attrs['SPICE_KERNELS'])
                    except:
                        self.is_predictive_time = True

                        if self.is_predictive_time:
                            logger.info(f'Predictive UTC times used in {current_l0_file}!')

                    # Initialize existing packet Dataframe
                    self.existing_data = pd.DataFrame()

                    # Get existing packet SHA in database between
                    # l0 start/end times
                    query_start = self.l0_start_time - timedelta(minutes=1)
                    query_end = self.l0_end_time + timedelta(minutes=1)
                    logger.debug(f'Getting existing TmLog.sha between {query_start} and {query_end}')
                    existing_tm = self._get_existing_data(TmLog, TmLog.sha,
                                                            start_time=query_start,
                                                            end_time=query_end)
                    logger.info(f'{existing_tm.shape[0]} TmLog.sha entries found between {query_start} and {query_end}')
                    if existing_tm.shape[0] > 0:
                        self.existing_data = pd.concat(
                            [self.existing_data, existing_tm]).reset_index(drop=True)
                    logger.debug(f'Getting existing TcLog.sha between {query_start} and {query_end}')
                    existing_tc = self._get_existing_data(TcLog, TcLog.sha,
                                                        start_time=query_start,
                                                        end_time=query_end)
                    logger.info(
                        f'{existing_tc.shape[0]} TmLog.sha entries found between {query_start} and {query_end}')
                    if existing_tc.shape[0] > 0:
                        self.existing_data = pd.concat([self.existing_data,
                            existing_tc]).reset_index(drop=True)

                    # Insert input L0 data into database
                    try:
                        inserted_count = self.insert_l0(l0,
                                                        include=self.include,
                                                        exclude=self.exclude)
                    except:
                        self.failed_files.append(self.current_l0_file)
                        logger.exception(f'Insertion has failed for {self.current_l0_file} in task {self.job_id}')
                        break
                    else:
                        logger.info(f'{inserted_count} new packets '
                                    f'inserted for {self.current_l0_file}')
                        self.inserted_count += inserted_count
                        self.processed_files.append(self.current_l0_file)
            except:
                self.failed_files.append(self.current_l0_file)
                logger.exception(f'Cannot open {self.current_l0_file} in task {self.job_id}!')
                break

        logger.info(f'{self.inserted_count} new packets inserted in the database'
                    f' from files: {", ".join(self.processed_files)}')
        if len(self.failed_files) > 0:
            logger.error(f'Insertion has failed for files: {", ".join(self.failed_files)} in task {self.job_id}')

        logger.info(f'Task {self.job_id} has ended correctly')

    def insert_l0(self, l0,
                  packet_type=PACKET_TYPE,
                  include=[],
                  exclude=[]):
        """
        Insert L0 packet data into the database.
        Multiple packet insertions in parallel is possible.

        :param l0: h5.group object containing current L0 packet data
        :param packet_type: Filter by type of packets (TM, TC)
        :param include: List of packets to insert (all by default)
        :param exclude: List of exclude from insertion (empty list by default)
        :return: Number of inserted packets
        """
        inserted_count = 0
        # Build list of packets to insert
        # (Filter if required using include/exclude keywords)
        packet_list = []
        packet_count = 0
        for current_type in packet_type:
            packet_count += int(l0[current_type].attrs['COUNT'])
            packet_list.extend([f'{current_type}/{current_packet}'
                                for current_packet in l0[current_type].keys()
                                if self.is_packet_valid(current_packet,
                                                        include=include,
                                                        exclude=exclude)])

        logger.info(f'{packet_count} packets from {len(l0["TM"].keys())} TM and {len(l0["TC"].keys())} TC found in {self.current_l0_file}   (workers={self.workers})')

        # Loop over each TM/TC packet in L0
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            # Start the load operations and mark each future with its file
            future_to_packet = {executor.submit(self.insert_packet,
                                                l0,
                                                current_packet,
                                                ):
                                current_packet for current_packet in packet_list}

            for i, future in enumerate(concurrent.futures.as_completed(future_to_packet)):
                current_packet = future_to_packet[future]
                try:
                    n_pkt_to_insert = future.result()
                except:
                    logger.exception(f'Bulk insertion has failed for {current_packet} in {self.current_l0_file} for task {self.job_id}!')
                else:
                    logger.info(f'{n_pkt_to_insert} {current_packet} new packets inserted from {self.current_l0_file}')
                    inserted_count += n_pkt_to_insert

        return inserted_count

    def insert_packet(self, l0, packet_name):
        """
        Insert data for the input packet name found in L0 file

        :param l0: h5.group (root) in the L0 file
        :param packet_name: Name of packet for which data must be inserted
        :return: number of packets inserted
        """

        # Get table class
        current_type = packet_name[:2]
        current_model = PIPELINE_TABLES[f'{current_type.lower()}_log']

        # Convert input l0 packet data to pandas.DataFrame
        logger.debug(f'Preparing {packet_name} data for insertion for {self.current_l0_file}')
        current_df = self.packet_to_dataframe(l0, packet_name)

        # Remove already inserted packet data
        # Only keep unique SHA
        if current_df.shape[0] > 0:
            if self.existing_data.shape[0] > 0:
                logger.debug(f'Removing {self.existing_data.shape[0]} {packet_name} data already inserted for {self.current_l0_file}')
                current_df = current_df[
                    ~current_df.sha.isin(self.existing_data.sha)]

        n_pkt_to_insert = current_df.shape[0]
        if n_pkt_to_insert == 0:
            logger.debug(f'There is no new {packet_name} to insert in {self.current_l0_file}')
        else:
            if not self.param_only:
                logger.debug(f'Inserting {n_pkt_to_insert} {packet_name} from {self.current_l0_file}')
                # Only keep tm_log/tc_log columns to insert
                if 'data' not in current_df.columns:
                    columns = get_columns(current_model, remove=[
                                          'id', 'binary', 'data'])
                else:
                    columns = get_columns(current_model, remove=['id', 'binary'])
                # convert to list of dictionaries
                data_to_insert = current_df[columns].to_dict('records')
                # Insert bulk of data
                bulk_insert(self.session, current_model, data_to_insert)
            else:
                logger.debug(f'Inserting {packet_name} packet parameters from {self.current_l0_file}')

            # Insert other tables data
            self._insert_packet_param(packet_name, current_df)

        return n_pkt_to_insert

    def packet_to_dataframe(self, l0, packet_name):
        """
        Convert data of input l0 packet into pandas.DataFrame object.

        :param l0: h5.group containing l0 file packets data
        :param packet_name: name of the packet for which data must be converted
        :return: instance of pandas.DataFrame containing packet data
        """

        # Get packet type (TM or TC)
        packet_type = packet_name[:2]
        data_grp = PACKET_DATA_GROUP[packet_type]

        # Get number of packets
        packet_nsamp = l0[packet_name].attrs['COUNT']

        # Get packet header
        packet_header = load_param(l0[packet_name][
            'packet_header'])
        # Get packet data field header
        data_field_header = load_param(l0[packet_name][
            'data_field_header'])

        # Compute APID of the packet
        packet_apid = compute_apid(packet_header.process_id[0],
                                   packet_header.packet_category[0])

        # If exclude_tm/tc_apid not empty list,
        # then skip packet if its APID in the exclude_tm/tc_apid list
        if packet_type == 'TM' and self.exclude_tm_apid and packet_apid in self.exclude_tm_apid:
            logger.info(f'{packet_name} ({packet_apid}) is in excluded apid list ({self.exclude_tm_apid})')
            return pd.DataFrame()
        elif packet_type == 'TC' and self.exclude_tc_apid and packet_apid in self.exclude_tc_apid:
            logger.info(f'{packet_name} ({packet_apid}) is in excluded apid list ({self.exclude_tc_apid})')
            return pd.DataFrame()

        # Get packet data
        packet_data = load_param(l0[packet_name][
            data_grp])

        # Concatenate packet headers and data dataframes
        packet_df = pd.concat(
            [packet_header, data_field_header, packet_data], axis=1)

        # Use a dict first to store data (to avoid Pandas PerformanceWarning)
        packet_info = dict()

        # Add insertion time
        packet_info['insert_time'] = [self.insert_time] * packet_nsamp

        # Get packet_length
        packet_info['length'] = packet_df['packet_length']

        # Add APID
        packet_info['apid'] = [packet_apid] * packet_nsamp

        # Store packet utc time values
        packet_info['utc_time'] = l0[packet_name]['utc_time'][()]

        # Store packet binary data (as hexa string)
        packet_info['binary'] = l0[packet_name]['binary'][()]

        packet_info['utc_time_is_predictive'] = [
            self.is_predictive_time] * packet_nsamp

        packet_info['palisade_id'] = [
            packet_name.split('/')[-1]] * packet_nsamp
        packet_info['srdb_id'] = [l0[packet_name].attrs[
            'SRDB_ID']] * packet_nsamp
        packet_info['category'] = [l0[packet_name].attrs[
            'PACKET_CATEGORY']] * packet_nsamp

        # Add info to dataframe
        packet_df = pd.concat(
            [packet_df, pd.DataFrame.from_dict(packet_info)],
            axis=1)

        # Convert utc_time byte strings into datetime objects
        packet_df['utc_time'] = packet_df['utc_time'].apply(
            lambda x: datetime.strptime(x.decode('UTF-8')[: -4] + 'Z', TIME_ISO_STRFORMAT))

        # Convert binary from bytes to string
        packet_df['binary'] = packet_df['binary'].apply(
            lambda x: x.decode('UTF-8'))

        # Case of compressed TM packets
        if 'compressed' in l0[packet_name].keys():
            # Be sure that compressed TM have the right
            # PALISADE_ID, SDRB_ID and CATEGORY
            where_compressed = (l0[
                packet_name]['compressed'][()] == 1)
            packet_df.loc[where_compressed, 'srdb_id'] = l0[packet_name].attrs[
                'SRDB_ID_C']
            packet_df.loc[where_compressed, 'category'] = l0[packet_name].attrs[
                'PACKET_CATEGORY_C']
            packet_df.loc[where_compressed,
                          'palisade_id'] = packet_name + '_C'

        if packet_type == 'TM':

            # Init dict (to avoid Pandas PerformanceWarning)
            packet_info = dict()

            # Get cuc_time
            packet_info['cuc_time'] = packet_df['time'].apply(
                lambda x: self.spice.cuc2str(x[0], x[1]))

            # Get obt_time
            packet_info['obt_time'] = packet_df['time'].apply(
                lambda x: self.spice.cuc2datetime(x[0], x[1]))

            # Get packet sync_flag
            packet_info['sync_flag'] = packet_df['time'].apply(
                lambda x: x[2] == 0)

            # Get TM source data
            packet_info['data'] = [null()] * packet_nsamp

            # Add to packet_df dataframe
            packet_df = pd.concat(
                [packet_df, pd.DataFrame.from_dict(packet_info)],
                axis=1)

            try:
                # Only store event and TC ack. TM packets in the
                # database
                apid_to_store = EVENT_TM_APID + TC_ACK_APID + HK_TM_APID
                where_apid = (packet_df['apid'].isin(apid_to_store))
                packet_df.loc[where_apid, ('data')] = packet_df.loc[
                    where_apid, l0[packet_name][data_grp].keys()].to_dict('records')
            except:
                # If failed, assume there is no parameter for this TM
                pass

        elif packet_type == 'TC':

            # Init dict (to avoid Pandas PerformanceWarning)
            packet_info = dict()

            packet_info['unique_id'] = l0[
                packet_name]['unique_id'][()].astype(str)
            packet_info['sequence_name'] = l0[
                packet_name]['sequence_name'][()].astype(str)
            current_tc_state = l0[
                packet_name]['tc_ack_state'][()].astype(str)
            packet_info['tc_acc_state'] = current_tc_state[:, 0]
            packet_info['tc_exe_state'] = current_tc_state[:, 1]

            # Get TC application data
            try:
                packet_info['data'] = packet_df[
                    l0[packet_name][data_grp].keys()].to_dict('records')
            except:
                # If failed, assume there is no parameter for this TC
                pass

            # Add to packet_df dataframe
            packet_df = pd.concat(
                [packet_df, pd.DataFrame.from_dict(packet_info)],
                axis=1)

            # Only store PASSED/FAILED TC in database
            packet_df = packet_df.loc[packet_df[
                'tc_exe_state'].isin(TC_ACK_ALLOWED_STATUS)]

        # If there is no packet anymore to insert, then return empty DataFrame
        if packet_df.shape[0] == 0:
            logger.debug(f'{packet_name} DataFrame is empty in {self.current_l0_file}!')
            return pd.DataFrame()

        # Compute SHA
        packet_info = {'sha': packet_df.apply(
            lambda x: get_packet_sha(x),
            axis=1)}
        # Add SHA to dataframe
        packet_df = pd.concat([packet_df, pd.DataFrame.from_dict(packet_info)],
                              axis=1)

        # Make sure to have unique packets (unique SHA values)
        packet_df.drop_duplicates(subset=['sha'], inplace=True)

        return packet_df

    def is_packet_valid(self, packet_name,
                        include=[],
                        exclude=[]):
        """
        Check if input packet name is
        in the include and/or exclude lists

        :param packet_name:
        :param include: list of packets to include (if empty list, then return True)
        :param exclude: list of packets to exclude (default is empty list)
        :return: True if packet_name is include and/or not in exclude
        """
        is_valid = True
        if packet_name in exclude:
            logger.debug(f'{packet_name} excluded')
            is_valid = False
        if include and packet_name not in include:
            logger.debug(f'{packet_name} not in {include}')
            is_valid = False
        return is_valid

    def _insert_packet_param(self, packet_name, packet_data):
        """
        Insert following data for current packet:
             - sbm_log
             - bia_sweep_log
             - lfr_kcoeff_dump

        It is assumed that input data are not already stored in the
        database.

        :param packet_name: Name of the input packet
        :param packet_data: packet data as a pandas.DataFrame
        :return: number of packets inserted
        """
        n_packet = packet_data.shape[0]
        packet_name = packet_name.split('/')[-1]
        # Set inputs corresponding to input packet
        if packet_name in SBM_LOG_PACKETS:
            logger.info(f'Inserting {packet_name} data into pipeline.sbm_log table')
            model = SbmLog
            columns = get_columns(model, remove=['id', 'retrieved_time'])
            sbm_type = int(packet_name[-1])
            packet_data['sbm_type'] = [sbm_type] * n_packet
            packet_data['selected'] = [False] * n_packet
            packet_data['status'] = ["Unknown"] * n_packet
            packet_data['sbm_qf'] = packet_data[f'HK_RPW_S20_SBM{sbm_type}_QF_D'].astype(float)
            packet_data['sbm_algo'] = packet_data[f'SY_DPU_SBM{sbm_type}_ALGO'].astype(int)
            packet_data['sbm_algo_param'] = packet_data.apply(
                lambda x: self.extract_sbm_algo_param(x),
                axis=1)

            # Compute event occurred time
            occurred_time_key = f'HK_RPW_S20_SBM{sbm_type}_TIME_D'
            packet_data['cuc_time'] = packet_data[occurred_time_key].apply(
                lambda x: self.spice.cuc2str(x[0], x[1]))
            packet_data['obt_time'] = packet_data[occurred_time_key].apply(
                lambda x: self.spice.cuc2datetime(x[0], x[1]))
            packet_data['utc_time'] = packet_data[occurred_time_key].apply(
                self.cuc2utc)

        elif packet_name in BIA_SWEEP_LOG_PACKETS:
            logger.info(f'Inserting {packet_name} data into pipeline.bia_sweep_log table')
            model = BiaSweepLog
            columns = get_columns(model, remove=['id'])
            packet_data['sweep_step'] = packet_data.apply(
                lambda x: CIWT0130TM[int(x['PA_DPU_BIA_SWEEP_PR_CODE'])],
                axis=1,
            )
            packet_data['utc_time'] = packet_data[
                'PA_DPU_BIA_SWEEP_TIME'].apply(self.cuc2utc)
        elif packet_name in LFR_KCOEFF_DUMP_PACKETS:
            logger.info(f'Inserting {packet_name} data into pipeline.lfr_kcoeff_dump table')
            model = LfrKcoeffDump
            columns = get_columns(model, remove=['id'])
            packet_data["kcoeff_pkt_cnt"] = packet_data[
                'PA_LFR_KCOEFF_PKT_CNT'].astype(int)
            packet_data["kcoeff_pkt_nr"] = packet_data[
                'PA_LFR_KCOEFF_PKT_NR'].astype(int)
            packet_data["kcoeff_blk_nr"] = packet_data[
                'PA_LFR_KCOEFF_BLK_NR'].astype(int)
            packet_data["kcoeff_values"] = packet_data.apply(
                lambda x: self.extract_lfr_kcoeff(x),
                axis=1
            )
        else:
            # Otherwise exit insertion normally
            # logger.debug(f'No extra data to insert for {packet_name}')
            return True

        data_to_insert = packet_data[columns].to_dict('records')
        try:
            bulk_insert(self.session, model, data_to_insert)
        except IntegrityError:
            logger.error(f'Bulk insertion in table {model} may be incompleted '
                         f'for {packet_name} in {self.current_l0_file} for task {self.job_id}')
            n_packet = 0
        except:
            logger.exception(f'Bulk insertion in table {model} has failed '
                             f'for {packet_name} in {self.current_l0_file} for task {self.job_id}')
            n_packet = 0

        return n_packet

    def cuc2utc(self, cuc_time, naif_id=NAIF_SOLO_ID):
        """
        Convert input RPW CUC time into UTC time

        :param cuc_time:
        :return: UTC time as returned by SpiceManager.obt2utc() method
        """
        obt_time = self.spice.cuc2obt(cuc_time)
        return self.spice.obt2utc(naif_id, obt_time)

    def _get_existing_data(self, model, fields,
                           start_time=None,
                           end_time=None,
                           to_dict=None):
        """
        Query database to return existing data for a given table

        :param model: class of the table
        :param fields: fields to query
        :param start_time: Filter query by start time
        :param end_time: filter query by end time
        :param to_dict: See pandas.DataFrame.to_dict()
        :return: returned rows (as a DataFrame by default)
        """

        # Get list of existing data in the database
        filters = list()
        # Add start_time/end_time filters (if passed)
        if start_time:
            filters.append(model.utc_time >= str(
                start_time - timedelta(hours=1)))
        if end_time:
            filters.append(model.utc_time <= str(
                end_time + timedelta(hours=1)))

        if fields is None:
            fields = model

        results = query_db(self.session, fields,
                           filters=(and_(*filters) if filters else None),
                           tryouts=self.tryouts,
                           wait=self.wait,
                           limit=self.limit,
                           to_dict=to_dict)

        return results

    def extract_sbm_algo_param(self, current_packet):
        """
        Extract SBM algo parameters from current packet

        :param current_packet: current packat data as a pandas.DataFrame
        :return: list of parameters returned as a JSON string
        """
        current_sbm_algo_param = {
            current_param: current_packet[current_param]
            for current_param in SBM_ALGO_PARAM_LIST[current_packet['sbm_type']]
        }
        # Store SBM algo parameters as a JSON string
        return current_sbm_algo_param

    def extract_lfr_kcoeff(self, packet_data):
        """
        Extract LFR Kcoeff parameters from current TM
        kcoeff data are returned in JSON format, where
        keyword is the frequency index and values are arrays of [LFR_KCOEFF_PARAM_NR, kcoeff_blk_nr] samples

        :param packet_data: current TM packet_data
        :return:json.dumps object
        """
        kcoeffs = {}
        blk_nr = packet_data['kcoeff_blk_nr']
        for current_freq in packet_data['SY_LFR_KCOEFF_FREQUENCY']:
            kcoeffs[current_freq] = ",".join([
                str(packet_data[f'SY_LFR_KCOEFF_{j + 1}'][0:blk_nr])
                for j in range(LFR_KCOEFF_PARAM_NR)])

        return json.dumps(kcoeffs)


def get_l0_files(pipeline):
    try:
        l0_files = pipeline.args.rpw_l0_files
        if not isinstance(l0_files, list):
            l0_files = [l0_files]
        return sorted(l0_files)
    except:
        # If not defined as input argument, then assume that it is already
        # defined as target input
        pass


def load_param(current_group):
    """
    Sub-methods to save h5py.Data array in
    a pandas.DataFrame

    :param current_group:
    :return: DataFrame with h5py.Data
    """
    # Input group must be a h5py.Group object
    if not isinstance(current_group, h5py.Group):
        return pd.DataFrame()

    current_df = dict()
    for key, val in current_group.items():
        current_val = val[()]
        if len(current_val.shape) > 1:
            arr = sparse.coo_matrix(current_val)
            current_df[key] = arr.toarray().tolist()
        else:
            current_df[key] = current_val

    return pd.DataFrame.from_dict(current_df)
