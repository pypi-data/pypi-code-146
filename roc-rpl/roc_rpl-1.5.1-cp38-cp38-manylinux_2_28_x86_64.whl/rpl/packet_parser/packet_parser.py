#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib

try:
    from poppy.core.db.connector import Connector
    from poppy.core.generic.manager import MultipleClassManager
    from poppy.core.generic.metaclasses import SingletonManager
    from poppy.core.generic.signals import Signal
    from poppy.core.logger import logger
    from poppy.core.properties import Properties
    from poppy.core.generic.cache import CachedProperty
except:
    print('POPPy framework is not installed!')

from roc.rpl.constants import VALID_PACKET, INVALID_PACKET_HEADER, INVALID_PACKET_DATA
from roc.rpl.packet_parser.base_packet import BasePacket
from roc.rpl.packet_parser.palisade import palisade_metadata
from roc.rpl.time import Time


__all__ = ['PacketParser']


class PacketParser(object):
    """
    A class to make the parsing of input RPW packets.
    """

    # signal to indicate that a new packet class has been created and that
    # special packets needs to be registered again
    reseted = Signal()

    def __init__(self,
                 idb_version=None,
                 idb_source='MIB',
                 time=Time()):
        """
        Initialize the PacketParser library by loading some information from the
        database.
        """

        # Initialize idb manager
        self.idb_manager = None

        self.idb = (idb_source, idb_version)

        # create the IDB manager
        self.create_idb_manager()

        # signal for errors
        self.extract_error = Signal()

        # Get Time instance
        self.time = time

        palisade_version = (self.idb_version
                            if self.idb_source == 'PALISADE' else None)
        self.palisade_metadata = palisade_metadata(
            palisade_version=palisade_version)

        # List of identified/parsed packets
        self._identified_packets = []
        self._parsed_packets = []

    @property
    def idb_version(self):
        return self._idb_version

    @property
    def idb_source(self):
        return self._idb_source

    @property
    def idb(self):
        return self.idb_manager[(self._idb_source, self._idb_version)]

    @idb.setter
    def idb(self, source_version_tuple):
        # set the idb source/version
        self._idb_source, self._idb_version = source_version_tuple

    @property
    def identified_packets(self):
        return self._identified_packets

    @identified_packets.setter
    def identified_packets(self, values):
        self._identified_packets = values

    @property
    def parsed_packets(self):
        return self._parsed_packets

    @parsed_packets.setter
    def parsed_packets(self, values):
        self._parsed_packets = values

    def reset(self):
        """
        Defines a packet class with its own manager for this instance of the
        PacketParser object.
        """
        self.packet = self._create_packet_class()

        # send signal that a new packet class has been reseted and that some
        # packets may want to register
        self.reseted(self.packet)

        self._identified_packets = []

        self._parsed_packets = []

    @Connector.if_connected('MAIN-DB')
    def create_idb_manager(self):
        """
        Create the IDB manager for easily switching between versions inside the
        PacketParser object.
        """
        # get the manager
        self.idb_manager = Connector.manager['MAIN-DB'].idb_manager

    def add_packet(self, current_packet):
        """
        Add input packet to the Packet class instance of PacketParser
        (Required before parsing data of the packet)

        :param current_packet:
        :return: True if packet has been added, False otherwise
        """

        is_added = False
        try:
            if current_packet.get('status') == VALID_PACKET:
                # Get/create new packet instance (one per palisade_id)
                packet = self.packet(current_packet['palisade_id'])
                # Force srdb_id setting (since compressed packets already
                # initialized has srdb_id = None)
                packet.srdb_id = current_packet['srdb_id']
                # Pass idb_source/idb_version into packet (required for L0
                # writing)
                packet.idb_source = current_packet['idb_source']
                packet.idb_version = current_packet['idb_version']
                packet.category = current_packet['category']
                packet.is_valid = True

                # add the packet
                packet.add()

                is_added = True
            elif current_packet.get('status') == INVALID_PACKET_HEADER:
                logger.warning(f'Packet {current_packet} has an invalid header!')
            elif current_packet.get('status') == INVALID_PACKET_DATA:
                logger.warning(f'Packet {current_packet} has invalid data!')
            else:
                logger.warning(f'Packet {current_packet} is not valid!')
        except:
            logger.exception(f'Packet {current_packet} cannot be added!')

        return is_added

    def identify_packets(self, packet_list,
                         start_time=None,
                         end_time=None,
                         valid_only=True,
                         ):
        """
        Given a list of packets, analyze the binary content
        to identify the packets and allocate space for data.

        :param packet_list: List of
        :param start_time: Only keep packet(s) created/executed after start_time
        :param end_time: Only keep packet(s) created/executed before end_time
        :param valid_only: If True only returns valid packets
        :return: tuple containing list
        """

        # Import identify_packets Cython method
        from roc.rpl.packet_parser.parser.identify_packets import identify_packets

        identified_packets = identify_packets(self, packet_list,
                                start_time=start_time,
                                end_time=end_time)

        if valid_only:
            self.identified_packets = PacketParser.packet_status(identified_packets, status=VALID_PACKET)
        else:
            self.identified_packets = identified_packets

        return self.identified_packets

    def parse_packets(self, packet_list,
                      start_time=None,
                      end_time=None,
                      valid_only=True):
        """
        Parse input RPW TM/TC packets and store their information
        in the packet structure.

        :param packet_list: List of raw binary data of the packets
        :param start_time: Only keep packet(s) created/executed after start_time
        :param end_time: Only keep packet(s) created/executed before end_time
        :param valid_only: If True only return valid packets
        :return: Store results in the PacketParser object
        """
        from roc.rpl.packet_parser.parser.parse_packets import parse_packets

        parsed_packets = parse_packets(self, packet_list,
                      start_time=start_time,
                      end_time=end_time)

        if valid_only:
            self.parsed_packets = self.packet_status(parsed_packets, status=VALID_PACKET)
        else:
            self.parsed_packets = parsed_packets

        return self.parsed_packets

    def _create_packet_class(meta_data):
        class Packet(
            BasePacket,
            metaclass=SingletonManager,
            manager=MultipleClassManager,
        ):
            """
            Create a class for managing packets to parse
            their data, with flexibility to take into account the particularity
            of the TNR/HFR packets with their micro-commands structure.
            """
            # variable for meta information
            meta = Properties()

            def __init__(self, name,
                         srdb_id=None,
                         category=None,
                         idb_version=None,
                         idb_source=None):

                # store the name of the packet (PALISADE_ID)
                self.name = name

                # Store idb_version and idb_source of the packet
                self.idb_version = idb_version
                self.idb_source = idb_source

                # Store SRDB_ID of the packet
                if not srdb_id:
                    srdb_id = meta_data.palisade_metadata[name]['srdb_id']
                self.srdb_id = srdb_id

                # Store packet category
                if not category:
                    category = meta_data.palisade_metadata[name]['packet_category']
                self.category = category

                # init a counter for storing the presence of a packet or not
                self.counter = 0
                self.internal_counter = 0

                # an attribute for storing the data
                self.data = None

                logger.debug(f'Creating packet {self.name}...')

                # store the parameters associated to this packet
                self.parameters = meta_data.idb.packets[self.name].parameters

                # if there are no parameters, we store just headers and skip
                # data extraction
                self.skip_data = False
                if len(self.parameters) <= 0:
                    self.skip_data = True

                # store also the packet size. This is the byte size without
                # accounting for block repetitions. You can consider that it is
                # the size of the packet with only one occurrence of each block
                self.byte_size = meta_data.idb.packets[self.name].byte_size

                # by default, it is not a compressed packet
                self.is_compressed = False

                # Valid packet flag
                self.is_valid = True

        return Packet

    @staticmethod
    def packet_status(packet_list, status=VALID_PACKET, invert=False):
        """
        Return list of packets with a given status.

        :param packet_list: List of input packets to filter
        :param invert: if True apply opposite status filtering
        :return: list of packets with given status
        """
        if invert:
            return [current_packet for current_packet in packet_list
                    if current_packet.get('status') != status]
        else:
            return [current_packet for current_packet in packet_list
                    if current_packet.get('status') == status]


    @staticmethod
    def hex_to_bytes(string):
        """
        Convert an hexadecimal string into a byte array.
        """
        # transform to an array of bytes
        return bytearray.fromhex(string)

    @staticmethod
    def get_packet_sha(packet_data):
        """
        Compute the SHA256 of the input packet.
        TM sha is computed from binary
        TC sha is computed from binary and execution UTC time

        :param packet_data: dictionary containing data of the input packet
        :return: string containing SHA (hexdigest)
        """
        sha = None
        binary = packet_data.get('binary', None)
        type = packet_data.get('type', None)
        if binary and type:
            if type == 'TC':
                utc_time = packet_data.get('utc_time')
                srdb_id = packet_data.get('srdb_id')
                ack_acc_state = packet_data.get('ack_acc_state')
                ack_exe_state = packet_data.get('ack_exe_state')
                srdb_id = packet_data.get('srdb_id')

                raw_sha = hashlib.sha256()
                raw_sha.update(binary.encode('utf-8'))
                raw_sha.update(srdb_id.encode('utf-8'))
                raw_sha.update(ack_acc_state.encode('utf-8'))
                raw_sha.update(ack_exe_state.encode('utf-8'))
                raw_sha.update(utc_time.isoformat().encode('utf-8'))
                sha = str(raw_sha.hexdigest())
            elif type == 'TM':
                raw_sha = hashlib.sha256()
                raw_sha.update(binary.encode('utf-8'))
                sha = str(raw_sha.hexdigest())
            else:
                logger.error(f'Unknown packet type {type} ({packet_data})')
        elif binary:
            # If only binary is known, use it for computing SHA256
            raw_sha = hashlib.sha256()
            raw_sha.update(binary.encode('utf-8'))
            sha = str(raw_sha.hexdigest())
        else:
            logger.error(f'Unknown packet type {type} ({packet_data})')

        return sha

    def get_binary(packet_data):

        binary = None
        if 'binary' in packet_data:
            binary = packet_data['binary']
        elif 'Packet' in packet_data:
            binary = packet_data['Packet']
        elif 'RawBodyData' in packet_data:
            binary = packet_data['RawBodyData']
        else:
            logger.warning('No "binary" keyword in the input packet data')

        return binary
