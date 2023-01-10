#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.dingo plugin.
"""
import pytest
import os.path as osp
from argparse import Namespace
from datetime import datetime

from poppy.core.pipeline import Pipeline
from poppy.core.logger import logger

from roc.dingo.tasks import CheckFileInDb
from roc.dingo.models.file import FileLog
from roc.dingo.tests.test_log_file import \
    DingoLogFileTaskTestCase, DingoLogFileTest


# Tests on roc.dingo.tasks.log_file methods
class TestDingoLogFileCheckFileInDb(DingoLogFileTaskTestCase):

    @pytest.mark.parametrize('root, data_file', [
        ('SK-1/', 'roc_sk_files_1.dat'),
    ])
    def test_check_file_in_db(self, root, data_file):
        """
        Test the DINGO CheckFileInDb task with standard parameters
        Start from an empty database
        Give a roc_data_files list
        All items should be marked as "to insert"
        No items should be marked as "to update"

        :return:
        """

        logger.info('test_check_file_in_db() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)
        dir1 = ['ck', 'fk', 'ik', 'lsk', 'pck', 'sclk', 'spk']

        # --- initialise task & pipeline --
        self.task = CheckFileInDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- initialise inputs ---
        self.task.inputs['roc_data_files'].data = data1.copy()
        self.task.inputs['roc_dir_list'].data = dir1.copy()

        # --- run the task ---
        self.run_task()

        # --- get results ---
        data_to_insert = self.task.outputs['roc_data_files_to_insert'].data
        data_to_update = self.task.outputs['roc_data_files_to_update'].data

        # --- make assertions ---

        assert data_to_insert == data1
        assert data_to_update == {}

        # close session
        session.close()

    @pytest.mark.parametrize('root, data_file', [
        ('SK-1/', 'roc_sk_files_1.dat'),
    ])
    def test_check_file_already_in_db(self, root, data_file):
        """
        Test the DINGO CheckFileInDb task with standard parameters
        Start from an empty database
        Populates it by had with roc_data_files data
        Give a roc_data_files list to the task
        No items should be marked as "to insert"
        No items should be marked as "to update"

        :return:
        """

        logger.info('test_check_file_already_in_db() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)
        dir1 = ['ck', 'fk', 'ik', 'lsk', 'pck', 'sclk', 'spk']

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = CheckFileInDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- initialise inputs ---
        self.task.inputs['roc_data_files'].data = data1.copy()
        self.task.inputs['roc_dir_list'].data = dir1.copy()

        # --- run the task ---
        self.run_task()

        # --- get results ---
        data_to_insert = self.task.outputs['roc_data_files_to_insert'].data
        data_to_update = self.task.outputs['roc_data_files_to_update'].data

        # --- make assertions ---

        assert data_to_insert == {}
        assert data_to_update == {}

        # --- close session
        session.close()

    # run 2 tests : one with date in past, one with date in future
    @pytest.mark.parametrize('root, data_file, file, date', [
        ('SK-1/',
         'roc_sk_files_1.dat',
         'solo_ANC_soc-sclk_20200904_V01.tsc',
         datetime(2000, 1, 1, 0, 0, 0)),
        ('SK-1/',
         'roc_sk_files_1.dat',
         'solo_ANC_soc-sclk_20200904_V01.tsc',
         datetime(2100, 1, 1, 0, 0, 0)),
    ])
    def test_check_file_modified_ctime_in_db(
            self, root, data_file, file, date):
        """
        Test the DINGO CheckFileInDb task with standard parameters
        Start from an empty database
        Populates it by had with roc_data_files data
        Change ctime of an item
        Give a roc_data_files list to the task
        The modified item should be marked as "to update"
        No items should be marked as "to insert"

        :return:
        """

        logger.info('test_check_file_modified_ctime_in_db() ')

        # --- set up arguments ---
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)
        dir1 = ['ck', 'fk', 'ik', 'lsk', 'pck', 'sclk', 'spk']

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = CheckFileInDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        file_to_change = file
        data1[file_to_change]['creation_time'] = date
        item_changed = data1[file_to_change]

        # --- initialise inputs ---
        self.task.inputs['roc_data_files'].data = data1.copy()
        self.task.inputs['roc_dir_list'].data = dir1.copy()

        # --- run the task ---
        self.run_task()

        # --- get results ---
        data_to_insert = self.task.outputs['roc_data_files_to_insert'].data
        data_to_update = self.task.outputs['roc_data_files_to_update'].data

        # --- make assertions ---

        assert data_to_insert == {}
        assert data_to_update == {file_to_change: item_changed}

        # --- close session
        session.close()

    @pytest.mark.parametrize('root, data_file, file', [
        ('SK-1/',
         'roc_sk_files_1.dat',
         'solo_ANC_soc-sclk_20200904_V01.tsc'),
    ])
    def test_check_file_modified_size_in_db(self, root, data_file, file):
        """
        Test the DINGO CheckFileInDb task with standard parameters
        Start from an empty database
        Populates it by had with roc_data_files data
        Change size of an item
        Give a roc_data_files list to the task
        The modified item should be marked as "to update"
        No items should be marked as "to insert"

        :return:
        """

        logger.info('test_check_file_modified_size_in_db() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)
        dir1 = ['ck', 'fk', 'ik', 'lsk', 'pck', 'sclk', 'spk']

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = CheckFileInDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        file_to_change = file
        data1[file_to_change]['size'] = 1
        item_changed = data1[file_to_change]

        # --- initialise inputs ---
        self.task.inputs['roc_data_files'].data = data1.copy()
        self.task.inputs['roc_dir_list'].data = dir1.copy()

        # --- run the task ---
        self.run_task()

        # --- get results ---
        data_to_insert = self.task.outputs['roc_data_files_to_insert'].data
        data_to_update = self.task.outputs['roc_data_files_to_update'].data

        # --- make assertions ---

        assert data_to_insert == {}
        assert data_to_update == {file_to_change: item_changed}

        # --- close session
        session.close()

    @pytest.mark.parametrize('root, data_file, file', [
        ('SK-1/',
         'roc_sk_files_1.dat',
         'solo_ANC_soc-sclk_20200904_V01.tsc'),
    ])
    def test_check_file_modified_dirname_in_db(self, root, data_file, file):
        """
        Test the DINGO CheckFileInDb task with standard parameters
        Start from an empty database
        Populates it by had with roc_data_files data
        Change dirname of an item
        Give a roc_data_files list to the task
        The modified item should be marked as "to update"
        No items should be marked as "to insert"

        :return:
        """

        logger.info('test_check_file_modified_dirname_in_db() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)
        dir1 = ['ck', 'fk', 'ik', 'lsk', 'pck', 'sclk', 'spk']

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = CheckFileInDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        file_to_change = file
        data1[file_to_change]['filepath'] = 'old/' + file_to_change
        item_changed = data1[file_to_change]

        # --- initialise inputs ---
        self.task.inputs['roc_data_files'].data = data1.copy()
        self.task.inputs['roc_dir_list'].data = dir1.copy()

        # --- run the task ---
        self.run_task()

        # --- get results ---
        data_to_insert = self.task.outputs['roc_data_files_to_insert'].data
        data_to_update = self.task.outputs['roc_data_files_to_update'].data

        # --- make assertions ---

        assert data_to_insert == {}
        assert data_to_update == {file_to_change: item_changed}

        # --- close session
        session.close()

    @pytest.mark.parametrize('root, data_file, file', [
        ('SK-1/',
         'roc_sk_files_1.dat',
         'solo_ANC_soc-sclk_20200904_V01.tsc'),
    ])
    def test_check_file_removed(self, root, data_file, file):
        """
        Test the DINGO CheckFileInDb task with standard parameters
        Start from an empty database
        Populates it by had with roc_data_files data
        Delete an item in roc_data_files
        Give a roc_data_files list to the task
        No items should be marked as "to update"
        No items should be marked as "to insert"
        Database should be modified with is_removed

        :return:
        """

        logger.info('test_check_file_removed() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)
        dir1 = ['ck', 'fk', 'ik', 'lsk', 'pck', 'sclk', 'spk']

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = CheckFileInDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        file_to_change = file
        data1.pop(file_to_change)

        # --- initialise inputs ---
        self.task.inputs['roc_data_files'].data = data1.copy()
        self.task.inputs['roc_dir_list'].data = dir1.copy()

        # --- run the task ---
        self.run_task()

        # --- get results ---
        data_to_insert = self.task.outputs['roc_data_files_to_insert'].data
        data_to_update = self.task.outputs['roc_data_files_to_update'].data

        # --- make assertions ---

        assert data_to_insert == {}
        assert data_to_update == {}

        results = session.query(FileLog).filter(
            FileLog.basename == file_to_change)
        for item in results:
            assert item.is_removed

        # --- close session
        session.close()

    @pytest.mark.parametrize('root, data_file, file', [
        ('SK-1/',
         'roc_sk_files_1.dat',
         'solo_ANC_soc-sclk_20200904_V01.tsc'),
    ])
    def test_check_file_not_removed(self, root, data_file, file):
        """
        Test the DINGO CheckFileInDb task with standard parameters
        Start from an empty database
        Populates it by had with roc_data_files data
        Mark an item as removed in db
        Give a roc_data_files list to the task
        No items should be marked as "to update"
        No items should be marked as "to insert"
        Item should be modified with is_removed=False

        :return:
        """

        logger.info('test_check_file_not_removed() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)
        dir1 = ['ck', 'fk', 'ik', 'lsk', 'pck', 'sclk', 'spk']

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            # mark the file as removed
            if file_log.basename == file:
                file_log.is_removed = True
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = CheckFileInDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- initialise inputs ---
        self.task.inputs['roc_data_files'].data = data1.copy()
        self.task.inputs['roc_dir_list'].data = dir1.copy()

        # --- run the task ---
        self.run_task()

        # --- get results ---
        data_to_insert = self.task.outputs['roc_data_files_to_insert'].data
        data_to_update = self.task.outputs['roc_data_files_to_update'].data

        # --- make assertions ---

        assert data_to_insert == {}
        assert data_to_update == {}

        # --- close session
        session.close()

    @pytest.mark.parametrize('root, data_file', [
        ('SK-1/', 'roc_sk_files_1.dat'),
    ])
    def test_check_file_force(self, root, data_file):
        """
        Test the DINGO CheckFileInDb task with "force" parameter
        Start from an empty database
        Populates it by had with roc_data_files data
        Give a roc_data_files list to the task
        All items should be marked as "to update"
        No items should be marked as "to insert"

        :return:
        """

        logger.info('test_check_file_force() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, force=True, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)
        dir1 = ['ck', 'fk', 'ik', 'lsk', 'pck', 'sclk', 'spk']

        # populate database
        for item in data1:
            data = data1[item]
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            session.add(file_log)
        session.flush()

        # --- initialise task & pipeline --
        self.task = CheckFileInDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- initialise inputs ---
        self.task.inputs['roc_data_files'].data = data1.copy()
        self.task.inputs['roc_dir_list'].data = dir1.copy()

        # --- run the task ---
        self.run_task()

        # --- get results ---
        data_to_insert = self.task.outputs['roc_data_files_to_insert'].data
        data_to_update = self.task.outputs['roc_data_files_to_update'].data

        # --- make assertions ---

        assert data_to_insert == {}
        assert data_to_update == data1

        # --- close session
        session.close()
