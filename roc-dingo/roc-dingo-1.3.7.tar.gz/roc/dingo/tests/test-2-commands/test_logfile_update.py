#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.dingo plugin.
"""
import pytest
import os.path as osp
from roc.dingo.models.file import FileLog
from roc.dingo.tests.test_dingo import DingoTest
from roc.dingo.tests.test_log_file import \
    DingoLogFileCommandTestCase, DingoLogFileTest


# Tests on roc.dingo.tasks.log_file methods
class TestDingoLogFileUpdate(DingoLogFileCommandTestCase):

    def setup_method(self, method):
        super().setup_method(method)

        # empty the database
        self.session.query(FileLog).delete()
        self.session.flush()

    def teardown_method(self, method):
        super().teardown_method(method)

        # close database
        self.session.close()

    @pytest.mark.parametrize('root, nb_files, file_to_update', [
        ('DATA-1', 61, 'solo_L1_rpw-hfr-surv-cdag_20200819_V07.cdf'),
    ])
    def test_logfile_update(self, root, nb_files, file_to_update):
        """
        After data insertion, modify file_to_update and test its update
        """
        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)

        # --- initialize the command ---
        main_command = ['pop',
                        'dingo',
                        'logfile_to_rocdb',
                        '--root', root
                        ]

        # --- run the command ---
        self.run_command(main_command)

        results = self.session.query(FileLog).all()
        assert len(results) == nb_files

        # modify DB to mark a file to be updated
        # and set to null some fields

        db_file_before = DingoTest.get_db_values(
            self.session.query(FileLog).
            filter(FileLog.basename == file_to_update).one())

        db_file = {}
        db_file['to_update'] = True
        db_file['creation_time'] = '1970-01-01'
        db_file['url'] = ''
        db_file['dataset_id'] = ''
        db_file['version'] = '0'
        db_file['start_time'] = '1970-01-01'
        db_file['end_time'] = '1970-01-01'
        db_file['product'] = ''
        db_file['is_delivered'] = True
        db_file['is_archived'] = True
        db_file['public_filename'] = 'x'
        db_file['public_dirname'] = 'y'

        fields = db_file.keys()
        # these fields will not be changed by the update
        # because they are handled by another task
        not_changed_fields = ['is_delivered',
                              'is_archived',
                              'public_filename',
                              'public_dirname']

        self.session.query(FileLog).\
            filter(FileLog.basename == file_to_update).update(db_file)
        self.session.flush()

        # -- get the modified version
        db_file_modified = DingoTest.get_db_values(
            self.session.query(FileLog).
            filter(FileLog.basename == file_to_update).one())

        # --- make assertions ---
        for key in fields:
            assert db_file_modified[key] != db_file_before[key]

        # --- initialize the command ---
        main_command = ['pop',
                        'dingo',
                        'update_filelog',
                        '--root', root
                        ]

        # --- run the command ---
        self.run_command(main_command)

        # -- get the new version
        db_file_after = DingoTest.get_db_values(
            self.session.query(FileLog).
            filter(FileLog.basename == file_to_update).one())

        # --- make assertions ---
        for key in fields:
            if key in not_changed_fields:
                # these fields are not changed by update_filelog
                assert db_file_after[key] != db_file_before[key]
                assert db_file_after[key] == db_file_modified[key]
            else:
                # these fields have to get their value back
                assert db_file_after[key] == db_file_before[key]
                assert db_file_after[key] != db_file_modified[key]

        # -- also check that there was one file updated
        # wil be done after Outflow migration

        self.session.close()
