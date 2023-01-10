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

from roc.dingo.tasks import StoreDelivered
from roc.dingo.models.file import FileLog
from roc.dingo.tests.test_log_file import \
    DingoLogFileTaskTestCase, DingoLogFileTest


# Tests on roc.dingo.tasks.log_file methods
class TestDingoLogFileStoreDelivered(DingoLogFileTaskTestCase):

    @pytest.mark.parametrize(
        'root, delivered_root, data_file, public_data_file, '
        'nb_before, nb_pub_before, nb_stored, nb_removed', [
            ('DATA-1/', 'DELIVERED-1/',
             'roc_data_files_all.dat',
             'roc_data_files_public_filename.dat', 61, 31, 31, 0)])
    def test_store_delivered(
            self, root, delivered_root, data_file, public_data_file,
            nb_before, nb_pub_before, nb_stored, nb_removed):
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
        delivered_root = osp.join(data_test_path, delivered_root)
        args = Namespace(delivered=delivered_root, dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # files with their public_filename
        public_filename = DingoLogFileTest.read_data(public_data_file)
        public_filename = [line.split() for line in public_filename]
        public_filename = {line[0]: line[1] for line in public_filename}

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            if file_log.basename in public_filename:
                file_log.public_filename = public_filename[file_log.basename]
            session.add(file_log)
        session.flush()

        # --- get database entries ---
        db_before = session.query(FileLog).all()
        assert len(db_before) == nb_before

        db_before_pub = session.query(FileLog).\
            filter(FileLog.public_filename.isnot(None)).all()
        assert len(db_before_pub) == nb_pub_before

        # --- initialise task & pipeline --
        self.task = StoreDelivered()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- initialise inputs ---

        # --- run the task ---
        self.run_task()

        # --- get database entries ---
        db_after = session.query(FileLog).filter(
            FileLog.is_delivered == True).all()  # noqa : E712

        # --- get results ---
        store_results = self.task.outputs['store_delivered_results'].data

        # --- make assertions ---

        assert len(db_after) == nb_stored
        assert store_results['files_stored'] == nb_stored
        assert store_results['removed_files'] == nb_removed

        # --- close session
        session.close()
