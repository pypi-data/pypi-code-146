# -*- coding: utf-8 -*-
import collections
import os
from datetime import datetime

import h5py
import numpy as np
from poppy.core.logger import logger
from roc.idb.parsers.idb_parser import IDBParser
from roc.rpl.constants import VALID_PACKET

from roc.film import L0ProdFailure, MIN_DATETIME, MAX_DATETIME, PACKET_TYPE, TIME_L0_STRFORMAT, TIME_ISO_STRFORMAT
from roc.film.tools.file_helpers import is_packet
from roc.film.tools import valid_data_version, Map, decode

__all__ = ['L0']

class L0:
    # Class to handle L0 file data

    # Class attributes
    h5py_str_dtype = h5py.special_dtype(vlen=str)

    l0_file_prefix = 'solo_L0_rpw'

    L0_FIELDS = {'TM': ['utc_time',
                        'binary',
                        'idb',
                        'compressed',
                        'data_field_header',
                        'packet_header',
                        'source_data'],
                 'TC': ['utc_time',
                        'binary',
                        'idb',
                        'tc_ack_state',
                        'unique_id',
                        'sequence_name',
                        'packet_header',
                        'data_field_header',
                        'application_data']}

    def __init__(self, filepath=None):
        self.filepath = filepath
        self.header = L0.extract_header(filepath)
        self.version = L0.version_from_header(filepath)
        if not self.version:
            self.version = L0.version_from_file(filepath)

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @staticmethod
    def extract_header(filepath):
        if filepath and os.path.isfile(filepath):
            with h5py.File(filepath, 'r') as file:
                header = {key: val for key, val in file.attrs.items()}
        else:
            header = {}
        return header

    @staticmethod
    def version_from_file(filepath):
        """
        Extract data file version from the name of the input file.
        (file naming must comply with Solar Orbiter data standards).

        :param filepath: Path of the file from which data version must be extracted
        :return: data version as a string of the form "XX", where XX are 2 digit integers
        """
        try:
            return os.path.splitext(os.path.basename(filepath))[0].split('_')[4][1:]
        except:
            return ''

    @staticmethod
    def version_from_header(filepath):
        """
        Extract data file version from the header of the input file.
        (file must comply with Solar Orbiter data standards).

        :param filepath: Path of the file from which data version must be extracted
        :return: data version as a string of the form "XX", where XX are 2 digit integers
        """
        try:
            with h5py.File(filepath, 'r') as file:
                return valid_data_version(file.attrs['Data_version'])
        except:
            return ''

    @staticmethod
    def to_hdf5(filepath,
                packet_parser=None,
                metadata={}):
        """
        Given an PacketParser object like and the target on which to put the packets data,
        generate the L0 HDF5 file in format with all the necessary meta information.

        :return:
        """

        if os.path.isfile(filepath):
            action = 'a'
        else:
            action = 'w'

        # Create instance of L0 class
        l0 = L0()

        try:
            with h5py.File(filepath, action) as hdf5:

                # Add l0 root metadata
                for key, val in metadata.items():
                    if key in hdf5.attrs:
                        logger.debug(f'{key} L0 metadata already defined: '
                                     f'{hdf5.attrs[key]}!')
                    hdf5.attrs[key] = val

                # write packets data into the file
                if packet_parser and len(packet_parser.parsed_packets) > 0:
                    l0._to_hdf5(hdf5, packet_parser)

        except:
            logger.exception(f'{filepath} production has failed!')
            raise L0ProdFailure()

        if not L0.is_l0(filepath):
            logger.exception(f'{filepath} not saved correctly!')
            raise L0ProdFailure()

        return filepath

    def _to_hdf5(self, hdf5, packet_parser):
        """
        Given a file name, create an HDF5 file containing the data from the
        different packets provided by the packet_parser object.
        """

        self.hdf5 = hdf5
        self.packet_parser = packet_parser

        # create a group for TM and an other for TC packets
        # and initialize counters
        if 'TM' not in self.hdf5.keys():
            tm = self.hdf5.create_group('TM')
            tm_count = 0
        else:
            tm = self.hdf5['TM']
            tm_count = tm.attrs['COUNT']

        if 'TC' not in self.hdf5.keys():
            tc = self.hdf5.create_group('TC')
            tc_count = 0
        else:
            tc = self.hdf5['TC']
            tc_count = tc.attrs['COUNT']

        # loop over registered packets
        for packet in packet_parser.packet.manager.instances:

            # if the packet is empty do not try to add it
            # same thing if it is a compressed one
            if packet.is_compressed or packet.counter == 0:
                continue

            # Filter by packet.status=VALID_PACKET (if required)
            criterion = packet.status == VALID_PACKET
            new_counter = len(packet.status[criterion])
            if not packet.counter == new_counter:
                logger.warning(f'{packet.name} has {packet.counter - new_counter} invalid packets')
                # Loop over packet attributes
                for key, val in packet.__dict__.items():
                    try:
                        # When attribute has the same length than status
                        # apply filtering
                        packet.__dict__[key] = packet.__dict__[key][criterion]
                    except:
                        pass
                # Update packet counter
                packet.counter = len(packet.status)

            # send the packet to the good type
            logger.debug('Insert {0} into L0 file'.format(packet))
            if packet.type == 0:
                # call the method to store into hdf5 for each packet
                tm_count += self.packet_to_hdf5(packet, tm)
            elif packet.type == 1:
                # same for tc
                tc_count += self.packet_to_hdf5(packet, tc, tc=True)

        # Set TM / TC packet counters
        tm.attrs['COUNT'] = tm_count
        tc.attrs['COUNT'] = tc_count

        return tm, tc

    def packet_to_hdf5(self, packet, group, tc=False):
        """
        Put a packet instance and the associated data into the provided HDF5 group.
        """
        # create a group of the name of the packet
        if packet.name not in group.keys():
            packet_group = group.create_group(packet.name)
        else:
            packet_group = group[packet.name]

        # Store some metadata of current packet
        # as H5 datasets in L0 packet group
        # Mapping dict of the attributes to add
        attrs_dict = {'SRDB_ID': (packet.__dict__, 'srdb_id'),
                      'PACKET_CATEGORY': (packet.__dict__, 'category')}
        self.add_packet_attrs(packet, attrs_dict, packet_group)

        # Store number of packets
        try:
            if 'COUNT' in packet_group.attrs:
                packet_count = packet_group.attrs['COUNT']
            else:
                packet_count = 0

            packet_group.attrs['COUNT'] = packet_count + packet.counter
        except:
            logger.warning(f'No counter found for packet {packet.name}')

        # packet_header, data_field_header, source_data ou application_data

        # inside it, create groups for the packet_header,
        # data_field_header and the source_data/application_data
        self._packet_to_hdf5('packet_header', packet.header, packet_group)
        self._packet_to_hdf5('data_field_header',
                             packet.data_header, packet_group)

        if tc:
            self._packet_to_hdf5('application_data', packet.data, packet_group)

            # Add TC specific info:
            # array of Ack. TC acceptance/execution state
            self._packet_to_hdf5('tc_ack_state',
                                 packet.tc_ack_state.astype(
                                     self.h5py_str_dtype),
                                 packet_group)

            # unique ID as a string
            self._packet_to_hdf5('unique_id',
                                 packet.unique_id.astype(self.h5py_str_dtype),
                                 packet_group)

            # sequence name ID as a string
            self._packet_to_hdf5('sequence_name',
                                 packet.sequence_name.astype(
                                     self.h5py_str_dtype),
                                 packet_group)

        else:
            self._packet_to_hdf5('source_data', packet.data, packet_group)

        # Add binary
        self._packet_to_hdf5('binary',
                             packet.binary.astype(self.h5py_str_dtype),
                             packet_group)

        # Add idb_source and idb_version
        self._packet_to_hdf5('idb',
                             packet.idb.astype(self.h5py_str_dtype),
                             packet_group)

        # save utc time as string
        # Note: datetime64 could be also saved as int64
        self._packet_to_hdf5('utc_time',
                             np.datetime_as_string(packet.utc_time, timezone='UTC').astype(
                                 self.h5py_str_dtype),
                             packet_group)

        # Save compression status (only if any compressed packet)
        if not np.all(packet.compressed == 0) or 'compressed' in packet_group.keys():
            self._packet_to_hdf5('compressed',
                                 packet.compressed,
                                 packet_group)
            # Mapping dict of the attributes to add for compressed packets
            packet_name_c = packet.name + '_C'
            attrs_dict = {'SRDB_ID_C': (self.packet_parser.palisade_metadata[packet_name_c],
                                        'srdb_id'),
                          'PACKET_CATEGORY_C': (self.packet_parser.palisade_metadata[packet_name_c],
                                                'packet_category')}
            self.add_packet_attrs(packet, attrs_dict, packet_group)

        # Return number of packets
        return packet_group.attrs['COUNT']

    def _packet_to_hdf5(self, name, data, group):
        """
        The recursive function to set a given numpy data array into the HDF5
        group.
        """
        # if the dtype of the data doesn't have a name, we have a
        # dataset
        if data.dtype.names is None:
            # If dataset already exists, update it
            if name in group.keys():
                # If already defined, then append new data to l0 dataset
                dataset = group[name]
                old_dset_shape = list(dataset.shape)
                # First resize dataset along axis 0 (i.e., time) to append new
                # samples
                dataset.resize(dataset.shape[0] + data.shape[0], axis=0)
                # if it is a 2 dim array ...
                if len(data.shape) == 2:
                    # Only resize axis 1 dataset if the size of input data
                    # is greater than the current one
                    # Check the delta_size to decide if resizing is required
                    delta_size = data.shape[1] - dataset.shape[1]
                    if delta_size > 0:
                        # If delta size is positive, it means that we need to increase
                        # the size of dataset array along axis 1
                        logger.debug(f'Resizing axis 1 of {name} from {dataset.shape[1]} to {dataset.shape[1] + delta_size}')
                        dataset.resize(dataset.shape[1] + delta_size, axis=1)

                    # Than save 2D array data
                    dataset[old_dset_shape[0]:, :data.shape[
                        1]] = data[:, :data.shape[1]]

                else:
                    # Saving data along axis 0 if dim = 1
                    dataset[old_dset_shape[0]:] = data[:]
            else:
                # Else if the dataset does not exist, create it and insert input data
                # Make sure that dataset is resizable (None == unlimited)
                # to allow future insertion of data
                if len(data.shape) == 1:
                    maxshape = (None,)
                elif len(data.shape) == 2:
                    maxshape = (None, None)

                # Create and fill new chunked dataset
                dataset = group.create_dataset(name, data.shape, dtype=data.dtype,
                                               maxshape=maxshape, chunks=True)
                dataset[:] = data

        # in this case, this is a part of the record array, so treating
        # it as a group
        else:
            # create a group
            if name not in group.keys():
                new_group = group.create_group(name)
            else:
                new_group = group[name]

            # loop over fields in the record array
            for field in data.dtype.names:
                self._packet_to_hdf5(field, data[field], new_group)

    def add_packet_attrs(self, packet, ds_dict, packet_group):
        """
        Add H5 attributes to a given packet

        :param packet: RPL Packet class instance
        :param ds_dict: dictionary containing attributes to add.
                        Keyword must be the name of H5 attribute to add in the L0.
                        Value must be a tuple with the dictionary and the corresponding key to get value
        :param packet_group: H5 packet group
        :return: List of True/False depending of the adding result
        """
        is_added = []
        for attr_name, packet_key in ds_dict.items():
            try:
                packet_group.attrs[attr_name] = packet_key[0][packet_key[1]]
            except:
                logger.warning(f'No "{packet_key[1]}" for {packet.name}')
                is_added.append(False)
            else:
                is_added.append(True)

        return is_added

    @staticmethod
    def is_l0(filepath):
        """
        Check if input file has a valid RPW L0 HDF5 file name.

        :param filepath: Path of the file to check
        :return: True if input file exists and has a valid RPW L0 file name, False otherwise
        """
        return os.path.isfile(filepath) and L0.l0_file_prefix in os.path.basename(filepath)

    @staticmethod
    def set_attr(l0_attrs, metadata):
        """
        Can be used to set the value of L0 HDF5 attributes.

        :param metadata: attributes to be set
        :type metadata: dict
        :param l0_attrs: attributes of the HDF5 file group
        :type l0_attrs: HDF5 group attrs
        :return: None
        """

        for key, val in metadata.items():
            if key in l0_attrs:
                logger.debug(f'{key} L0 attribute already defined: '
                             f'Replace by {l0_attrs[key]}')
            l0_attrs[key] = val

    @staticmethod
    def l0_to_packet_list(files,
                          include=[],
                          exclude=[],
                          start_time=MIN_DATETIME,
                          end_time=MAX_DATETIME,
                          packet_type=PACKET_TYPE,
                          no_header=False,
                          no_data=False,
                          ascending=True,
                          to_dataframe=False):
        """
        Parse list of input RPW L0 files
        and return list of TM/TC packets

        :param files: list of input RPW L0 files
        :param include: list of TM/TC packets to include (all included by default.). Use PALISADE_ID.
        :param exclude: list of TM/TC packets to exclude. Use PALISADE_ID.
        :param packet_type: Filter by type of packet (TM or TC).
        :param start_time: Filter by start_time (datetime object).
        :param end_time: Filter by end_time (datetime object).
        :param no_header: Do not parse and return packet header parameters (PACKET_HEADER and DATA_FIELD_HEADER).
        :param no_data: Do not parse and return packet data parameters (SOURCE_DATA or APPLICATION_DATA)
        :param ascending: Sort TM/TC packet list by ascending creation/execution times (True by default).
        :param to_dataframe: Return packet data as Pandas.DataFrame object instead of list
        :return: list of TM/TC packet data found in the input L0 files. (One row contains a dictionary with packet data).
        """

        import pandas as pd
        import scipy.sparse as sparse

        def load_param(current_group, current_df):

            if not isinstance(current_group, h5py.Group):
                return False

            for key, val in current_group.items():
                current_val = val[()]
                if len(current_val.shape) > 1:
                    arr = sparse.coo_matrix(current_val)
                    current_df[key] = arr.toarray().tolist()
                else:
                    current_df[key] = current_val

            return True

        packet_data = {}

        total_sample_num = 0
        file_num = len(files)
        for file_idx, file in enumerate(files):

            logger.debug(f'Opening {file}... ({file_idx + 1}/{file_num})')
            with h5py.File(file, 'r') as l0:
                for current_type in packet_type:
                    for current_packet in l0[current_type].keys():

                        if ((current_packet in exclude) or
                                (include and current_packet not in include)):
                            logger.debug(f'{current_packet} excluded')
                            continue
                        #else:
                        #    logger.debug(f'{current_packet} included')

                        # Initialize DataFrame instance for the current packet
                        current_df = pd.DataFrame()

                        current_times = decode(l0[current_type][
                            current_packet]['utc_time'][()])

                        current_binary = decode(l0[current_type][
                            current_packet]['binary'][()])

                        # Get number of
                        current_nsamp = len(current_times)
                        current_counter = l0[current_type][
                            current_packet].attrs['COUNT']
                        try:
                            assert current_nsamp == current_counter
                        except:
                            logger.warning(f'Something goes wrong for {current_packet} COUNT in {file}')
                        else:
                            logger.debug(f'{current_counter} {current_packet} found in {file}')

                        # Store packet utc time values
                        current_df['utc_time'] = current_times
                        # Convert utc_time strings into datetime objects
                        current_df['utc_time'] = current_df['utc_time'].apply(
                            lambda x: datetime.strptime(x, TIME_L0_STRFORMAT))

                        # Convert binary hexa packet data to string hexa
                        current_df['binary'] = current_binary
                        current_df['palisade_id'] = [
                            current_packet] * current_nsamp
                        current_df['srdb_id'] = [l0[current_type][current_packet].attrs[
                            'SRDB_ID']] * current_nsamp
                        current_df['category'] = [l0[current_type][current_packet].attrs[
                            'PACKET_CATEGORY']] * current_nsamp

                        # Get IDB source/version
                        current_idb = l0[current_type][
                            current_packet]['idb'][()]
                        current_df['idb_source'] = decode(current_idb[:, 0])
                        current_df['idb_version'] = decode(current_idb[:, 1])

                        # Case of compressed TM packets
                        if 'compressed' in l0[current_type][current_packet].keys():
                            # Add compressed array to the current dataframe
                            current_df['compressed'] = l0[current_type][
                                current_packet]['compressed'][()]

                            # Be sure that compressed TM have the right
                            # PALISADE_ID, SDRB_ID and CATEGORY
                            where_compressed = (current_df.compressed == '1')
                            current_df.loc[where_compressed, 'srdb_id'] = l0[current_type][current_packet].attrs[
                                'SRDB_ID_C']
                            current_df.loc[where_compressed, 'category'] = l0[current_type][current_packet].attrs[
                                'PACKET_CATEGORY_C']
                            current_df.loc[where_compressed,
                                           'palisade_id'] = current_packet + '_C'

                        if current_type == 'TM':
                            data_grp = 'source_data'
                        elif current_type == 'TC':
                            data_grp = 'application_data'
                            current_df['unique_id'] = decode(l0[current_type][
                                current_packet]['unique_id'][()])
                            current_df['sequence_name'] = decode(l0[current_type][
                                current_packet]['sequence_name'][()])
                            current_tc_state = l0[current_type][
                                current_packet]['tc_ack_state'][()]
                            current_df['tc_acc_state'] = decode(current_tc_state[:, 0])
                            current_df['tc_exe_state'] = decode(current_tc_state[:, 1])

                        if not no_header:
                            load_param(l0[current_type][current_packet][
                                'packet_header'], current_df)
                            load_param(l0[current_type][current_packet][
                                'data_field_header'], current_df)

                        if not no_data:
                            load_param(l0[current_type][current_packet][
                                data_grp], current_df)

                        # Filter by start_time/end_time
                        current_mask = (current_df['utc_time'] >= start_time)
                        current_mask = current_mask & (
                            current_df['utc_time'] <= end_time)
                        current_df = current_df.loc[current_mask]
                        # Get actual number of samples
                        current_nsamp = len(current_df.index)

                        # Increment total number of samples counter
                        total_sample_num += current_nsamp

                        if current_packet not in packet_data:
                            packet_data[current_packet] = current_df
                        else:
                            packet_data[current_packet] = pd.concat([packet_data[
                                current_packet], current_df])


                        logger.debug(
                            f'{current_nsamp} samples extracted from {current_packet} (total samples extracted: {total_sample_num})')

                        # Free memory
                        current_df = None

        logger.info(f'RPW packet loading completed '
                    f'({total_sample_num} samples extracted)')

        if to_dataframe:
            logger.debug('Return packet data as a Pandas DataFrame object')
            return packet_data

        logger.info('Converting to list of RPW packets...')
        packet_list = [None] * total_sample_num
        counter = 0
        for key, val in packet_data.items():
            current_samples = val.to_dict('Records')
            current_nsamp = len(current_samples)
            packet_list[counter:counter + current_nsamp] = current_samples
            counter += current_nsamp
            perc = '{: .2f}'.format(100.0 * counter / total_sample_num)
            logger.debug(f'{current_nsamp} {key} samples added to the packet list ({perc}% completed)')

        # Sort by ascending packet creation times
        if ascending:
            logger.info(
                'Sorting packet list by ascending packet creation time...')
            key = 'utc_time'
            sorted_packet_list = sorted(packet_list, key=lambda i: i[key])
        else:
            sorted_packet_list = packet_list

        return sorted_packet_list

    @staticmethod
    def is_valid_packet(packet):
        """
        Check if input packet content is valid.

        :param packet: dictionary containing packet data (as returned by l0_to_packet_list())
        :return: True if valid, False otherwise
        """

        for mandatory_key in ['palisade_id', 'srdb_id',
                              'utc_time', 'binary',
                              'category', 'idb_version',
                              'idb_source']:
            if not packet.get(mandatory_key):
                return False

        if packet['palisade_id'].startswith('TM'):
            pass
        elif packet['palisade_id'].startswith('TC'):
            for mandatory_key in ['unique_id',
                                  'sequence_name',
                                  'tc_acc_state',
                                  'tc_exe_state']:
                if not packet.get(mandatory_key):
                    return False
        else:
            return False

        return True

    @staticmethod
    def l0_to_raw(l0_file_list,
                  expected_packet_list=[],
                  start_time=None,
                  end_time=None,
                  increasing_time=True):
        """
        Extract packet data from a list of L0 files.

        :param l0_file_list: List of l0 files from which packet data must be extracted
        :param expected_packet_list: List of expected packet to extract (if empty, then extract all packets). The palisade IDs must be given.
        :param start_time: start time filter value (datetime object)
        :param end_time: end time filter value (datetime object)
        :param increasing_time: If True, sort output packet list by increasing time
        :return: a list containing extracted header info + packet parameters
        """

        # Initialize output list
        output_packet_list = []

        # Make sure that input l0 file list is a list
        if not isinstance(l0_file_list, list):
            l0_file_list = [l0_file_list]

        if len(l0_file_list) == 0:
            logger.warning('Input list of L0 file is empty!')
            return {'packet_list': []}

        # loop over L0 file(s) to get data and save packet data
        for i, l0_file in enumerate(l0_file_list):
            logger.debug(f'Parsing {l0_file}...')
            with h5py.File(l0_file, 'r') as l0:

                # Get L0 time minimum/maximum
                l0_time_min = datetime.strptime(
                    l0.attrs['TIME_MIN'], TIME_ISO_STRFORMAT)
                l0_time_max = datetime.strptime(
                    l0.attrs['TIME_MAX'], TIME_ISO_STRFORMAT)
                # If start_time/end_time passed, then filter L0 data outside
                # time range
                if start_time and l0_time_max < start_time:
                    logger.info(f'{l0_file} time max. is less than {start_time}, skip it')
                    continue

                if end_time and l0_time_min > end_time:
                    logger.info(f'{l0_file} time min. is greater than {end_time}, skip it')
                    continue

                file_id = l0.attrs['File_ID']
                creation_date = l0.attrs['Generation_date']

                # if expected_packet_list not passed as an input
                # then load all packets
                if not expected_packet_list:
                    l0_expected_packet_list = []
                    if 'TM' in l0.keys():
                        l0_expected_packet_list.extend(list(l0['TM'].keys()))
                    if 'TC' in l0.keys():
                        l0_expected_packet_list.extend(list(l0['TC'].keys()))
                else:
                    l0_expected_packet_list = expected_packet_list

                # Loop over list of expected packets
                for expected_packet in l0_expected_packet_list:

                    if expected_packet.startswith('TM'):
                        current_type = 'TM'
                        current_data_group = 'source_data'
                    elif expected_packet.startswith('TC'):
                        current_type = 'TC'
                        current_data_group = 'application_data'
                    else:
                        logger.warning(f'Unknown packet type: {expected_packet}')
                        continue

                    # Check that packet(s) are found in the present l0 file
                    if not is_packet(expected_packet, l0[current_type]):
                        logger.debug(f'No {expected_packet} packet found in {l0_file}')
                        # if not continue
                        continue

                    # Get L0 data for current packet
                    current_packet = l0[current_type][expected_packet]

                    # Get packet data
                    current_packet_data = current_packet[current_data_group]

                    # Get list of TC execution UTC times
                    utc_time_list = decode(current_packet['utc_time'][()])

                    # Get number of packets
                    current_packet_num = len(utc_time_list)

                    # Loop over packets in l0
                    logger.debug(f'Extracting {current_packet_num} '
                                 f'{expected_packet} packets...')
                    for j, utc_time in enumerate(utc_time_list):

                        try:
                            # Put current packet parameter values into a
                            # dictionary
                            parameters = {
                                name: current_packet_data[name][j]
                                for name in current_packet_data.keys()
                            }
                        except:
                            # if packet_data is a dataset (i.e. no application_data/source_data parameter)
                            # then provide an empty dictionary
                            parameters = {}

                        # Get current packet header
                        current_packet_header = L0.l0_packet_to_dotdict(
                            l0[current_type][expected_packet]['packet_header'], j)

                        # Get current packet data field header
                        current_packet_data_header = L0.l0_packet_to_dotdict(
                            l0[current_type][expected_packet]['data_field_header'], j)

                        # Compute packet APID
                        current_apid = IDBParser.compute_apid(current_packet_header['process_id'],
                                                              current_packet_header['packet_category'])

                        # Get some packet attributes in L0
                        try:
                            srdb_id = current_packet.attrs['SRDB_ID']
                            packet_cat = current_packet.attrs[
                                'PACKET_CATEGORY']
                        except:
                            logger.warning(f'Attributes missing in {l0_file}!')
                            srdb_id = None
                            packet_cat = None

                        # Get compression flag
                        try:
                            current_compressed = current_packet[
                                'compressed'][:]
                        except:
                            current_compressed = None

                        # Add current packet parameters to lists
                        # utc_time, name of packet and parameters
                        current_packet_fields = {
                            'utc_time': L0.l0_utc_time_to_dt(utc_time),
                            'palisade_id': expected_packet,
                            'srdb_id': srdb_id,
                            'data': parameters,
                            'type': current_type,
                            'category': packet_cat,
                            'binary': current_packet['binary'][j],
                            'idb_source': current_packet['idb'][j][0],
                            'idb_version': current_packet['idb'][j][1],
                            'length': current_packet_header['packet_length'] + 7,
                            'apid': current_apid,
                            'header': current_packet_header,
                            'data_header': current_packet_data_header,
                            'compressed': current_compressed,
                        }

                        # If TC or TM, add also specific attributes
                        if current_type == 'TC':
                            current_packet_fields[
                                'unique_id'] = current_packet['unique_id'][j]
                            current_packet_fields['sequence_name'] = current_packet[
                                'sequence_name'][j]
                            current_packet_fields['ack_acc_state'] = current_packet[
                                'tc_ack_state'][j][0]
                            current_packet_fields['ack_exe_state'] = current_packet[
                                'tc_ack_state'][j][1]
                        elif current_type == 'TM':
                            current_packet_fields[
                                'sync_flag'] = current_packet_data_header['time'][2]
                            current_packet_fields['obt_time'] = f'1/' \
                                f"{current_packet_data_header['time'][0]}:" \
                                f"{current_packet_data_header['time'][1]}"

                        output_packet_list.append(current_packet_fields)

        output_packet_num = len(output_packet_list)
        if output_packet_num == 0:
            logger.info(f'No packet has been returned')
            return {'packet_list': []}
        else:
            logger.debug(f'{output_packet_num} packets returned')
            # Sort list by increasing time
            if increasing_time:
                output_packet_list = sorted(
                    output_packet_list,
                    key=lambda
                    k: k['utc_time'])

        # FIXME - Strange output combining data from one L0
        #  (l0_time_min, l0_time_max, file_id, creation_date)
        #   and for several L0 (packet_list)
        l0_data = {
            'time_min': l0_time_min,
            'time_max': l0_time_max,
            'file_id': file_id,
            'creation_date': creation_date,
            'packet_list': output_packet_list
        }

        return l0_data

    @staticmethod
    def filter_l0_files(l0_file_list, start_time=None, end_time=None):
        """
        Keep only RPW L0 files between start_time and end_time
        from the input list of files.

        :param l0_file_list: list of input L0 files to filter
        :param start_time: datetime object for start time filtering
        :param end_time: datetime object for end time filtering
        :return: list of L0 files between start_time and end_time
        """

        # Initialize output list
        output_file_list = []

        # Make sure that input l0 file list is a list
        if isinstance(l0_file_list, str):
            l0_file_list = [l0_file_list]

        if len(l0_file_list) == 0:
            logger.warning('Input list of L0 file is empty!')
            return output_file_list

        # loop over L0 file(s) to filter by time range
        for i, l0_file in enumerate(l0_file_list):
            with h5py.File(l0_file, 'r') as l0:

                # Get L0 time minimum/maximum
                l0_time_min = datetime.strptime(
                    l0.attrs['TIME_MIN'], TIME_ISO_STRFORMAT)
                l0_time_max = datetime.strptime(
                    l0.attrs['TIME_MAX'], TIME_ISO_STRFORMAT)
                # If start_time/end_time passed, then filter L0 data outside
                # time range
                if start_time and l0_time_max < start_time:
                    # logger.debug(f'{l0_file} time max. is less than
                    # {start_time}, skip it')
                    continue

                if end_time and l0_time_min > end_time:
                    # logger.debug(f'{l0_file} time min. is greater than
                    # {end_time}, skip it')
                    continue

                output_file_list.append(l0_file)

        return output_file_list

    @staticmethod
    def l0_packet_to_dotdict(group, k):
        """
        For a given packet return a given packet group
        (packet_header, data_field_header) as an object where
         group content is accessible with dot separator

        :param group: Group to return as an object
        :param i: Index of the packet in the L0
        :return: resulting object
        """
        output_dict = Map()
        for key in group.keys():
            output_dict[key] = group[key][k]

        return output_dict

    @staticmethod
    def l0_utc_time_to_dt(l0_utc_time):
        """
        Convert input time value as stored in the utc_time dataset of a RPW L0 HDF5 file
        into datetime object.

        :param l0_utc_time: input L0 utc time value to convert
        :return: corresponding datetime object
        """
        # Nanoseconds not supported by datetime and must removed from input l0
        # utc time
        return datetime.strptime(decode(l0_utc_time)[:-4] + 'Z',
                                 TIME_ISO_STRFORMAT)

    @staticmethod
    def count_packets(l0_file,
                      tm=True,
                      tc=True):
        """
        Count number of Packet elements in the input RPW L0 file.

        :param l0_file: input RPW L0 file
        :param tm: If True, count TM packets
        :param tc: If True, count TC packets
        :return: number of Packets in the input file
        """
        # Initialize output
        packet_num = 0

        with h5py.File(l0_file, 'r') as l0:
            tm_num = l0['TM'].attrs['COUNT']
            tc_num = l0['TC'].attrs['COUNT']

            if not tm and not tc:
                logger.warning(
                    'At least tm and/or tc keyword must be set to True')
                return packet_num

            if tm:
                packet_num += tm_num
            if tc:
                packet_num += tc_num

            return packet_num

    @staticmethod
    def order_by_utc(l0_file,
                     unique=False,
                     update_time_minmax=False):
        """
        Order data in an input RPW L0 HDF5 file
        by packet creation UTC times.

        :param l0_file: Path of the L0 file to update
        :param unique: If True, only keep unique packets utc times values
        :param update_time_minmax: If True, update values of TIME_MIN/TIME_MAX
                                 root attributes with actual values.
        :return:
        """
        # Internal function to sort a dataset according to input indices
        def _sort_dataset(group, item, unique_idx, sorted_idx):
            # If not dtype.names, then we have a dataset
            if isinstance(group[item], h5py.Dataset):
                # Take dataset array from L0
                current_dataset = group[item]

                # Only update dataset if no empty data
                if current_dataset.shape[0] > 0:
                    # Extract sorted/unique dataset array
                    sorted_dataset = (current_dataset[()][unique_idx])[
                        sorted_idx]

                    # If there duplicate values, then resize L0 HDF5 dataset
                    if sorted_dataset.shape[0] < current_dataset.shape[0]:
                        delta_shape = current_dataset.shape[
                            0] - sorted_dataset.shape[0]
                        current_dataset.resize(current_dataset.shape[
                                               0] - delta_shape, axis=0)

                    # Then update it with sorted indices
                    current_dataset[...] = sorted_dataset

            # Otherwise it is a group
            else:
                for field in group[item].keys():
                    _sort_dataset(group[item], field, unique_idx, sorted_idx)

        # Initialize time_min / time_max
        time_min = '9999-12-31T23:59:59.999999999Z'
        time_max = '0000-01-01T00:00:00.000000000Z'

        # Open L0 file
        with h5py.File(l0_file, 'a') as l0:

            # Loop over TM/TC groups in L0
            for cat in ['TM', 'TC']:
                # Check that TM/TC group exists
                if cat in l0.keys():
                    # Loop over each TM packet in L0
                    new_packet_count = []
                    for packet_name in l0[cat].keys():

                        # Get packet utc_time values
                        original_utc_time = l0[cat][
                            packet_name]['utc_time'][()]

                        if unique:
                            # If unique input keyword is True,
                            if cat == 'TM':
                                # then if TM
                                # apply the uniqueness of the tuple (packet,
                                # binary) over packets in l0 file
                                binary = l0[cat][
                                    packet_name]['binary'][()]
                                binary, unique_idx = np.unique(
                                    binary, return_index=True)
                                utc_time = original_utc_time[unique_idx]
                            else:
                                # then if TC
                                # apply the uniqueness of the tuple (packet,
                                # utc_time) over packets in l0 file
                                utc_time, unique_idx = np.unique(
                                    original_utc_time, return_index=True)

                            # Update packet COUNT attribute
                            l0[cat][packet_name].attrs[
                                'COUNT'] = utc_time.shape[0]
                            new_packet_count.append(utc_time.shape[0])

                        else:
                            unique_idx = np.arange(original_utc_time.shape[0])

                        if cat == 'TM' and utc_time.shape[0] != original_utc_time.shape[0]:
                            duplicated_times = [item for item, count in collections.Counter(
                                original_utc_time).items() if count > 1]
                            logger.warning(f'There are duplicated times ({duplicated_times}) for packet {packet_name} in {l0_file}!')

                            # Code block to get indices of duplicated elements
                            # duplicated_indices = []
                            # for current_dtime in duplicated_times:
                            #    duplicated_indices.extend([i for i,c in enumerate(original_utc_time) if c == current_dtime])

                        # Get sorted indices of UTC times
                        sorted_idx = np.argsort(utc_time)

                        # Loop over each item in the current packet group
                        for item in L0.L0_FIELDS[cat]:
                            if item in l0[cat][packet_name].keys():
                                _sort_dataset(
                                    l0[cat][packet_name], item, unique_idx, sorted_idx)

                        if np.min(utc_time):
                            time_min = min([decode(np.min(utc_time)), time_min])
                        if np.max(utc_time):
                            time_max = max([decode(np.max(utc_time)), time_max])

                    # If unique is True, then update the COUNT attribute of
                    # TM/TC group
                    if unique:
                        l0[cat].attrs['COUNT'] = sum(new_packet_count)

            if update_time_minmax:
                # Save microsecond resolution
                l0.attrs['TIME_MIN'] = time_min[:-4] + 'Z'
                l0.attrs['TIME_MAX'] = time_max[:-4] + 'Z'
