#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test dds_to_tm command of the roc.film plugin.
"""

import filecmp
import os
import tempfile
from pprint import pformat

import pytest
import shutil
import unittest.mock as mock

from poppy.core.logger import logger
from poppy.core.test import CommandTestCase
from roc.film.tests.test_film import FilmTest


class TestDdsToTm(CommandTestCase):
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
    ])
    def test_classify_tmraw(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # input_dir_path, inputs = self.get_inputs('classify_tmraw')
        # expected_output_dir_path, expected_outputs = self.get_expected_outputs('classify_tmraw')
        #
        # generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        # os.makedirs(generated_output_dir_path, exist_ok=True)
        #
        # # initialize the main command
        # main_command = ['pop', 'film',
        #                 'classify_tmraw',
        #                 '--dds-files',
        #                 ' '.join([
        #                     os.path.join(input_dir_path, input_file)
        #                     for input_file in inputs]),
        #                 '--output-dir', generated_output_dir_path,
        #                 '-ll', 'INFO']
        #
        # # define the required plugins
        # plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.dingo' ,'roc.film']
        #
        # # run the command
        # # force the value of the plugin list
        # with mock.patch.object(Settings, 'configure',
        #                        autospec=True,
        #                        side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
        #     self.run_command('pop db upgrade heads -ll INFO')
        #     self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
        #     self.run_command(main_command)
        #
        # # compare directory content
        # dirs_cmp = filecmp.dircmp(generated_output_dir_path,
        #                           expected_output_dir_path)
        #
        # dirs_cmp.report()
        #
        # # ensure that we have the same files in both directories
        # assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)
        #
        # for filename in self.get_diff_files(dirs_cmp):
        #     # compare only xml files with differences
        #     if filename.endswith('.xml'):
        #         # use cdf compare to compute the differences between expected output and the command output
        #         result = filecmp.cmpfiles(
        #             os.path.join(generated_output_dir_path, filename),
        #             os.path.join(expected_output_dir_path, filename),
        #         )
        #         # compare the difference dict with the expected one
        #         if result:
        #             logger.error(f'Differences between expected output and the command output: {pformat(result)}')
        #
        #         assert result == {}
