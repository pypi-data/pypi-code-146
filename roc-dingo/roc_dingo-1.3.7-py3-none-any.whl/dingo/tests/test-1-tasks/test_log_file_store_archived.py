#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.dingo plugin.
"""
import pytest
import os.path as osp
from random import randrange, sample
from argparse import Namespace
from unittest import mock

from poppy.core.pipeline import Pipeline
from poppy.core.logger import logger

from roc.dingo.tasks import CheckSOARDataAvailability
from roc.dingo.models.file import FileLog
from roc.dingo.tests.test_log_file import \
    DingoLogFileTaskTestCase, DingoLogFileTest


# Tests on roc.dingo.tasks.log_file methods
class TestDingoLogFileCheckSOARDataAvailability(DingoLogFileTaskTestCase):

    @mock.patch(
        'roc.dingo.tasks.CheckSOARDataAvailability.soar_run_query')
    @pytest.mark.parametrize(
        'root, data_file, public_data_file, nb_to_archive', [
            ('DATA-1/', 'roc_data_files_all.dat',
             'roc_data_files_public_filename.dat', 31)])
    def test_store_archived(
            self, mock_query, root, data_file, public_data_file,
            nb_to_archive):
        """
        Start from an empty database
        populates it by hand with files from data_file
        and public filename from public_data_file
        mock the respone from the TAP service

        :return:
        """

        logger.info('test_store_archived() ')

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        args = Namespace(url='fakeurl', dry_run=False)

        # --- database setup ---
        session = DingoLogFileTest.setup_session()

        # --- define data test --
        data1 = DingoLogFileTest.open_test_data(data_file, root)

        # files with their public_filename
        public_filename = DingoLogFileTest.read_data(public_data_file)
        public_filename = [line.split() for line in public_filename]
        public_filename = {line[0]: line[1] for line in public_filename}
        delivered_files = []

        # populate database
        for item, data in data1.items():
            file_log = DingoLogFileTest.data_to_file_log(data, root)
            if file_log.basename in public_filename:
                file_log.public_filename = public_filename[file_log.basename]
                file_log.is_delivered = True
                delivered_files.append([file_log.public_filename])

            session.add(file_log)
        session.flush()

        # --- get database entries ---
        db_before = session.query(FileLog).filter(
            FileLog.public_filename.isnot(None)).all()

        # create the mocked response from the TAP service
        fake_nb_archived = randrange(len(delivered_files))
        fake_archived = {'data': sample(delivered_files, fake_nb_archived)}

        # --- define mock session result
        mock_query.return_value = fake_archived

        # --- initialise task & pipeline --
        self.task = CheckSOARDataAvailability()
        self.task.pipeline = Pipeline(args)
        self.task.instantiate_targets()
        self.task.session = session

        # --- initialise inputs ---

        # --- run the task ---
        self.run_task()

        # --- get database entries ---
        db_after = session.query(FileLog).filter(
            FileLog.is_archived == True).all()  # noqa : E712

        # --- get results ---
        store_results = self.task.outputs['store_archived'].data

        # --- make assertions ---

        assert len(db_before) == nb_to_archive
        assert len(db_after) == fake_nb_archived
        assert store_results['files_to_archive'] == nb_to_archive
        assert store_results['files_archived'] == fake_nb_archived

        # --- close session
        session.close()
