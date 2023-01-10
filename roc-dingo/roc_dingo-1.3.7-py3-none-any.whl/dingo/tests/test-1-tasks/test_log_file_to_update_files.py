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

from roc.dingo.models.file import FileLog
from roc.dingo.tests.test_log_file import \
    DingoLogFileTaskTestCase, DingoLogFileTest
from roc.dingo.tasks import SearchForUpdate


# Tests on roc.dingo.tasks.log_file methods
class TestDingoLogFileSearchForUpdate(DingoLogFileTaskTestCase):

    @pytest.mark.parametrize('root, data_file', [
        ('DATA-1/',
         'roc_data_files_all.dat'),
    ])
    def test_search_files_to_update(
            self, root, data_file):
        """
        Test the DINGO SearchForUpdate task with standard parameters

        :return:
        """

        logger.info('test_search_for_update() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # mark some files to be updated
        nb_to_update = randrange(len(data1))
        logger.debug('Nb to update = {}'.format(nb_to_update))
        to_update = sample(list(data1), nb_to_update)
        logger.debug('To update = {}'.format(nb_to_update))

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            if item in to_update:
                file_log.to_update = True
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = SearchForUpdate()
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

        # compare results with expected data
        assert len(roc_files_update) == nb_to_update
        for item in roc_files_update:
            assert item in to_update

        session.close()

    @pytest.mark.parametrize('root, data_file, missing_file_data', [
        ('DATA-1/',
         'roc_data_files_all.dat',
         'roc_data_old_removed_file.dat'),
    ])
    def test_with_missing_file(
            self, root, data_file, missing_file_data):
        """
        Test the DINGO SearchForUpdate task with a missing file

        :return:
        """

        logger.info('test_search_for_update() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            session.add(file_log)
        session.flush()

        # add a file in DB that will miss in FS
        # read the object and insert in DB
        # it has to_update = true and is not in FS
        data2 = DingoLogFileTest.open_test_data(missing_file_data, root)
        old_file_name = list(data2)[0]
        item = data2[old_file_name]

        old_file = DingoLogFileTest.data_to_file_log(item, root)
        old_file.to_update = True

        assert not old_file.is_removed

        session.add(old_file)
        session.flush()

        # --- initialise task & pipeline --
        self.task = SearchForUpdate()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- run the task ---
        self.run_task()

        # --- get results ---
        roc_files_update = self.task.outputs['roc_data_files_to_update'].data
        roc_files_insert = self.task.outputs['roc_data_files_to_insert'].data

        # --- make assertions ---

        # both case roc_files_insert and roc_files_update should be empty
        assert roc_files_insert == {}
        assert roc_files_update == {}

        # also check that is has been flagged as removed
        new_item = session.query(FileLog).filter(
            FileLog.basename == old_file_name).one()

        assert new_item.is_removed
        assert new_item.state == 'OK'
        assert new_item.error_log is None
        assert not new_item.to_update

        session.close()

    @pytest.mark.parametrize('root, data_file', [
        ('DATA-1/',
         'roc_data_files_all.dat'),
    ])
    def test_with_no_update(
            self, root, data_file):
        """
        Test the DINGO SearchForUpdate task with no files to update

        :return:
        """

        logger.info('test_search_for_update() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = SearchForUpdate()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- run the task ---
        self.run_task()

        # --- get results ---
        roc_files_update = self.task.outputs['roc_data_files_to_update']
        roc_files_insert = self.task.outputs['roc_data_files_to_insert']

        # --- make assertions ---

        # in any case roc_files_insert should be empty
        assert roc_files_insert.data == {}
        assert roc_files_update.data == {}

        assert roc_files_insert.is_empty is True
        assert roc_files_update.is_empty is True

        session.close()
