#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Contains task to merge SolO MOC DDS TmRaw XML files.
"""

import collections
import os
from glob import glob

from edds_process.response import \
    xml_to_dict, remove_scos_header

from poppy.core.task import Task
from poppy.core.logger import logger
from poppy.core.target import FileTarget, PyObjectTarget

from roc.film import TM_PACKET_CATEG, ARCHIVE_DAILY_DIR, TIME_DAILY_STRFORMAT, TMRAW_PREFIX_BASENAME
from roc.film.tools.file_helpers import get_output_dir
from roc.film.tools import get_latest_file

from roc.rpl.time import Time
from roc.rpl.packet_structure.data import Data

class MergeTmRaw(Task):
    """
    Task to merge input set of DDS TmRaw Packet XML Elements
    into daily XML files.
    """
    plugin_name = 'roc.film'
    name = 'merge_tmraw'

    def add_targets(self):
        self.add_input(identifier='dds_xml',
                       target_class=FileTarget)
        self.add_input(identifier='dds_data',
                       target_class=PyObjectTarget)

    def get_dds_xml(self):
        return self.pipeline.get('dds_xml', default=[])

    def setup_inputs(self):

        # Get/create list of failed DDS files
        self.failed_dds_files = self.pipeline.get(
            'failed_dds_files', default=[], create=True)

        # Get input DDS XML file
        dds_file = None
        try:
            dds_file = self.inputs['dds_xml'].filepath
            if not os.path.isfile(dds_file):
                raise FileNotFoundError
        except:
            logger.exception(f"Cannot load input DDS XML file '{dds_file}'")
            self.failed_dds_files.append(dds_file)
            return False
        else:
            self.dds_file = dds_file

        # Get packet category from input DDS filename
        # (Convention should be "RPW_<packet_category>_*.xml"
        try:
            self.packet_category = os.path.basename(
                self.dds_file).split('_')[1].lower()
        except:
            logger.exception(f'Packet category cannot be extracted from DDS filename!')
            self.failed_dds_files.append(self.dds_file)
            return False

        # If output directory not found, create it
        self.output_dir = get_output_dir(self.pipeline)
        if not os.path.isdir(self.output_dir):
            logger.debug(f'Making {self.output_dir}...')
            os.makedirs(self.output_dir)

        # Get local archive path
        self.archive_path = self.pipeline.get(
            'archive_path', default=[None])[0]

        # Get list of dates to process
        self.filter_date = self.pipeline.get('filter_date', default=[])
        if self.filter_date:
            self.filter_date = [filter_date.date()
                                for filter_date in self.filter_date]

        # Get input TmRaw data
        try:
            dds_data = self.inputs['dds_data'].value
        except:
            logger.exception("Cannot retrieve input 'dds_data' input!")
            self.failed_dds_files.append(self.dds_file)
            return False
        else:
            # Build output for input list of TmRaw data
            self.tmraw_data = self._get_tmraw_packets(dds_data)

        # Get packet cache
        self.packet_cache = self.pipeline.get(
            'packet_cache', default={tm_cat: {}
                                     for tm_cat in TM_PACKET_CATEG},
            create=True)

        # And flag to indicated if there are new packets
        self.has_new_packet = self.pipeline.get(
            'has_new_packet', default={tm_cat: {}
                                       for tm_cat in TM_PACKET_CATEG},
            create=True)

        return True

    def run(self):

        logger.debug('Running MergeTmRaw Task...')

        # get/initialize inputs
        if not self.setup_inputs():
            logger.warning('Missing inputs for MergeTmRaw Task!')
            return

        # Check/Get existing data for previous TmRaw daily files (if any)
        existing_packet_data = {
            current_date: self._get_existing_data(current_date)[current_date]
            for current_date in self.tmraw_data.keys()
        }

        # Loop over each day in the outputs
        for current_date, output_data in self.tmraw_data.items():

            if self.filter_date and current_date not in self.filter_date:
                logger.info(f'Skipping current date {current_date}')
                continue

            # Check if existing data and new data are the same
            current_existing_data = existing_packet_data[current_date]

            # If current_date.year <= 2000, output_data contains not synchronized packets
            # in this case, always write packets into an output file
            new_data = list(set(output_data) - set(current_existing_data))
            if (current_date.year > 2000 and
                    not new_data):
                logger.info(f'No new packet for {current_date} in {self.dds_file}')
                self.has_new_packet[self.packet_category][current_date] = False
            else:
                logger.info(f'{len(new_data)} new TmRaw Packet elements found '
                             f'for {current_date} in {self.dds_file}...')

                # If existing data list is not empty ...
                if current_existing_data:
                    # Mix existing and new output set of packets
                    new_data.extend(current_existing_data)

                # Sort output list of TmRaw data by ascending packet times
                new_data.sort(key=lambda tup: tup[0])

                # Update current_existing_data
                current_existing_data = new_data

                # Update new packet flag (used by MakeDailyTm Task)
                self.has_new_packet[self.packet_category][current_date] = True

            # Store new packets for given category and date in the packet_cache
            if current_existing_data:
                self.packet_cache[self.packet_category][
                    current_date] = current_existing_data

    def _get_packet_time(self, packet_data,
                         scos_header=True):
        """
        Extract CUC time from current packet binary.

        :param packet_data: Packet data (hexa including the 76-bytes of SCOS header)
        :param scos_header: If True remove 76-bytes SCOS header from packet binary.
        :return: tuple with (packet date, (packet cuc time, packet binary))
        """

        # Extract CCSDS CUC packet time from packet header (as datetime object)
        try:
            if scos_header:
                packet_raw_data = remove_scos_header(packet_data)
            else:
                packet_raw_data = packet_data
            packet_bytes_data = bytearray.fromhex(packet_raw_data)
            packet_data = Data(bytes(packet_bytes_data),
                               len(packet_bytes_data)
                               )
            data_field_header = packet_data.extract_tm_header()
            packet_time = Time.cuc_to_datetime(data_field_header.time[:2])[0]
        except:
            logger.exception(f'Packet CUC time cannot be retrieved '
                             f'from Packet element {packet_data}, skip it '
                             )
            if packet_data not in self.failed_tmraw:
                self.failed_tmraw.append(packet_data)
            return None, None
        else:
            return packet_time.date(), (packet_time, packet_raw_data)

    def _get_existing_data(self, packet_date):
        """
        Check if daily files already exist for the input packet date,
        If yes, then retrieve data inside
        and build expected output file path.

        :param packet_date: input packet date
        :return: existing packet data for input date (if any)
        """

        # First check if there are already packets store in packet_cache
        if packet_date in self.packet_cache[self.packet_category]:
            logger.info(f'Retrieving existing {self.packet_category} '
                        f'data for {packet_date} from pipeline cache '
                        f'({len(self.packet_cache[self.packet_category][packet_date])} packets) ...')
            return self.packet_cache[self.packet_category]

        # If not initialize output data
        output_data = {packet_date: []}
        latest_existing_file = None

        # Build list of directories where to check for existing TM files
        dir_list = [self.output_dir]
        if self.archive_path:
            dir_list.append(os.path.join(self.archive_path,
                                         packet_date.strftime(ARCHIVE_DAILY_DIR)))

        # Loop over directories where to check for existing file
        # (start to check in output directory then in archive dir if provided)
        for current_dir in dir_list:
            latest_existing_file = self._check_existence(
                current_dir, packet_date)
            if latest_existing_file:
                break

        # Then, if latest existing file was found, parse it to retrieve data
        if latest_existing_file:
            logger.info(f'Loading existing TmRaw data from {latest_existing_file}...')
            output_data = self._get_tmraw_packets(xml_to_dict(latest_existing_file),
                                                  scos_header=False)
        else:
            logger.info(f'No existing {self.packet_category} TmRaw data file found '
                        f' for {packet_date}')

        return output_data

    def _check_existence(self, dir_path, packet_date):

        # Convert input packet date into string
        packet_date_str = packet_date.strftime(TIME_DAILY_STRFORMAT)

        # Build output TmRaw file basename
        file_basename = '_'.join([
            TMRAW_PREFIX_BASENAME + '-' + self.packet_category,
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

    def _get_tmraw_packets(self, tmraw_xml_dict,
                           scos_header=True):
        """
        Extract TmRaw Packet Element list from a dictionary
        of a input TmRaw XML file

        :param tmraw_xml_dict: EDDS TmRaw XML dictionary
        :param scos_header: See _get_packet_time() method 'scos_header' keyword definition
        :return: dictionary where keyword is packet dates and
                 values are lists of tuple (packet time, packet raw data)
        """

        # Get/create list of already processed tmraw packets
        self.processed_tmraw = self.pipeline.get(
            'processed_tmraw', default=[], create=True)

        # Get/create list of failed tmraw packets
        self.failed_tmraw = self.pipeline.get(
            'failed_tmraw', default=[], create=True)

        output_packet_list = tmraw_xml_dict['ns2:ResponsePart']\
            ['Response']['PktRawResponse'] \
            ['PktRawResponseElement']

        # Make sure that returned output_tmraw_list is a list
        # (If only one Packet element is found in the XML
        # the xml_to_dict method returns a collections.OrderedDict() instance).
        if isinstance(output_packet_list, collections.OrderedDict):
            output_packet_list = [output_packet_list]

        # Add packet date and time to output list
        # Make sure to take unique packets
        logger.debug(f'Extracting packet CUC time from '
                     f'{len(output_packet_list)} TmRaw Packet elements...')

        output_packet_list = list(set([
            self._get_packet_time(current_packet['Packet'],
                                  scos_header=scos_header)
            for current_packet in output_packet_list
        ]))

        # return output as a dictionary of packet date keywords
        output_packet_dict = collections.defaultdict(list)
        for key, val in output_packet_list:
            if key is not None:
                output_packet_dict[key].append(val)

        return output_packet_dict
