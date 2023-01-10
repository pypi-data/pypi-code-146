#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.dingo plugin.
"""
import pytest
import os.path as osp
import yaml
from argparse import Namespace

from poppy.core.pipeline import Pipeline
from poppy.core.logger import logger

from roc.dingo.tasks import LogFileToDb
from roc.dingo.models.file import FileLog
from roc.dingo.tests.test_log_file import \
    DingoLogFileTaskTestCase, DingoLogFileTest


# Tests on roc.dingo.tasks.log_file methods
class TestDingoLogFileToDb(DingoLogFileTaskTestCase):

    @pytest.mark.parametrize('root, data_file, expected_data_dump', [
        ('DATA-1/', 'roc_data_files_all.dat', 'roc_data_files_all_dump.yml'),
    ])
    def test_log_file_to_db(self, root, data_file, expected_data_dump):
        """
        Test the DINGO ogFileToDb task with standard parameters
        Start from an empty database
        Give a roc_data_files list
        All items should be inserted

        :return:
        """

        logger.info('test_log_file_to_db() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # --- initialise task & pipeline --
        self.task = LogFileToDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- initialise inputs ---
        self.task.inputs['roc_data_files_to_insert'].data = data1.copy()

        self.task.inputs['roc_data_files_to_update'].data = {}
        self.task.inputs['roc_data_files_to_update'].is_empty = True

        # --- run the task ---
        self.run_task()

        # --- get results ---
        results = session.query(FileLog).all()

        # --- read expected data
        path = osp.abspath(osp.dirname(__file__))
        path = osp.join(path, '../data-tasks', expected_data_dump)
        with open(path) as f:
            expected_data = yaml.load(f, Loader=yaml.FullLoader)

        # --- make assertions ---
        # all files should have been inserted
        assert len(results) == len(expected_data)

        for item in results:
            assert item.basename in expected_data
            assert item.as_dict() == expected_data[item.basename]

        # --- close session
        session.close()

    @pytest.mark.parametrize('root, data_file, expected_data_dump', [
        ('SK-1/', 'roc_sk_files_1.dat', 'roc_sk_files_1_dump.yml'),
    ])
    def test_log_file_sk_to_db(self, root, data_file, expected_data_dump):
        """
        Test the DINGO LogFileToDb task with standard parameters
        Start from an empty database
        Give a roc_data_files spice kernel list
        All items should be inserted

        :return:
        """

        logger.info('test_log_file_sk_to_db() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # --- initialise task & pipeline --
        self.task = LogFileToDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- initialise inputs ---
        self.task.inputs['roc_data_files_to_insert'].data = data1.copy()

        self.task.inputs['roc_data_files_to_update'].data = {}
        self.task.inputs['roc_data_files_to_update'].is_empty = True

        # --- run the task ---
        self.run_task()

        # --- get results ---
        results = session.query(FileLog).filter(FileLog.level == 'SK').all()

        # --- read expected data
        path = osp.abspath(osp.dirname(__file__))
        path = osp.join(path, '../data-tasks', expected_data_dump)
        with open(path) as f:
            expected_data = yaml.load(f, Loader=yaml.FullLoader)

        # --- make assertions ---
        # all files should have been inserted
        assert len(results) == len(expected_data)

        for item in results:
            assert item.basename in expected_data
            assert item.as_dict() == expected_data[item.basename]

        # --- close session
        session.close()

    @pytest.mark.parametrize('root, data_file, file, old_file', [
        ('DATA-1/',
         'roc_data_files_2020_08_19.dat',
         'solo_L1_rpw-lfr-surv-bp1-cdag_20200819_V07.cdf',
         'solo_L1_rpw-lfr-surv-bp1-cdag_20200819_V06.cdf'),
    ])
    def test_add_file_with_old_version_removed(
            self, root, data_file, file, old_file):
        """
        https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO/-/issues/23
        Some files are removed but still indicated as latest

        Test the DINGO CheckFileInDb task with standard parameters
        Start from an empty database
        Populates it by hand with roc_data_files data
        Remove a file from the list
        Start the task
        Removed file is flagged as removed but still latest
        Give a new data file containing a new version of the file removed
        The removed version should be flagged as not latest

        :return:
        """

        logger.info('test_add_file_with_old_version_removed() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(root=root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # replace the old file by the new file
        item = data1.pop(file)
        item['filepath'] = item['filepath'].replace(file, old_file)
        data1[old_file] = item

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            # mark the old file as removed
            if file_log.basename == old_file:
                file_log.is_removed = True
            session.add(file_log)
        session.flush()

        # new file has to be inserted
        item = data1.pop(old_file)
        item['filepath'] = item['filepath'].replace(old_file, file)
        data2 = {}
        data2[file] = item

        # --- initialise task & pipeline --
        self.task = LogFileToDb()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- initialise inputs ---
        self.task.inputs['roc_data_files_to_insert'].data = data2.copy()

        self.task.inputs['roc_data_files_to_update'].data = {}
        self.task.inputs['roc_data_files_to_update'].is_empty = True

        # --- run the task ---
        self.run_task()

        results = session.query(FileLog).filter(
            FileLog.basename == file)
        for item in results:
            assert not item.is_removed
            assert item.is_latest

        results = session.query(FileLog).filter(
            FileLog.basename == old_file)
        for item in results:
            assert item.is_removed
            assert not item.is_latest

        # --- close session
        session.close()
