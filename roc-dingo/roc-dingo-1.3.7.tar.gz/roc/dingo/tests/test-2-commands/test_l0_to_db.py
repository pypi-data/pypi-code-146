#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.dingo l0_to_db command and related tasks.
"""
import datetime
import glob
import os
import shlex
import tarfile
import tempfile

import pytest
import unittest.mock as mock
from pathlib import Path

from poppy.core.conf import Settings
from poppy.core.logger import logger
from poppy.core.generic.requests import download_file
from poppy.core.test import TaskTestCase, CommandTestCase
from sqlalchemy import inspect

from roc.dingo.models.packet import TmLog, TcLog
from roc.dingo.models.data import SbmLog, BiaSweepLog

from roc.dingo.tests.test_dingo import DingoTest


class TestDingoL0ToDbCommand(CommandTestCase):

    def setup_method(self, method):
        super().setup_method(method)

        # empty the database
        self.session.query(TmLog).delete()
        self.session.query(TcLog).delete()
        self.session.query(SbmLog).delete()
        self.session.query(BiaSweepLog).delete()
        self.session.flush()

    def teardown_method(self, method):
        super().teardown_method(method)

        # close database
        self.session.close()

    @pytest.mark.parametrize('idb_source,idb_version, exclude_tm_apid', [
        ('MIB', '20200131', '1212 1228 1244 1260 1276 1292 1204 1220 1236 1252 1269 1300'),
    ])
    def test_l0_to_db(self, idb_source, idb_version, exclude_tm_apid):

        # Command name
        cmd = 'l0_to_db'

        # First get test data to insert (i.e. L0 input file(s))
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

            logger.info(f'Downloading {test_data_url}')
            download_file(test_data_path,
                          test_data_url,
                          auth=(test_dingo.username, test_dingo.password))
        else:
            logger.info(f'{test_data_path} already found, skip downloading')

        # Extract tarball
        if tarfile.is_tarfile(test_data_path):
            logger.debug(f'Extracting {test_data_path} ...')
            with tarfile.open(test_data_path, 'r:*') as tarball:
                tarball.extractall(path=test_data_dir)
        else:
            raise tarfile.ReadError(f'{test_data_path} is not a valid tarball!')

        # Get list of input files
        input_dir = os.path.join(test_data_dir, 'inputs')
        input_file = list(glob.glob(os.path.join(input_dir, 'solo_L0_rpw*.h5')))
        if not input_file:
            raise FileNotFoundError(f'No input L0 file found in {input_dir}!')
        elif len(input_file) > 1:
            raise ValueError('/inputs must contain only one L0 test file!')
        else:
            # Make sure to have only file
            input_file = input_file[0]

        # Check that SPICE kernels are present in ./data/spice_kernels folder
        spice_kernels_dir = DingoTest.get_spice_kernel_dir()
        if not os.path.isdir(spice_kernels_dir):
            raise FileNotFoundError(f'No SPICE kernel set found in {spice_kernels_dir}!')
        else:
            # Get latest version of SCLK et LSK SPICE kernels
            sclk = max((Path(spice_kernels_dir) / 'sclk').glob(
                'solo_ANC_soc-sclk_*.tsc'), key=os.path.getctime)
            lsk = max((Path(spice_kernels_dir) / 'lsk').glob(
                'naif*.tls'), key=os.path.getctime)

        # initialize the main command
        command_to_test = ' '.join(['pop',
                                    'dingo',
                                    '--idb-source',
                                    idb_source,
                                    '--idb-version',
                                    idb_version,
                                    '--sclk',
                                    str(sclk),
                                    '--lsk',
                                    str(lsk),
                                    cmd,
                                    '-l0',
                                    input_file,
                                    '--exclude-tm-apid',
                                    exclude_tm_apid,
                                    '-ll', 'INFO'])

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.dingo']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            logger.debug(f'Running : {command_to_test}')
            self.run_command(shlex.split(command_to_test))

        # Check that TM data are in the database
        logger.debug(f'Querying pipeline.tm_log table in database ...')
        rows = (
            self.session.query(TmLog)
                .order_by(TmLog.utc_time)
                .all()
                )

        assert isinstance(rows, list)
        assert len(rows) == 205

        # Convert first/last row objects to dictionaries (for debugging)
        #first_row = DingoTest.get_db_values_columns_only(rows[0])
        #last_row = DingoTest.get_db_values_columns_only(rows[-1])
        #print(first_row)
        #print(last_row)

        assert rows[0].palisade_id == 'TM_DPU_EVENT_LE_DPU_AHB'
        assert rows[0].utc_time == datetime.datetime(2022, 5, 27, 0, 11, 9, 979413)
        assert rows[-1].palisade_id == 'TM_TDS_TC_EXE_SUCCESS'
        assert rows[-1].utc_time == datetime.datetime(2022, 5, 28, 0, 2, 0, 619423)

        # Check that TC data are in the database
        logger.debug(f'Querying pipeline.tc_log table in database ...')
        rows = (
            self.session.query(TcLog)
                .order_by(TcLog.utc_time)
                .all()
                )

        assert isinstance(rows, list)
        assert len(rows) == 19

        # Convert first/last row objects to dictionaries (for debugging)
        #first_row = DingoTest.get_db_values_columns_only(rows[0])
        #last_row = DingoTest.get_db_values_columns_only(rows[-1])
        #print(first_row)
        #print(last_row)

        assert rows[0].palisade_id == 'TC_TDS_DUMP_NORMAL_TSWF'
        assert rows[0].sha == 'f0025d34ff033fc0337c1ecf5326675a1ae9d410f0a1bb01402f780774a9c9eb'
        assert rows[-1].palisade_id == 'TC_TDS_DUMP_NORMAL_TSWF'
        assert rows[-1].sha == '842de20f0c4371fe925b9ca338e9399988c6bbd57353731ce8c658489311acfa'

       # Check that SBM data are in the database
        logger.debug(f'Querying pipeline.sbm_log table in database ...')
        rows = (
            self.session.query(SbmLog)
                .order_by(SbmLog.utc_time)
                .all()
                )

        # Convert first/last row objects to dictionaries (for debugging)
        #first_row = DingoTest.get_db_values_columns_only(rows[0])
        #last_row = DingoTest.get_db_values_columns_only(rows[-1])
        #print(first_row)
        #print(last_row)

        assert isinstance(rows, list)
        assert len(rows) == 4

        assert rows[0].sbm_type == 1
        assert rows[0].cuc_time == '706939205:9843'
        assert rows[-1].sbm_type == 1
        assert rows[-1].cuc_time == '707010490:58727'

       # Check that Bias sweep data are in the database
        logger.debug(f'Querying pipeline.bia_sweep_log table in database ...')
        rows = (
            self.session.query(BiaSweepLog)
                .order_by(BiaSweepLog.utc_time)
                .all()
                )

        # Convert first/last row objects to dictionaries (for debugging)
        first_row = DingoTest.get_db_values_columns_only(rows[0])
        last_row = DingoTest.get_db_values_columns_only(rows[-1])
        print(first_row)
        print(last_row)

        assert isinstance(rows, list)
        assert len(rows) == 6

        assert rows[0].sweep_step == 'START_ANT1'
        assert rows[0].cuc_time == '706968074:1672'
        assert rows[-1].sweep_step == 'END_ANT3'
        assert rows[-1].cuc_time == '706968266:1450'

