#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Reference documentation: ROC-GEN-SYS-NTT-00038-LES

"""
Database model for tm_log and tc_log tables.
"""

from poppy.core.db.non_null_column import NonNullColumn

from poppy.core.db.base import Base
from sqlalchemy import String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship, validates, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    BOOLEAN,
    DOUBLE_PRECISION,
    ENUM,
    INTEGER,
    SMALLINT,
    TIMESTAMP,
    JSONB,
)

__all__ = [
    'TmLog',
    'TcLog',
    'InvalidPacketLog',
]


class TmLog(Base):
    """
    Class representation of the table for tm_log table in the ROC database.
    """

    id = NonNullColumn(BIGINT(), primary_key=True)
    length = NonNullColumn(INTEGER(), nullable=True,
                           descr='Packet length in bytes')
    category = NonNullColumn(String(512), nullable=True,
                             descr='Packet PALISADE category')
    apid = NonNullColumn(INTEGER(), nullable=True,
                         descr='Packet APID')
    sync_flag = NonNullColumn(BOOLEAN, nullable=True,
                              descr='TM packet time synchronization flag')
    srdb_id = NonNullColumn(String(16), nullable=True,
                            descr='Packet name (SRDB ID)')
    palisade_id = NonNullColumn(String(256), nullable=True,
                                descr='Packet PALISADE ID')
    binary = NonNullColumn(String(), nullable=True,
                           descr='Packet raw binary data (in hexadecimal)')
    data = NonNullColumn(JSONB(), nullable=True,
                           descr='Packet source data (JSON format)')
    sha = NonNullColumn(String(),
                        descr='Packet sha (hexdigest)')
    sequence_cnt = NonNullColumn(BIGINT(), nullable=True,
                                 descr='Packet sequence counter')
    cuc_time = NonNullColumn(String(1024),
                             descr='Packet creation on-board time in CCSDS CUC format "coarse:fine".')
    obt_time = NonNullColumn(TIMESTAMP, nullable=True,
                             descr='Packet creation on-board time in SQL timestamp format".')
    utc_time = NonNullColumn(TIMESTAMP, nullable=True,
                             descr='Packet creation UTC time in SQL timestamp format".')
    utc_time_is_predictive = NonNullColumn(BOOLEAN, nullable=True,
                                           descr='Flag to indicate if Packet creation UTC time is predictive (True) or definitive (False)')
    insert_time = NonNullColumn(TIMESTAMP,
                                descr='Database insertion local time.')

    __tablename__ = 'tm_log'
    __table_args__ = (
        UniqueConstraint('sha'),
        {
            'schema': 'pipeline',
        }
    )


class TcLog(Base):
    """
    Class representation of the table for tc_log table in the ROC database.
    """

    id = NonNullColumn(BIGINT(), primary_key=True)
    length = NonNullColumn(INTEGER(),
                           descr='Packet length in bytes')
    category = NonNullColumn(String(512), nullable=True,
                             descr='Packet PALISADE category')
    apid = NonNullColumn(INTEGER(), nullable=True,
                         descr='Packet APID')
    utc_time = NonNullColumn(TIMESTAMP,
                             descr='Packet execution time in UTC')
    srdb_id = NonNullColumn(String(16),
                            descr='Packet name (SRDB ID)')
    palisade_id = NonNullColumn(String(256),
                                descr='Packet PALISADE ID')
    binary = NonNullColumn(String(), nullable=True,
                           descr='Packet raw binary data (in hexadecimal)')
    data = NonNullColumn(JSONB(), nullable=True,
                           descr='Packet application data (JSON format)')
    sha = NonNullColumn(String(),
                        descr='Packet sha (hexdigest)')
    tc_exe_state = NonNullColumn(String(16), nullable=True,
                                 descr='TC acknowledgment'
                                 'execution completion status')
    tc_acc_state = NonNullColumn(String(16), nullable=True,
                                 descr='TC acknowledgment acceptance status')
    sequence_name = NonNullColumn(String(16), nullable=True,
                                  descr='TC sequence name')
    unique_id = NonNullColumn(String(256), nullable=True,
                              descr='TC unique ID')
    insert_time = NonNullColumn(TIMESTAMP,
                                descr='Database insertion local time.')

    __tablename__ = 'tc_log'
    __table_args__ = (
        UniqueConstraint('sha'),
        {
            'schema': 'pipeline',
        }
    )


class InvalidPacketLog(Base):
    """
    Class representation of the table for invalid_packet_log table in the ROC database.
    """

    id = NonNullColumn(BIGINT(), primary_key=True)
    sha = NonNullColumn(String(),
                        descr='sha256 computed from invalid packet data (hexdigest)')
    srdb_id = NonNullColumn(String(16), nullable=True,
                            descr='Packet name (SRDB ID)')
    apid = NonNullColumn(INTEGER(), nullable=True,
                         descr='Packet APID')
    palisade_id = NonNullColumn(String(256), nullable=True,
                                descr='Packet PALISADE ID')
    utc_time = NonNullColumn(TIMESTAMP, nullable=True,
                             descr='Packet time in UTC')
    data = NonNullColumn(JSONB(), nullable=True,
                           descr='Packet content data (when extraction is possible)')
    status = NonNullColumn(SMALLINT(),
                           descr='Status of the packet (INVALID_PACKET_HEADER = 1, '
                                 'INVALID_PACKET_DATA = 2, OUTSIDE_RANGE_PACKET = 3, '
                                 'INVALID_PACKET_CDATA = 4, INVALID_PACKET_TIME = 5, '
                                 'UNKNOWN_STATUS = -1)')
    comment = NonNullColumn(String(), nullable=True,
                        descr='Additional comment about packet status')
    insert_time = NonNullColumn(TIMESTAMP,
                                descr='Database insertion local time.')

    __tablename__ = 'invalid_packet_log'
    __table_args__ = (
        UniqueConstraint('sha'),
        {
            'schema': 'pipeline',
        }
    )
