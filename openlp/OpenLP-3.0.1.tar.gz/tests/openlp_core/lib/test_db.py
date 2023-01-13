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
Package to test the openlp.core.lib package.
"""
from pathlib import Path
from sqlite3 import OperationalError as SQLiteOperationalError
from unittest.mock import MagicMock, patch

from sqlalchemy import MetaData
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.pool import NullPool

from openlp.core.lib.db import Manager, delete_database, get_upgrade_op, init_db, upgrade_db


def test_init_db_calls_correct_functions():
    """
    Test that the init_db function makes the correct function calls
    """
    # GIVEN: Mocked out SQLAlchemy calls and return objects, and an in-memory SQLite database URL
    with patch('openlp.core.lib.db.create_engine') as mocked_create_engine, \
            patch('openlp.core.lib.db.MetaData') as MockedMetaData, \
            patch('openlp.core.lib.db.sessionmaker') as mocked_sessionmaker, \
            patch('openlp.core.lib.db.scoped_session') as mocked_scoped_session:
        mocked_engine = MagicMock()
        mocked_metadata = MagicMock()
        mocked_sessionmaker_object = MagicMock()
        mocked_scoped_session_object = MagicMock()
        mocked_create_engine.return_value = mocked_engine
        MockedMetaData.return_value = mocked_metadata
        mocked_sessionmaker.return_value = mocked_sessionmaker_object
        mocked_scoped_session.return_value = mocked_scoped_session_object
        db_url = 'sqlite://'

        # WHEN: We try to initialise the db
        session, metadata = init_db(db_url)

        # THEN: We should see the correct function calls
        mocked_create_engine.assert_called_with(db_url, poolclass=NullPool)
        MockedMetaData.assert_called_with(bind=mocked_engine)
        mocked_sessionmaker.assert_called_with(autoflush=True, autocommit=False, bind=mocked_engine)
        mocked_scoped_session.assert_called_with(mocked_sessionmaker_object)
        assert session is mocked_scoped_session_object, 'The ``session`` object should be the mock'
        assert metadata is mocked_metadata, 'The ``metadata`` object should be the mock'


def test_init_db_defaults():
    """
    Test that initialising an in-memory SQLite database via ``init_db`` uses the defaults
    """
    # GIVEN: An in-memory SQLite URL
    db_url = 'sqlite://'

    # WHEN: The database is initialised through init_db
    session, metadata = init_db(db_url)

    # THEN: Valid session and metadata objects should be returned
    assert isinstance(session, ScopedSession), 'The ``session`` object should be a ``ScopedSession`` instance'
    assert isinstance(metadata, MetaData), 'The ``metadata`` object should be a ``MetaData`` instance'


def test_get_upgrade_op():
    """
    Test that the ``get_upgrade_op`` function creates a MigrationContext and an Operations object
    """
    # GIVEN: Mocked out alembic classes and a mocked out SQLAlchemy session object
    with patch('openlp.core.lib.db.MigrationContext') as MockedMigrationContext, \
            patch('openlp.core.lib.db.Operations') as MockedOperations:
        mocked_context = MagicMock()
        mocked_op = MagicMock()
        mocked_connection = MagicMock()
        MockedMigrationContext.configure.return_value = mocked_context
        MockedOperations.return_value = mocked_op
        mocked_session = MagicMock()
        mocked_session.bind.connect.return_value = mocked_connection

        # WHEN: get_upgrade_op is executed with the mocked session object
        op = get_upgrade_op(mocked_session)

        # THEN: The op object should be mocked_op, and the correction function calls should have been made
        assert op is mocked_op, 'The return value should be the mocked object'
        mocked_session.bind.connect.assert_called_with()
        MockedMigrationContext.configure.assert_called_with(mocked_connection)
        MockedOperations.assert_called_with(mocked_context)


def test_delete_database_without_db_file_name():
    """
    Test that the ``delete_database`` function removes a database file, without the file name parameter
    """
    # GIVEN: Mocked out AppLocation class and delete_file method, a test plugin name and a db location
    with patch('openlp.core.lib.db.AppLocation') as MockedAppLocation, \
            patch('openlp.core.lib.db.delete_file') as mocked_delete_file:
        MockedAppLocation.get_section_data_path.return_value = Path('test-dir')
        mocked_delete_file.return_value = True
        test_plugin = 'test'
        test_location = Path('test-dir', test_plugin)

        # WHEN: delete_database is run without a database file
        result = delete_database(test_plugin)

        # THEN: The AppLocation.get_section_data_path and delete_file methods should have been called
        MockedAppLocation.get_section_data_path.assert_called_with(test_plugin)
        mocked_delete_file.assert_called_with(test_location)
        assert result is True, 'The result of delete_file should be True (was rigged that way)'


def test_delete_database_with_db_file_name():
    """
    Test that the ``delete_database`` function removes a database file, with the file name supplied
    """
    # GIVEN: Mocked out AppLocation class and delete_file method, a test plugin name and a db location
    with patch('openlp.core.lib.db.AppLocation') as MockedAppLocation, \
            patch('openlp.core.lib.db.delete_file') as mocked_delete_file:
        MockedAppLocation.get_section_data_path.return_value = Path('test-dir')
        mocked_delete_file.return_value = False
        test_plugin = 'test'
        test_db_file = 'mydb.sqlite'
        test_location = Path('test-dir', test_db_file)

        # WHEN: delete_database is run without a database file
        result = delete_database(test_plugin, test_db_file)

        # THEN: The AppLocation.get_section_data_path and delete_file methods should have been called
        MockedAppLocation.get_section_data_path.assert_called_with(test_plugin)
        mocked_delete_file.assert_called_with(test_location)
        assert result is False, 'The result of delete_file should be False (was rigged that way)'


def test_skip_db_upgrade_with_no_database(temp_folder):
    """
    Test the upgrade_db function does not try to update a missing database
    """
    # GIVEN: Database URL that does not (yet) exist
    url = 'sqlite:///{tmp}/test_db.sqlite'.format(tmp=temp_folder)
    mocked_upgrade = MagicMock()

    # WHEN: We attempt to upgrade a non-existent database
    upgrade_db(url, mocked_upgrade)

    # THEN: upgrade should NOT have been called
    assert mocked_upgrade.called is False, 'Database upgrade function should NOT have been called'


@patch('openlp.core.lib.db.init_url')
@patch('openlp.core.lib.db.create_engine')
def test_manager_finalise_exception(mocked_create_engine, mocked_init_url, temp_folder, settings):
    """Test that the finalise method silently fails on an exception"""
    # GIVEN: A db Manager object
    mocked_init_url.return_value = f'sqlite:///{temp_folder}/test_db.sqlite'
    mocked_session = MagicMock()

    def init_schema(url):
        return mocked_session

    mocked_create_engine.return_value.execute.side_effect = SQLAlchemyOperationalError(
        statement='vacuum',
        params=[],
        orig=SQLiteOperationalError('database is locked')
    )
    manager = Manager('test', init_schema)
    manager.is_dirty = True

    # WHEN: finalise() is called
    manager.finalise()

    # THEN: vacuum should have been called on the database
    mocked_create_engine.return_value.execute.assert_called_once_with('vacuum')


@patch('openlp.core.lib.db.init_url')
@patch('openlp.core.lib.db.create_engine')
def test_manager_finalise(mocked_create_engine, mocked_init_url, temp_folder, settings):
    """Test that the finalise method works correctly"""
    # GIVEN: A db Manager object
    mocked_init_url.return_value = f'sqlite:///{temp_folder}/test_db.sqlite'
    mocked_session = MagicMock()

    def init_schema(url):
        return mocked_session

    manager = Manager('test', init_schema)
    manager.is_dirty = True

    # WHEN: finalise() is called
    manager.finalise()

    # THEN: vacuum should have been called on the database
    mocked_create_engine.return_value.execute.assert_called_once_with('vacuum')
