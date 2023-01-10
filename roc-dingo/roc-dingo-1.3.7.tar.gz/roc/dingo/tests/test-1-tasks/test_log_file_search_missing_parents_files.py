#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.dingo plugin.
"""
import pytest
import os.path as osp
from random import sample, randrange
from argparse import Namespace

from poppy.core.pipeline import Pipeline
from poppy.core.logger import logger

from roc.dingo.tests.test_log_file import \
    DingoLogFileTaskTestCase, DingoLogFileTest
from roc.dingo.tasks import SearchMissingParentsFiles


# Tests on roc.dingo.tasks.log_file methods
class TestDingoLogFileSearchMissingParentsFiles(DingoLogFileTaskTestCase):

    @pytest.mark.parametrize('root, data_file, expected_missing_parents', [
        ('DATA-1/',
         'roc_data_files_all.dat',
         'roc_data_files_missing_parents.dat'),
    ])
    def test_search_missing_parents(
            self, root, data_file, expected_missing_parents):
        """
        Test the DINGO SearchMissingParentsFiles task with standard parameters

        :return:
        """

        logger.info('test_search_missing_parents() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # files marked with Missing parents
        missing = DingoLogFileTest.read_data(expected_missing_parents)

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            if item in missing:
                file_log.error_log = 'Missing parents : xxx, yyy'
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = SearchMissingParentsFiles()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- run the task ---
        self.run_task()

        # --- get results ---
        roc_files_update = self.task.outputs['roc_data_files_to_update'].data
        roc_files_insert = self.task.outputs['roc_data_files_to_insert'].data

        # --- make assertions ---

        # in any case roc_files_insert should be empty
        assert roc_files_insert == {}

        # read expected data
        expected_data = missing

        # compare resulsts with expected data
        assert len(expected_data) == len(roc_files_update)
        for item in roc_files_update:
            assert item in expected_data

        session.close()

    @pytest.mark.parametrize('root, data_file, expected_missing_parents', [
        ('DATA-1/',
         'roc_data_files_all.dat',
         'roc_data_files_missing_parents.dat'),
    ])
    def test_search_missing_parents_not_removed(
            self, root, data_file, expected_missing_parents):
        """
        Test the DINGO SearchMissingParentsFiles task with standard parameters
        mark some files as removed.
        They should not be returned as "to be updated"

        :return:
        """

        logger.info('test_search_missing_parents() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # files marked with Missing parents
        missing = DingoLogFileTest.read_data(expected_missing_parents)

        # mark some data as removed
        nb_removed = randrange(len(missing))
        logger.debug('Nb removed = {}'.format(nb_removed))
        removed = sample(missing, nb_removed)
        logger.debug('Removed = {}'.format(removed))

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            if item in missing:
                file_log.error_log = 'Missing parents : xxx, yyy'
            if item in removed:
                file_log.is_removed = True
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = SearchMissingParentsFiles()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- run the task ---
        self.run_task()

        # --- get results ---
        roc_files_update = self.task.outputs['roc_data_files_to_update'].data
        roc_files_insert = self.task.outputs['roc_data_files_to_insert'].data

        # --- make assertions ---

        # in any case roc_files_insert should be empty
        assert roc_files_insert == {}

        # set expected data
        expected_data = [value for value in missing if value not in removed]

        # compare resulsts with expected data
        assert len(roc_files_update) == len(expected_data)
        for item in roc_files_update:
            assert item in expected_data

        session.close()
