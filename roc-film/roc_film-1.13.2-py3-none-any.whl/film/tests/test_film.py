#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.film plugin.
"""
import glob
import shlex
import tarfile
from pathlib import Path
import os
import tempfile

from poppy.core.generic.requests import download_file
from poppy.core.logger import logger
from poppy.core.conf import settings


class FilmTest:
    # Base URL for downloading test data for FILM plugin
    base_url = 'https://rpw.lesia.obspm.fr/roc/data/private/devtest/roc/test_data/rodp/film'

    # test credentials
    host = 'roc2-dev.obspm.fr'
    username = os.environ.get('ROC_TEST_USER', 'roctest')
    password = None

    def __init__(self):
        logger.debug('FilmTest setup_class()')
        logger.debug(f'base_url = {self.base_url}')
        try:
            self.password = os.environ['ROC_TEST_PASSWORD']
        except KeyError:
            raise KeyError('You have to define the test user password using'
                           'the "ROC_TEST_PASSWORD" environment variable')

    @staticmethod
    def get_test_data_path(command=None):
        """
        Get the path where to store the test dataset locally

        :param command: name of the plugin command to test

        :return: data_test_path, string containing the path
        """
        # Define default value
        data_test_path = os.path.join(tempfile.gettempdir(), 'roc', 'film')

        # Get pipeline configuration parameters
        conf = FilmTest.load_configuration()

        # Check if ROC_TEST_DATA_PATH env. variable is defined
        # in: (1) config file, (2) shell env.
        for source in [conf['environment'], os.environ]:
            try:
                data_test_path = os.path.join(source['ROC_TEST_DATA_PATH'], 'roc', 'film')
            except Exception:
                # logger.debug('Env. variable ROC_TEST_DATA_PATH not set')
                pass
            else:
                break

        if command:
            data_test_path = os.path.join(data_test_path, command.lower())

        logger.info(f'Using {data_test_path} to store test data')
        # Make sure the directory exists (ignore if it does)
        Path(data_test_path).mkdir(parents=True, exist_ok=True)

        return data_test_path

    def get_test_data(self, command,
                      base_url=None,
                      test_data_dir=None,
                      test_data_file='test_data.tar.gz',
                      target_dir=None,
                      overwrite=False,
                      extract=True):
        """
        Try to get data for the current FILM command test.

        :param command: Name of the command for which test data must be retrieved (e.g., "dds_to_l0", "l0_to_hk", ...)
        :param base_url: Base URL where test data are stored
        :param test_data_dir: Local base directory where test data are saved
        :param test_data_file: Basename of the tarball (.tar.gz) file containing test data
        :param overwrite: Overwrite existing tarball file. Default is False
        :param extract: Extracting content of the tarball file. Default is True
        :return: Local path to the test data tarball file
        """
        if not test_data_dir:
            test_data_dir = FilmTest.get_test_data_path(command=command)
        Path(test_data_dir).mkdir(exist_ok=True, parents=True)

        # Build local path of the test data file (tarball)
        test_data_path = os.path.join(test_data_dir, test_data_file)

        if not base_url:
            base_url = self.base_url

        # Define directory where tarball must be extracted
        # if extract=True. Default is the tarball folder
        if not target_dir:
            target_dir = test_data_dir

        # get authentication login and password
        auth = (self.username, self.password)

        if not os.path.isfile(test_data_path) or overwrite:

            # Build complete URL and download file
            test_data_url = '/'.join([base_url, command, test_data_file])
            if all([val is not None for val in auth]):
                logger.info(f'Downloading {test_data_url} in {test_data_dir} ...')
                download_file(test_data_path, test_data_url, auth=auth)
            else:
                raise IOError(f'At least one of the following arguments missing: [username, password]!')

        else:
            logger.info(f'{test_data_path} already exists')

        if extract:
            if tarfile.is_tarfile(str(test_data_path)):
                logger.info(f'Extracting {test_data_path} ...')
                with tarfile.open(str(test_data_path), 'r:*') as tarball:
                    tarball.extractall(path=target_dir)
            else:
                raise tarfile.ReadError(f'{test_data_path} is not a valid tarball!')

        return test_data_path

    @staticmethod
    def get_output_dir_path(command):
        """
        Get the path where to save the files produced during the test

        :return: output_dir_path, string containing the path
        """
        # Define value using command name
        if command:
            output_dir_path = os.path.join(FilmTest.get_test_data_path(command), 'output')
        else:
            # Else attempt to get from config file or env variables.
            # Get pipeline configuration parameters
            conf = FilmTest.load_configuration()

            # Check if pipeline.output_path variable is defined in config
            try:
                output_dir_path = conf['pipeline']['output_path']
            except KeyError:
                logger.debug('Variable pipeline.output_path not set in the config. file!')
            else:
                if output_dir_path.startswith('$ROOT_DIRECTORY'):
                    output_dir_path = output_dir_path.replace('$ROOT_DIRECTORY', settings.ROOT_DIRECTORY)

        # Create directory
        Path(output_dir_path).mkdir(exist_ok=True, parents=True)
        logger.debug(f'Using {output_dir_path} to store data produced during the test')

        return output_dir_path

    @staticmethod
    def get_inputs(test_data_dir):
        """
        Return the paths of the input data directory and files

        :param test_data_dir: Root path of the test data directory
        :return: tuple (input_dir_path, inputs)
        """
        input_dir_path = os.path.join(test_data_dir, 'inputs')
        if not os.path.isdir(input_dir_path):
            logger.warning(f'{input_dir_path} not found')
            inputs = list()
        else:
            inputs = [item for item in os.listdir(input_dir_path)
                      if os.path.isfile(os.path.join(input_dir_path, item))]
            if len(inputs) == 0:
                logger.warning(f'No input file found in {input_dir_path}')

        return input_dir_path, inputs

    @staticmethod
    def get_expected_outputs(test_data_dir):
        """
        Return the paths of the expected output data directory and files

        :param test_data_dir: Root path of the test data directory
        :return: tuple (expected_output_dir_path, expected_outputs)
        """
        expected_output_dir_path = os.path.join(test_data_dir, 'expected_outputs')
        if not os.path.isdir(expected_output_dir_path):
            logger.warning(f'{expected_output_dir_path} not found')
            expected_outputs = list()
        else:
            expected_outputs = [item for item in os.listdir(expected_output_dir_path)
                                if os.path.isfile(os.path.join(expected_output_dir_path, item))]
            if len(expected_outputs) == 0:
                logger.warning(f'No input file found in {expected_output_dir_path}')

        return expected_output_dir_path, expected_outputs

    @staticmethod
    def get_spice_kernel_dir():
        """
        Returns SPICE kernels directory

        :return: spice_kernels_dir
        """
        # Define default value
        spice_kernels_dir = os.path.join(Path.cwd(), 'data', 'spice_kernels')

        # Get pipeline configuration parameters
        conf = FilmTest.load_configuration()

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
    def get_diff_files(dirs_cmp, path=''):
        for name in dirs_cmp.diff_files:
            yield os.path.join(path, name)
        for parent, sub_dirs_cmp in dirs_cmp.subdirs.items():
            for filepath in FilmTest.get_diff_files(sub_dirs_cmp, path=os.path.join(path, parent)):
                yield filepath

    @staticmethod
    def load_configuration():
        from poppy.core.configuration import Configuration

        configuration = Configuration(os.getenv('PIPELINE_CONFIG_FILE', None))
        configuration.read()

        return configuration

    @staticmethod
    def get_idb_release_dir_path():
        """
        Get the path where to store the IDB release files locally

        :return: idb_release_dir_path, string containing the path
        """
        # Define default value
        idb_release_dir_path = os.path.join(tempfile.gettempdir(), 'roc', 'idb_release')

        # Get pipeline configuration parameters
        conf = FilmTest.load_configuration()

        # Check if IDB_INSTALL_DIR env. variable is defined
        # in: (1) config file, (2) shell env.
        for source in [conf['environment'], os.environ]:
            try:
                idb_dump_dir_path = os.path.join(source['IDB_INSTALL_DIR'])
            except Exception:
                # logger.debug('Env. variable IDB_INSTALL_DIR not set')
                pass
            else:
                break

        logger.info(f'Using {idb_release_dir_path} to store RPW IDB source files')

        return idb_release_dir_path

    @staticmethod
    def load_idb(test_class_instance,
                 idb_version=None,
                 idb_dump_file=None,
                 user=os.environ.get('ROC_TEST_USER', 'roctest'),
                 password=os.environ.get('ROC_TEST_PASSWORD', None),
                 install_dir=None,
                 log_level='ERROR'):
        """
        Function that gathers commands to load IDB in the database.

        :param test_class_instance: Instance of test class containing the poppy.core.test.run_command() method
        :param idb_version: Version of the MIB IDB to load (ignored if idb_dump_file is passed)
        :param idb_dump_file: SQL text file containing the IDB to dump
        :param user: Login user to download idb_dump_file from ROC private server
        :param password: Login password to download idb_dump_file from ROC private server
        :param install_dir: IDB source files installation directory
        :param log_level: level of log to print
        :return:
        """

        # Make sure to have an up-and-running database
        test_class_instance.run_command('pop db upgrade heads -ll INFO')

        if not install_dir:
            install_dir = FilmTest.get_idb_release_dir_path()

        if idb_dump_file:
            # Loading IDB dump file in the database
            # (required a valid dump file and psql command line tool)
            command = [
                'pop',
                '-ll',
                log_level,
                'idb',
                '--force',
                'load_idb_dump',
                '--i',
                install_dir,
                '-d',
                idb_dump_file,
                '-a',
                user, password,
            ]
            test_class_instance.run_command(command)
        elif idb_version:
            # Load PALISADE IDB first (always)
            idb_palisade_loading = [
                'pop',
                'idb',
                'install',
                '-i',
                install_dir,
                '-s',
                'PALISADE',
                '-v',
                '4.3.5_MEB_PFM',
                '--load',
                '-ll',
                log_level,
            ]

            # Then load MIB
            idb_mib_loading = [
                'pop',
                'idb',
                'install',
                '-i',
                install_dir,
                '-s',
                'MIB',
                '-v',
                idb_version,
                '--load',
                '-ll',
                log_level,
            ]

            # Apply IDB loading
            test_class_instance.run_command(idb_palisade_loading)

            # Apply IDB loading
            test_class_instance.run_command(idb_mib_loading)
        else:
            raise ValueError('Missing input argument to load IDB!')

    @staticmethod
    def load_l0(test_class_instance, l0_dir_path, idb_version,
                idb_source='MIB',
                pattern='solo_L0_rpw*.h5'):
        """
        Insert L0 data in the database (required to run some tests)

        :param test_class_instance:
        :param l0_dir_path:
        :param pattern:
        :return:
        """

        # Build list of L0 files
        l0_files_path = list(glob.glob(os.path.join(l0_dir_path, pattern)))

        # Get SCLK and LSK SPICE kernels
        kernels_dir = FilmTest.get_spice_kernel_dir()
        try:
            sclk_file = sorted(list(glob.glob(os.path.join(kernels_dir, 'sclk', '*.tsc'))))[-1]
        except:
            raise FileNotFoundError('No SPICE SCLK kernel loaded!')
        else:
            logger.info(f'Use {sclk_file}')
        try:
            lsk_file = sorted(list(glob.glob(os.path.join(kernels_dir, 'lsk', '*.tls'))))[-1]
        except:
            raise FileNotFoundError('No SPICE LSK kernel loaded!')
        else:
            logger.info(f'Use {lsk_file}')

        # Inserting L0 data into the database
        cmd = ' '.join(['pop',
                        '-ll INFO',
                        'dingo',
                        f'--idb-version {idb_version}',
                        f'--idb-source {idb_source}',
                        f'--sclk {sclk_file}',
                        f'--lsk {lsk_file}',
                        'l0_to_db',
                        '-l0 ' + ' '.join(l0_files_path)])
        logger.debug(cmd)
        test_class_instance.run_command(shlex.split(cmd))

        # Inserting HFR time info in the database
        cmd = 'pop -ll INFO dingo l0_to_hfrtimelog -l0 ' + ' '.join(l0_files_path)
        logger.debug(cmd)
        test_class_instance.run_command(shlex.split(cmd))
