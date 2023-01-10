#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from tempfile import gettempdir

from poppy.core.test import CommandTestCase
from roc.idb.models.idb import IdbRelease

from sqlalchemy.exc import NoResultFound

import pytest

from roc.idb.tools.db import clean_idb


class TestClearReleaseCommand(CommandTestCase):
    """
    Test the clear_release command of the roc.idb plugin.
    """
    #@pytest.mark.skip
    @pytest.mark.parametrize(
        'idb_source,idb_version',
        [('MIB', '20200113')],
    )
    def test_clear_release(self, idb_source, idb_version):

        # initialize the commands
        self.install_dir = os.path.join(gettempdir(),
                                        f'idb-{idb_source}-{idb_version}')

        # Run database migrations
        db_upgrade = ['pop', 'db', 'upgrade', 'heads', '-ll', 'ERROR']
        self.run_command(db_upgrade)

        # IDB loading
        idb_loading = [
            'pop',
            'idb',
            'install',
            '--force',
            '--install-dir', self.install_dir,
            '-s',
            idb_source,
            '-v',
            idb_version,
            '--load',
            '-ll',
            'ERROR',
        ]

        # Command to test
        command = [
            'pop',
            'idb',
            'clear_release',
            idb_version,
            '-s',
            idb_source,
            '--force',
            '-ll',
            'ERROR',
        ]

        # Make sure the idb was not already loaded
        if clean_idb(self.session, idb_source, idb_version):
            # Apply IDB loading
            self.run_command(idb_loading)

            # Run command to test
            self.run_command(command)

            # Verify expected behaviour
            try:
                is_found = (
                    self.session.query(IdbRelease)
                    .filter(
                        IdbRelease.idb_version == idb_version,
                        IdbRelease.idb_source == idb_source,
                    )
                    .one()
                )
            except NoResultFound:
                assert True
            else:
                assert False, f'IDB [{idb_source}-{idb_version}] has not been correctly deleted'
        else:
            assert False

    def teardown_method(self, method):
        """
        Method called immediately after the test method has been called and the result recorded.

        This is called even if the test method raised an exception.

        :param method: the test method
        :return:
        """

        # rollback the database
        super().teardown_method(method)

        # Remove IDB folder
        shutil.rmtree(self.install_dir)
