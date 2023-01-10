#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

try:
    from poppy.core.generic.cache import CachedProperty
    from poppy.core.logger import logger
except:
    print('POPPy framework is not installed')

from roc.rpl.constants import TYPE_TO_NUMPY_DTYPE, \
    UNKNOWN_UNIQUE_ID, UNKNOWN_ACK_STATE, UNKNOWN_IDB, \
    RECOVERED_PACKETS, UNKNOWN_STATUS

from roc.rpl.exceptions import RPLError, PacketParsingError
from roc.rpl.packet_structure.data import header_foot_offset


__all__ = ['BasePacket']

def _create_packet_dtype(parameters):
    # track parameter names inside packet, because it is possible to have
    # the same parameter appear multiple times in one packet, so for such
    # parameters, raise an error. Behavior changed compared to previous version
    # where a suffix was added to the parameter name
    tracker = set()

    # create the dtype of the array, taking into account the case where
    # we have block of parameters on which to loop
    dtype = []
    in_block = False
    for parameter in parameters:
        # check we are in block
        in_block = parameter.group > 0

        # store the last parameter if not in block
        if not in_block:
            last_parameter = parameter

        # check if the parameter is already present in the dtype
        if parameter.name in tracker:
            raise RPLError(
                (
                    'The parameter {0} is appearing multiple times in a ' +
                    'packet. It seems that the IDB part of the ROC database ' +
                    'is corrupted.'
                ).format(parameter.name)
            )
        else:
            name = parameter.name

        # create the dtype

        if in_block:
            dtype.append(
                (
                    name,
                    TYPE_TO_NUMPY_DTYPE[parameter.type],
                    parameter.counter if parameter.counter != 0 else 0
                )
            )
        else:
            dtype.append((name, TYPE_TO_NUMPY_DTYPE[parameter.type]))

        # add the parameter to say that it is already used
        tracker.add(parameter.name)

    return dtype

class BasePacket(object):

    def reshape_data(self, packet_list):
        """
        Reshape the packet to match the expected dtype/shape

        - Replace None with NaN-filled/zero-filled numpy array
        - Fill remaining space of parameters block with NaNs/zeroes

        :param packet_list: The content of packets organized as a list of tuples
        :return: The reshaped packets
        :rtype: Iterator[tuple]
        """
        #
        for packet in packet_list:
            if packet is None:
                # create an empty packet
                packet_content = [None] * len(self.data_dtype)
            else:
                # use the packet content
                packet_content = packet

            # loop over packet parameters
            for parameter_position, dtype in enumerate(self.data_dtype):

                if packet is None:
                    logger.warning(f'Empty parameter {dtype[0]} in packet {self.name}')
                    # fill the packet appropriate empty numpy array
                    if len(dtype) > 2:
                        # fill the block with NaN like values
                        packet_content[parameter_position] = np.full(dtype[2], np.nan, dtype=dtype[1])
                    else:
                        # add a single NaN like value with the appropriate dtype
                        packet_content[parameter_position] = np.full(1, np.nan, dtype=dtype[1])

                # if it's a parameter block (multiple parameters with the same dtype)
                if len(dtype) > 2:
                    # compute the difference between the current block length and the expected one
                    nan_block_len = dtype[2] - len(packet_content[parameter_position])

                    # if needed, add NaN to fill the remaining space
                    if nan_block_len > 0:
                        parameter_dtype = packet_content[parameter_position].dtype
                        packet_content[parameter_position].resize(dtype[2])
                        packet_content[parameter_position][-nan_block_len:] = np.full(nan_block_len, np.nan,
                                                                                      dtype=parameter_dtype)

            yield tuple(packet_content)

    @property
    def data(self):
        if len(self._data) > 0:
            # ensure that the packet contents have the expected numpy shape/dtype
            return np.array(list(self.reshape_data(self._data)), dtype=self.data_dtype)
        else:
            # return the empty array
            return np.array(self._data)

    @data.setter
    def data(self, data):
        self._data = data

    def add(self):
        """
        To be called each time a packet of this type is detected, to
        get some information from the data if necessary also.
        """
        self.counter += 1

    def initialize(self):
        """
        Initialize some attributes and data for packets.
        """
        # array for the header common to all type of packets
        header_dtype = self._header_dtype()

        # generate the array for the header
        self.header = np.zeros(self.counter, dtype=header_dtype)
        #self.header.fill(np.nan)

        # generate an array to store utc times
        self.utc_time = np.full(self.counter, np.nan, dtype='datetime64[ns]')

        # generate 2D string array to store TC ack acceptance and execution states
        self.tc_ack_state = np.full([self.counter, 2], '', dtype='U16')

        # Generate string array to store TC unique ID
        self.unique_id = np.full(self.counter, UNKNOWN_UNIQUE_ID, dtype='U24')

        # Generate string array to store TC sequence ID
        self.sequence_name = np.full(self.counter, UNKNOWN_UNIQUE_ID, dtype='U24')

        # generate 2D string array to store idb source/version
        self.idb = np.full([self.counter, 2], UNKNOWN_IDB, dtype='U24')

        # generate string array to store binary
        self.binary = np.full(self.counter, '', dtype=object)

        # generate string array to store sha
        self.sha = np.full(self.counter, '', dtype='U64')

        # Generate 1d-element vector with packet compression status
        self.compressed = np.zeros(self.counter, dtype=int)

        # Generate 1d-element vector for packet status and related message (if any)
        self.status = np.full(self.counter, UNKNOWN_STATUS, dtype=int)
        self.message = np.full(self.counter, '', dtype='U64')

        # if this not a packet with data, create empty array
        if self.skip_data:
            self.data = np.array([])
            return

        # create the dtype for the array of the packet
        self.data_dtype = _create_packet_dtype(self.parameters)

        # generate the array for the data
        self.data = [None, ] * self.counter

    @classmethod
    def initialize_all(cls):
        """
        Initialize all instances of packets for their data.
        """
        for instance in cls.manager.instances:
            instance.initialize()

    def _get_header(self, data):
        # get the header
        return data.extract_header()

    def _get_data_header(self, data):
        # extract the data header
        if self.type == 0:
            data_header = data.extract_tm_header()
        elif self.type == 1:
            data_header = data.extract_tc_header()

        # add it to data
        return data_header

    def _get_data(self, data, header, packet_length):
        # get header and footer offsets
        header_offset, foot_offset = header_foot_offset(
            header.packet_type
        )

        # get values from
        values, offset = data.extract_parameters(
            header_offset,
            self.parameters,
        )

        # add the foot offset
        offset += foot_offset

        # get the size of the packet in bytes
        packet_length = (
            header.packet_length if packet_length is None else packet_length
        )

        # compare computed size from expected size of the header
        computed_size = self.byte_size + offset - 7
        if computed_size != packet_length:
            message = (
                'Packet {0} not aligned.\n Expected {1} ' +
                'found {2} bytes. Check IDB version.'
            ).format(
                self.name,
                packet_length,
                computed_size,
            )

            # If the problem is known, recovers the packet
            if not self.name in RECOVERED_PACKETS:
                logger.debug(f'Recovering {self.name}')
            else:
                # else raise en exception
                raise PacketParsingError(message)

        return values

    def extract_data(self, data,
                     packet_length=None,
                     packet_data=None):
        """
        Given the data of the packet, extract it and store it in the
        right format.
        WARNING - Do not forget to update the compressed version of extract_data
        (roc.rpl.compressed.utils.BaseCompressed.extract_data) if you change this method!)

        :param data: Packet binary source/application data to extract
        :param packet_length: packet length
        :param packet_data: dictionary containing packet metadata
        :return: Extracted packet data parameters
        """
        result = None
        try:
            # extract header
            header = self._get_header(data)
            self.header[self.internal_counter] = header.to_tuple()

            # get the type (TM=0, TC=1) of the packet from the first accession
            self.type = self.header['packet_type'][self.internal_counter]

            # extract data header
            data_header = self._get_data_header(data)
            self.data_header[self.internal_counter] = data_header.to_tuple()

            # do not extract data if empty packet
            if not self.skip_data:
                result = self._get_data(
                    data,
                    header,
                    packet_length,
                )

                # store the values
                self._data[self.internal_counter] = result

                # update the dtype
                for idx, dtype in enumerate(self.data_dtype):
                    if isinstance(result[idx], np.ndarray):
                        # compute the max size of parameter blocks
                        block_len = max(len(result[idx]), dtype[2])

                        # and update the dtype
                        self.data_dtype[idx] = dtype[:2] + (block_len,)
        except Exception as e:
            raise e
        finally:
            if packet_data:
                self.utc_time[self.internal_counter] = np.datetime64(packet_data['utc_time'])
                self.tc_ack_state[self.internal_counter, 0] = packet_data.get('ack_acc_state', UNKNOWN_ACK_STATE)
                self.tc_ack_state[self.internal_counter, 1] = packet_data.get('ack_exe_state', UNKNOWN_ACK_STATE)
                self.unique_id[self.internal_counter] = packet_data.get('unique_id', UNKNOWN_UNIQUE_ID)
                self.sequence_name[self.internal_counter] = packet_data.get('sequence_name', UNKNOWN_UNIQUE_ID)
                self.idb[self.internal_counter, 0] = packet_data.get('idb_source', UNKNOWN_IDB)
                self.idb[self.internal_counter, 1] = packet_data.get('idb_version', UNKNOWN_IDB)
                self.binary[self.internal_counter] = packet_data.get('binary')
                self.sha[self.internal_counter] = packet_data.get('sha')
                self.compressed[self.internal_counter] = packet_data.get('compressed', 0)
                self.status[self.internal_counter] = packet_data.get('status', UNKNOWN_STATUS)
                self.message[self.internal_counter] = packet_data.get('message', '')

            # increment counter of packets (gives the possibility to see a hole
            # inside data if a packet have a problem)
            self.internal_counter += 1

        return result

    @CachedProperty
    def data_header(self):

        # create dtype in function of the category
        if self.type == 0:
            data_header_dtype = self._tm_header_dtype()
        elif self.type == 1:
            data_header_dtype = self._tc_header_dtype()

        # create the array for data field header
        data_header = np.empty(
            self.counter,
            dtype=data_header_dtype,
        )
        #data_header.fill(np.nan)

        # return the array
        return data_header

    @staticmethod
    def _header_dtype():
        """
        Create the dtype of the numpy array associated to the common
        header of packets.
        """
        return [
            ('ccsds_version_number', 'uint8'),
            ('packet_type', 'uint8'),
            ('data_field_header_flag', 'uint8'),
            ('process_id', 'uint8'),
            ('packet_category', 'uint8'),
            ('segmentation_grouping_flag', 'uint8'),
            ('sequence_cnt', 'uint16'),
            ('packet_length', 'uint16'),
        ]

    @staticmethod
    def _tm_header_dtype():
        return [
            ('spare_1', 'uint8'),
            ('pus_version', 'uint8'),
            ('spare_2', 'uint8'),
            ('service_type', 'uint8'),
            ('service_subtype', 'uint8'),
            ('destination_id', 'uint8'),
            ('time', TYPE_TO_NUMPY_DTYPE['time']),
        ]

    @staticmethod
    def _tc_header_dtype():
        return [
            ('ccsds_secondary_header_flag', 'uint8'),
            ('pus_version', 'uint8'),
            ('ack_execution_completion', 'uint8'),
            ('ack_execution_progress', 'uint8'),
            ('ack_execution_start', 'uint8'),
            ('ack_acceptance', 'uint8'),
            ('service_type', 'uint8'),
            ('service_subtype', 'uint8'),
            ('source_id', 'uint8'),
        ]

    def __repr__(self):
        return 'Packet[{0}]'.format(self.name)
