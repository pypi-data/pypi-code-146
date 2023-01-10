#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

try:
    from poppy.core.db.connector import Connector
    from poppy.core.logger import logger
except:
    print('POPPy framework is not installed!')

try:
    from roc.idb.models.palisade_metadata import PalisadeMetadata
except:
    print('roc.idb plugin is not installed!')

from roc.rpl.packet_parser.packet_cache import PacketCache

__all__ = ['latest_palisade_version',
           'query_palisade_metadata',
           'palisade_metadata']


@Connector.if_connected('MAIN-DB')
def latest_palisade_version():
    """
    Get latest palisade IDB version in the database

    :return: latest palisade IDB version
    """

    # Initialize output
    latest_palisade_version = None

    # get a database session
    session = Connector.manager['MAIN-DB'].session

    # Get/create PacketCache single instance
    packet_cache = PacketCache()

    # Check in packet_cache for latest version
    if packet_cache.latest_palisade_version:
        latest_palisade_version = packet_cache.latest_palisade_version
    else:
        # Get latest version from database
        try:
            logger.debug(f'Querying latest PALISADE IDB version from the database')
            result = session.query(func.max(PalisadeMetadata.palisade_version)).one()
        except:
            logger.exception('Get palisade latest version from the database has failed!')
        else:
            latest_palisade_version = result[0]
            # Store in packet cache
            packet_cache.latest_palisade_version = latest_palisade_version

    return latest_palisade_version


@Connector.if_connected('MAIN-DB')
def query_palisade_metadata(palisade_version=None):
    """
    Method to retrieve PALISADE IDB metadata from database.

    :param palisade_version: Version of the PALISADE IDB
    :return: packet PALISADE metadata as a result of the query
    """

    # Initialize output dict
    palisade_metadata = {}

    # get a database session
    session = Connector.manager['MAIN-DB'].session

    # Get/create PacketCache single instance
    packet_cache = PacketCache()

    # Get palisade version
    if not palisade_version:
        # Return palisade version
        palisade_version = latest_palisade_version()

    if (palisade_version
        and palisade_version in packet_cache.palisade_metadata_query):
        # Check if input parameters are already in the cache for the given palisade_version
        palisade_metadata = packet_cache.palisade_metadata_query[palisade_version]
    elif palisade_version:
        # Else get palisade_metadata from database
        try:
            logger.debug(f'Querying palisade metadata for version {palisade_version}')
            query = session.query(PalisadeMetadata)
            query = query.filter_by(palisade_version=palisade_version)
            results = query.all()
        except NoResultFound:
            logger.exception(f'No palisade metadata found in the database for version {palisade_version}')
        else:
            packet_cache.palisade_metadata_query[palisade_version] = results
            palisade_metadata = results

    return palisade_metadata

def palisade_metadata(palisade_version=None):
        """
        Method to retrieve PALISADE IDB metadata from database.

        :param palisade_version: Version of the PALISADE IDB
        :return: packet PALISADE metadata as a dictionary (keywords are the srdb and palisade id)
        """

        # output dictionary initialization
        palisade_metadata_dict = {}

        # Get palisade version
        if not palisade_version:
            # Return palisade version
            palisade_version = latest_palisade_version()

        # Get packet cache
        packet_cache = PacketCache()
        if (palisade_version and
            palisade_version in packet_cache.palisade_metadata_dict):
            # Check if already in the cache for the given palisade_version
            palisade_metadata_dict = packet_cache.palisade_metadata_dict[palisade_version]
        elif palisade_version:
            # If not in the cache, build palisade_metadata_dict dictionary
            palisade_metadata_query = query_palisade_metadata(palisade_version=palisade_version)

            if palisade_metadata_query:
                # Initialize output dictionary
                palisade_metadata_dict[palisade_version] = {}

                # And fill the output dictionary
                for row in palisade_metadata_query:
                    # Create two keyword entries in the dictionary:
                    # One for the palisade_id (row values are also returned into a dictionary)
                    palisade_metadata_dict[row.palisade_id] = {c.name: getattr(row, c.name) for c in row.__table__.columns}
                    # One for the srdb_id (row values are also returned into a dictionary)
                    palisade_metadata_dict[row.srdb_id] = {c.name: getattr(row, c.name) for c in row.__table__.columns}

                    packet_cache.palisade_metadata_dict[palisade_version] = palisade_metadata_dict

        return palisade_metadata_dict
