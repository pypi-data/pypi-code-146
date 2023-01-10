#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions used in all DINGO tests
"""
import os
import os.path as osp
import copy
from pathlib import Path

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from poppy.core.logger import logger
from poppy.core.generic.requests import download_file

from roc.dingo.constants import TEST_DATABASE


# Models to be adapted for each Dingo model
#
# from poppy.core.test import TaskTestCase, CommandTestCase
# class DingoTaskTestCase(TaskTestCase):
#
#     @classmethod
#     def setup_class(cls):
#         logger.debug('setup_class DingoLogFileTaskTestCase')
#         d = DingoTest()
#         d.get_test_data()
#
#    #     # --- database setup ---
#    #     session = DingoTestLogFile.setup_session()
#
#    # @classmethod
#    # def teardown_class(cls):
#    #     logger.debug('teardown_class DingoTaskTestCase')
#
#    #     # --- close session
#    #     session.close()
#
# class DingoCommandTestCase(CommandTestCase):
#
#     @classmethod
#     def setup_class(cls):
#         logger.debug('setup_class DingoCommandTestCase')
#         d = DingoTest()
#         d.get_test_data()


class DingoTest:
    base_url = 'https://rpw.lesia.obspm.fr/roc/data/private/devtest/roc/test_data/rodp/dingo'  # noqa: E501
    base_path = '/volumes/plasma/rpw/roc/data/https/private/devtest/roc/test_data/rodp/dingo'  # noqa: E501

    # test credentials
    host = 'roc2-dev.obspm.fr'
    username = os.environ.get('ROC_TEST_USER', 'roctest')
    password = None

    def __init__(self):
        logger.debug('DingoTest setup_class()')
        logger.debug(f'base_url = {self.base_url}')
        logger.debug(f'base_path = {self.base_path}')
        try:
            self.password = os.environ['ROC_TEST_PASSWORD']
        except KeyError:
            raise KeyError('You have to define the test user password using'
                           'the "ROC_TEST_PASSWORD" environment variable')

    def compare_data_to_expected(expected_data, data):
        """
        Compare expected_data to the data array dictionnary
            -> check if every expected item is in data
            -> check if every data item is in expected data

            :param expected_data: expected data
            :param data: the data to be compared
        """
        # check length
        assert len(expected_data) == len(data)

        # check content
        for item in data:
            assert item in expected_data, \
                'item {} is not in expected data'.format(item)

        for item in expected_data:
            assert item in data, \
                'item {} is not in result'.format(item)
            assert data[item] == expected_data[item], \
                'item {} is not the one expected :' \
                'expected {} / got {}'.format(
                    item, expected_data[item], data[item])

    def read_data(file):
        """
        Read a file located in the data-tasks directory
        and returns file content as an array of strings

            :param file: file to open
        """
        path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(path, 'data-tasks', file)
        data = []
        with open(path, 'r') as f:
            # read a line corresponding to a directory
            for line in f.readlines():
                # append the data
                data.append(line.strip())
        return data

    @staticmethod
    def get_test_data_path():
        """
        Read the config file and returns ROC_DINGO_TEST_DATA_PATH
        which is the path where to store the test dataset locally
        """
        conf = DingoTest.load_configuration()

        try:
            data_test_path = conf['environment']['ROC_DINGO_TEST_DATA_PATH']
        except Exception:
            logger.info('Env. variable ROC_DINGO_TEST_DATA_PATH not set')
            logger.info('Using /tmp/DINGO_TEST_DATA/')
            data_test_path = '/tmp/DINGO_TEST_DATA/'

        logger.debug(f'ROC_DINGO_TEST_DATA_PATH = {data_test_path}')
        return data_test_path

    def get_test_data(self):
        """
        Get the test dataset indicated by the environment variable
        ROC_DINGO_TEST_DATA_PATH

        :param subdir: optional subdirectory

        Try to make a rsync with the roctest account
        A public kay has to be setup on the server to allow connexion
        If the command is not available (Windows),
        use the download_file() method
        """
        data_test_path = DingoTest.get_test_data_path()
        os.makedirs(data_test_path, exist_ok=True)

        try:
            logger.info('Starting rsync')
            ssh_option = '\"ssh -o \'StrictHostKeyChecking no\'\"'
            rsync_cmd = 'rsync -e {} -irtzuv {}@{}:{}/ {}/'.format(
                ssh_option,
                self.username,
                self.host,
                self.base_path,
                data_test_path
            )
            logger.info('Executing ' + rsync_cmd)
            output = os.popen(rsync_cmd)
            rsync_output = output.read()
            if output.close() is not None:
                raise ValueError('Rsync failed : {}'.format(rsync_output))
        except ValueError:
            logger.info('Rsync failed, using download_test_data()')
            self.download_test_data(data_test_path)

    def download_test_data(self, data_test_path):
        """
        Download the manifest.txt file located at self.base_url
        And for each file, download it only if the file does not exist
        in data_test_path
        """
        logger.debug('download_test_data()')
        manifest_filepath = osp.join(data_test_path, 'manifest.txt')

        manifest_file_url = self.base_url + '/manifest.txt'
        auth = (self.username, self.password)

        file_list = list(self.load_manifest_file(
            manifest_filepath, manifest_file_url, auth=auth))

        for relative_filepath in file_list:
            # skip empty strings
            if not relative_filepath:
                continue

            # get the complete filepath
            filepath = osp.join(data_test_path, relative_filepath)
            os.makedirs(osp.dirname(filepath), exist_ok=True)

            # download it only if it does not exist
            if not osp.isfile(filepath):
                logger.info('Downloading {}'.format(filepath))
                download_file(filepath,
                              f'{self.base_url}/{relative_filepath}',
                              auth=auth)

    def load_manifest_file(
        self, manifest_filepath, manifest_file_url, auth=None):
        """
        Read the manifest.txt file located at manifest_file_url
        and returns the list composed by the file list
        """

        download_file(manifest_filepath, manifest_file_url, auth=auth)

        with open(manifest_filepath) as manifest_file:
            for line in manifest_file:
                yield line.strip('\n\r')

        os.remove(manifest_filepath)

    @staticmethod
    def load_configuration():
        from poppy.core.configuration import Configuration

        configuration = Configuration(os.getenv('PIPELINE_CONFIG_FILE', None))
        configuration.read()

        return configuration

    @staticmethod
    def get_spice_kernel_dir():
        """
        Returns SPICE kernels directory

        :return: spice_kernels_dir
        """
        # Define default value
        spice_kernels_dir = os.path.join(Path.cwd(), 'data', 'spice_kernels')

        # Get pipeline configuration parameters
        conf = DingoTest.load_configuration()

        # Check if SPICE_KERNEL_PATH env. variable is defined
        # in: (1) config file, (2) shell env.
        for source in [conf['environment'], os.environ]:
            try:
                spice_kernels_dir = os.path.join(source['SPICE_KERNEL_PATH'])
            except Exception:
                # logger.debug('Env. variable SPICE_KERNEL_PATH not set')
                pass
            else:
                break

        return spice_kernels_dir

    @staticmethod
    def setup_session():
        # Read config file
        conf = DingoTest.load_configuration()

        database_info = list(filter(
            lambda db: db['identifier'] == TEST_DATABASE,
            conf['pipeline.databases']))[0]

        # Create an Engine, which the Session will use for connection resources
        engine = create_engine('{}://{}@{}/{}'.format(
            database_info['login_info']['vendor'],
            database_info['login_info']['user'],
            database_info['login_info']['address'],
            database_info['login_info']['database']
        ))
        # create a configured "Session" class
        Session = sessionmaker(bind=engine, autocommit=False)
        # create a Session
        session = Session()

        return session

    def get_db_values(item):
        """
        returns a dict for any object in DB returned by session.query

        :param item: the object
        """

        return copy.copy(item.__dict__)

    @staticmethod
    def get_db_values_columns_only(item):
        """
        Convert an input item as returned by SQLAlchemy.query into dictionary.
        (Same than DingoTest.get_db_values(), but with columns only)
        See https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict

        :param item: SQLAlchemy table model class instance
        :return: dictionary with columns as keywords and entries as values
        """
        return {c.expression.name: getattr(item, c.key)
                for c in inspect(item).mapper.column_attrs}
