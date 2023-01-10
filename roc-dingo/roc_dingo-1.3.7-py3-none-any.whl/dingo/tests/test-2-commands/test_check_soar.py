#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.dingo plugin.
"""
import pytest
import os.path as osp
from roc.dingo.models.file import FileLog
from roc.dingo.tests.test_log_file import \
    DingoLogFileCommandTestCase, DingoLogFileTest


# Tests on roc.dingo.tasks.log_file methods
class TestDingoCheckSoar(DingoLogFileCommandTestCase):

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
        'root, public_root, delivered_root, nb_archived_files', [
            ('DATA-1', 'PUBLIC-1', 'DELIVERED-1', 72),
        ])
    def test_check_soar(self,
                        root,
                        public_root,
                        delivered_root,
                        nb_archived_files):
        """
        Insert dataset with logfile_to_rocdb, store delivered file,
        and after check the SOAR report
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

        # --- insert delivered data ---
        main_command = ['pop',
                        'dingo',
                        'store_delivered',
                        '--public',
                        public_root,
                        '--delivered',
                        delivered_root
                        ]

        # --- run the command ---
        self.run_command(main_command)

        # --- check for SOAR data availability ---
        main_command = ['pop',
                        'dingo',
                        'check_soar'
                        ]

        # --- run the command ---
        self.run_command(main_command)

        # --- make assertions ---

        # Count the is_archived files
        results = self.session.query(FileLog).\
            filter(FileLog.is_archived == True).all()  # noqa: E712

        assert len(results) == nb_archived_files

        self.session.close()
