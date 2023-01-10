#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

import numpy
from poppy.core.generic.cache import CachedProperty
from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from roc.idb.models.idb import (
    PacketHeader,
    ParamInfo,
    ItemInfo,
    IdbRelease,
    PacketMapInfo,
    TransferFunction,
)
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

__all__ = ['IDBManager', 'IDB', 'PacketData']


class IdbManagerError(Exception):
    pass


class PacketData(object):
    """
    A class for storing information and meta data about packets from the IDB.
    """

    def __init__(
        self,
        name,
        byte_size,
        description,
        parameters,
        srdbid,
        spid,
        pid,
        stype,
        subtype,
        sid,
        cat,
    ):
        self.name = name  # palisadeid
        self.srdbid = srdbid
        self.spid = spid
        self.pid = pid
        self.type = stype
        self.subtype = subtype
        self.sid = sid
        self.byte_size = byte_size
        self.description = description
        self.parameters = parameters
        self.category = cat


class IDB(object):
    """
    Class used as a container for the information about packets and parameters
    from the IDB database, with versioning.
    """

    def __init__(self, source, version, session):
        self.source = source
        self.version = version
        self.session = session

    @CachedProperty
    def packets(self):
        """
        Store in a cached property the structure of the defined packets in the
        IBD into a dictionary, whose keys are packets name and the values an
        instance of the :class:`~PacketData` structure.
        """
        from roc.rpl.packet_structure.parameter import Parameter

        # get the version of the IDB to use
        try:
            idb = self.get_idb()
        except NoResultFound:
            raise IdbManagerError(
                f'IDB ({self.source}, {self.version}) was not found in the database'
            )

        # make the query to load all necessary information
        info_alias = aliased(ItemInfo, name='param')
        query = self.session.query(
            ItemInfo.palisade_id,
            info_alias.palisade_id,
            PacketMapInfo.byte_position,
            PacketMapInfo.bit_position,
            PacketMapInfo.group_size,
            PacketMapInfo.block_size,
            PacketMapInfo.loop_value,
            ParamInfo.par_bit_length,
            ParamInfo.par_type,
            ParamInfo.par_max,
        )
        query = query.filter_by(idb=idb)
        query = query.join(
            PacketHeader, ItemInfo.id_item_info == PacketHeader.item_info_id
        )
        query = query.join(PacketMapInfo)
        query = query.join(ParamInfo)
        query = query.join(
            info_alias, info_alias.id_item_info == ParamInfo.item_info_id
        )
        query = query.order_by(
            ItemInfo.palisade_id,
            PacketMapInfo.byte_position,
            PacketMapInfo.bit_position,
        )

        # query data
        data = query.all()

        # query names of packets and their meta data
        query = self.session.query(
            ItemInfo.palisade_id,
            ItemInfo.item_descr,
            PacketHeader.byte_size,
            ItemInfo.srdb_id,
            PacketHeader.spid,
            PacketHeader.pid,
            PacketHeader.service_type,
            PacketHeader.service_subtype,
            PacketHeader.sid,
            PacketHeader.cat,
        )
        query = query.filter_by(idb=idb)
        query = query.join(PacketHeader)
        names = query.all()

        # now we create a map for packets and their list of parameters ordered
        # by byte and bit position, to have the order to work with, and also
        # other information on the data of the parameters.
        packets = {}

        # populate the dictionary of packets
        for (
            name,
            description,
            size,
            srdbid,
            spid,
            pid,
            stype,
            subtype,
            sid,
            cat,
        ) in names:
            packets[name] = PacketData(
                name=name,
                byte_size=size,
                description=description,
                parameters=[],
                srdbid=srdbid,
                spid=spid,
                pid=pid,
                stype=stype,
                subtype=subtype,
                sid=sid,
                cat=cat,
            )

        # now loop over parameters to associate them to the good packet
        for values in data:
            # transform none maximal value to zero
            val = [x for x in values]
            if val[-1] is None:
                val[-1] = 0
            if math.isnan(val[-1]) is True:
                val[-1] = numpy.nan

            logger.debug(f'Creation of parameter {val}')
            packets[values[0]].parameters.append(Parameter(*val[1:]))
        return packets

    @CachedProperty
    def parameters(self):
        # get the version of the IDB to use
        idb = self.get_idb()

        # same for parameters
        query = self.session.query(ItemInfo.palisade_id, ParamInfo,)
        query = query.filter_by(idb=idb)
        query = query.join(ParamInfo)

        # store packet names in a set for fast search
        parameters = query.all()
        return {x[0]: x[1] for x in parameters}

    @CachedProperty
    def transfer_function(self):
        """
        Cached Property for transfer function

        :return: dictionary with transfer function SRDB ID as keyword and list of ('raw', 'eng') as value
        """

        # get the version of the IDB to use
        idb = self.get_idb()

        # same for parameters
        query = self.session.query(
            ItemInfo.srdb_id, TransferFunction.raw, TransferFunction.eng,
        )
        query = query.filter_by(idb=idb)
        query = query.join(TransferFunction)

        # Sort by increasing raw values
        query = query.order_by(TransferFunction.raw)

        # Get transfer function
        tf_entries = query.all()

        # Initialize output dictionary containing set of raw, eng values of each TF SRDB ID
        tf_dict = {}
        for x in tf_entries:
            if x.srdb_id not in tf_dict:
                tf_dict[x.srdb_id] = []
            tf_dict[x.srdb_id].append((x.raw, x.eng))

        return tf_dict

    def get_idb(self):
        logger.debug(f'Getting IDB ({self.source}, {self.version})')
        query = self.session.query(IdbRelease)
        query = query.filter_by(
            idb_source=self.source, idb_version=self.version
        )
        return query.one()

    @staticmethod
    @Connector.if_connected('MAIN-DB')
    def get_version(current_datetime, idb_source='MIB', session=None):
        """
        Get the version of the working IDB for a given time.

        :param current_datetime: Time of the working IDB version to retrieve
        :param idb_source: IDB Source ('MIB', 'SRDB' or 'PALISADE')
        :param session: database session
        :return: string containing the version of the IDB
        """

        if session is None:
            # get a database session
            session = Connector.manager['MAIN-DB'].session

        # Build filters of query
        filters = [IdbRelease.idb_source == idb_source]
        filters.append(current_datetime >= IdbRelease.validity_min)
        filters.append(current_datetime < IdbRelease.validity_max)

        result = []
        try:
            query = session.query(IdbRelease)
            query = query.filters(**filters)
            result = query.one()
        except NoResultFound:
            logger.info(
                f'No IDB version found for {str(current_datetime)} '
                f'and source "{idb_source}"'
            )
        except MultipleResultsFound:
            logger.warning(
                f'Multiple IDB versions found for {str(current_datetime)} '
                f'and source "{idb_source}"!'
            )
        except:
            logger.exception(f'querying {query} has failed!')

        return result


class IDBManager(object):
    """
    A manager for the IDB interface acting like a cache for several IDB
    versions.
    """

    def __init__(self, session):
        """
        Provide a session for the connection with the database when requesting
        information about an IDB version.
        """
        self.session = session

        # init the cache
        self._cache = {}

    def __getitem__(self, source_version_tuple):
        """
        Create the IDB interface if not already present in the cache. If the
        version in argument is in the cache, returns the correct IDB.
        """
        # already loaded, provide information
        if source_version_tuple in self._cache:
            return self._cache[source_version_tuple]

        idb_source, idb_version = source_version_tuple

        idb_source_list = ['MIB', 'SRDB', 'PALISADE']

        if idb_source not in idb_source_list:
            raise Exception(
                f'The idb source shall be one of the following item: {idb_source_list}'
            )

        # create an IDB and add it to the cache
        idb = IDB(idb_source, idb_version, self.session,)
        self._cache[source_version_tuple] = idb
        return idb

    def delete(self, version):
        """
        Delete the version in argument from the manager (the cache) if present.
        """
        if version in self._cache:
            self._cache.pop(version)

    def clear(self):
        """
        Clear the cache of the manager, in case you need to reload things with
        a new state.
        """
        self._cache.clear()
