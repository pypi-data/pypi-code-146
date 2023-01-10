#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Contains task to gather SolO MOC DDS TcReport XML content in daily XML files.
"""

import collections
import os
from datetime import datetime
from glob import glob

from edds_process.response import make_tcreport_xml, xml_to_dict
from poppy.core.logger import logger
from poppy.core.target import PyObjectTarget, FileTarget
from poppy.core.task import Task

from roc.film import DATA_VERSION, TIME_DAILY_STRFORMAT, TCREPORT_PREFIX_BASENAME, ARCHIVE_DAILY_DIR, TIME_ISO_STRFORMAT
from roc.film.tools.file_helpers import get_output_dir
from roc.film.tools import valid_data_version, sort_dict_list, get_latest_file


class MergeTcReport(Task):
    """
    Task to merge input set of DDS TcReport XML Elements
    into daily XML files.
    """
    plugin_name = 'roc.film'
    name = 'merge_tcreport'

    def add_targets(self):
        self.add_input(identifier='dds_data',
                       target_class=PyObjectTarget)
        self.add_output(identifier='tcreport_daily_xml', many=True,
                        target_class=FileTarget)

    def setup_inputs(self):

        # Get data_version input keyword (can be used to force version of
        # output file)
        self.data_version = valid_data_version(
            self.pipeline.get('data_version', default=[DATA_VERSION])[0])

        # Get/create list of well processed L0 files
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)
        # Get/create list of failed DDS files
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get/create list of already processed tcreport
        self.processed_tcreport = self.pipeline.get(
            'processed_tcreport', default=[], create=True)

        # Get/create TcReport failed
        self.failed_tcreport = self.pipeline.get(
            'failed_tcreport', default=[], create=True)

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

        # Get input TcReport data
        try:
            dds_data = self.inputs['dds_data'].value
        except:
            logger.exception("Cannot retrieve input 'dds_data' input!")
            return False
        else:
            self.tcreport_data = self._get_tcreport_elements(dds_data)

        return True

    def run(self):

        logger.info('Running MergeTcReport Task...')

        # get/initialize inputs
        if not self.setup_inputs():
            return

        # Check/Get existing data for previous TcReport daily files (if any)
        existing_packet_data = {
            current_date: self._get_existing_data(current_date)[current_date]
            for current_date in self.tcreport_data.keys()
        }

        # Loop over each day in the outputs
        output_files = []
        for current_date, output_data in self.tcreport_data.items():

            if self.filter_date and current_date not in self.filter_date:
                logger.info(f'Skipping current date {current_date}')
                continue

            # Check if existing data and new data are the same
            current_existing_data = existing_packet_data[current_date]
            if not [True for current_data in output_data
                    if current_data not in current_existing_data]:
                logger.info(f'No new tcreport element for {current_date}')
                continue
            else:
                logger.debug(f'Creating a new daily TcReport XML file in {self.output_dir} '
                             f'for {current_date}')

            # If existing data list is not empty ...
            new_data = output_data.copy()
            if current_existing_data:
                # Mix existing and new output set of packets
                new_data.extend(current_existing_data)

            # Make sure it has unique elements
            new_data = [i for n, i in enumerate(new_data)
                        if i not in new_data[n + 1:]]

            # Make sure new data is time sorted
            new_data = sort_dict_list(new_data, 'ExecutionTime')

            # define format of data version
            data_version = f'V{int(self.data_version):02d}'

            # Build output TcReport file basename
            packet_date_str = current_date.strftime(TIME_DAILY_STRFORMAT)
            file_basename = '_'.join([
                TCREPORT_PREFIX_BASENAME,
                packet_date_str]
            )

            # Build full new output file basename
            file_basename = '_'.join([file_basename, data_version]) + '.xml'

            # Build output file path
            output_target_path = os.path.join(self.output_dir, file_basename)

            # Write output file
            logger.info(f'Writing {len(output_data)} TcReport elements '
                        f'into {output_target_path}')
            if make_tcreport_xml(new_data, output_target_path,
                                 overwrite=True,
                                 logger=logger):
                self.processed_files.append(output_target_path)
                output_files.append(output_target_path)
            else:
                logger.error(f'Writing {output_target_path} has failed!')
                self.failed_files.append(output_target_path)

        self.outputs['tcreport_daily_xml'].filepath = output_files

    def _get_existing_data(self, packet_date):
        """
        Check if daily files already exist for the input tcreport date,
        If yes, then retrieve data inside
        and build expected output file path.

        :param packet_date: date of the tcreport ExecutionTime
        :return: existing tcreport data (if any) as dictionary
        """

        # Initialize output data
        output_data = {packet_date: []}

        # Build list of directories where to check for existing TM files
        dir_list = [self.output_dir]
        if self.archive_path:
            dir_list.append(os.path.join(self.archive_path,
                                         packet_date.strftime(ARCHIVE_DAILY_DIR)))

        # Loop over directories where to check for existing file
        # (start to check in output directory then in archive dir if provided)
        latest_existing_file = None
        for current_dir in dir_list:
            latest_existing_file = self._check_existence(
                current_dir, packet_date)
            if latest_existing_file:
                break

        # Then, if latest existing file was found, parse it to retrieve data
        if latest_existing_file:
            logger.info(f'Loading existing TcReport data from {latest_existing_file}...')
            output_data = self._get_tcreport_elements(
                xml_to_dict(latest_existing_file))
        else:
            logger.info(f'No existing TcReport data file found '
                        f' for {packet_date}')

        return output_data

    def _check_existence(self, dir_path, packet_date):

        # Convert input packet date into string
        packet_date_str = packet_date.strftime(TIME_DAILY_STRFORMAT)

        # Build output TmRaw file basename
        file_basename = '_'.join([
            TCREPORT_PREFIX_BASENAME,
            packet_date_str]
        )

        existing_files = glob(os.path.join(
            dir_path, file_basename + '_V??.xml'))
        if existing_files:
            logger.debug(f'{len(existing_files)} already exists for {packet_date}')
            # If files found then get latest version
            latest_existing_file = get_latest_file(existing_files)
        else:
            latest_existing_file = None

        return latest_existing_file

    def _get_tcreport_elements(self, tcreport_xml_dict):
        """
        Extract TcReport Elements from a dictionary
        of a input TcReport XML file

        :param tcreport_xml_dict: EDDS TcReport XML dictionary
        :return: list of TcReport XML elements
        """

        output_tcreport_list = tcreport_xml_dict['ns2:ResponsePart'] \
            ['Response']['PktTcReportResponse'] \
            ['PktTcReportList']['PktTcReportListElement']

        # Make sure that returned output_tcreport_list is a list
        # (If only one PktTcReportListElement is found in the XML
        # the xml_to_dict method returns a collections.OrderedDict() instance).
        if isinstance(output_tcreport_list, collections.OrderedDict):
            output_tcreport_list = [output_tcreport_list]

        # return output as a dictionary of packet execution date keywords
        output_tcreport_dict = collections.defaultdict(list)
        for current_tcreport in output_tcreport_list:
            try:
                key = datetime.strptime(current_tcreport['ExecutionTime'],
                                        TIME_ISO_STRFORMAT).date()
            except:
                logger.warning(f'Cannot get ExecutionTime for {current_tcreport}')
                if current_tcreport not in self.failed_tcreport:
                    self.failed_tcreport.append(current_tcreport)
            else:
                output_tcreport_dict[key].append(current_tcreport)

        return output_tcreport_dict
