#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.dingo efecs_to_db command and related tasks.
"""
import glob
import os
import shlex
import tarfile
import tempfile

import unittest.mock as mock
from pathlib import Path

from poppy.core.conf import Settings
from poppy.core.logger import logger
from poppy.core.generic.requests import download_file
from poppy.core.test import TaskTestCase, CommandTestCase
from sqlalchemy import inspect

from roc.dingo.models.data import EfecsEvents

# Tests on roc.dingo efecs_to_db command
from roc.dingo.tests.test_dingo import DingoTest


class TestDingoEfecsToDbCommand(CommandTestCase):

    def setup_method(self, method):
        super().setup_method(method)

        # empty the database
        self.session.query(EfecsEvents).delete()
        self.session.flush()

    def teardown_method(self, method):
        super().teardown_method(method)

        # close database
        self.session.close()

    def test_efecs_to_db(self):

        # Name of the command to test
        cmd = 'efecs_to_db'

        # First get test data to insert (i.e. EFECS XML input files)
        test_data_tarball = "test_data.tar.gz"

        test_data_dir = os.environ.get('ROC_TEST_DATA_PATH',
                                       os.path.join(tempfile.tempdir, 'DINGO_TEST_DATA'))
        test_data_dir = os.path.join(test_data_dir, cmd)
        Path(test_data_dir).mkdir(exist_ok=True, parents=True)
        test_data_path = os.path.join(test_data_dir, test_data_tarball)
        if not os.path.isfile(test_data_path):
            # Build test data tarball URL
            test_data_url = "/".join([DingoTest.base_url, cmd, test_data_tarball])
            # Get username/password
            test_dingo = DingoTest()

            download_file(test_data_path,
                          test_data_url,
                          auth=(test_dingo.username, test_dingo.password))

        # Extract tarball
        if tarfile.is_tarfile(test_data_path):
            logger.info(f'Extracting {test_data_path} ...')
            with tarfile.open(test_data_path, 'r:*') as tarball:
                tarball.extractall(path=test_data_dir)
        else:
            raise tarfile.ReadError(f'{test_data_path} is not a valid tarball!')

        # Get list of EFECS files
        input_dir = os.path.join(test_data_dir, 'inputs')
        input_files = sorted(list(glob.glob(os.path.join(input_dir, 'EFECS_M??.xml'))))
        if not input_files:
            raise FileNotFoundError(f'No EFECS XML file found in {input_dir}')

        # initialize the main command
        command_to_test = ' '.join(['pop',
                                    'dingo',
                                    cmd,
                                    '--efecs-files',
                                    ' '.join(input_files),
                                    '-ll', 'INFO'])

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.dingo']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command(shlex.split(command_to_test))

        # Check that test data are in the database
        logger.debug(f'Querying efecs_events table in database ...')
        rows = (
            self.session.query(EfecsEvents)
        ).all()

        assert isinstance(rows, list)
        assert len(rows) == 3378

        # Convert first/last row objects to dictionaries (for debugging)
        #first_row = DingoTest.get_db_values_columns_only(rows[0])
        #last_row = DingoTest.get_db_values_columns_only(rows[-1])
        #print(first_row)
        #print(last_row)

        assert rows[0].name == 'ATT_DIST'
        assert rows[0].ltp_count == 1
        assert rows[-1].name == 'NAV'
        assert rows[-1].ltp_count == 2


