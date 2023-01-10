#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test l0_to_hk command of the roc.film plugin.
"""

import filecmp
import os
import shlex
from pprint import pformat

import pytest
import shutil
import unittest.mock as mock

from maser.tools.cdf.cdfcompare import cdf_compare

from poppy.core.logger import logger
from poppy.core.test import CommandTestCase

from roc.film.tests.test_film import FilmTest


class TestL0ToHk(CommandTestCase):
    film = FilmTest()

    cmd = 'l0_to_hk'

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
    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
    ])
    def test_l0_to_hk(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'l0_to_hk'

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

        # initialize the main command
        command_to_test = ' '.join(['pop',
                                    'film',
                                    '--force',
                           '--idb-version', idb_version,
                           '--idb-source', idb_source,
                           cmd,
                           os.path.join(input_dir_path, inputs[0]),
                           '--output-dir', output_dir_path,
                           '-ll', 'INFO'])

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.dingo', 'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            # Load IDB in the database
            FilmTest.load_idb(self, idb_version=idb_version)
            self.run_command(shlex.split(command_to_test))

        # compare directory content
        dirs_cmp = filecmp.dircmp(output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

        for filename in FilmTest.get_diff_files(dirs_cmp):
            # compare only cdf files with differences
            if filename.endswith('.cdf'):
                # use cdf compare to compute the differences between expected output and the command output
                result = cdf_compare(
                    os.path.join(output_dir_path, filename),
                    os.path.join(expected_output_dir_path, filename),
                    list_ignore_gatt=[
                        'File_ID',
                        'Generation_date',
                        'Pipeline_version',
                        'Pipeline_name',
                        'Software_version',
                        'IDB_version'
                    ]
                )

                # compare the difference dict with the expected one
                if result:
                    logger.error(f'Differences between expected output and the command output: {pformat(result)}')

                assert result == {}
