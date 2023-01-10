#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions used in all DINGO FileLog tests
"""
import os
import re
from datetime import datetime

from poppy.core.logger import logger
from poppy.core.test import TaskTestCase, CommandTestCase

from roc.dingo.models.file import FileLog
from roc.dingo.constants import \
    DATA_ALLOWED_EXTENSIONS, \
    SPICE_KERNEL_ALLOWED_EXTENSIONS
from roc.dingo.tests.test_dingo import DingoTest


class DingoLogFileTaskTestCase(TaskTestCase):

    @classmethod
    def setup_class(cls):
        logger.debug('setup_class DingoLogFileTaskTestCase')
        d = DingoLogFileTest()
        d.get_test_data()

    #     # --- database setup ---
    #     session = DingoTestLogFile.setup_session()

    # @classmethod
    # def teardown_class(cls):
    #     logger.debug('teardown_class DingoTaskTestCase')

    #     # --- close session
    #     session.close()


class DingoLogFileCommandTestCase(CommandTestCase):

    @classmethod
    def setup_class(cls):
        logger.debug('setup_class DingoLogFileCommandTestCase')
        d = DingoLogFileTest()
        d.get_test_data()


class DingoLogFileTest(DingoTest):

    base_url = f'{DingoTest.base_url}/logfile_to_rocdb'
    base_path = f'{DingoTest.base_path}/logfile_to_rocdb'

    def open_test_data(expected_filename, root):
        """
        Open <expected_filename> file, which contains a list of
            file1 size1 timestamp1
            file2 size2 timestamp2
            ...
        And creates a dictionnary array

            :param expected_filename: filename containing expected data
            :param root: the data root in the file system
            :return: a dictionnary array
        """

        # open the data_files file with data for test
        path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(path, 'data-tasks', expected_filename)
        expected_data = {}
        with open(path, 'r') as f:
            # read a line corresponding to a file
            for line in f.readlines():
                relpath, size, cdate = line.split()
                basename = os.path.basename(relpath)
                # append the data
                expected_data[basename] = {
                    'filepath': os.path.join(
                        root, relpath),
                    'size': int(size),
                    'creation_time': datetime.utcfromtimestamp(int(cdate))
                }

        return expected_data

    def data_to_file_log(data, root):
        dirname = os.path.dirname(data['filepath']).replace(root, '')
        basename = os.path.basename(data['filepath'])
        file_path = dirname.split('/')
        file_name, file_extension = os.path.splitext(basename)

        is_data = True
        re_ext = '|'.join(DATA_ALLOWED_EXTENSIONS)

        if file_extension.replace('.', '') in SPICE_KERNEL_ALLOWED_EXTENSIONS:
            is_data = False
            re_ext = '|'.join(SPICE_KERNEL_ALLOWED_EXTENSIONS)

        if is_data:
            level = file_path[0]
            res = re.search(r'(v|V)([0-9a-zA-Z]+)\.(' + re_ext + ')', basename)
            res_id = 2
        else:
            level = 'SK'
            res = re.search(r'([0-9]+)\.(' + re_ext + ')', basename)
            res_id = 1

        try:
            version = res.group(res_id)
        except Exception:
            version = '0'

        product = re.sub(r'^([^\.]+)_V[0-9U]+\.[^$]+$', r'\1', basename)

        file_log = {
            'basename': basename,
            'product': product,
            'dirname': dirname,
            'size': data['size'],
            'creation_time': data['creation_time'],
            'version': version,
            'state': 'OK',
            'status': 'Terminated',
            'level': level,
            'insert_time': datetime.now(),
            'is_archived': False,
            'is_latest': True
        }
        return FileLog(**file_log)

    def setup_session():

        session = DingoTest.setup_session()

        # empty the table FileLog
        session.query(FileLog).delete()
        session.flush()

        return session
