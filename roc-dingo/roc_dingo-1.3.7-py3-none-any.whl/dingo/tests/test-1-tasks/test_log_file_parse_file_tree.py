#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.dingo plugin.
"""
import pytest
import os.path as osp
from argparse import Namespace

from poppy.core.pipeline import Pipeline
from poppy.core.logger import logger

from roc.dingo.tests.test_log_file import \
    DingoLogFileTaskTestCase, DingoLogFileTest


# Tests on roc.dingo.tasks methods
class TestDingoLogFileParseFileTree(DingoLogFileTaskTestCase):

    @pytest.mark.parametrize('root, dir_file, expected_data_file', [
        ('DATA-1/', 'roc_dir_list_all.dat', 'roc_data_files_all.dat'),
    ])
    def test_parse_file_tree(self, root, dir_file, expected_data_file):
        """
        Test the DINGO ParseFileTree task with standard parameters

        :return:
        """

        # --- initialize the task ---
        from roc.dingo.tasks import ParseFileTree

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- initialise task & pipeline --
        self.task = ParseFileTree()
        self.task.pipeline = Pipeline(args)

        # --- run the task ---
        self.task.instantiate_targets()
        self.run_task()

        # --- get results ---
        roc_dir_list = self.task.outputs['roc_dir_list'].data
        roc_data_files = self.task.outputs['roc_data_files'].data

        # --- make assertions ---
        # --- DIR LIST ---

        # open the dir_list file with data for test
        roc_dir_list_all = DingoLogFileTest.read_data(dir_file)

        # check content
        assert roc_dir_list == roc_dir_list_all, \
            'dir list is not the one expected'

        # --- FILE LIST ---
        # read expected data
        expected_data = DingoLogFileTest.open_test_data(
            expected_data_file, root)

        # compare results with expected data
        DingoLogFileTest.compare_data_to_expected(
            expected_data, roc_data_files)

    @pytest.mark.parametrize('root, date, dir_file, expected_data_file', [
        ('DATA-1/',
         '2020/08/19',
         'roc_dir_list_2020_08_19.dat',
         'roc_data_files_2020_08_19.dat'),
    ])
    def test_parse_file_tree_with_day_date(
            self, root, date, dir_file, expected_data_file):
        """
        Test the DINGO ParseFileTree task with a day date parameter
        All files set in a month or mission basis should be excluded
        :return:
        """

        # --- initialize the task ---
        from roc.dingo.tasks import ParseFileTree

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, date=date, dry_run=False)

        # --- initialise task & pipeline --
        self.task = ParseFileTree()
        self.task.pipeline = Pipeline(args)

        # --- run the task ---
        self.task.instantiate_targets()
        self.run_task()

        # --- get results ---
        roc_dir_list = self.task.outputs['roc_dir_list'].data
        roc_data_files = self.task.outputs['roc_data_files'].data

        logger.debug('--- results ---')
        logger.debug(len(roc_data_files))
        for key, item in roc_data_files.items():
            logger.debug(item['filepath'].replace(root, ''))

        # --- make assertions ---
        # --- DIR LIST ---

        # open the dir_list file with data for test
        roc_dir_list_all = DingoLogFileTest.read_data(dir_file)

        # check content
        assert roc_dir_list == roc_dir_list_all, \
            'dir list is not the one expected'

        # --- FILE LIST ---
        # read expected data
        expected_data = DingoLogFileTest.open_test_data(
            expected_data_file, root)

        # compare resulsts with expected data
        DingoLogFileTest.compare_data_to_expected(
            expected_data, roc_data_files)

    @pytest.mark.parametrize('root, date, dir_file', [
        ('DATA-1/',
         '2020/08/18',
         'roc_dir_list_2020_08_18.dat'),
    ])
    def test_parse_file_tree_with_another_day_date(
            self, root, date, dir_file):
        """
        Test the DINGO ParseFileTree task with a another day date parameter
        File list should be empty
        :return:
        """

        # --- initialize the task ---
        from roc.dingo.tasks import ParseFileTree

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, date=date, dry_run=False)

        # --- initialise task & pipeline --
        self.task = ParseFileTree()
        self.task.pipeline = Pipeline(args)

        # --- run the task ---
        self.task.instantiate_targets()
        self.run_task()

        # --- get results ---
        roc_dir_list = self.task.outputs['roc_dir_list'].data
        roc_data_files = self.task.outputs['roc_data_files'].data

        logger.debug('--- results ---')
        logger.debug(len(roc_data_files))
        for key, item in roc_data_files.items():
            logger.debug(item['filepath'].replace(root, ''))

        # --- make assertions ---
        # --- DIR LIST ---

        # open the dir_list file with data for test
        roc_dir_list_all = DingoLogFileTest.read_data(dir_file)

        # check content
        assert roc_dir_list == roc_dir_list_all, \
            'dir list is not the one expected'

        # --- FILE LIST ---
        # read expected data
        expected_data = {}

        # compare resulsts with expected data
        DingoLogFileTest.compare_data_to_expected(
            expected_data, roc_data_files)

    @pytest.mark.parametrize('root, date, dir_file, expected_data_file', [
        ('DATA-1/',
         '2020/08',
         'roc_dir_list_2020_08.dat',
         'roc_data_files_2020_08.dat'),
    ])
    def test_parse_file_tree_with_month_date(
            self, root, date, dir_file, expected_data_file):
        """
        Test the DINGO ParseFileTree task with a month date parameter
        All files set in the mission basis should be excluded
        :return:
        """

        # --- initialize the task ---
        from roc.dingo.tasks import ParseFileTree

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, date=date, dry_run=False)

        # --- initialise task & pipeline --
        self.task = ParseFileTree()
        self.task.pipeline = Pipeline(args)

        # --- run the task ---
        self.task.instantiate_targets()
        self.run_task()

        # --- get results ---
        roc_dir_list = self.task.outputs['roc_dir_list'].data
        roc_data_files = self.task.outputs['roc_data_files'].data

        logger.debug('--- results ---')
        logger.debug(len(roc_data_files))
        for key, item in roc_data_files.items():
            logger.debug(item['filepath'].replace(root, ''))

        # --- make assertions ---
        # --- DIR LIST ---

        # open the dir_list file with data for test
        roc_dir_list_all = DingoLogFileTest.read_data(dir_file)

        # check content
        assert roc_dir_list == roc_dir_list_all, \
            'dir list is not the one expected'

        # --- FILE LIST ---
        # read expected data
        expected_data = DingoLogFileTest.open_test_data(
            expected_data_file, root)

        # compare resulsts with expected data
        DingoLogFileTest.compare_data_to_expected(
            expected_data, roc_data_files)

    @pytest.mark.parametrize('root, expected_data_file', [
        ('DATA-1/', 'roc_data_files_all.dat')
    ])
    def test_parse_file_tree_nf(self, root, expected_data_file):
        """
        Test the DINGO ParseFileTree task with the option -nf
        files from "former_versions" should be excluded

        :return:
        """

        # --- initialize the task ---
        from roc.dingo.tasks import ParseFileTree

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, no_former_versions=True, dry_run=False)

        # --- initialise task & pipeline --
        self.task = ParseFileTree()
        self.task.pipeline = Pipeline(args)

        # --- run the task ---
        self.task.instantiate_targets()
        self.run_task()

        # --- get results ---
        roc_data_files = self.task.outputs['roc_data_files'].data

        # --- make assertions ---
        # useless to test directory here
        # --- FILE LIST ---
        expected_data = DingoLogFileTest.open_test_data(
            expected_data_file, root)
        # remove "former_versions" items
        for key, item in expected_data.copy().items():
            if 'former_versions' in item['filepath']:
                expected_data.pop(key)

        # compare resulsts with expected data
        DingoLogFileTest.compare_data_to_expected(
            expected_data, roc_data_files)

    @pytest.mark.parametrize('root, expected_data_file', [
        ('SK-1/', 'roc_sk_files_1.dat'),
    ])
    def test_parse_file_tree_sk(self, root, expected_data_file):
        """
        Test the DINGO ParseFileTree task for spice kernels

        :return:
        """

        # --- initialize the task ---
        from roc.dingo.tasks import ParseFileTree

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, level='SK', dry_run=False)

        # --- initialise task & pipeline --
        self.task = ParseFileTree()
        self.task.pipeline = Pipeline(args)

        # --- run the task ---
        self.task.instantiate_targets()
        self.run_task()

        # --- get results ---
        roc_dir_list = self.task.outputs['roc_dir_list'].data
        roc_data_files = self.task.outputs['roc_data_files'].data

        # --- make assertions
        # --- DIR LIST ---
        roc_dir_list_all = ['ck', 'fk', 'ik', 'lsk', 'pck', 'sclk', 'spk']
        assert roc_dir_list == roc_dir_list_all, \
            'dir list is not the one expected'

        # --- FILES LIST ---
        # read expected data
        expected_data = DingoLogFileTest.open_test_data(
            expected_data_file, root)

        # compare resulsts with expected data
        DingoLogFileTest.compare_data_to_expected(
            expected_data, roc_data_files)
