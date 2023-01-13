#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Reference documentation: ROC-GEN-SYS-NTT-00038-LES

"""
Database model for packet_log table.
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
)

__all__ = [
     'PacketLog',
]
class PacketLog(Base):
    """
    Class representation of the table for packet_log table in the ROC database.
    """

    id_packet_log = NonNullColumn(BIGINT(), primary_key=True)
    length = NonNullColumn(INTEGER(),
                            descr='Packet length in bytes')
    type = NonNullColumn(String(8),
                         descr='Packet type (TC or TM)')
    category = NonNullColumn(String(512),
                         descr='Packet PALISADE category')
    apid = NonNullColumn(INTEGER(), nullable=True,
                         descr='Packet APID')
    sync_flag = NonNullColumn(BOOLEAN, nullable=True,
                                    descr='TM packet time synchronization flag')
    utc_time = NonNullColumn(TIMESTAMP,
                             descr='Packet creation/execution UTC time')
    srdb_id = NonNullColumn(String(16),
                         descr='Packet name (SRDB ID)')
    palisade_id = NonNullColumn(String(256),
                          descr='Packet PALISADE ID')
    binary = NonNullColumn(String(),
                             descr='Packet raw binary data (in hexadecimal)')
    sha = NonNullColumn(String(), nullable=True,
                             descr='Packet sha (hexdigest)')
    idb_version = NonNullColumn(String(128), nullable=True,
                          descr='IDB version used to identify packet')
    idb_source = NonNullColumn(String(128), nullable=True,
                          descr='IDB source used to identify packet')
    creation_time = NonNullColumn(String(1024), nullable=True,
                                    descr='Packet creation time in CCSDS CUC format coarse:fine. For TM only.')
    ack_exe_state = NonNullColumn(String(16), nullable=True,
                                             descr='Packet acknowledgment'
                                                   'execution completion status. For TC only.')
    ack_acc_state = NonNullColumn(String(16), nullable=True,
                                   descr='TC packet acknowledgment acceptance status. For TC only.')
    sequence_name = NonNullColumn(String(16), nullable=True,
                         descr='Sequence name. For TC only.')
    unique_id = NonNullColumn(String(256), nullable=True,
                         descr='Unique ID. For TC only.')
    insertion_time = NonNullColumn(TIMESTAMP,
                                    descr='Packet insertion local time.')

    __tablename__ = 'packet_log'
    __table_args__ = (
        UniqueConstraint('utc_time', 'srdb_id'),
        {
            'schema': 'gse',
        }
    )

class InvalidPacketLog(Base):
    """
    Class representation of the table for invalid_packet_log table in the ROC database.
    """

    id_invalid_packet_log = NonNullColumn(BIGINT(), primary_key=True)
    idb_version = NonNullColumn(String(128), nullable=True,
                          descr='IDB version used to analyze packet')
    idb_source = NonNullColumn(String(128), nullable=True,
                          descr='IDB source used to analyze packet')
    apid = NonNullColumn(INTEGER(), nullable=True,
                         descr='Packet APID')
    binary = NonNullColumn(String(),
                             descr='Packet raw binary data (in hexadecimal)')
    comment = NonNullColumn(String(), nullable=True,
                          descr='Additional comment about why packet is invalid')
    insertion_time = NonNullColumn(TIMESTAMP,
                                    descr='Packet insertion local time.')
    utc_time = NonNullColumn(TIMESTAMP,
                             descr='Packet creation/execution UTC time', nullable=True)
    srdb_id = NonNullColumn(String(16),
                         descr='Packet name (SRDB ID)', nullable=True)
    sha = NonNullColumn(String(), nullable=True,
                             descr='Packet sha (hexdigest)')

    __tablename__ = 'invalid_packet_log'
    __table_args__ = (
        UniqueConstraint('binary'),
        {
            'schema': 'gse',
        }
    )
