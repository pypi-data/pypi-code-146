#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test all l0_to_l1_bia* commands of the roc.film plugin.
"""

import filecmp
import os
import tempfile
from pprint import pformat

import pytest
import shutil
import unittest.mock as mock

from maser.tools.cdf.cdfcompare import cdf_compare

from poppy.core.logger import logger
from poppy.core.test import CommandTestCase

from roc.film.tests.test_film import FilmTest


class TestL0ToL1Bia(CommandTestCase):
    film = FilmTest()

    def setup_method(self, method):
        super().setup_method(method)

        self.tmp_dir_path = tempfile.mkdtemp()

    def teardown_method(self, method):
        """
        Method called immediately after the test method has been called and the result recorded.

        This is called even if the test method raised an exception.

        :param method: the test method
        :return:
        """

        # rollback the database
        super().teardown_method(method)

        # clear the downloaded files
        shutil.rmtree(self.tmp_dir_path)

    @pytest.mark.skip(reason='Not working')
    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
        ('PALISADE', '4.3.5_MEB_PFM'),
    ])
    def test_l0_to_anc_bia_sweep_table(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'l0_to_anc_bia_sweep_table'

    #     input_dir_path, inputs = self.get_inputs(cmd)
    #     expected_output_dir_path, expected_outputs = self.get_expected_outputs(cmd)
    #     ancillary_dir_path, ancillaries = self.get_ancillaries(cmd)
    #
    #     # extract spice kernels
    #     spice_kernel_dir_path = self.unzip_kernels(ancillaries[0])
    #
    #     generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
    #     os.makedirs(generated_output_dir_path, exist_ok=True)
    #
    #     # initialize the main command
    #     main_command = ['pop', 'film',
    #                     '--idb-version', idb_version,
    #                     '--idb-source', idb_source,
    #                     '--monthly',
    #                     cmd,
    #                     '--l0-files',
    #                     ' '.join([
    #                         os.path.join(input_dir_path, input_file)
    #                         for input_file in inputs]),
    #                     '--output-dir', generated_output_dir_path,
    #                     '-ll', 'INFO']
    #
    #     # define the required plugins
    #     plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.film']
    #
    #     # run the command
    #     # force the value of the plugin list
    #     with mock.patch.object(Settings, 'configure',
    #                            autospec=True,
    #                            side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
    #         self.run_command('pop db upgrade heads -ll INFO')
    #         self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
    #         self.run_command(main_command)
    #
    #     # compare directory content
    #     dirs_cmp = filecmp.dircmp(generated_output_dir_path,
    #                               expected_output_dir_path)
    #
    #     dirs_cmp.report()
    #
    #     # ensure that we have the same files in both directories
    #     assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0), \
    #         'Different files in expected and generated output directories!'
    #
    #     for filename in self.get_diff_files(dirs_cmp):
    #         # compare only cdf files with differences
    #         if filename.endswith('.cdf'):
    #             # use cdf compare to compute the differences between expected output and the command output
    #             result = cdf_compare(
    #                 os.path.join(generated_output_dir_path, filename),
    #                 os.path.join(expected_output_dir_path, filename),
    #                 list_ignore_gatt=[
    #                     'File_ID',
    #                     'Generation_date',
    #                     'Pipeline_version',
    #                     'Pipeline_name',
    #                     'Software_version',
    #                     'IDB_version'
    #                 ]
    #             )
    #         elif filename.endswith('.csv'):
    #             result = filecmp.cmpfiles(
    #                 os.path.join(generated_output_dir_path, filename),
    #                 os.path.join(expected_output_dir_path, filename)
    #             )
    #         else:
    #             result = {}
    #
    #         # compare the difference dict with the expected one
    #         assert result == {}, \
    #         f'Differences between expected output and the command output: {pformat(result)}'
    #
    # @pytest.mark.skip()
    # @pytest.mark.parametrize('idb_source,idb_version', [
    #     ('MIB', '20200131'),
    #     ('PALISADE', '4.3.5_MEB_PFM'),
    # ])
    # def test_l0_to_l1_bia_sweep(self, idb_source, idb_version):
    #     from poppy.core.conf import Settings
    #
    #     # Name of the command to test
    #     cmd = 'l0_to_anc_bia_sweep_table'
    #
    #     input_dir_path, inputs = self.get_inputs(cmd)
    #     expected_output_dir_path, expected_outputs = self.get_expected_outputs(cmd)
    #     ancillary_dir_path, ancillaries = self.get_ancillaries(cmd)
    #
    #     # extract spice kernels
    #     spice_kernel_dir_path = self.unzip_kernels(ancillaries[0])
    #
    #     generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
    #     os.makedirs(generated_output_dir_path, exist_ok=True)
    #
    #     # Build list of inputs
    #     l0_files = ' '.join([
    #                         os.path.join(input_dir_path, input_file)
    #                         for input_file in inputs
    #                         if os.path.basename(input_file).startswith('solo_L0_rpw')
    #                         ])
    #     sweep_tables = ' '.join([
    #                         os.path.join(input_dir_path, input_file)
    #                         for input_file in inputs
    #                         if os.path.basename(input_file).startswith('solo_ANC_rpw-bia-sweep-table')
    #                         ])
    #
    #     # initialize the main command
    #     main_command = ['pop', 'film',
    #                     '--idb-version', idb_version,
    #                     '--idb-source', idb_source,
    #                     '--cdag',
    #                     cmd,
    #                     '--l0-files', l0_files,
    #                     '--sweep-tables', sweep_tables,
    #                     '--output-dir', generated_output_dir_path,
    #                     '-ll', 'INFO']
    #
    #     # define the required plugins
    #     plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.film']
    #
    #     # run the command
    #     # force the value of the plugin list
    #     with mock.patch.object(Settings, 'configure',
    #                            autospec=True,
    #                            side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
    #         self.run_command('pop db upgrade heads -ll INFO')
    #         self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
    #         self.run_command(main_command)
    #
    #     # compare directory content
    #     dirs_cmp = filecmp.dircmp(generated_output_dir_path,
    #                               expected_output_dir_path)
    #
    #     dirs_cmp.report()
    #
    #     # ensure that we have the same files in both directories
    #     assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0), \
    #         'Different files in expected and generated output directories!'
    #
    #     for filename in self.get_diff_files(dirs_cmp):
    #         # compare only cdf files with differences
    #         if filename.endswith('.cdf'):
    #             # use cdf compare to compute the differences between expected output and the command output
    #             result = cdf_compare(
    #                 os.path.join(generated_output_dir_path, filename),
    #                 os.path.join(expected_output_dir_path, filename),
    #                 list_ignore_gatt=[
    #                     'File_ID',
    #                     'Generation_date',
    #                     'Pipeline_version',
    #                     'Pipeline_name',
    #                     'Software_version',
    #                     'IDB_version'
    #                 ]
    #             )
    #         elif filename.endswith('.csv'):
    #             result = filecmp.cmpfiles(
    #                 os.path.join(generated_output_dir_path, filename),
    #                 os.path.join(expected_output_dir_path, filename)
    #             )
    #         else:
    #             result = {}
    #
    #         # compare the difference dict with the expected one
    #         assert result == {}, f'Differences between expected output and the command output: {pformat(result)}'
    #
    # @pytest.mark.skip()
    # @pytest.mark.parametrize('idb_source,idb_version', [
    #     ('MIB', '20200131'),
    #     ('PALISADE', '4.3.5_MEB_PFM'),
    # ])
    # def test_l0_to_l1_bia_current(self, idb_source, idb_version):
    #     from poppy.core.conf import Settings
    #
    #     # Name of the command to test
    #     cmd = 'l0_to_anc_bia_sweep_table'
    #
    #     input_dir_path, inputs = self.get_inputs(cmd)
    #     expected_output_dir_path, expected_outputs = self.get_expected_outputs(cmd)
    #     ancillary_dir_path, ancillaries = self.get_ancillaries(cmd)
    #
    #     # extract spice kernels
    #     spice_kernel_dir_path = self.unzip_kernels(ancillaries[0])
    #
    #     generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
    #     os.makedirs(generated_output_dir_path, exist_ok=True)
    #
    #     # initialize the main command
    #     main_command = ['pop', 'film',
    #                     '--idb-version', idb_version,
    #                     '--idb-source', idb_source,
    #                     '--cdag',
    #                     '--monthly',
    #                     cmd,
    #                     '--l0-files',
    #                     ' '.join([
    #                         os.path.join(input_dir_path, input_file)
    #                         for input_file in inputs]),
    #                     '--output-dir', generated_output_dir_path,
    #                     '-ll', 'INFO']
    #
    #     # define the required plugins
    #     plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.film']
    #
    #     # run the command
    #     # force the value of the plugin list
    #     with mock.patch.object(Settings, 'configure',
    #                            autospec=True,
    #                            side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
    #         self.run_command('pop db upgrade heads -ll INFO')
    #         self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
    #         self.run_command(main_command)
    #
    #     # compare directory content
    #     dirs_cmp = filecmp.dircmp(generated_output_dir_path,
    #                               expected_output_dir_path)
    #
    #     dirs_cmp.report()
    #
    #     # ensure that we have the same files in both directories
    #     assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0), \
    #         'Different files in expected and generated output directories!'
    #
    #     for filename in self.get_diff_files(dirs_cmp):
    #         # compare only cdf files with differences
    #         if filename.endswith('.cdf'):
    #             # use cdf compare to compute the differences between expected output and the command output
    #             result = cdf_compare(
    #                 os.path.join(generated_output_dir_path, filename),
    #                 os.path.join(expected_output_dir_path, filename),
    #                 list_ignore_gatt=[
    #                     'File_ID',
    #                     'Generation_date',
    #                     'Pipeline_version',
    #                     'Pipeline_name',
    #                     'Software_version',
    #                     'IDB_version'
    #                 ]
    #             )
    #         elif filename.endswith('.csv'):
    #             result = filecmp.cmpfiles(
    #                 os.path.join(generated_output_dir_path, filename),
    #                 os.path.join(expected_output_dir_path, filename)
    #             )
    #         else:
    #             result = {}
    #
    #         # compare the difference dict with the expected one
    #         assert result == {}, \
    #             f'Differences between expected output and the command output: {pformat(result)}'
