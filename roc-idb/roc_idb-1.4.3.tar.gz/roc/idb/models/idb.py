#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Reference documentation
# ROC-GEN-SYS-NTT-00038-LES_Iss01_Rev02(Mission_Database_Description_Document)

from poppy.core.db.base import Base
from poppy.core.db.non_null_column import NonNullColumn

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    BOOLEAN,
    DOUBLE_PRECISION,
    ENUM,
    INTEGER,
    SMALLINT,
    TIMESTAMP,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, validates, backref

__all__ = [
    'ItemInfo',
    'PacketMapInfo',
    'IdbRelease',
    'PacketMetadata',
    'ParamInfo',
    'PacketHeader',
    'TransferFunction',
]

idb_source_enum = ['PALISADE', 'MIB', 'SRDB']


class IdbRelease(Base):
    """
    The “idb_release” table provides information about the IDB releases stored
    in the database.
    """

    id_idb_release = NonNullColumn(INTEGER(), primary_key=True)

    idb_version = NonNullColumn(String(128), descr='Version of the RPW IDB')

    idb_source = NonNullColumn(
        ENUM(*idb_source_enum, name='idb_source_type', schema='idb'),
        descr='Sources of the IDB. Possible values '
        f'are : {idb_source_enum}',
    )

    mib_version = NonNullColumn(
        String(),
        nullable=True,
        descr='First row of the vdf.dat table including tabs',
    )

    current = NonNullColumn(
        BOOLEAN(),
        descr='"True" = current IDB to be used'
        ' by default, "False" otherwise',
    )

    validity_min = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Minimal date/time of the IDB validity',
    )

    validity_max = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Maximal date/time of the IDB validity',
    )

    __tablename__ = 'idb_release'
    __table_args__ = (
        UniqueConstraint('idb_version', 'idb_source'),
        {'schema': 'idb',},
    )


class ItemInfo(Base):
    """
    The “item_info” table provides general information about RPW TM/TC packets
    and packet parameters defined in the IDB.
    """

    id_item_info = NonNullColumn(INTEGER(), primary_key=True)

    idb_release_id = NonNullColumn(
        INTEGER(), ForeignKey('idb.idb_release.id_idb_release')
    )

    srdb_id = NonNullColumn(
        String(10), nullable=True, descr='SRDB ID of the packet or parameter'
    )

    palisade_id = NonNullColumn(
        String(128),
        nullable=True,
        descr='PALISADE ID of the packet or parameter',
    )

    item_descr = NonNullColumn(
        String(), nullable=True, descr='Description of the packet or parameter'
    )

    idb = relationship(
        'IdbRelease',
        backref=backref('item_info_idb_release', cascade='all,delete-orphan'),
    )

    __tablename__ = 'item_info'
    __table_args__ = (
        UniqueConstraint('srdb_id', 'idb_release_id'),
        {'schema': 'idb',},
    )

    @validates('srdb_id')
    def validate_srdbid(self, key, srdb_id):
        if srdb_id is None:
            pass
        elif srdb_id.startswith('CIW'):
            assert len(srdb_id) == 10
        else:
            assert len(srdb_id) == 8
        return srdb_id


class PacketMetadata(Base):
    """
    The “packet_metadata” table provides information about the SCOS-2000 packet
    description.
    """

    id_packet_metadata = NonNullColumn(INTEGER(), primary_key=True)

    idb_release_id = NonNullColumn(
        INTEGER(), ForeignKey('idb.idb_release.id_idb_release')
    )

    packet_category = NonNullColumn(
        String(256), nullable=True, descr='Packet category'
    )

    idb = relationship(
        'IdbRelease',
        backref=backref(
            'packet_metadata_idb_release', cascade='all,delete-orphan'
        ),
    )

    __tablename__ = 'packet_metadata'
    __table_args__ = {
        'schema': 'idb',
    }


class TransferFunction(Base):
    """
    The "transfer_function" table provides information about the transfer functions.
    """

    id_transfer_function = NonNullColumn(INTEGER(), primary_key=True)

    item_info_id = NonNullColumn(
        INTEGER(), ForeignKey('idb.item_info.id_item_info')
    )

    raw = NonNullColumn(BIGINT(), descr='Raw value of the parameter')

    eng = NonNullColumn(
        String(),
        descr='Engineering value of the parameter after transfer function applies',
    )

    item_info = relationship(
        'ItemInfo',
        backref=backref(
            'transfer_function_item_info', cascade='all,delete-orphan'
        ),
    )

    __tablename__ = 'transfer_function'
    __table_args__ = {
        'schema': 'idb',
    }


class PacketHeader(Base):
    """
    The “packet_header” table provides information about the CCSDS packet
    header description.
    """

    id_packet_header = NonNullColumn(INTEGER(), primary_key=True)
    item_info_id = NonNullColumn(
        INTEGER(), ForeignKey('idb.item_info.id_item_info')
    )
    packet_metadata_id = NonNullColumn(
        INTEGER(),
        ForeignKey('idb.packet_metadata.id_packet_metadata'),
        nullable=True,
    )
    cat_eng = NonNullColumn(
        String(128), descr='Packet category in engineering value'
    )
    cat = NonNullColumn(BIGINT(), descr='Packet category in raw value')
    packet_type = NonNullColumn(
        String(16), descr='Packet type in engineering value'
    )
    byte_size = NonNullColumn(INTEGER(), descr='Packet byte size')
    pid_eng = NonNullColumn(
        String(128), nullable=True, descr='Packet PID in engineering value'
    )
    pid = NonNullColumn(
        BIGINT(), nullable=True, descr='Packet PID in raw value'
    )
    spid = NonNullColumn(BIGINT(), nullable=True, descr='Packet SPID')
    sid_eng = NonNullColumn(
        String(128), nullable=True, descr='Packet SID in engineering value'
    )
    sid = NonNullColumn(
        BIGINT(), nullable=True, descr='Packet SID in raw value'
    )
    service_type_eng = NonNullColumn(
        String(128),
        nullable=True,
        descr='Packet service type in engineering' ' value',
    )
    service_type = NonNullColumn(
        BIGINT(), descr='Packet service type in raw value'
    )
    service_subtype_eng = NonNullColumn(
        String(128),
        nullable=True,
        descr='Packet service subtype in ' 'engineering value',
    )
    service_subtype = NonNullColumn(
        BIGINT(), descr='Packet service subtype in raw value'
    )

    item_info = relationship(
        'ItemInfo',
        backref=backref(
            'packet_header_item_info', cascade='all,delete-orphan'
        ),
    )
    packet_metadata = relationship(
        'PacketMetadata',
        backref=backref(
            'packet_header_packet_metadata', cascade='all,delete-orphan'
        ),
    )

    __tablename__ = 'packet_header'
    __table_args__ = {
        'schema': 'idb',
    }


class ParamInfo(Base):
    """
    The “param_info” table provides information about the CCSDS packet
    parameter description.
    """

    id_param_info = NonNullColumn(INTEGER(), primary_key=True)
    item_info_id = NonNullColumn(
        INTEGER(), ForeignKey('idb.item_info.id_item_info')
    )
    par_bit_length = NonNullColumn(
        SMALLINT(), descr='Bit length of the parameter'
    )
    par_type = NonNullColumn(String(16), descr='Type of parameter')
    par_max = NonNullColumn(
        DOUBLE_PRECISION(), nullable=True, descr='Parameter maximum value'
    )
    par_min = NonNullColumn(
        DOUBLE_PRECISION(), nullable=True, descr='Parameter minimum value'
    )
    par_def = NonNullColumn(
        String(64), nullable=True, descr='Parameter default value'
    )
    cal_num = NonNullColumn(
        String(16), nullable=True, descr='raw-eng. cal. num.'
    )
    cal_val = NonNullColumn(
        BIGINT(), nullable=True, descr='raw-eng. cal. val.'
    )
    par_unit = NonNullColumn(String(8), nullable=True, descr='Parameter unit')
    par_is_editable = NonNullColumn(
        BOOLEAN, nullable=True, descr='Parameter edition possibility'
    )

    transfer_function_id = NonNullColumn(
        INTEGER(), ForeignKey('idb.item_info.id_item_info'), nullable=True
    )

    __tablename__ = 'param_info'
    __table_args__ = {
        'schema': 'idb',
    }

    info = relationship(
        ItemInfo,
        foreign_keys=[item_info_id],
        backref=backref('param_info_item_info', cascade='all,delete-orphan'),
    )
    transfer_function = relationship(
        ItemInfo,
        foreign_keys=[transfer_function_id],
        backref=backref(
            'param_info_transfer_function', cascade='all,delete-orphan'
        ),
    )

    name = association_proxy('info', 'palisade_id')
    description = association_proxy('info', 'item_descr')


class PacketMapInfo(Base):
    """
    The “packet_map_info” table provides mapping information between the packet
    and parameter description.
    """

    id_packet_map_info = NonNullColumn(INTEGER(), primary_key=True)
    packet_header_id = NonNullColumn(
        INTEGER(), ForeignKey('idb.packet_header.id_packet_header')
    )
    param_info_id = NonNullColumn(
        INTEGER(), ForeignKey('idb.param_info.id_param_info')
    )
    block_size = NonNullColumn(INTEGER(), descr='Size of the block')
    group_size = NonNullColumn(INTEGER(), descr='Group size')
    loop_value = NonNullColumn(INTEGER(), descr='Number of loop over blocks')
    byte_position = NonNullColumn(INTEGER(), descr='Byte position')
    bit_position = NonNullColumn(INTEGER(), descr='Bit position')

    __tablename__ = 'packet_map_info'
    __table_args__ = {
        'schema': 'idb',
    }

    packet = relationship(
        'PacketHeader',
        backref=backref('packet_parameters', cascade='all,delete-orphan'),
    )
    parameter = relationship(
        'ParamInfo',
        backref=backref(
            'packet_map_info_param_info', cascade='all,delete-orphan'
        ),
    )

    def __init__(
        self,
        parameter,
        packet,
        byte_position=0,
        bit_position=0,
        group_size=0,
        block_size=0,
        loop_value=0,
    ):
        self.parameter = parameter
        self.packet = packet
        self.byte_position = byte_position
        self.bit_position = bit_position
        self.group_size = group_size
        self.block_size = block_size
        self.loop_value = loop_value
