#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Contains task to concatenate input SolO HK DDS data files into daily XML files.
"""

import collections
import os
from datetime import datetime
from glob import glob

from edds_process.response import make_param_xml, xml_to_dict
from poppy.core.logger import logger
from poppy.core.target import FileTarget
from poppy.core.task import Task

from roc.film import DATA_VERSION, TIME_DAILY_STRFORMAT, TIME_ISO_STRFORMAT, ARCHIVE_DAILY_DIR
from roc.film.constants import SOLOHK_PREFIX_BASENAME
from roc.film.tools.file_helpers import get_output_dir
from roc.film.tools import valid_data_version, sort_dict_list, get_latest_file

__all__ = ['CatSoloHk']

class CatSoloHk(Task):
    """
    Task to concatenate and sort by ascending time a list of ParamSampleListElement XML element
    containing SOLO HK parameters.
    ParamSampleListElement XML elements are loaded from a
    set of input SOLO EDDS Param XML files
    """
    plugin_name = 'roc.film'
    name = 'cat_solo_hk'

    def add_targets(self):
        self.add_input(identifier='dds_xml', many=True,
                       target_class=FileTarget,
                       filepath=self.get_dds_xml())
        self.add_output(identifier='solohk_daily_xml', many=True,
                        target_class=FileTarget)

    def get_dds_xml(self):
        return self.pipeline.get('dds_files', default=[])

    def setup_inputs(self):

        # Get data_version input keyword (can be used to force version of
        # output file)
        self.data_version = valid_data_version(
            self.pipeline.get('data_version', default=[DATA_VERSION])[0])

        # Get input list of DDS XML files
        self.dds_file_list = self.inputs['dds_xml'].filepath
        self.dds_file_num = len(self.dds_file_list)
        if self.dds_file_num == 0:
            logger.warning('No input DDS XML file passed as input argument!')
            return False

        # Get/create list of well processed L0 files
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)
        # Get/create list of failed DDS files
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get/create list of already processed DDS
        self.processed_dds_files = self.pipeline.get('processed_dds_files',
                                                     default=[], create=True)

        # Get/create list of failed DDS
        self.failed_dds_files = self.pipeline.get('failed_dds_files',
                                                  default=[], create=True)

        # Get local archive path
        self.archive_path = self.pipeline.get(
            'archive_path', default=[None])[0]

        # Get list of dates to process
        self.filter_date = self.pipeline.get('filter_date', default=[])
        if self.filter_date:
            self.filter_date = [filter_date.date()
                                for filter_date in self.filter_date]

        # If output directory not found, create it
        self.output_dir = get_output_dir(self.pipeline)
        if not os.path.isdir(self.output_dir):
            logger.debug(f'Making {self.output_dir}...')
            os.makedirs(self.output_dir)

        return True

    def run(self):

        # Initialize task inputs
        if not self.setup_inputs():
            self.pipeline.exit()
            return

        # Initialize the dictionary containing
        # ParamSampleListElement Elements with SOLO HK data for each day
        solo_hk_dict = collections.defaultdict(list)

        # Loop over list of input files
        for input_dds_file in self.dds_file_list:

            # Retrieve list of SOLO HK PARAMS inside the XML
            try:
                xml_param_list = CatSoloHk.parse_dds_param_xml(input_dds_file)
            except FileNotFoundError:
                logger.warning(f'Input file {input_dds_file} not found!')
                continue
            except:
                logger.exception(f'Cannot parse {input_dds_file}')
                if input_dds_file not in self.failed_dds_files:
                    self.failed_dds_files.append(input_dds_file)
                continue
            else:
                if input_dds_file not in self.processed_dds_files:
                    self.processed_dds_files.append(input_dds_file)

            # Add XML param list
            self._append_output(solo_hk_dict, xml_param_list)

        # Loop over days in solo_hk_dict
        output_files = []
        for current_date, current_param_list in solo_hk_dict.items():

            # Check if output file already exists for the current
            # day
            existing_data = self._get_existing_data(current_date)
            existing_num = len(existing_data)
            logger.info(f'{existing_num} Solo HK elements already '
                        f'found for {current_date}')

            # Append new elements in the list of existing data
            new_data = existing_data.copy()
            [new_data.append(current_data)
             for current_data in current_param_list
                if current_data not in existing_data]

            # If no difference with existing data, no need to save new output
            # file
            new_data_num = len(new_data)
            if existing_num == new_data_num:
                logger.info(f'No new SOLO HK element for {current_date}')
                continue
            else:
                logger.debug(f'Creating a new SOLO HK daily file in {self.output_dir} '
                             f'for {current_date}')

            # Always make sure that elements are unique and sorted
            # by ascending timestamp
            # Make sure it has unique elements
            new_data = [i for n, i in enumerate(new_data)
                        if i not in new_data[n + 1:]]

            # Make sure new data is time sorted
            new_data = sort_dict_list(new_data, 'TimeStampAsciiA')

            # define format of data version
            data_version = f'V{int(self.data_version):02d}'

            # Convert input date into string
            date_str = current_date.strftime(TIME_DAILY_STRFORMAT)

            # Build output solo hk daily file basename
            file_basename = '_'.join([
                SOLOHK_PREFIX_BASENAME,
                date_str]
            )

            # Build full new output file basename
            file_basename = '_'.join([file_basename, data_version]) + '.xml'

            # Build output file path
            output_target_path = os.path.join(self.output_dir, file_basename)

            # Write output file
            logger.info(f'Writing {len(new_data)} Solo HK elements '
                        f'into {output_target_path}')
            if make_param_xml(new_data, output_target_path,
                              overwrite=True,
                              logger=logger):
                self.processed_files.append(output_target_path)
                output_files.append(output_target_path)
            else:
                logger.error(f'Writing {output_target_path} has failed!')
                self.failed_files.append(output_target_path)

        self.outputs['solohk_daily_xml'].filepath = output_files

    @staticmethod
    def parse_dds_param_xml(xml_file):
        """
        Parse input SolO EDDS XML file with ParamSampleListElement Elements

        :param xml_file: Input EDDS Param XML file
        :return: List of ParamSampleListElement
        """
        # Initialize output list
        ParamSampleListElement = []

        if os.path.isfile(xml_file):
            ParamSampleListElement = xml_to_dict(xml_file)['ns2:ResponsePart'] \
                ['Response']['ParamResponse'] \
                ['ParamSampleList']['ParamSampleListElement']

            # Make sure that returned output is a list
            # (If only one PktTcReportListElement is found in the XML
            # the xml_to_dict method returns a collections.OrderedDict()
            # instance).
            if isinstance(ParamSampleListElement, collections.OrderedDict):
                ParamSampleListElement = [ParamSampleListElement]
        else:
            raise FileNotFoundError

        return ParamSampleListElement

    def _append_output(self, solo_hk_dict, param_list):
        """
        Append input ParamSampleListElement list
        into the solo_hk_dict dictionary

        :param solo_hk_dict: Dictionary to update with ParamSampleListElement list
        :param param_list: List of ParamSampleListElement
        :return:
        """

        # Loop over ParamSampleListElement in the input list
        for current_param in param_list:

            # Get element timestamp
            current_timestamp = self._extract_timestamp(current_param)
            # Get date
            key = current_timestamp.date()
            # Store element timestamp and content in a dictionary containing
            # a list of elements per day
            solo_hk_dict[key].append(current_param)

    def _extract_timestamp(self, param_element):
        """
        Extract TimeStampAsciiA from a given ParamSampleListElement

        :param param_element: ParamSampleListElement element
        :return: ParamSampleListElement TimeStampAsciiA as datetime object
        """

        return datetime.strptime(param_element['TimeStampAsciiA'],
                                 TIME_ISO_STRFORMAT[:-1])

    def _get_existing_data(self, date):
        """
        Check if SOLO HK daily files already exist for the input date
        in the local RPW data archive.
        If yes, then return data for the latest file

        :param date: date for which checking must be done
        :return: existing Solo HK data (if any) as a list
        """

        # Initialize output data
        output_data = []

        # Convert input date into string
        date_str = date.strftime(TIME_DAILY_STRFORMAT)

        # Get SOLO HK daily file local archive directory path
        if self.archive_path:
            solo_hk_data_dir = os.path.join(self.archive_path,
                                            date.strftime(ARCHIVE_DAILY_DIR))
        else:
            # Otherwise get output directory
            solo_hk_data_dir = self.output_dir

        # Build SOLO HK daily file basename
        file_basename = '_'.join([
            SOLOHK_PREFIX_BASENAME,
            date_str]
        )

        # Check if daily file(s) already exists in the target directory
        logger.debug(f'Checking for SOLO HK daily file existence '
                     f'on {solo_hk_data_dir} for {date} ...')
        existing_files = glob(os.path.join(
            solo_hk_data_dir, file_basename + '_V??.xml'))
        if existing_files:
            logger.debug(f'{len(existing_files)} files already exist for {date}')
            # If files found then get latest version
            latest_existing_file = get_latest_file(existing_files)
        else:
            latest_existing_file = None

        # Then, if latest existing file was found...
        if latest_existing_file:
            # parse it to retrieve data
            output_data = CatSoloHk.parse_dds_param_xml(latest_existing_file)

        return output_data
