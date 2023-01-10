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

from roc.dingo.tasks import StorePublicFilename
from roc.dingo.models.file import FileLog
from roc.dingo.tests.test_log_file import \
    DingoLogFileTaskTestCase, DingoLogFileTest


# Tests on roc.dingo.tasks.log_file methods
class TestDingoLogFileStorePublicFilename(DingoLogFileTaskTestCase):

    @pytest.mark.parametrize(
        'root, public_root, data_file, expected_result, '
        'nb_before, nb_stored, nb_added', [
            ('DATA-1/', 'PUBLIC-1/',
             'roc_data_files_all.dat',
             'roc_data_files_public_filename.dat', 61, 76, 45)])
    def test_store_public_filename(
            self, root, public_root, data_file, expected_result,
            nb_before, nb_stored, nb_added):
        """
        Start from an empty database
        populates it by hand with files from data_file
        Launch task and check result

        :return:
        """

        logger.info('test_store_public_filename() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        public_root = osp.join(data_test_path, public_root)
        args = Namespace(public=public_root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            session.add(file_log)
        session.flush()

        # --- get database entries ---
        db_before = session.query(FileLog).all()
        assert len(db_before) == nb_before

        # files with their public_filename
        public_filename = DingoLogFileTest.read_data(expected_result)
        public_filename = [line.split() for line in public_filename]
        public_filename = {line[0]: line[1] for line in public_filename}

        # --- initialise task & pipeline --
        self.task = StorePublicFilename()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- initialise inputs ---

        # --- run the task ---
        self.run_task()

        # --- get database entries ---
        db_after = session.query(FileLog).filter(
            FileLog.public_filename.isnot(None)).all()

        # --- get results ---
        store_results = self.task.outputs['store_public_filename_results'].data

        # --- make assertions ---
        for r in db_after:
            assert r.basename in public_filename
            assert public_filename[r.basename] == r.public_filename

        assert len(db_after) == len(public_filename)

        assert store_results['files_stored'] == nb_stored
        assert store_results['files_added'] == nb_added

        # --- close session
        session.close()
