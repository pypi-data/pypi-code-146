# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2023 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
Package to test the openlp.core.common.db package.
"""
import gc
import os
import pytest
import shutil
import time
from tempfile import mkdtemp

import sqlalchemy

from openlp.core.common.db import drop_column, drop_columns
from openlp.core.lib.db import get_upgrade_op, init_db
from tests.utils.constants import TEST_RESOURCES_PATH


@pytest.fixture
def op():
    tmp_folder = mkdtemp()
    db_path = os.path.join(TEST_RESOURCES_PATH, 'songs', 'songs-1.9.7.sqlite')
    db_tmp_path = os.path.join(tmp_folder, 'songs-1.9.7.sqlite')
    shutil.copyfile(db_path, db_tmp_path)
    db_url = 'sqlite:///' + db_tmp_path
    session, metadata = init_db(db_url)
    upgrade_op = get_upgrade_op(session)
    yield upgrade_op
    session.close()
    session = None
    gc.collect()
    retries = 0
    while retries < 5:
        try:
            if os.path.exists(tmp_folder):
                shutil.rmtree(tmp_folder)
            break
        except Exception:
            time.sleep(1)
            retries += 1


def test_delete_column(op):
    """
    Test deleting a single column in a table
    """
    # GIVEN: A temporary song db

    # WHEN: Deleting a columns in a table
    drop_column(op, 'songs', 'song_book_id')

    # THEN: The column should have been deleted
    meta = sqlalchemy.MetaData(bind=op.get_bind())
    meta.reflect()
    columns = meta.tables['songs'].columns

    for column in columns:
        if column.name == 'song_book_id':
            assert "The column 'song_book_id' should have been deleted."


def test_delete_columns(op):
    """
    Test deleting multiple columns in a table
    """
    # GIVEN: A temporary song db

    # WHEN: Deleting a columns in a table
    drop_columns(op, 'songs', ['song_book_id', 'song_number'])

    # THEN: The columns should have been deleted
    meta = sqlalchemy.MetaData(bind=op.get_bind())
    meta.reflect()
    columns = meta.tables['songs'].columns

    for column in columns:
        if column.name == 'song_book_id' or column.name == 'song_number':
            assert "The column '%s' should have been deleted." % column.name
