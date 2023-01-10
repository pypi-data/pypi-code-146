#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from tempfile import gettempdir

from poppy.core.test import CommandTestCase
from roc.idb.models.idb import IdbRelease

import pytest

from roc.idb.tools.db import clean_idb


class TestSetTrangeCommand(CommandTestCase):
    """
    Test the set_trange command of roc.idb plugin.

    """
    #@pytest.mark.skip
    @pytest.mark.parametrize(
        'idb_source,idb_version,validity_min,validity_max',
        [
            ('MIB', '20200113', '2020-01-13T00:00:00', '2050-12-31T23:59:59'),
        ],
    )
    def test_set_trange(
        self, idb_source, idb_version, validity_min, validity_max
    ):

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
            'set_trange',
            idb_version,
            '-s',
            idb_source,
            '--validity-min',
            validity_min,
            '--validity-max',
            validity_max,
            '-ll',
            'ERROR',
        ]

        # apply database migrations
        self.run_command(db_upgrade)

        # Make sure the idb was not already loaded
        if clean_idb(self.session, idb_source, idb_version):
            # Apply IDB loading
            self.run_command(idb_loading)

            # Run command to test
            self.run_command(command)

            # Verify expected behaviour
            try:
                expected_values = (
                    self.session.query(
                        IdbRelease.validity_min, IdbRelease.validity_max
                    )
                    .filter(
                        IdbRelease.idb_version == idb_version,
                        IdbRelease.idb_source == idb_source,
                    )
                    .one()
                )

                time_strformat = '%Y-%m-%dT%H:%M:%S'
                assert (
                    expected_values[0].strftime(time_strformat) == validity_min
                ) and (expected_values[1].strftime(time_strformat) == validity_max)
            except:
                assert False
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
