#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.dingo plugin.
"""
import pytest
import tempfile
import shutil
import os.path as osp
from os import listdir
from roc.dingo.models.file import FileLog
from roc.dingo.tests.test_log_file import \
    DingoLogFileCommandTestCase, DingoLogFileTest


# Tests on roc.dingo.tasks.log_file methods
class TestDingoStoreDelivered(DingoLogFileCommandTestCase):

    def setup_method(self, method):
        super().setup_method(method)

        # empty the database
        self.session.query(FileLog).delete()
        self.session.flush()

    def teardown_method(self, method):
        super().teardown_method(method)

        # close database
        self.session.close()

    @pytest.mark.parametrize(
        'root, public_root, delivered_root, remove_files, '
        'nb_files_after_logfile_to_rocdb, '
        'nb_files_after_store_delivered, '
        'nb_public_files, nb_delivered_files', [
            ('DATA-1', 'PUBLIC-1', 'DELIVERED-1', True, 61, 106, 76, 72),
            ('DATA-1', 'PUBLIC-1', 'DELIVERED-1', False, 61, 106, 76, 72),
        ])
    def test_store_delivered(self,
                             root,
                             public_root,
                             delivered_root,
                             remove_files,
                             nb_files_after_logfile_to_rocdb,
                             nb_files_after_store_delivered,
                             nb_public_files,
                             nb_delivered_files):
        """
        Insert dataset with logfile_to_rocdb and store delivered file after
        """
        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)
        public_root = osp.join(data_test_path, public_root)
        delivered_root = osp.join(data_test_path, delivered_root)

        # --- initialize the Db with files from DATA-1 ---
        main_command = ['pop',
                        'dingo',
                        'logfile_to_rocdb',
                        '--root',
                        root
                        ]

        # --- run the command ---
        self.run_command(main_command)

        results = self.session.query(FileLog).all()
        assert len(results) == nb_files_after_logfile_to_rocdb

        # No files should be tagged is_removed
        results = self.session.query(FileLog).\
            filter(FileLog.is_removed == True).all()  # noqa: E712
        assert len(results) == 0

        # As the store_delivered command will delete file,
        # copy the folder to a tmp one

        tmp_delivered_root = tempfile.mkdtemp()
        for f in listdir(delivered_root):
            shutil.copy(osp.join(delivered_root, f), tmp_delivered_root)

        # Check the copy
        results = listdir(tmp_delivered_root)
        assert len(results) == nb_delivered_files

        # --- insert delivered data ---
        main_command = ['pop',
                        'dingo',
                        'store_delivered',
                        '--public',
                        public_root,
                        '--delivered',
                        tmp_delivered_root
                        ]

        if remove_files:
            main_command += ['--remove_files']

        # --- run the command ---
        self.run_command(main_command)

        # --- make assertions ---

        # Nb files after store_delivered
        results = self.session.query(FileLog).all()
        assert len(results) == nb_files_after_store_delivered

        # All the files added should be tagged is_removed
        results = self.session.query(FileLog).\
            filter(FileLog.is_removed == True).all()  # noqa: E712
        assert len(results) == \
            nb_files_after_store_delivered - nb_files_after_logfile_to_rocdb

        # Check the nb of files with a public file mentionned
        results = self.session.query(FileLog).\
            filter(FileLog.public_filename.isnot(None)).all()
        assert len(results) == nb_public_files

        # Check the nb of delivered files
        results = self.session.query(FileLog).\
            filter(FileLog.is_delivered == True).all()  # noqa: E712
        assert len(results) == nb_delivered_files

        # Check all the delivered files have been removed
        # if remove_files has been set
        results = listdir(tmp_delivered_root)
        if remove_files:
            assert len(results) == 0
        else:
            assert len(results) == nb_delivered_files

        # remove temporary directory
        shutil.rmtree(tmp_delivered_root)

        self.session.close()
