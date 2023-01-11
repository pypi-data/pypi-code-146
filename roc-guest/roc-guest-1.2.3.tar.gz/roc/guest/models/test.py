#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Reference documentation
# ROC-GEN-SYS-NTT-00038-LES_Iss01_Rev02(Mission_Database_Description_Document)

"""
Database model for rpw file processing history tables.
"""

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import BIGINT, \
    TIMESTAMP, ENUM

from poppy.core.db.base import Base
from poppy.core.db.non_null_column import NonNullColumn

__all__ = [
     'TestLog',
]


test_state_list = ['OK', 'WARNING', 'ERROR']
test_status_list = ['Running', 'Pending', 'Terminated']

test_state_enum = ENUM(*test_state_list, name='test_state_type', schema='gse')
test_status_enum = ENUM(*test_status_list, name='test_status_type', schema='gse')

class TestLog(Base):
    """
    Class representation of the table for test_log table in the ROC database.
    """


    id_test_log = NonNullColumn(BIGINT(),
                                primary_key=True)
    test_id = NonNullColumn(String(48),
                              descr='uuid of the test',
                              unique=True)
    test_name = NonNullColumn(String(512),
                              descr='Name the test')
    test_sha = NonNullColumn(String(512), nullable=True,
                              descr='SHA of the test')
    test_version = NonNullColumn(String(16), nullable=True,
                                 descr='Data version of the test (if any)')
    test_state = NonNullColumn(test_state_enum, nullable=True,
                                descr='State of the test. Possible values'
                                      f' are: {test_state_list}')
    test_status = NonNullColumn(test_status_enum,
                                descr='Status of the test. Possible values'
                                      f' are: {test_status_list}')
    test_creation_date = NonNullColumn(TIMESTAMP(), nullable=True,
                                       descr='Local date and time of the test '
                                             'creation',
                                       comment='')
    test_insert_date = NonNullColumn(TIMESTAMP(),
                                     descr='Local date and time of the test '
                                           'insertion in the database',
                                     nullable=True)
    test_descr = NonNullColumn(String(512), nullable=True,
                              descr='Description of the test')
    test_author = NonNullColumn(String(512), nullable=True,
                              descr='Author of the test')
    test_launched = NonNullColumn(TIMESTAMP(),
                                   descr='Start time of test')
    test_terminated = NonNullColumn(TIMESTAMP(),
                                 descr='End time of test')
    file_parent = NonNullColumn(String(512), nullable=True,
                                 descr='Parent file (if any)')

    __tablename__ = 'test_log'
    __table_args__ = (
        {
            'schema': 'gse',
        }
    )
