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
class TestDingoLogFileToRocdb(DingoLogFileCommandTestCase):

    def setup_method(self, method):
        super().setup_method(method)

        # empty the database
        self.session.query(FileLog).delete()
        self.session.flush()

    def teardown_method(self, method):
        super().teardown_method(method)

        # close database
        self.session.close()

    @pytest.mark.parametrize('root, date, level, nb_files', [
        ('DATA-1', None, None, 61),
        ('DATA-1', '2020/08/19', None, 31),
        ('DATA-1', '2020/08/19', ['L0'], 1),
        ('DATA-1', '2020/08/19', ['L0', 'L1'], 14),
        ('DATA-1', '2020/08/19', ['L2'], 0),
        ('DATA-1', '2020/08', ['L2'], 17),
    ])
    def test_logfile_to_rocdb(self, root, date, level, nb_files):
        """
        Test insertion with different input parameters
        Check the number of files inserted in db after each
        """
        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)

        # --- initialize the command ---
        main_command = ['pop',
                        'dingo',
                        'logfile_to_rocdb'
                        ]

        if root is not None:
            main_command += ['--root', root]

        if date is not None:
            main_command += ['--date', date]

        if level is not None:
            main_command += ['--level'] + level

        # --- run the command ---
        self.run_command(main_command)

        # --- make assertions ---

        results = self.session.query(FileLog).all()
        assert len(results) == nb_files

        self.session.close()

    @pytest.mark.parametrize('root', [
        ('DATA-1'),
    ])
    def test_logfile_to_rocdb_multiple(self, root):
        """
        Test multiple insertion with different input parameters
        Check the number of files inserted in db after each
        """

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)

        # --- initialize the commands ---
        commands = [['pop',
                     'dingo',
                     'logfile_to_rocdb',
                     '--root', root,
                     '--date', '2020/08/19',
                     '--level', 'L0', 'L1'],
                    ['pop',
                     'dingo',
                     'logfile_to_rocdb',
                     '--root', root,
                     '--date', '2020/08/19',
                     '--level', 'L0'],
                    ['pop',
                     'dingo',
                     'logfile_to_rocdb',
                     '--root', root,
                     '--date', '2020/08',
                     '--level', 'L2']
                    ]

        nb_files = [14, 14, 31]

        for i, cmd in enumerate(commands):
            # --- run the  command ---
            self.run_command(cmd)

            # --- make assertions ---
            results = self.session.query(FileLog).all()
            assert len(results) == nb_files[i]

        self.session.close()

    @pytest.mark.parametrize('root', [
        ('SK-1'),
    ])
    def test_logsk_to_rocdb(self, root):
        """
        Test spice kernel insertion
        Check the number of files inserted in db after each
        """
        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        root = osp.join(data_test_path, root)

        # --- initialize the commands ---
        command = ['pop',
                   'dingo',
                   'logsk_to_rocdb',
                   '--root', root
                   ]

        nb_files = 5

        # --- run the  command ---
        self.run_command(command)

        # --- make assertions ---
        results = self.session.query(FileLog).filter(
            FileLog.level == 'SK').all()
        assert len(results) == nb_files

        self.session.close()

    @pytest.mark.parametrize(
        'filesroot, skroot, expected_before, expected_after',
        [(
            'DATA-1', 'SK-1', 32, 12
        )]
    )
    def test_update_missing_parents_in_db(
            self, filesroot, skroot, expected_before, expected_after):
        """
        Test spice kernel insertion
        Check the number of files inserted in db after each
        """

        # --- set up arguments ---
        data_test_path = DingoLogFileTest.get_test_data_path()
        filesroot = osp.join(data_test_path, filesroot)
        skroot = osp.join(data_test_path, skroot)

        command = ['pop',
                   'dingo',
                   'logfile_to_rocdb',
                   '--root', filesroot
                   ]
        self.run_command(command)
        command = ['pop',
                   'dingo',
                   'logsk_to_rocdb',
                   '--root', skroot
                   ]
        self.run_command(command)

        results = self.session.query(FileLog).filter(
            FileLog.error_log.like('%Missing parents%')).all()
        assert len(results) == expected_before

        command = ['pop',
                   'dingo',
                   'update_missing_parents_in_db',
                   '--root', filesroot
                   ]
        self.run_command(command)

        results = self.session.query(FileLog).filter(
            FileLog.error_log.like('%Missing parents%')).all()
        assert len(results) == expected_after

        self.session.close()
