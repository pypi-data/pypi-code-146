#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import func

try:
    from poppy.core.db.connector import Connector
    from poppy.core.logger import logger
except:
    print('POPPy framework is not installed')

try:
    from roc.idb.models.idb import PacketHeader, ItemInfo
except:
    print('roc.idb plugin is not installed!')

from roc.rpl.exceptions import InvalidPacketID
from roc.rpl.packet_parser.packet_cache import PacketCache
from roc.rpl.packet_structure.data import Data
from roc.rpl.packet_structure.data import header_foot_offset


__all__ = ['ExtendedData']


class ExtendedData(Data):
    """
    Extended data class which allows to manage the analysis of the packet header
    as well as the identification of the PALISADE ID.
    """

    # Use __new__ instead of __init__ since Data parent class is supposed as immutable class
    # __new__ is then required to introduce idb ExtendedData class argument
    # FIXME - See why roc.rap installation fails when using settings.PIPELINE_DATABASE
    #@Connector.if_connected('MAIN-DB')
    def __new__(cls, data, size, idb):

        instance = super(ExtendedData, cls).__new__(cls, data, size)

        # Get/create PacketCache singleton instance
        instance._cache = PacketCache()

        # Initialize IDB
        if idb in instance._cache.idb:
            instance.idb = instance._cache.idb[idb][0]
            instance.session = instance._cache.idb[idb][1]
        else:
            instance.idb = idb.get_idb()
            instance.session = idb.session
            instance._cache.idb[idb] = (instance.idb, instance.session)

        return instance

    def _get_max_sid(self, header, data_header):
        """
        Get Packet max_sid value

        :param header: packet_header parameters
        :param data_header: packet data_field_header parameters
        :return: max_sid value
        """

        # Return Sid value if already in the cache
        param_tuple = (self.idb,
                       header.packet_type,
                       header.process_id,
                       header.packet_category,
                       data_header.service_type,
                       data_header.service_subtype)
        if param_tuple in self._cache.max_sid:
            return self._cache.max_sid[param_tuple]

        # Else, retrieve value from IDB data in the database

        # The structure_id (sid) is required to fully identify TM packets
        if header.packet_type == 0:
            query_max_sid = self.session.query(func.max(PacketHeader.sid))
            query_max_sid = query_max_sid.join(ItemInfo)
            query_max_sid = query_max_sid.filter_by(idb=self.idb)

            query_max_sid = query_max_sid.filter(
                PacketHeader.cat == header.packet_category)
            query_max_sid = query_max_sid.filter(
                PacketHeader.pid == header.process_id)
            if data_header is not None:
                query_max_sid = query_max_sid.filter(
                    PacketHeader.service_type == data_header.service_type)
                query_max_sid = query_max_sid.filter(
                    PacketHeader.service_subtype == data_header.service_subtype)

            max_sid_value = query_max_sid.one()[0]
            # now we can obtain the palisade name
        else:
            max_sid_value = None

        # add max_sid_value in cache
        self._cache.max_sid[param_tuple] = max_sid_value

        return max_sid_value

    def _get_sid(self, header, data_header, max_sid_value):
        """
        Get Packet sid value

        :param header: packet_header parameters
        :param data_header: packet data_field_header parameters
        :param max_sid_value: max sid value
        :return: sid value
        """

        # get header and footer offsets
        header_offset, _ = header_foot_offset(header.packet_type)

        # For service 1 TM packets, add 4 bytes to the offset
        if data_header.service_type == 1:
            header_offset += 4

        # get the value from data
        if max_sid_value <= 255:
            value = self.u8p(header_offset, 0, 8)
            # logger.warning('8 bits data')

        else:
            value = self.u16p(header_offset, 0, 16)
            # logger.warning('16 bits data')

        return value

    def _get_packet_ids(self, header, data_header):
        """
        Get packet IDs (SRDB_ID and PALISADE ID)

        :param header: packet_header parameters
        :param data_header: packet data_field_header parameters
        :param max_sid_value: max SID value
        :param sid_value:
        :return: tuple (SRDB ID, PALISADE ID) for the current packet
        """

        # Initialize outputs
        srdb_id = None
        palisade_id = None

        # extract the Structure ID (SID) only if the packet is not empty ...

        # get the max possible value for the SID
        max_sid_value = self._get_max_sid(header, data_header)

        # If it is a TM packet and it has a SID, then...
        if max_sid_value is not None:
            # SID is always positive, so if max_sid_value == 0, then ...
            if max_sid_value == 0:
                sid_value = 0
            else:
                # check the first byte of data to get the SID
                sid_value = self._get_sid(header, data_header, max_sid_value)
        else:
            sid_value = None

        # Return SRDB ID and palisade ID if already stored in the cache
        param_tuple = (self.idb,
                       header.packet_category,
                       header.process_id,
                       data_header.service_type,
                       data_header.service_subtype,
                       max_sid_value, sid_value)

        if param_tuple in self._cache.packet_ids:
            return self._cache.packet_ids[param_tuple]

        # Else, build query to retrieve the TM/TC packet srdb and palisade IDs
        query_packet_ids = self.session.query(
            ItemInfo.srdb_id, ItemInfo.palisade_id)
        query_packet_ids = query_packet_ids.filter_by(idb=self.idb)
        query_packet_ids = query_packet_ids.join(PacketHeader)
        query_packet_ids = query_packet_ids.filter(
            PacketHeader.cat == header.packet_category)
        query_packet_ids = query_packet_ids.filter(
            PacketHeader.pid == header.process_id)
        # logger.warning('packet_category: '+str(header.packet_category))
        # logger.warning('process_id: '+str(header.process_id))
        if data_header is not None:
            query_packet_ids = query_packet_ids.filter(
                PacketHeader.service_type == data_header.service_type)
            query_packet_ids = query_packet_ids.filter(
                PacketHeader.service_subtype == data_header.service_subtype)
        # logger.warning('max sid value: '+str(max_sid_value))

        # If it is a TM packet and it has a SID, then...
        if max_sid_value is not None:
            # SID is always positive, so if max_sid_value == 0, then ...
            if max_sid_value == 0:
                sid_value = 0
            else:
                sid_value = self._get_sid(header, data_header, max_sid_value)
            query_packet_ids = query_packet_ids.filter(
                PacketHeader.sid == sid_value)

        try:
            srdb_id, palisade_id = query_packet_ids.all()[0]
        except InvalidPacketID:
            logger.warning('Unknown palisade ID')
        except:
            logger.exception('Querying packet IDs has failed!')
        else:
            # add into the cache
            self._cache.packet_ids[param_tuple] = (srdb_id, palisade_id)
        finally:
            return (srdb_id, palisade_id)

    def get_packet_summary(self,
                           srdb_id=None,
                           palisade_id=None):
        """
        Get a summary (srdb_id, palisade_id, header, data_header) of the packet.

        :return: srdb_id, palisade_id, header, data_header
        """

        # extract the header
        header = self.extract_header()

        # check if there is a data header
        data_header = None
        if header.data_field_header_flag:
            # check if the packet is a TM or a TC
            packet_type = header.packet_type
            if packet_type == 0:
                data_header = self.extract_tm_header()
            elif packet_type == 1:
                data_header = self.extract_tc_header()

            # get srdb and palisade ids
            if srdb_id is None or palisade_id is None:
                srdb_id, palisade_id = self._get_packet_ids(
                    header, data_header)

        else:
            logger.warning('No data header')

        return srdb_id, palisade_id, header, data_header
