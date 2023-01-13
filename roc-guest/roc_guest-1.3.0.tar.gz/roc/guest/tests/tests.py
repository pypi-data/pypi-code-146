#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for roc.guest plugin.
"""

import os
import tempfile
import subprocess

import unittest.mock as mock

from poppy.core.generic.requests import download_file
from poppy.core.logger import logger
from poppy.core.test import CommandTestCase
from poppy.core.db.connector import Connector

from roc.guest.models.meb_gse_data.event import Event
from roc.guest.exceptions import MebDbTransactionError


class TestGuest(CommandTestCase):
    base_url = \
        'https://rpw.lesia.obspm.fr/roc/data/private/' \
        'devtest/roc/test_data/rgts/guest'
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
            raise KeyError('You have to define the test user password '
                           'using the "ROC_TEST_PASSWORD" environment'
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

    def get_files(self, name_test, category=None):
        categories = ['input', 'expected_output']
        if category not in categories:
            raise ValueError('Invalid category. Expected one of: %s' % categories)

        auth = (self.username, self.password)

        dir_path = os.path.join(self.tmp_dir_path, category)
        os.makedirs(dir_path, exist_ok=True)
        manifest_filepath = os.path.join(dir_path, 'manifest.txt')
        manifest_file_url = f'{self.base_url}/{name_test}/{category}s/manifest.txt'
        file_list = list(self.load_manifest_file(manifest_filepath,
                                                 manifest_file_url, auth=auth))

        for relative_filepath in file_list:
            # skip empty strings
            if not relative_filepath:
                continue

            # get the complete filepath
            filepath = os.path.join(dir_path, relative_filepath)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            current_url = f'{self.base_url}/{name_test}/' \
                          f'{category}s/{relative_filepath}'
            download_file(filepath,
                          current_url,
                          auth=auth)

        return dir_path, file_list

    def get_inputs(self, name_test):
        return self.get_files(name_test, category='input')

    def get_expected_outputs(self, name_test):
        return self.get_files(name_test, category='expected_output')

    # @pytest.mark.parametrize("idb_source,idb_version", [
    #     ("MIB", "20190624"),
    #     ("PALISADE", "4.3.3_MEB_PFM"),
    # ])
    # def test_from_xml(self, idb_source, idb_version):
    #     from poppy.core.conf import Settings

    #     input_dir_path, inputs = self.get_inputs('from_xml')
    #     expected_output_dir_path, expected_outputs = self.get_expected_outputs('from_xml')

    #     generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
    #     os.makedirs(generated_output_dir_path, exist_ok=True)

    #     # initialize the main command
    #     main_command = ['pop', "guest",
    #                     "--idb-version", idb_version,
    #                     "--idb-source", idb_source,
    #                     "from_xml",
    #                     "--xml-test-log", os.path.join(input_dir_path, inputs[0]),
    #                     "--output-dir", generated_output_dir_path,
    #                     "-ll", "INFO"]

    #     # define the required plugins
    #     plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.guest', 'roc.film']

    #     # run the command
    #     # force the value of the plugin list
    #     with mock.patch.object(Settings, 'configure',
    #                            autospec=True,
    #                            side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
    #         self.run_command('pop db upgrade heads -ll INFO')
    #         self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
    #         self.run_command(main_command)

    #     # compare directory content
    #     dirs_cmp = filecmp.dircmp(generated_output_dir_path,
    #                               expected_output_dir_path)

    #     dirs_cmp.report()

    #     # ensure that we have the same files in both directories
    #     assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

    #     for filename in self.get_diff_files(dirs_cmp):
    #         # compare only cdf files with differences
    #         if filename.endswith('.cdf'):
    #             # use cdf compare to compute the differences between expected output and the command output
    #             result = cdf_compare(
    #                 os.path.join(generated_output_dir_path, filename),
    #                 os.path.join(expected_output_dir_path, filename),
    #                 list_ignore_gatt=[
    #                     'File_ID', 'File_UUID',
    #                     'Generation_date',
    #                     'Pipeline_version',
    #                     'Software_version',
    #                     'IDB_version'
    #                 ]
    #             )

    #             # compare the difference dict with the expected one
    #             if result:
    #                 logger.error(f'Differences between expected output and the command output: {pformat(result)}')

    #             assert result == {}

    # @pytest.mark.parametrize("idb_source,idb_version", [
    #     ("PALISADE", "4.3.3_MEB_PFM"),
    # ])
    # def test_xml_to_dds(self, idb_source, idb_version):
    #     from poppy.core.conf import Settings

    #     input_dir_path, inputs = self.get_inputs('from_xml')
    #     expected_output_dir_path, expected_outputs = self.get_expected_outputs('from_xml')

    #     generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
    #     os.makedirs(generated_output_dir_path, exist_ok=True)

    #     # initialize the main command
    #     main_command = ['pop', "guest",
    #                     "--idb-version", idb_version,
    #                     "--idb-source", idb_source,
    #                     "xml_to_dds",
    #                     "--scos-header-size", '76',
    #                     os.path.join(input_dir_path, inputs[0]),
    #                     "--output-dir", generated_output_dir_path,
    #                     "-ll", "INFO"]

    #     # define the required plugins
    #     plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.guest', 'roc.film']

    #     # run the command
    #     # force the value of the plugin list
    #     with mock.patch.object(Settings, 'configure',
    #                            autospec=True,
    #                            side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
    #         self.run_command('pop db upgrade heads -ll INFO')
    #         self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
    #         self.run_command(main_command)

    #     # compare directory content
    #     dirs_cmp = filecmp.dircmp(generated_output_dir_path,
    #                               expected_output_dir_path)

    #     dirs_cmp.report()

    #     # ensure that we have the same files in both directories
    #     assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)

    #     # TODO - Add output xml comparison
    #     #for filename in self.get_diff_files(dirs_cmp):
    #         # compare only cdf files with differences

    # def get_diff_files(self, dirs_cmp, path=''):
    #     for name in dirs_cmp.diff_files:
    #         yield os.path.join(path, name)
    #     for parent, sub_dirs_cmp in dirs_cmp.subdirs.items():
    #         for filepath in self.get_diff_files(sub_dirs_cmp, path=os.path.join(path, parent)):
    #             yield filepath

    # def teardown_method(self, method):
    #     """
    #     Method called immediately after the test method has been called and the result recorded.

    #     This is called even if the test method raised an exception.

    #     :param method: the test method
    #     :return:
    #     """

    #     # rollback the database
    #     super().teardown_method(method)

    #     # clear the downloaded files
    # #     shutil.rmtree(self.tmp_dir_path)

    # def findDiff(self, xml1, xml2):
    #     for i in range(0, len(xml1)):
    #         if xml1[i] != xml2[i]:
    #             print(f'Difference found at pos {i}')
    #             if i > 20:
    #                 start = i-20
    #             else:
    #                 start = i
    #             end = i+50
    #             print(f'{xml1[start:end]} != {xml2[start:end]}')
    #             break

    def test_xml_to_mebdb(self):
        from poppy.core.conf import Settings

        input_dir_path, inputs = self.get_inputs('xml_to_mebdb')

        # initialize the main command
        main_command = 'pop guest xml_to_mebdb ' \
                       f'{os.path.join(input_dir_path, inputs[0])} '

        # define the required plugins
        # plugin_list = ['poppy.pop', 'roc.guest']

        # run the command
        subprocess.run(main_command, shell=True, check=True, timeout=36000)

        connector = Connector.manager[Settings.MEB_DATABASE]
        database = connector.get_database()

        # check the database is connected
        database.connectDatabase()

        # get the selected database from the MEB connector
        meb = connector.selected

        # connect to the database
        meb.connectDatabase()

        # check that the connection is made
        if not meb.connected:
            message = '{0} is not connected'.format(meb)
            logger.error(message)
            raise MebDbTransactionError(message)

        # Insert test log TestDescriptor data into the MEB GSE database
        with meb.query_context() as session:
            row = session.query(Event).count()

        assert (row == 59882)

    def test_l0_to_xml(self):
        from poppy.core.conf import Settings
        # import h5py

        input_dir_path, inputs = self.get_inputs('l0_to_xml')
        expected_output_dir_path, expected_outputs = self.get_expected_outputs('l0_to_xml')

        generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        os.makedirs(generated_output_dir_path, exist_ok=True)

        # initialize the main command
        output_xml = os.path.join(generated_output_dir_path,
                                  os.path.splitext(inputs[0])[0] + '.xml')
        main_command = f'pop guest l0_to_xml {os.path.join(input_dir_path, inputs[0])} ' \
                       f'--test-log-xml {output_xml}'

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.idb', 'roc.guest']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(
                                   dictionary={'PLUGINS': plugin_list})):
            self.run_command(main_command)

        xmlOutputGenerated = XmlReader(generated_output_dir_path)
        xmlOutputExpected = XmlReader(expected_output_dir_path)

        # Remove some metadata defined "on-the-fly"
        xmlOutputGenerated.removeMarkup(['TestLogDescriptor', 'TestUUID'])
        xmlOutputExpected.removeMarkup(['TestLogDescriptor', 'TestUUID'])

        # Compare expected output XML and output XML
        assert (xmlOutputGenerated.file == xmlOutputExpected.file)


class XmlReader:
    file = ''

    def __init__(self, path_to_dir):
        for file in path_to_dir:
            if os.path.isfile(file):
                f = open(file, 'r')
                self.file = f.read()

    def removeMarkup(self, list_markup):
        for name_markup in list_markup:
            print(f'Before len : {len(self.file)}')
            start_index, end_index = self.findIndexMarkup(name_markup)
            str_to_remove = self.file[start_index:end_index]
            print(f'Removing : {str_to_remove}')
            self.file = self.file.replace(str_to_remove, '')
            print(f'After len : {len(self.file)}')

    def findIndexMarkup(self, name_markup):
        start_index = self.file.find(f'<{name_markup}>')
        end_index = self.file.find(f'</{name_markup}>')
        return start_index, end_index + len(f'</{name_markup}>')
