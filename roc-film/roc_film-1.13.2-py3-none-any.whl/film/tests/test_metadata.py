#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.film plugin.
"""

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
            'Data_version': '01'
                }

        assert set_logical_file_id(meta) == 'solo_L1_rpw-hfr-surv_20220103_V01'
