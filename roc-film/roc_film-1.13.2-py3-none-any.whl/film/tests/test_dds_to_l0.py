#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test tm_to_l0 command of the roc.film plugin.
"""

import filecmp
import os
import tempfile
from pathlib import Path
from pprint import pformat

import pytest
import shutil
import shlex
import unittest.mock as mock

from poppy.core.logger import logger
from poppy.core.test import CommandTestCase

from roc.film.tests.hdf5_compare import Hdf5Diff
from roc.film.tests.test_film import FilmTest


class TestDdsToL0(CommandTestCase):
    film = FilmTest()

    def setup_method(self, method):
        super().setup_method(method)

    def teardown_method(self, method):
        """
        Method called immediately after the test method has been called and the result recorded.

        This is called even if the test method raised an exception.

        :param method: the test method
        :return:
        """

        # rollback the database
        super().teardown_method(method)

        # clear the files produced during test
        shutil.rmtree(self.output_dir_path)

    #@pytest.mark.skip()
    @pytest.mark.parametrize(
        'date_to_test,idb_source,idb_version',
        [('20220501', 'MIB', '20200131')],
    )
    def test_dds_to_l0(self, date_to_test, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'dds_to_l0'

        # Retrieve data for current test
        test_data_path = FilmTest().get_test_data(cmd, extract=True)
        test_data_dir = os.path.dirname(test_data_path)
        self.test_data_dir = test_data_dir

        # Initialize inputs and expected outputs
        input_dir_path, inputs = FilmTest.get_inputs(test_data_dir)
        if not inputs:
            raise FileNotFoundError(f'No input found in {test_data_dir}!')
        expected_output_dir_path, expected_outputs = FilmTest.get_expected_outputs(test_data_dir)
        if not expected_outputs:
            raise FileNotFoundError(f'No expected output found in {test_data_dir}!')

        # Initialize directory where files produced during test will be saved
        output_dir_path = os.path.join(test_data_dir, 'output')
        self.output_dir_path = output_dir_path

        # Check that SPICE kernels are present in ./data/spice_kernels folder
        spice_kernels_dir = FilmTest.get_spice_kernel_dir()
        if not os.path.isdir(spice_kernels_dir):
            raise FileNotFoundError(f'No SPICE kernel set found in {spice_kernels_dir}!')

        # length in scos header bytes to remove from input binary TM packets
        scos_header_byte_length = '0'

        # Split inputs between two lists containing RPW TM and TC files respectively
        tm_inputs = ' '.join([
            os.path.join(input_dir_path, input_file)
            for input_file in inputs
            if os.path.basename(input_file).startswith('solo_TM_')
        ])
        tc_inputs = ' '.join([
            os.path.join(input_dir_path, input_file)
            for input_file in inputs
            if os.path.basename(input_file).startswith('solo_TC_')
        ])

        # initialize the main command
        # Make sure that start-time/end_time keyword values are consistent with input DDS files
        command_to_test = ' '.join(['pop', 'film',
                           '--force',
                           '--idb-version', idb_version,
                           '--idb-source', idb_source,
                           '--scos-header', scos_header_byte_length,
                           '--cdag',
                           cmd, date_to_test,
                           '--dds-tmraw-xml', tm_inputs,
                           '--dds-tcreport-xml', tc_inputs,
                           '--output-dir', output_dir_path,
                           '-ll', 'INFO'])

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.dingo', 'roc.film']
        #
        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            # Load IDB in the database
            FilmTest.load_idb(self, idb_version=idb_version)

            # Run the command to test
            logger.info(f'Running {command_to_test}')
            self.run_command(shlex.split(command_to_test))

        # compare directory content
        dirs_cmp = filecmp.dircmp(output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()
        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

        # ensure the name of the two expected and generated L0 files is the same
        produced_l0_path = os.path.join(output_dir_path, f'solo_L0_rpw-cdag_{date_to_test}_V01.h5')
        expected_l0_path = os.path.join(expected_output_dir_path, f'solo_L0_rpw-cdag_{date_to_test}_V01.h5')
        assert Path(produced_l0_path).name == Path(expected_l0_path).name

        # Compare content of the two L0 files
        attributes_to_ignore = [
                         'File_ID',
                         'Generation_date',
                         'Pipeline_version',
                         'Pipeline_name',
                         'Software_version',
                         'IDB_version'
                    ]
        result = Hdf5Diff(produced_l0_path, expected_l0_path, '/', '/',
                          exclude_attr=attributes_to_ignore).diff_files()
        if result:
            logger.error(f'Differences between expected output and the command output: {pformat(result)}')

        assert result == []
