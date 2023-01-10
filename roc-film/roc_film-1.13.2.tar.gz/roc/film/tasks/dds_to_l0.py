#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections
import os
from datetime import datetime
import uuid

from edds_process.response import count_packets, xml_to_dict

from poppy.core.logger import logger
from poppy.core.task import Task
from poppy.core.target import FileTarget
from poppy.core.db.connector import Connector

from roc.film.tools.file_helpers import generate_filepath, get_output_dir, is_output_dir
from roc.film.tools.metadata import init_l0_meta, get_spice_kernels
from roc.film.constants import TIME_ISO_STRFORMAT, CHUNK_SIZE, SCOS_HEADER_BYTES, \
    DATA_VERSION, TC_ACK_ALLOWED_STATUS

from roc.film.exceptions import L0ProdFailure

from roc.film.tools.l0 import L0
from roc.film.tools.tools import valid_data_version

# roc.rpl task class for the L0 file generation
from roc.rpl.constants import INVALID_UTC_DATETIME, VALID_PACKET

# Database query modules from dingo plugin
from roc.dingo.models.packet import InvalidPacketLog
from roc.dingo.tools import get_or_create_in_db
from roc.dingo.constants import PIPELINE_DATABASE

__all__ = ['DdsToL0']


class DdsToL0(Task):
    """
    Make the RPW L0 data file from RPW DDS files.
    The L0 writing is perform by chunk of packets.
    """
    plugin_name = 'roc.film'
    name = 'dds_to_l0'

    def add_targets(self):
        self.add_input(target_class=FileTarget,
                       identifier='dds_tmraw_xml',
                       many=True,
                       filepath=self.get_dds_tmraw_xml())
        self.add_input(target_class=FileTarget,
                       identifier='dds_tcreport_xml',
                       many=True,
                       filepath=self.get_dds_tcreport_xml())
        self.add_output(target_class=FileTarget,
                        identifier='l0_file')

    def get_dds_tmraw_xml(self):
        return self.pipeline.get('dds_tmraw_xml', default=[])

    def get_dds_tcreport_xml(self):
        return self.pipeline.get('dds_tcreport_xml', default=[])

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):

        # Import external Tasks, classes and methods (if any)
        from roc.rpl.packet_parser import PacketParser, palisade_metadata
        from roc.rpl.time import Time

        # Initialize Time instance
        self.time_instance = Time()

        # Pass input arguments for the Time instance
        self.time_instance.kernel_date = self.pipeline.get(
            'kernel_date', default=None, args=True)
        self.time_instance.predictive = self.pipeline.get(
            'predictive', default=True, args=True)
        self.time_instance.no_spice = self.pipeline.get(
            'no_spice', default=False, args=True)

        # Load SPICE kernels
        if not self.time_instance.spice:
            logger.error('Cannot load SPICE kernels for the current task!')
            return False

        # Get IDB inputs
        self.idb_version = self.pipeline.get('idb_version', default=[None])[0]
        self.idb_source = self.pipeline.get('idb_source', default=[None])[0]

        # Initialize PacketParser instance
        self.PacketParser = PacketParser

        # Initialize list of DDS files to process
        self.dds_file_list = []

        # Get input DDS TmRaw files
        tmraw_files = self.inputs['dds_tmraw_xml'].filepath
        if tmraw_files:
            tmraw_file_num = len(tmraw_files)
            logger.info(f'{tmraw_file_num} DDS TmRaw XML files to process')
            self.dds_file_list.extend(tmraw_files)
        else:
            logger.info('No DDS TmRaw XML file to process')

        # Get input DDS TcReport files
        tcreport_files = self.inputs['dds_tcreport_xml'].filepath
        if tcreport_files:
            tcreport_files_num = len(tcreport_files)
            logger.info(f'{tcreport_files_num} DDS TcReport XML files to process')
            self.dds_file_list.extend(tcreport_files)
        else:
            logger.info('No DDS TcReport XML file to process')

        # If no DDS file, exit
        self.dds_file_num = len(self.dds_file_list)
        if self.dds_file_num == 0:
            return False

        # Get chunk size
        self.chunk_size = self.pipeline.get('chunk', default=CHUNK_SIZE)

        # Get products directory (folder where final output files will be
        # moved)
        self.products_dir = self.pipeline.get('products_dir',
                                              default=[None], args=True)[0]

        # Get force optional keyword
        self.force = self.pipeline.get('force', default=False, args=True)

        # Get/create list of well processed DDS files
        self.processed_dds_files = self.pipeline.get(
            'processed_dds_files', default=[], create=True)
        # Get/create list of failed DDS files
        self.failed_dds_files = self.pipeline.get(
            'failed_dds_files', default=[], create=True)

        # Get/create list of well processed L0 files
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)
        # Get/create list of failed DDS files
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # get data_version keyword (if passed)
        self.data_version = valid_data_version(
            self.pipeline.get('data_version', default=[DATA_VERSION])[0])

        # Get scos header size to remove
        self.scos_header = self.pipeline.get(
            'scos_header', default=[SCOS_HEADER_BYTES])[0]

        if self.idb_source and self.idb_source == 'PALISADE':
            palisade_version = self.idb_version
        else:
            palisade_version = None

        # Get output dir
        self.output_dir = get_output_dir(self.pipeline)
        if not is_output_dir(self.output_dir,
                             products_dir=self.products_dir):
            logger.debug(f'Making {self.output_dir}')
            os.makedirs(self.output_dir)
        else:
            logger.info(f'Output files will be '
                        f'saved into existing folder {self.output_dir}')

        # Get palisade metadata
        self.palisade_metadata = palisade_metadata(
            palisade_version=palisade_version)

        # Get start_time/end_time
        self.start_time = self.pipeline.get('start_time', default=[None])[0]
        self.end_time = self.pipeline.get('end_time', default=[None])[0]

        # Get --cdag keyword
        self.is_cdag = self.pipeline.get('cdag', default=False, create=True)

        # get a database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

        return True

    def run(self):

        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = f'DdsToL0-{self.job_uuid[:8]}'
        logger.info(f'Task {self.job_id} is starting')
        try:
            # Initialize task inputs
            self.setup_inputs()
        except:
            logger.exception(f'Initializing inputs has failed for task {self.job_id}!')
            self.pipeline.exit()
            return

        # get L0 metadata
        logger.debug(f'Building output L0 file path...    [{self.job_id}]')
        extra_attrs = {'Data_version': self.data_version}
        metadata = init_l0_meta(self,
                                extra_attrs=extra_attrs)

        # Generate output filepath
        l0_file = generate_filepath(
            self, metadata, '.h5', is_cdag=self.is_cdag)
        logger.info(f'Packet data will be saved into {l0_file}   [{self.job_id}]')

        # Add some metadata
        metadata['Generation_date'] = datetime.utcnow().isoformat()
        metadata['File_ID'] = str(uuid.uuid4())

        if self.start_time:
            metadata['TIME_MIN'] = self.start_time.strftime(TIME_ISO_STRFORMAT)

        if self.end_time:
            metadata['TIME_MAX'] = self.end_time.strftime(TIME_ISO_STRFORMAT)

        # Add SPICE SCLK kernel as an entry
        # of the "Kernels" g. attr
        sclk_file = get_spice_kernels(time_instance=self.time_instance,
                                      pattern='solo_ANC_soc-sclk')
        if sclk_file:
            metadata['SPICE_KERNELS'] = sclk_file[-1]
        else:
            logger.warning('No SPICE SCLK kernel '
                           f'saved for {l0_file}    [{self.job_id}]')

        # Get total number of packets
        logger.info(f'Getting total number of packets to process...    [{self.job_id}]')
        dds_packet_num_list = [count_packets(
            dds_file) for dds_file in self.dds_file_list]
        dds_total_packet_num = sum(dds_packet_num_list)

        logger.info(
            f'{dds_total_packet_num} packets in the {self.dds_file_num} input DDS files    [{self.job_id}]')

        if dds_total_packet_num == 0:
            logger.info(f'No packet to process, exit {DdsToL0.name} task    [{self.job_id}]')
            return

        # Initialize some loop variables
        parent_list = []
        packet_count = 0

        # Start loop over dds XML file
        for i, dds_file in enumerate(self.dds_file_list):

            # (Re)initialize loop variables
            dds_data = None
            packet_parser = None
            valid_packet_parser = None

            # Parse input RPW TM/TC DDS format file
            logger.info(f'Parsing {dds_file}...')

            try:
                dds_data = self._parse_dds(dds_file)

                # Add current file to the parent list
                dds_basename = os.path.basename(dds_file)
                if dds_basename not in parent_list:
                    parent_list.append(dds_basename)

                packet_num = len(dds_data)
                if packet_num == 0:
                    logger.info(f'No DDS TM/TC packet found in {dds_file}    [{self.job_id}]')
                    continue

                # Parse TM/TC packets (identify packets and extract parameter
                # data)
                try:
                    logger.info(f'Extracting {dds_packet_num_list[i]} packets from {dds_file}...    [{self.job_id}]')
                    packet_parser = self._parse_packet(dds_data)
                except:
                    logger.exception(f'Parsing current packet list has failed!    [{self.job_id}]')
                    continue

                # Get only valid packets
                valid_packets = self.PacketParser.packet_status(
                    packet_parser.parsed_packets,
                    status=VALID_PACKET)
                n_valid = len(valid_packets)

                # Get only invalid packets
                invalid_packets = self.PacketParser.packet_status(
                    packet_parser.parsed_packets,
                    status=VALID_PACKET, invert=True)
                n_invalid = len(invalid_packets)

                if n_invalid > 0:
                    logger.error(f'{n_invalid} invalid TM/TC packets found in {dds_file}!    [{self.job_id}]')
                    try:
                        self.invalid_to_db(invalid_packets)
                    except:
                        logger.exception(f'Invalid packets cannot be inserted in the database!    [{self.job_id}]')
                        raise L0ProdFailure

                # Check if valid packets are found
                if n_valid == 0:
                    logger.info(f'No valid TM/TC packet found in {dds_file}    [{self.job_id}]')
                    continue
                else:
                    logger.info(f'{n_valid} valid TM/TC packets found in {dds_file}    [{self.job_id}]')

                # Write metadata and packets into the L0 file
                L0().to_hdf5(l0_file,
                             packet_parser=packet_parser,
                             metadata=metadata)

            except L0ProdFailure:
                logger.exception('L0ProdFailure')
                self.failed_files.append(l0_file)
                break
            except:
                logger.exception(f'Error when parsing {dds_file}!    [{self.job_id}]')
                self.failed_dds_files.append(dds_file)
            else:
                self.processed_dds_files.append(dds_file)

        if os.path.isfile(l0_file) and l0_file not in self.failed_files:

            # Add final parent list as L0 root attribute
            # (Done at the end to make sure to
            # have also input DDS files with no packet in the parent list)
            metadata['Parents'] = ','.join(parent_list)
            L0().to_hdf5(l0_file,
                         metadata=metadata)

            # Sort packet datasets in L0 by ascending UTC Time
            logger.info(f'Sorting {l0_file} file by ascending packet creation time (UTC)    [{self.job_id}]')
            L0.order_by_utc(l0_file, unique=True, update_time_minmax=True)

            # Set output target 'l0_file' filepath
            self.processed_files.append(l0_file)
            self.outputs['l0_file'].filepath = l0_file

    def _parse_dds(self, dds_file):
        """
        Parse input dds file and return packet data as a
        list of dictionaries

        :param dds_file: Path of the input DDS file (can TmRaw or TcReport)
        :return: list of dictionaries with packet data
        """

        output_list = []

        dds_data = xml_to_dict(dds_file)['ns2:ResponsePart']\
            ['Response']

        if 'PktRawResponse' in dds_data:
            dds_data = dds_data['PktRawResponse'] \
                ['PktRawResponseElement']
            dds_type = 'TM'
        elif 'PktTcReportResponse' in dds_data:
            dds_data = dds_data['PktTcReportResponse'] \
                ['PktTcReportList']['PktTcReportListElement']
            dds_type = 'TC'
        else:
            logger.warning(f'Invalid input dds file {dds_file}')
            return output_list

        # Make sure that returned dds_data is a list
        # (If only one XML element is found in the file
        # the xml_to_dict method returns a collections.OrderedDict() instance).
        if isinstance(dds_data, collections.OrderedDict):
            dds_data = [dds_data]

        output_list = [self._build_packet_dict(current_packet, dds_type)
                       for current_packet in dds_data]

        # Remove wrong packets
        output_list = [current_packet
                       for current_packet in output_list
                       if current_packet]

        return output_list

    def _build_packet_dict(self, packet, dds_file_type):
        """
        Build RawData compatible packet dictionary from input DDS XML packet data

        :param packet: input DDS XML packet data (can PktTcReportElement or PktRawResponseElement)
        :param dds_file_type: type of DDS data.
            Possible values are 'TM' (for TmRaw) or 'TC' (for TcReport).
        :return: packet dictionary as expected by RawData class
        """

        # Initialize output dictionary
        packet_dict = {}

        file_type = dds_file_type.upper()

        if file_type == 'TC':

            # Get packet SRDB id
            srdb_id = packet.get('CommandName', None)

            # Get corresponding PALISADE ID
            if srdb_id:
                palisade_id = self.palisade_metadata[srdb_id]['palisade_id']
            else:
                palisade_id = None

            # Get corresponding packet category
            if srdb_id:
                packet_category = self.palisade_metadata[
                    srdb_id]['packet_category']
            else:
                packet_category = None

            try:
                utc_time = datetime.strptime(packet.get(
                    'ExecutionTime'), TIME_ISO_STRFORMAT)
            except:
                utc_time = INVALID_UTC_DATETIME

            # Get ack execution completion status
            # If Playback (routine) ...
            ack_exe_state = packet.get('ExecCompPBState', 'UNKNOWN')
            if ack_exe_state not in TC_ACK_ALLOWED_STATUS:
                # If realtime downlink (e.g., commissioning) ...
                ack_exe_state = packet.get('ExecCompState', 'UNKNOWN')

            # Get ack acceptation completion status
            # If Playback (routine) ...
            ack_acc_state = packet.get('OnBoardAccPBState', 'UNKNOWN')
            if ack_acc_state not in TC_ACK_ALLOWED_STATUS:
                # If realtime downlink (e.g., commissioning) ...
                ack_acc_state = packet.get('OnBoardAccState', 'UNKNOWN')

            try:
                unique_id = 'UNKNOWN'
                for i, field in enumerate(packet['CustomField']):
                    if field['FieldName'] == 'uniqueID':
                        unique_id = packet['CustomField'][i]['Value']
                        break
            except:
                unique_id = 'UNKNOWN'

            # Only keep "PASSED" and "FAILED" exe status in L0
            if ack_exe_state in TC_ACK_ALLOWED_STATUS:
                # Build dictionary for the current packet
                packet_dict = {'binary': packet.get('RawBodyData', None),
                               'srdb_id': srdb_id,
                               'palisade_id': palisade_id,
                               'descr': packet.get('Description', None),
                               'category': packet_category,
                               'type': 'TC',
                               'utc_time': utc_time,
                               'ack_exe_state': ack_exe_state,
                               'ack_acc_state': ack_acc_state,
                               'sequence_name': packet.get('SequenceName', None),
                               'unique_id': unique_id,
                               'release_state': packet.get('ReleaseState', 'UNKNOWN'),
                               'release_time': packet.get('ReleaseTime', 'UNKNOWN'),
                               'ground_state': packet.get('GroundState', 'UNKNOWN'),
                               'uplink_state': packet.get('UplinkState', 'UNKNOWN'),
                               'uplink_time': packet.get('UplinkTime', 'UNKNOWN'),
                               'onboard_state': packet.get('OnBoardState', 'UNKNOWN'),
                               }
        elif file_type == 'TM':
            packet_dict = {'type': 'TM',
                           'srdb_id': None,
                           'palisade_id': None,
                           'binary': packet['Packet']}
        else:
            logger.warning(f'Unknown dds file type: {file_type}')
            packet_dict = {}

        return packet_dict

    def _parse_packet(self, packet_list):
        """
        Analyze input packets.

        :param packet_list:
        :return:
        """

        parser = None

        # Initialize packet_parser
        parser = self.PacketParser(
            idb_version=self.idb_version,
            idb_source=self.idb_source,
            time=self.time_instance,
        )

        # connect to add exception when packet analysis is bad
        parser.extract_error.connect(self.exception)

        # Analyse input RPW TM/TC packets
        parser.parse_packets(packet_list,
                             start_time=self.start_time,
                             end_time=self.end_time,
                             valid_only=False)

        return parser

    def invalid_to_db(self, invalid_packets):
        """
        Insert invalid packets in the ROC database

        :param invalid_packets: List of invalid packets
        :return: List of invalid packets which have been not well inserted in the database
        """
        failed_insertion = []
        for current_packet in invalid_packets:
            new_entry = dict()
            # Compute specific SHA255 for invalid packet
            new_entry['sha'] = self.PacketParser.get_packet_sha(current_packet)

            # Get palisade_id, srdb_id, apid and utc_time (if known)
            new_entry['palisade_id'] = current_packet.get('palisade_id', None)
            new_entry['srdb_id'] = current_packet.get('srdb_id', None)
            new_entry['apid'] = current_packet.get('apid', None)
            new_entry['utc_time'] = current_packet.get('utc_time', None)

            # Get status and comment
            new_entry['status'] = current_packet['status']
            new_entry['comment'] = current_packet['comment']

            # Store packet data
            new_entry['data'] = {key: val
                                 for key, val in current_packet.items()
                                 if key not in new_entry.keys()}

            # Modify header and data_header content (to be writable in JSONB format)
            new_entry['data']['header'] = str(new_entry['data']['header'].to_dict())
            new_entry['data']['data_header'] = str(new_entry['data']['data_header'].to_dict())

            # Set insertion time
            new_entry['insert_time'] = datetime.today()

            # Insert new entry
            job, done, created = get_or_create_in_db(self.session, InvalidPacketLog, new_entry,
                                                     kwargs={'sha': new_entry['sha']})
            if done:
                if created:
                    logger.info(f'New entry in database for invalid packet {current_packet}')
                else:
                    logger.info(f'An entry already exists in database for invalid packet {current_packet}')
            else:
                logger.error(f'Cannot insert new entry in database for invalid packet {current_packet}!')
                failed_insertion.append(current_packet)

            return failed_insertion
