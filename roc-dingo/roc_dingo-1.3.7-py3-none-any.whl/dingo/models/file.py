#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Reference documentation
# ROC-GEN-SYS-NTT-00038-LES_Iss01_Rev02(Mission_Database_Description_Document)

"""
Database model for rpw file processing history tables.
"""

from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import \
    BIGINT, INTEGER, TIMESTAMP, ENUM, BOOLEAN

from poppy.core.db.base import Base
from poppy.core.db.non_null_column import NonNullColumn

__all__ = [
    'FileLog',
]


# File lists
FILE_STATE_LIST = ['OK', 'WARNING', 'ERROR']
FILE_STATUS_LIST = ['Pended', 'Terminated', 'InProgress', 'Locked', 'Failed']
FILE_LEVEL_LIST = [
    'CAL', 'TC', 'TM', 'SK', 'L0', 'HK', 'L1',
    'BIA', 'L1R', 'L2', 'L3', 'LL01']

# file_action_list = ['Process', 'Reprocess', 'Lock', 'Unlock', 'Delete']

file_state_enum = ENUM(
    *FILE_STATE_LIST, name='file_state_list')
file_status_enum = ENUM(
    *FILE_STATUS_LIST, name='file_status_list')
file_level_enum = ENUM(
    *FILE_LEVEL_LIST, name='file_level_list')

ParentsFileLog = Table(
    'parents_file_log',
    Base.metadata,
    Column('id_parent', INTEGER, ForeignKey('pipeline.file_log.id')),
    Column('id_child', INTEGER, ForeignKey('pipeline.file_log.id')),
    schema='pipeline'
)


class FileLog(Base):
    """
    Class representation of the table for file_log table in the ROC database.
    """

    id = NonNullColumn(
        BIGINT(),
        primary_key=True)
    sha = NonNullColumn(
        String(64),
        nullable=True,
        descr='SHA256 of the file')
    basename = NonNullColumn(
        String(512),
        descr='Basename of the file',
        unique=True)
    product = NonNullColumn(
        String(512),
        descr='Basename of the file without extension and version number')
    version = NonNullColumn(
        String(16),
        descr='Data version of the file')
    state = NonNullColumn(
        file_state_enum,
        descr=f'State of the file. Possible values are: {FILE_STATE_LIST}')
    status = NonNullColumn(
        file_status_enum,
        descr=f'Status of the file. Possible values are: {FILE_STATUS_LIST}')
    level = NonNullColumn(
        file_level_enum,
        descr=f'Level of the file. Possible values are: {FILE_LEVEL_LIST}')
    creation_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Local date and time of the file creation',
        comment='')
    insert_time = NonNullColumn(
        TIMESTAMP(),
        descr='Local date and time of the file insertion in the database',
        nullable=True)
    descr = NonNullColumn(
        String(512),
        nullable=True,
        descr='Description of the file')
    author = NonNullColumn(
        String(512),
        nullable=True,
        descr='Author of the file')
    dirname = NonNullColumn(
        String(512),
        nullable=True,
        descr='Relative path of the file directory (from data root base)')
    url = NonNullColumn(
        String(512),
        nullable=True,
        descr='URL of the file in the HTTPS server')
    size = NonNullColumn(
        BIGINT(),
        nullable=True,
        descr='Size of the file in kilobytes')
    start_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Start time of file')
    end_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='End time of file')
    validity_start = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Start time of validity range (for CAL files)')
    validity_end = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='End time of validity range (for CAL files)')
    dataset_id = NonNullColumn(
        String(512),
        nullable=True,
        descr='Dataset ID in the ROC database')
    is_archived = NonNullColumn(
        BOOLEAN,
        default=False,
        descr='True if file has been archived at ESAC')
    is_delivered = NonNullColumn(
        BOOLEAN,
        default=False,
        descr='True if file has been delivered ESAC')
    public_filename = NonNullColumn(
        String(512),
        descr='Public filename of the file delivered to ESAC',
        nullable=True,
        unique=False)
    public_dirname = NonNullColumn(
        String(512),
        descr='Public dirname of the file delivered to ESAC',
        nullable=True,
        unique=False)
    is_latest = NonNullColumn(
        BOOLEAN,
        default=False,
        descr='True if the version is the latest one')
    is_removed = NonNullColumn(
        BOOLEAN,
        default=False,
        descr='True if the file has been removed from the file directory')
    error_log = NonNullColumn(
        String(),
        nullable=True,
        descr='Log message when an error occured during insertion')
    to_update = NonNullColumn(
        BOOLEAN,
        default=False,
        descr='True if file has to be updated by DINGO')

    parents = relationship(
        'FileLog',
        secondary=ParentsFileLog,
        primaryjoin=ParentsFileLog.c.id_child == id,
        secondaryjoin=ParentsFileLog.c.id_parent == id,
        backref='children',
        cascade='all, delete',
    )

    __tablename__ = 'file_log'
    __table_args__ = (
        {
            'schema': 'pipeline',
        }
    )

    def as_dict(self):
        # init the dictionnary
        log_file_dict = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
        }

        # delete some useless columns
        log_file_dict.pop('id')
        log_file_dict.pop('insert_time')

        # datetime formatting
        fields = ['creation_time', 'start_time', 'end_time',
                  'validity_start', 'validity_end']
        for f in fields:
            time = log_file_dict[f]
            if time is not None:
                log_file_dict[f] = time.isoformat()

        log_file_dict['parents'] = []
        for p in self.parents:
            log_file_dict['parents'].append(p.basename)

        log_file_dict['parents'].sort()

        return log_file_dict
