#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test load_idb_dump command
"""

from pathlib import Path
import os
from tempfile import gettempdir

from sqlalchemy.orm.exc import NoResultFound
import pytest

from poppy.core.logger import logger
from poppy.core.test import CommandTestCase

from roc.idb.models.idb import IdbRelease
from roc.idb.tools.db import clean_idb

class TestLoadIdbDumpCommand(CommandTestCase):
    @pytest.mark.parametrize(
        'idb_source,idb_version,idb_dump_file,user,password',
        [('MIB', '20200131',
          'https://rpw.lesia.obspm.fr/roc/data/private/devtest/roc/test_data/idb_dump/MIB_20200131/idb_dump.sql',
          os.environ.get('ROC_TEST_USERNAME', 'roctest'),
          os.environ.get('ROC_TEST_PASSWORD', None))],
    )
    def test_load_idb_dump(self, idb_source, idb_version, idb_dump_file, user, password):

        # Build idb_dump local path
        self.local_idb_dump = os.path.join(gettempdir(), os.path.basename(idb_dump_file))

        # Make sure to have a clean database
        #db_downgrade = ['pop', 'db', 'downgrade', 'base', '-ll', 'ERROR']
        #self.run_command(db_downgrade)
        db_upgrade = ['pop', 'db', 'upgrade', 'heads', '-ll', 'ERROR']
        self.run_command(db_upgrade)
        #self.run_command(['pop', 'db', 'execute', '-e', 'SELECT 1', '-ll', 'ERROR'])

        if not password:
            logger.warning(f'Password is not defined for {user}!')

        # Loading IDB dump file
        command = [
            'pop',
            '-ll',
            'ERROR',
            'idb',
            '--force',
            'load_idb_dump',
            '--i',
            gettempdir(),
            '-d',
            idb_dump_file,
            '-a',
            user, password,
        ]

        # Make sure the idb was not already loaded
        if clean_idb(self.session, idb_source, idb_version):
            logger.debug(f'Running command: {" ".join(command)} ...')
            self.run_command(command)

            # Check idb sql dump file exits
            assert os.path.isfile(self.local_idb_dump)

            logger.debug('Querying IDB ...')
            try:
                idb_release_list = (
                    self.session.query(IdbRelease).all()
                )
            except NoResultFound:
                assert False
            else:
                assert True
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

        # Remove downloaded files
        Path(self.local_idb_dump).unlink(missing_ok=True)
