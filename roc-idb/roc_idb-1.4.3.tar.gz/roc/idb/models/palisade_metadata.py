#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.db.base import Base
from poppy.core.db.non_null_column import NonNullColumn

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.orm import validates

__all__ = [
    'PalisadeMetadata',
]


class PalisadeMetadata(Base):
    """
    The "palisade_metadata" table provides PALISADE metadata for each IDB packet/parameter

    This table is mainly used to store the mapping between PALISADE and SRDB IDs.
    Moreover, it contains the categories associated with each packet
    """

    id_palisade_metadata = NonNullColumn(INTEGER(), primary_key=True)

    palisade_version = NonNullColumn(
        String(32), descr='Version of the PALISADE IDB'
    )

    srdb_id = NonNullColumn(
        String(10), nullable=True, descr='SRDB ID of the packet or parameter'
    )

    palisade_id = NonNullColumn(
        String(128),
        nullable=True,
        descr='PALISADE ID of the packet or parameter',
    )

    packet_category = NonNullColumn(
        String(128),
        nullable=True,
        descr='The packet category (null for parameters)',
    )

    __tablename__ = 'palisade_metadata'
    __table_args__ = (
        UniqueConstraint('palisade_version', 'srdb_id'),
        {'schema': 'idb'},
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
