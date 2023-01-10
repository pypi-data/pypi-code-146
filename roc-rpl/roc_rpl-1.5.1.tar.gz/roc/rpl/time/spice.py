#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from glob import glob
from datetime import datetime
import re

import numpy as np

from spice_manager import SpiceManager

from poppy.core.logger import logger
from poppy.core.configuration import Configuration

from roc.rpl.constants import TIME_DAILY_STRFORMAT, SPICE_KERNEL_PATTERN, KERNEL_CATEGORY
from roc.rpl.exceptions import SpiceKernelNotValid

__all__ = ['SpiceHarvester']

STRPTIME = '%Y%m%d'


class SpiceHarvester(SpiceManager):
    """
    Class to get SPICE kernels for Solar Orbiter (inherits SpiceManager class)
    """

    def __init__(self, path):

        self.path = path
        self._kernels_time_version = {}
        self._failed = False

        super().__init__(spice_kernels=None,
                        logger=logger)

        # Make sure path in the OS environment variables (for kernel loading in mk)
        os.environ['SPICE_KERNEL_PATH'] = path

    @property
    def failed(self):
        return self._failed

    @failed.setter
    def failed(self, value):
        if isinstance(value, bool):
            self._failed = value

    @staticmethod
    def spice_kernel_path():

        # Get pipeline env. variable from configuration file
        try:
            env_vars = Configuration.manager['pipeline']['environment']
        except:
            logger.exception('No "environment" field defined in the pipeline configuration file')
            env_vars = None

        # If SPICE_KERNEL_PATH is provided, then load it
        if env_vars and 'SPICE_KERNEL_PATH' in env_vars:
            if env_vars['SPICE_KERNEL_PATH'].startswith('$'):
                spice_kernel_path = os.environ['SPICE_KERNEL_PATH']
            else:
                spice_kernel_path = env_vars['SPICE_KERNEL_PATH']
            logger.debug(f'SPICE_KERNEL_PATH = {spice_kernel_path} loaded from config. file')
        elif 'SPICE_KERNEL_PATH' in os.environ:
            spice_kernel_path = os.environ['SPICE_KERNEL_PATH']
            logger.debug(f'SPICE_KERNEL_PATH = {spice_kernel_path} loaded from OS environment')
        else:
            logger.info('No entry found for SPICE_KERNEL_PATH')
            spice_kernel_path = None

        return spice_kernel_path

    @classmethod
    def load_spice_kernels(cls,
                        path,
                        by_date=None,
                        ignore_type=[],
                        only_mk=False,
                        predictive=True,
                        flown=True,
                        ):
        """
        Get list of spice kernels to load for Solar Orbiter.

        :param path: Path of spice kernel root directory
        :param by_date: Get spice kernels valid for a given date. Input date value must a datetime.date object. If not provided try to load latest kernels.
        :param ignore_type: Filter spice kernels by type. Must be a list of extension without dot (e.g., "spk", "bsp", etc.). If not provided, then take all types.
        :param ignore_file: List of spice kernel file(s) to ignore.
        :param include_file: List of spice kernel file(s) to be included.
        :param only_mk: Load only meta kernels
        :param predictive: If True then load predictive kernels only, otherwise load predictive then as-flown
        :param flown: If True then load as-flown kernels only, otherwise load predictive then as-flown
        :return: list of spice kernels found
        """

        # If path is None, return None
        if not path or not os.path.isdir(path):
            logger.warning(f'Spice kernel directory path is not valid! ({path})')
            return None

        # Initialize harvester
        harvester = cls(path)

        if not by_date:
            logger.debug('Attempting to load latest SPICE kernels.')
            by_date = datetime.today()
            latest = True
        else:
            logger.debug(f'Loading SPICE kernels for {by_date}')
            latest = False

        if only_mk:
            logger.debug('Loading meta kernels "mk" only')
            # If only meta kernels requested, add all other kernel types in the
            # kernel to ignore
            ignore_type = list(SPICE_KERNEL_PATTERN.keys()).copy()
            ignore_type.remove('mk')

        # Set the kernel category (predictive and/or as-flown)
        if predictive and not flown:
            kernel_categ = ['pred']
        elif not predictive and flown:
            kernel_categ = ['flown']
        else:
            kernel_categ = KERNEL_CATEGORY

        # Check for spice kernels in "path"
        if os.path.isdir(path):

            # Walk through each spice kernels types
            # and get list of kernels found
            for current_type, current_pattern in SPICE_KERNEL_PATTERN.items():

                if current_type in ignore_type:
                    logger.debug(f'{current_type} SPICE kernels will be ignored')
                    continue

                # Define kernel sub-folder
                kernel_subdir = os.path.join(path, current_type)
                if not os.path.isdir(kernel_subdir):
                    logger.error(f'{kernel_subdir} does not exit, skip it')
                    continue

                # Initialize kernel list
                kernel_list = []
                if current_type == 'mk':
                    # Load other kernels from the meta kernel directory
                    os.chdir(os.path.join(path, 'mk'))
                    if latest:
                        # Load latest metakernel
                        suffix = 'mk'
                        kernel_list = [
                            os.path.join(kernel_subdir, f'solo_ANC_soc-{current_categ}-{suffix}.tm')
                            for current_categ in kernel_categ]
                    elif by_date:
                        # Load metakernel(s) for a given date
                        kernel_list = SpiceHarvester.load_mk(kernel_subdir, by_date,
                                                             category=kernel_categ)
                else:
                    logger.debug('Only "mk" SPICE kernel processing is supported currently')
                    continue

                if not kernel_list:
                    logger.warning(f'No SPICE kernel found for {current_type}')
                else:
                    # Load kernels
                    harvester.kernels = kernel_list

        else:
            logger.error(f'{path} does not exists!')
            return None

        return harvester

    @staticmethod
    def load_mk(mk_dir_path, by_date, category=KERNEL_CATEGORY):
        """
        Load SPICE metakernel (mk)

        :param mk_dir_path: Path of the mk directory
        :param by_date: date for which kernel must be loaded (take latest close date)
        :param category: list with kernel category ("flown" and/or "pred")
        :return: list of mk found
        """

        # Get file pattern for the mk kernel type
        kernel_pattern = SPICE_KERNEL_PATTERN['mk'][0]

        # Filter kernel by type
        pattern = os.path.join(mk_dir_path, kernel_pattern)
        mk_files = glob(pattern)
        nmk = len(mk_files)
        if nmk == 0:
            logger.warning(f'No "mk" kernel found in {mk_dir_path}!')
            return None
        else:
            logger.debug(f'{nmk} "mk" kernel(s) found in {mk_dir_path}')

        # For each file get the file category version, date and count
        versions = np.empty(nmk, dtype=int)
        dates = np.empty(nmk, dtype=datetime)
        counts = np.empty(nmk, dtype=int)
        for i, current_mk in enumerate(mk_files):

            # Get category, version date and count from filename fields
            fields = SpiceHarvester.extract_kernel_fields('mk', current_mk)

            if fields['category'] not in category:
                logger.info(f'{current_mk} has not the expected category: {fields["category"]}')
            else:
                versions[i] = fields['version']
                dates[i] = fields['date']
                counts[i] = fields['count']

        # Keep only the nearest but older kernel files w.r.t. by_date
        delta_dt = np.abs(dates - by_date)
        where_min_dt = np.where(delta_dt == min(delta_dt) and dates >= by_date)

        # If remaining kernels, keep the indices for max version
        if len(where_min_dt) > 1:
            where_max_version = np.where(versions[where_min_dt] == max(versions[where_min_dt]))

            # If remaining kernels, keep the indices for max count
            if len(where_max_version) > 1:
                where_max_count = np.where(versions[where_min_dt] == max(versions[where_min_dt]))

                idx = where_min_dt[where_max_version[where_max_count]]
            else:
                idx = where_min_dt[where_max_version]
        else:
            idx = where_min_dt

        # Return only slice of list for the resulting indices
        if idx:
            nearest_mk = mk_files[idx]
        else:
            logger.warning(f'Cannot determinate the "mk" kernel(s) to load for {by_date}')
            nearest_mk = []

        return nearest_mk

    @staticmethod
    def extract_kernel_fields(kernel_type, kernel_file):
        """
        Extract the filename fields from an input SPICE kernel file.

        :param kernel_type: Type of SPICE kernel
        :param kernel_file: SPICE kernel file for which must be extracted
        :return: dictionary with extracted fields
        """

        # regex pattern
        regex_field_pattern = SPICE_KERNEL_PATTERN[kernel_type][1]
        regex_field_num = SPICE_KERNEL_PATTERN[kernel_type][2]

        # Initialize output dictionary
        kernel_fields = {}

        # Retrieve date and version from kernel filename
        basename = os.path.basename(kernel_file)
        try:
            re_result = re.search(regex_field_pattern, basename)
            fields = re_result.groups()
            nfields = len(fields)
            # If there is not the expected number of fields then raise an exception
            if nfields != regex_field_num:
                raise SpiceKernelNotValid
        except Exception:
            logger.exception(f'Wrong file format for {kernel_file}')
        else:
            # Extract fields, depending of the type of kernel
            if kernel_type == 'mk':
                # Get pred/flown category from file name (e.g., solo_ANC_soc-flown-mk.tm)
                category = basename.split('_')[2].split('-')[1]
                kernel_fields = {'version': int(fields[0]),
                                  'date': datetime.strptime(fields[1], TIME_DAILY_STRFORMAT),
                                  'count': int(fields[2]),
                                  'starttime': None,
                                  'endtime': None,
                                  'category': category}
            else:
                logger.warning('Filtering other kernel type than "mk" not supported currently')

        return kernel_fields
