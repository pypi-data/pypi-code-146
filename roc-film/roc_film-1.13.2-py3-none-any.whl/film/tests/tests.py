#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.film plugin.
"""

import subprocess

from poppy.core.test import TaskTestCase

# Tests on roc.film.tasks.metadata methods
class TestFilmMetadata(TaskTestCase):
    # create the pipeline
    def test_build_file_basename(self):
        """
        Test the roc.film.tasks.metadata.build_file_basename,
        assuming the Logical_file_id attribute is not defined.

        :return:
        """

        # import method to test
        from roc.film.tools.file_helpers import build_file_basename

        # initialize meta dictionary with expected inputs
        meta = {
            'Source_name': 'SOLO>Solar Orbiter',
            'LEVEL': 'L1>Level 1 data processing',
            'Descriptor': 'RPW-HFR-SURV> RPW HFR survey data',
            'Datetime': '20220103',
            'Data_version' : '01'
                }

        assert build_file_basename(meta) == 'solo_L1_rpw-hfr-surv_20220103_V01'

    def test_build_file_basename_with_logical(self):
        """
        Test the roc.film.tasks.metadata.build_file_basename,
        assuming the Logical_file_id attribute is defined.

        :return:
        """

        # import method to test
        from roc.film.tools.file_helpers import build_file_basename

        meta = {'Logical_file_id': 'solo_L1_rpw-hfr-surv_20220103_V01'}
        assert build_file_basename(meta) == 'solo_L1_rpw-hfr-surv_20220103_V01'

    # def test_generate_filepath(self):

    def test_valid_data_version(self):
        """
        Test the roc.film.tasks.metadata.valid_data_version

        :return:
        """

        # import method to test
        from roc.film.tools.metadata import valid_data_version

        assert valid_data_version(1) == '01'

    def test_set_logical_file_id(self):
        """
        Test the roc.film.tasks.metadata.set_logical_file_id

        :return:
        """

        # import method to test
        from roc.film.tools.metadata import set_logical_file_id

        # initialize meta dictionary with expected inputs
        meta = {
            'File_naming_convention': '<Source_name>_<LEVEL>_<Descriptor>_' \
                                             '<Datetime>_V<Data_version>',
            'Source_name': 'SOLO>Solar Orbiter',
            'LEVEL': 'L1>Level 1 data processing',
            'Descriptor': 'RPW-HFR-SURV> RPW HFR survey data',
            'Datetime': '20220103',
            'Data_version' : '01'
                }

        assert set_logical_file_id(meta) == 'solo_L1_rpw-hfr-surv_20220103_V01'


import filecmp
import os
import tempfile
from pprint import pformat

import pytest
import shutil
import unittest.mock as mock
from maser.tools.cdf.cdfcompare import cdf_compare
from poppy.core.generic.requests import download_file
from poppy.core.logger import logger
from poppy.core.test import CommandTestCase


class TestFilmFileProd(CommandTestCase):
    base_url = 'https://rpw.lesia.obspm.fr/roc/data/private/devtest/roc/test_data/rodp/film'
    # test credentials
    username = 'roctest'
    password = None

    @classmethod
    def setup_class(cls):
        """
        Setup credentials
        """

        try:
            cls.password = os.environ['ROC_TEST_PASSWORD']
        except KeyError:
            raise KeyError('You have to define the test user password using the "ROC_TEST_PASSWORD" environment'
                           'variable ')

    def setup_method(self, method):
        super().setup_method(method)

        self.tmp_dir_path = tempfile.mkdtemp()

    def load_manifest_file(self, manifest_filepath, manifest_file_url, auth=None):

        download_file(manifest_filepath, manifest_file_url, auth=auth)

        with open(manifest_filepath) as manifest_file:
            for line in manifest_file:
                yield line.strip('\n\r')

        os.remove(manifest_filepath)

    def get_files(self, subdir, category=None):
        categories = ['input', 'expected_output', 'ancillarie']
        if category not in categories:
            raise ValueError('Invalid category. Expected one of: %s' % categories)

        auth = (self.username, self.password)

        dir_path = os.path.join(self.tmp_dir_path, subdir, category)
        os.makedirs(dir_path, exist_ok=True)
        manifest_filepath = os.path.join(dir_path, 'manifest.txt')
        manifest_file_url = f'{self.base_url}/{subdir}/{category}s/manifest.txt'
        file_list = list(self.load_manifest_file(manifest_filepath, manifest_file_url, auth=auth))

        for relative_filepath in file_list:
            # skip empty strings
            if not relative_filepath:
                continue

            # get the complete filepath
            filepath = os.path.join(dir_path, relative_filepath)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            download_file(filepath,
                          f'{self.base_url}/{subdir}/{category}s/{relative_filepath}',
                          auth=auth)

        return dir_path, file_list

    def get_diff_files(self, dirs_cmp, path=''):
        for name in dirs_cmp.diff_files:
            yield os.path.join(path, name)
        for parent, sub_dirs_cmp in dirs_cmp.subdirs.items():
            for filepath in self.get_diff_files(sub_dirs_cmp, path=os.path.join(path, parent)):
                yield filepath

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

    def get_inputs(self, subdir):
        return self.get_files(subdir, category='input')

    def get_expected_outputs(self, subdir):
        return self.get_files(subdir, category='expected_output')

    def get_ancillaries(self, subdir):
        return self.get_files(subdir, category='ancillarie')

    def unzip_kernels(self, zip_path,
                      pipeline_dir='/pipeline'):
        """
        Unzip input SPICE kernel ZIP file.

        :param zip_path: Path to the input zip file
        :param pipeline_dir: If provided, move unzipped kernels folder into pipeline_dir
        / data folder
        :return: path of the unzipped kernels folder
        """

        # Initialize output
        target_dir = None

        # check zip file existence
        if not os.path.isfile(zip_path):
            raise FileNotFoundError(f'ZIP file containing SPICE kernel not found ({zip_path})!')

        # Get zip directory
        zip_dir = os.path.dirname(zip_path)

        # Unzip ZIP file
        try:
            cmd = f'unzip -o {zip_path}'
            completed = subprocess.run(cmd,
                                       cwd=zip_dir,
                                       shell=True, timeout=3600)
            # Path of the unzipped kernels dir
            kernels_dir = os.path.join(zip_dir, 'kernels')
            if not os.path.isdir(kernels_dir):
                raise FileNotFoundError

        except:
            logger.exception(f'Extracting {zip_dir} has failed: \n'
                             f'{completed.stderr}')
        else:
            # Move unzipped "kernels" folder into /pipeline/data/spice_kernels
            if os.path.isdir(pipeline_dir):
                data_dir = os.path.join(pipeline_dir, 'data')
                os.makedirs(data_dir, exist_ok=True)
                target_dir = os.path.join(data_dir, 'spice_kernels')
                shutil.move(kernels_dir, target_dir)
            else:
                target_dir = kernels_dir

        return target_dir

    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
    ])
    def test_classify_tmraw(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        input_dir_path, inputs = self.get_inputs('classify_tmraw')
        expected_output_dir_path, expected_outputs = self.get_expected_outputs('classify_tmraw')

        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        # initialize the main command
        main_command = ['pop', 'film',
                        'classify_tmraw',
                        '--dds-files',
                        ' '.join([
                            os.path.join(input_dir_path, input_file)
                            for input_file in inputs]),
                        '--output-dir', generated_output_dir_path,
                        '-ll', 'INFO']

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.dingo' ,'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command('pop db upgrade heads -ll INFO')
            self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
            self.run_command(main_command)

        # compare directory content
        dirs_cmp = filecmp.dircmp(generated_output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

        for filename in self.get_diff_files(dirs_cmp):
            # compare only xml files with differences
            if filename.endswith('.xml'):
                # use cdf compare to compute the differences between expected output and the command output
                result = filecmp.cmpfiles(
                    os.path.join(generated_output_dir_path, filename),
                    os.path.join(expected_output_dir_path, filename),
                )
                # compare the difference dict with the expected one
                if result:
                    logger.error(f'Differences between expected output and the command output: {pformat(result)}')

                assert result == {}


    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
    ])
    def test_classify_tcreport(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        input_dir_path, inputs = self.get_inputs('classify_tcreport')
        expected_output_dir_path, expected_outputs = self.get_expected_outputs('classify_tcreport')

        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        # initialize the main command
        main_command = ['pop', 'film',
                        'classify_tcreport',
                        '--dds-files',
                        ' '.join([
                            os.path.join(input_dir_path, input_file)
                            for input_file in inputs]),
                        '--output-dir', generated_output_dir_path,
                        '-ll', 'INFO']

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.dingo' ,'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command('pop db upgrade heads -ll INFO')
            self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
            self.run_command(main_command)

        # compare directory content
        dirs_cmp = filecmp.dircmp(generated_output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

        for filename in self.get_diff_files(dirs_cmp):
            # compare only xml files with differences
            if filename.endswith('.xml'):
                # use cdf compare to compute the differences between expected output and the command output
                result = filecmp.cmpfiles(
                    os.path.join(generated_output_dir_path, filename),
                    os.path.join(expected_output_dir_path, filename),
                )
                # compare the difference dict with the expected one
                if result:
                    logger.error(f'Differences between expected output and the command output: {pformat(result)}')

                assert result == {}

    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
    ])
    def test_classify_process_solohk(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        input_dir_path, inputs = self.get_inputs('process_solohk')
        expected_output_dir_path, expected_outputs = self.get_expected_outputs('process_solohk')

        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        # initialize the main command
        main_command = ['pop', 'film',
                        'process_solohk',
                        '--dds-files',
                        ' '.join([
                            os.path.join(input_dir_path, input_file)
                            for input_file in inputs]),
                        '--output-dir', generated_output_dir_path,
                        '-ll', 'INFO']

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.dingo' ,'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command('pop db upgrade heads -ll INFO')
            self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
            self.run_command(main_command)

        # compare directory content
        dirs_cmp = filecmp.dircmp(generated_output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

        for filename in self.get_diff_files(dirs_cmp):
            # compare only xml files with differences
            if filename.endswith('.xml'):
                # use cdf compare to compute the differences between expected output and the command output
                result = filecmp.cmpfiles(
                    os.path.join(generated_output_dir_path, filename),
                    os.path.join(expected_output_dir_path, filename),
                )
                # compare the difference dict with the expected one
                if result:
                    logger.error(f'Differences between expected output and the command output: {pformat(result)}')

                assert result == {}

    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
        ('PALISADE', '4.3.5_MEB_PFM'),
    ])
    def test_l0_to_l1_surv(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'l0_to_l1_surv'

        input_dir_path, inputs = self.get_inputs(cmd)
        expected_output_dir_path, expected_outputs = self.get_expected_outputs(cmd)
        ancillary_dir_path, ancillaries = self.get_ancillaries(cmd)

        # extract spice kernels
        spice_kernel_dir_path = self.unzip_kernels(ancillaries[0])

        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        # initialize the main command
        main_command = ['pop', 'film',
                        '--idb-version', idb_version,
                        '--idb-source', idb_source,
                        '--cdag',
                        cmd,
                        os.path.join(input_dir_path, inputs[0]),
                        '--output-dir', generated_output_dir_path,
                        '-ll', 'INFO']

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command('pop db upgrade heads -ll INFO')
            self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
            self.run_command(main_command)

        # compare directory content
        dirs_cmp = filecmp.dircmp(generated_output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

        for filename in self.get_diff_files(dirs_cmp):
            # compare only cdf files with differences
            if filename.endswith('.cdf'):
                # use cdf compare to compute the differences between expected output and the command output
                result = cdf_compare(
                    os.path.join(generated_output_dir_path, filename),
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

    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
        ('PALISADE', '4.3.5_MEB_PFM'),
    ])
    def test_l0_to_hk(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'l0_to_hk'

        input_dir_path, inputs = self.get_inputs(cmd)
        expected_output_dir_path, expected_outputs = self.get_expected_outputs(cmd)
        ancillary_dir_path, ancillaries = self.get_ancillaries(cmd)

        # extract spice kernels
        spice_kernel_dir_path = self.unzip_kernels(ancillaries[0])

        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        # initialize the main command
        main_command = ['pop', 'film',
                        '--idb-version', idb_version,
                        '--idb-source', idb_source,
                        cmd,
                        os.path.join(input_dir_path, inputs[0]),
                        '--output-dir', generated_output_dir_path,
                        '-ll', 'INFO']

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.dingo', 'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command('pop db upgrade heads -ll INFO')
            self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
            self.run_command(main_command)

        # compare directory content
        dirs_cmp = filecmp.dircmp(generated_output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

        for filename in self.get_diff_files(dirs_cmp):
            # compare only cdf files with differences
            if filename.endswith('.cdf'):
                # use cdf compare to compute the differences between expected output and the command output
                result = cdf_compare(
                    os.path.join(generated_output_dir_path, filename),
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

    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
        ('PALISADE', '4.3.5_MEB_PFM'),
    ])
    def test_dds_to_l0(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'dds_to_l0'

        input_dir_path, inputs = self.get_inputs(cmd)
        expected_output_dir_path, expected_outputs = self.get_expected_outputs(cmd)
        ancillary_dir_path, ancillaries = self.get_ancillaries(cmd)

        # extract spice kernels
        spice_kernel_dir_path = self.unzip_kernels(ancillaries[0])
        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        date = '20200303'
        scos_header = '0'

        # Build list of tm and tc input files
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
        main_command = ['pop', 'film',
                        '--idb-version', idb_version,
                        '--idb-source', idb_source,
                        '--scos-header', scos_header,
                        '--cdag',
                        cmd, date,
                        '--dds-tmraw-xml', tm_inputs,
                        '--dds-tcreport-xml', tc_inputs,
                        '--output-dir', generated_output_dir_path,
                        '-ll', 'INFO']

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command('pop db upgrade heads -ll INFO')
            self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
            self.run_command(main_command)

        # compare directory content
        dirs_cmp = filecmp.dircmp(generated_output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

        # TODO - Adapt this part for HDF5 file (L0)
        # for filename in self.get_diff_files(dirs_cmp):
        #     # compare only cdf files with differences
        #     if filename.endswith('.cdf'):
        #         # use cdf compare to compute the differences between expected output and the command output
        #         result = cdf_compare(
        #             os.path.join(generated_output_dir_path, filename),
        #             os.path.join(expected_output_dir_path, filename),
        #             list_ignore_gatt=[
        #                 'File_ID',
        #                 'Generation_date',
        #                 'Pipeline_version',
        #                 'Pipeline_name',
        #                 'Software_version',
        #                 'IDB_version'
        #             ]
        #         )
        #
        #         # compare the difference dict with the expected one
        #         if result:
        #             logger.error(f'Differences between expected output and the command output: {pformat(result)}')
        #
        #         assert result == {}

    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
        ('PALISADE', '4.3.5_MEB_PFM'),
    ])
    def test_l0_to_l1_sbm(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'l0_to_l1_sbm'

        input_dir_path, inputs = self.get_inputs(cmd)
        expected_output_dir_path, expected_outputs = self.get_expected_outputs(cmd)
        ancillary_dir_path, ancillaries = self.get_ancillaries(cmd)

        # extract spice kernels
        spice_kernel_dir_path = self.unzip_kernels(ancillaries[0])

        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        # initialize the main command
        main_command = ['pop', 'film',
                        '--idb-version', idb_version,
                        '--idb-source', idb_source,
                        '--cdag',
                        cmd,
                        ' '.join([
                            os.path.join(input_dir_path, input_file)
                            for input_file in inputs]),
                        '--output-dir', generated_output_dir_path,
                        '-ll', 'INFO']

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command('pop db upgrade heads -ll INFO')
            self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
            self.run_command(main_command)

        # compare directory content
        dirs_cmp = filecmp.dircmp(generated_output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

        for filename in self.get_diff_files(dirs_cmp):
            # compare only cdf files with differences
            if filename.endswith('.cdf'):
                # use cdf compare to compute the differences between expected output and the command output
                result = cdf_compare(
                    os.path.join(generated_output_dir_path, filename),
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

    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
        ('PALISADE', '4.3.5_MEB_PFM'),
    ])
    def test_l0_to_anc_bia_sweep_table(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'l0_to_anc_bia_sweep_table'

        input_dir_path, inputs = self.get_inputs(cmd)
        expected_output_dir_path, expected_outputs = self.get_expected_outputs(cmd)
        ancillary_dir_path, ancillaries = self.get_ancillaries(cmd)

        # extract spice kernels
        spice_kernel_dir_path = self.unzip_kernels(ancillaries[0])

        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        # initialize the main command
        main_command = ['pop', 'film',
                        '--idb-version', idb_version,
                        '--idb-source', idb_source,
                        '--monthly',
                        cmd,
                        '--l0-files',
                        ' '.join([
                            os.path.join(input_dir_path, input_file)
                            for input_file in inputs]),
                        '--output-dir', generated_output_dir_path,
                        '-ll', 'INFO']

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command('pop db upgrade heads -ll INFO')
            self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
            self.run_command(main_command)

        # compare directory content
        dirs_cmp = filecmp.dircmp(generated_output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0), \
            'Different files in expected and generated output directories!'

        for filename in self.get_diff_files(dirs_cmp):
            # compare only cdf files with differences
            if filename.endswith('.cdf'):
                # use cdf compare to compute the differences between expected output and the command output
                result = cdf_compare(
                    os.path.join(generated_output_dir_path, filename),
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
            elif filename.endswith('.csv'):
                result = filecmp.cmpfiles(
                    os.path.join(generated_output_dir_path, filename),
                    os.path.join(expected_output_dir_path, filename)
                )
            else:
                result = {}

            # compare the difference dict with the expected one
            assert result == {}, \
            f'Differences between expected output and the command output: {pformat(result)}'

    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
        ('PALISADE', '4.3.5_MEB_PFM'),
    ])
    def test_l0_to_l1_bia_sweep(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'l0_to_anc_bia_sweep_table'

        input_dir_path, inputs = self.get_inputs(cmd)
        expected_output_dir_path, expected_outputs = self.get_expected_outputs(cmd)
        ancillary_dir_path, ancillaries = self.get_ancillaries(cmd)

        # extract spice kernels
        spice_kernel_dir_path = self.unzip_kernels(ancillaries[0])

        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        # Build list of inputs
        l0_files = ' '.join([
                            os.path.join(input_dir_path, input_file)
                            for input_file in inputs
                            if os.path.basename(input_file).startswith('solo_L0_rpw')
                            ])
        sweep_tables = ' '.join([
                            os.path.join(input_dir_path, input_file)
                            for input_file in inputs
                            if os.path.basename(input_file).startswith('solo_ANC_rpw-bia-sweep-table')
                            ])

        # initialize the main command
        main_command = ['pop', 'film',
                        '--idb-version', idb_version,
                        '--idb-source', idb_source,
                        '--cdag',
                        cmd,
                        '--l0-files', l0_files,
                        '--sweep-tables', sweep_tables,
                        '--output-dir', generated_output_dir_path,
                        '-ll', 'INFO']

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command('pop db upgrade heads -ll INFO')
            self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
            self.run_command(main_command)

        # compare directory content
        dirs_cmp = filecmp.dircmp(generated_output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0), \
            'Different files in expected and generated output directories!'

        for filename in self.get_diff_files(dirs_cmp):
            # compare only cdf files with differences
            if filename.endswith('.cdf'):
                # use cdf compare to compute the differences between expected output and the command output
                result = cdf_compare(
                    os.path.join(generated_output_dir_path, filename),
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
            elif filename.endswith('.csv'):
                result = filecmp.cmpfiles(
                    os.path.join(generated_output_dir_path, filename),
                    os.path.join(expected_output_dir_path, filename)
                )
            else:
                result = {}

            # compare the difference dict with the expected one
            assert result == {}, f'Differences between expected output and the command output: {pformat(result)}'

    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
        ('PALISADE', '4.3.5_MEB_PFM'),
    ])
    def test_l0_to_l1_bia_current(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'l0_to_anc_bia_sweep_table'

        input_dir_path, inputs = self.get_inputs(cmd)
        expected_output_dir_path, expected_outputs = self.get_expected_outputs(cmd)
        ancillary_dir_path, ancillaries = self.get_ancillaries(cmd)

        # extract spice kernels
        spice_kernel_dir_path = self.unzip_kernels(ancillaries[0])

        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        # initialize the main command
        main_command = ['pop', 'film',
                        '--idb-version', idb_version,
                        '--idb-source', idb_source,
                        '--cdag',
                        '--monthly',
                        cmd,
                        '--l0-files',
                        ' '.join([
                            os.path.join(input_dir_path, input_file)
                            for input_file in inputs]),
                        '--output-dir', generated_output_dir_path,
                        '-ll', 'INFO']

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.film']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            self.run_command('pop db upgrade heads -ll INFO')
            self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
            self.run_command(main_command)

        # compare directory content
        dirs_cmp = filecmp.dircmp(generated_output_dir_path,
                                  expected_output_dir_path)

        dirs_cmp.report()

        # ensure that we have the same files in both directories
        assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0), \
            'Different files in expected and generated output directories!'

        for filename in self.get_diff_files(dirs_cmp):
            # compare only cdf files with differences
            if filename.endswith('.cdf'):
                # use cdf compare to compute the differences between expected output and the command output
                result = cdf_compare(
                    os.path.join(generated_output_dir_path, filename),
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
            elif filename.endswith('.csv'):
                result = filecmp.cmpfiles(
                    os.path.join(generated_output_dir_path, filename),
                    os.path.join(expected_output_dir_path, filename)
                )
            else:
                result = {}

            # compare the difference dict with the expected one
            assert result == {}, \
                f'Differences between expected output and the command output: {pformat(result)}'
