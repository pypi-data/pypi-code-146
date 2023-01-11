#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import os.path as osp
import datetime as dt
import uuid
import os
import hashlib
from pathlib import Path

from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func

from poppy.core.logger import logger

from poppy.core.tools.text import get_valid_filename
from poppy.core.db.connector import Connector
from poppy.core.generic.cache import CachedProperty
from poppy.core.tools.hashfile import sha256_from_file

from roc.rpl.packet_parser import RawData
from roc.rpl.packet_parser.palisade import palisade_metadata
from roc.film.tools import valid_data_version

from roc.guest.models.test import TestLog
from roc.guest.constants import TIME_RANGE_STRFORMAT, \
    INVALID_ADS_TIME, INPUT_TIME_STRFORMAT, TESTLOG_STRFTIME, \
    TESTLOG_EVENTTIME_STRFORMAT, TESTLOG_EVENTDATE_STRFORMAT, TIME_ISO_STRFORMAT
from roc.guest.exceptions import ParseTestXmlError

__all__ = ['Test', 'parse_ads_file',
           'create_file_log']

class Request(object):
    """
    Container for request information, to be able to share it across tasks.
    """
    def __init__(self, sha256):
        """
        Create a request object from the necessary, mandatory minimal information
        from the point of view of the ROC.
        """
        # store minimal information
        self.sha256 = sha256
        self.uuid = uuid.UUID(sha256[:32])

    @classmethod
    def from_test_log_xml(cls, xml_path):
        # compute the uuid from file content
        sha256 = sha256_from_file(xml_path)
        return cls(sha256)


class Test(RawData):
    """
    Container for information on a test and be able to share it across tasks.
    """
    def __init__(self, test_name, test_date,
                 test_uuid=str(uuid.uuid4()),
                 creation_date=dt.datetime.today(),
                 description=None,
                 terminated_date=dt.datetime.today(),
                 status='Terminated',
                 author=None,
                 events=[],
                 file_path=None,
                 version=None):
        """
        Create a test object from the necessary, mandatory minimal information
        from the point of view of the ROC.

        :param test_name: Name of the test
        :param test_date: Launch date of the test
        :param test_uuid: UUID of the test
        :param creation_date: Creation date of the test
        :param description: Description of the test
        :param terminated_date: End date of the test
        :param status: Status of the test
        :param events: List of events inside the test
        :param file_path: Path to the test log file
        :param version: Version of the data (if any)
        """

        # Init RawData class
        super(Test, self).__init__()

        # store minimal information
        if test_name:
            self.name = test_name
        else:
            logger.warning(f'No test_name for input data, use test_uuid instead: {test_uuid}')
            self.name = test_uuid

        if test_date:
            self.date = test_date
        else:
            self.date = dt.datetime.today()
            logger.error(f'No test_date for input data, use {self.date} instead!')

        self.date = test_date
        self.uuid = test_uuid
        self.status = status
        self.creation_date = creation_date
        self.terminated_date = terminated_date
        self.description = description
        self.author = author
        self.file_path = file_path
        self.events = events
        self.version = version

        # create an identity
        self.sha1 = self.test_sha1()


    @property
    def time_min(self):
        return self.date

    @property
    def time_max(self):
        return self.terminated_date

    @property
    def descriptor_xml(self):
        return Test.build_descriptor_xml(self)

    @staticmethod
    def build_descriptor_xml(test):
        """
        Build TestDescriptor XML

        :return: TestDescriptor XML
        """

        if isinstance(test.terminated_date, dt.datetime):
            terminated_date = test.terminated_date.strftime(TIME_RANGE_STRFORMAT)
        elif isinstance(test.terminated_date, str):
            terminated_date = test.terminated_date
        else:
            terminated_date = ''
            logger.warning(f'Wrong terminated_date type ({type(terminated_date)})')

        xml = '<TestDescriptor'
        xml += f' TestName="{test.name}"'
        xml += f' TestUUID="{test.uuid}">'
        xml += '<GeneralInfo>'
        xml += f'<CreationDate>{test.creation_date.strftime(TIME_RANGE_STRFORMAT)}</CreationDate>'
        xml += f'<LongDescription>{test.description}</LongDescription>'
        xml += '</GeneralInfo>'
        xml += '<ExecutionInformation>'
        xml += f'<Status>{test.status}</Status>'
        xml += f'<LaunchedDate>{test.date.strftime(TIME_RANGE_STRFORMAT)}</LaunchedDate>'
        xml += f'<TerminatedDate>{terminated_date}</TerminatedDate>'
        xml += '</ExecutionInformation>'
        xml += '</TestDescriptor>'

        return xml

    @classmethod
    def from_meb_test(cls, test):
        """
        Create a test object for the information contained in the test of the
        MEB-GSE.
        """
        return cls(test.TestName, test.Launched, test_uuid=test.UUID)

    @classmethod
    def from_roc_test(cls, test):
        """
        Create a test object from information in the ROC database.
        """
        return cls(test.test_name, test.test_launched_date, test_uuid=test.test_uuid)

    @classmethod
    def from_testlog_xml(cls, xml_path,
                         header_only=False):
        """
        Parse the MEB GSE test log XML file and use the information
        to generate an instance of the Test class.

        :param xml_path: Path to the MEB GSE test log XML file
        :param header_only: If True, then retrieve test log header info only
        :return: instance of the Test class corresponding to the input test log XML information
        """

        logger.info(f'Parsing {xml_path} ...')

        test_name, test_uuid, launch_date, terminated_date, \
        creation_date, description, status, test_author = cls.get_testlog_header(xml_path)

        if not header_only:
            # Retrieve eventdescr too
            events = [event
                      for event in cls.events_from_file(xml_path)
                      ]
        else:
            events = []

        # return the test
        return cls(test_name, launch_date,
                   test_uuid=test_uuid,
                   terminated_date=terminated_date,
                   creation_date=creation_date,
                   description=description,
                   status=status,
                   author=test_author,
                   file_path=xml_path,
                   events=events)


    @staticmethod
    def get_testlog_header(xml_path):
        """
        Extract test log header info from the input file.

        :param xml_path: path of the MEB GSE test log XML file
        :return: test_name, test_uuid, launch_date, terminated_date, creation_date, description, status
        """

        # Make sure to have a string and not a list
        if isinstance(xml_path, list):
            xml_path = xml_path[0]

        # open the file
        try:
            with open(xml_path, 'r') as f:
                # loop without parsing on the document
                for event, elem in ET.iterparse(f, ['end']):
                    # if this an TestDescriptor
                    if elem.tag == 'TestDescriptor':
                        # store information about the test
                        test_name = elem.attrib['TestName']
                        test_uuid = elem.attrib['TestUUID']

                        # one for general information
                        gen_info = elem.find('GeneralInfo')
                        description = gen_info.find('LongDescription').text
                        author_tag = gen_info.find('Author')
                        if author_tag:
                            test_author = author_tag.text
                        else:
                            test_author = 'Undefined'
                        creation_date = dt.datetime.strptime(
                            gen_info.find(
                                'CreationDate'
                            ).text,
                            '%Y-%m-%dT%H:%M:%S',
                        )

                        # one for execution information
                        exec_info = elem.find('ExecutionInformation')
                        status = exec_info.find('Status').text
                        launch_date = dt.datetime.strptime(
                            exec_info.find(
                                'LaunchedDate'
                            ).text,
                            '%Y-%m-%dT%H:%M:%S',
                        )
                        terminated_date = dt.datetime.strptime(
                            exec_info.find(
                                'TerminatedDate'
                            ).text,
                            '%Y-%m-%dT%H:%M:%S',
                        )
        except Exception as e:
            logger.error(f'Parsing {xml_path} has failed: {e}')
            raise ParseTestXmlError

        return test_name, test_uuid, launch_date, terminated_date, \
               creation_date, description, status, test_author

    @staticmethod
    def events_from_file(xml_path):
        """
        Retrieve eventdescr data from test log XML, iterating on each tag found with yield command.

        :param xml: path of the MEB GSE test log xml file
        :return: dictionary containing the eventdescr info
        """

        with open(xml_path, 'r') as buff:
            # loop without parsing on the document
            for event, elem in ET.iterparse(buff, ['end']):
                # if this an TestDescriptor
                eventdescr = Test.xml_to_event(elem)
                if eventdescr:
                    yield eventdescr
                else:
                    continue

    @staticmethod
    def events_from_string(xml_string):
        """
        Retrieve eventdescr data from XML, iterating on each tag found with yield command.

        :param xml_string: List of XML string containing the eventdescr data
        :return: dictionary containing the eventdescr info
        """

        # Make sure that xml_string input is a list
        if not isinstance(xml_string, list):
            xml_string = [xml_string]

        # Loop over xml string list to get EventDescr tag data
        # and return it as a Test event
        for xml in xml_string:
            yield Test.xml_to_event(ET.fromstring(xml))

    @staticmethod
    def xml_to_event(xml_elem):
        """
        Store a xml element as a eventdescr dictionary

        :param xml_elem: xml element to parse
        :return: dictionary with eventdescr data
        """

        eventdescr = None
        if xml_elem.tag == 'EventDescr':
            # Only extract S_C device tags
            if (xml_elem.attrib['Device'] == 'S_C' and
                    (xml_elem.attrib['EventType'] == 'TM' or
                     xml_elem.attrib['EventType'] == 'TC_FEEDBACK')):
                eventdescr = {'EventDate': xml_elem.find('Common').find('EventDate').text,
                              'EventTime': xml_elem.find('Common').find('EventTime').text,
                              'Name': xml_elem.find('Content').find('Name').text,
                              'Data': xml_elem.find('Content').find('Data').text,
                              'Device': 'S_C',
                              'TestUUID': xml_elem.find('Common').find('TestUUID').text,
                              'EventType': xml_elem.attrib['EventType'],
                              'EventID': xml_elem.attrib['EventID'],
                              'Category': xml_elem.find('Content').find('Category').text,
                              'Collection': xml_elem.find('Content').find('Collection').text,
                              }

                # Get TC feedback status
                feedback = xml_elem.find('FeedBack')
                if feedback:
                    eventdescr['Status'] = feedback.find('Status').text

                # Build eventdescr xml
                eventdescr_xml = Test.event_to_xml(eventdescr)
                eventdescr['XML'] = eventdescr_xml

        return eventdescr

    @staticmethod
    def event_to_xml(eventdescr):
        """
        Build EventDescr xml from an input eventdescr dictionary

        :param eventdescr: dictionary containing event tags/attributes
        :return: xml of eventdesc
        """

        xml = f'<EventDescr Device="{eventdescr["Device"]}"'
        xml += f' EventID="{eventdescr["EventID"]}"'
        xml += f' EventType="{eventdescr["EventType"]}">'
        xml += '<Common>'
        xml += f'<EventDate>{eventdescr["EventDate"]}</EventDate>'
        xml += f'<EventTime>{eventdescr["EventTime"]}</EventTime>'
        xml += f'<TestUUID>{eventdescr["TestUUID"]}</TestUUID>'
        xml += '</Common>'
        xml += '<Content>'
        xml += f'<Name>{eventdescr["Name"]}</Name>'
        xml += f'<Category>{eventdescr["Category"]}</Category>'
        xml += f'<Collection>{eventdescr["Collection"]}</Collection>'
        xml += f'<Data>{eventdescr["Data"]}</Data>'
        xml += '</Content>'
        xml += '</EventDescr>'

        return xml

    @CachedProperty
    def short_sha1(self):
        return self.sha1[:7]
        #  return self.get_short_test_id()

    def test_sha1(self):
        """
        Given the characteristics of a test from the point of view of the ROC
        (name, uuid and date), gives the sha1 of the test that will be used to
        refer as an identity of the test.
        """
        # create sha1 object
        sha1 = hashlib.sha1()

        # update the object with information
        sha1.update(self.name.encode())
        sha1.update(self.uuid.encode())
        sha1.update(self.date.strftime(TESTLOG_STRFTIME).encode())

        # create the digest of the hash (the sha1)
        return sha1.hexdigest()

    def get_short_test_id(self, short=6, session=None):
        """
        Given the SHA-1 of a given test, search in the ROC database for a test
        with this already defined ID shorted to the length of the short
        argument. If this short SHA-1 is not unique, do the same thing with
        short incremented by one character.
        """

        # check the size of the short compared to test id
        if len(self.sha1) <= short:
            raise ValueError(
                (
                    'The test ID {0} with length {1} is too small for ' +
                    'shortening it to size {2}'
                ).format(self.sha1, len(self.sha1), short)
            )

        # get the connector of the roc to create a session to query the database
        if session is None:
            session = Connector.manager['MAIN-DB'].get_database().session()

        # query the ROC database for a test ID short as this one
        query = session.query(func.count(TestLog.test_sha))
        query = query.filter(
            TestLog.test_sha.like(self.sha1[:short] + '%')
        )

        # run the query
        try:
            # get number of test matching this short id
            count = query.one()[0]

            # if no one found, we can use the short id
            if count == 0:
                return self.sha1[:short]
            else:
                # run the query again but incrementing the short length
                self.get_short_test_id(short=short + 1, session=session)
        except NoResultFound:
            raise ValueError(
                (
                    'No result found when querying the count of SHA-1 ' +
                    'matching {0}'
                ).format(self.sha1[:short])
            )
        except MultipleResultsFound:
            raise ValueError(
                (
                    'Multiple results found when querying count of SHA-1 ' +
                    'matching {0}'
                ).format(self.sha1[:short])
            )

    def output_directory(self, task):
        """
        Given the pipeline, the name of a test and the ID of the test, create a
        directory for the data output of the test and validate it.

        :param task: Task object
        :return: string containing output directory path
        """
        # get the valid file name of the test, like slug for URL
        valid_filename = get_valid_filename(self.name)

        # get the short test ID
        short_id = self.short_sha1

        # directory where to put results
        path = osp.join(
            task.output,
            '__'.join([valid_filename, short_id, task.provider]),
        )

        # create the directory if not already done
        os.makedirs(path, exist_ok=True)

        # return the path
        return path

    def file_name_format(self, task, prefix,
                         data_version=None,
                         overwrite=False):
        """
        Generate a file name following the ROC convention given the information
        on the pipeline, dataset, etc.

        :param task: Task object
        :param prefix: filename prefix
        :param data_version: version of the output file
        :param overwrite: overwrite any existing output file
        :return: path and name of the output test log file with the right convention.
        """

        # get output directory
        output = self.output_directory(task)

        # pre-process data_version
        if not data_version and self.version:
            data_version = self.version
        elif not data_version and not self.version:
            data_version = '01'

        # generate datetime and free_field
        datetime = '-'.join([self.date.strftime(TIME_RANGE_STRFORMAT),
                             self.terminated_date.strftime(TIME_RANGE_STRFORMAT)])
        free_field = task.provider[:3] + '-' + self.short_sha1

        filepath = self._generate_filepath(output, prefix, datetime, data_version, free_field)

        # If overwrite then replace existing file
        if osp.isfile(filepath) and overwrite:
            return filepath

        # Then increment version to get new file
        while osp.isfile(filepath):
            data_version = f'{int(data_version)+1:02d}'
            filepath = self._generate_filepath(output, prefix, datetime, data_version, free_field)

        return filepath

    @staticmethod
    def _generate_filepath(output, prefix, datetime, version, free_field):
        """
        Generate filepath of test log

        :param output: path of the output directory
        :param prefix: filename prefix
        :param datetime: filename time range
        :param version: filename version
        :param free_field: filename free field
        :return: filepath of test log
        """
        version = 'V' + valid_data_version(version)
        return os.path.join(
            output,
            '_'.join(
                [prefix, datetime, version, free_field.lower()]
            )
        )


    def to_testlog_repr(self):
        """
        Return Test object as a TestLog database representation dictionary .

        :param test_log: Test object to insert
        :param xml: string containing test log file
        :param descriptor: test descriptor XML
        :return: dictionary containing TestLog representation
        """

        return dict(
            file_parent=os.path.basename(self.file_path),
            test_name=self.name,
            test_id=self.uuid,
            test_creation_date=self.creation_date,
            test_descr=self.description,
            test_author=self.author,
            test_status=self.status,
            test_launched=self.date,
            test_terminated=self.terminated_date,
            test_insert_date=dt.datetime.today().strftime(TESTLOG_STRFTIME),
        )

    @staticmethod
    def event_to_packet_log(event, file_log_id):
        """
        Generate a packet log representation of the ROC database from a given eventdescr dictionary.

        :param event: eventdescr to convert
        :param file_log_id: index of the corresponding file_log entry
        :return: packet log dictionary
        """


        # Return a
        return dict(
                packet_length = event['Data'],
                packet_type = event['EventType'][:2],
                packet_category = event['Category'],
                packet_creation_time = None,
                sync_flag = None,
                utc_time = event['EventDate'] + 'T' + event['EventTime'],
                name = None,
                palisade_id = event['Name'],
                raw_data = event['Data'],
                ack_exe_state = None,
                ack_acc_state = None,
                sequence_name = None,
                unique_id = None,
                file_log_id = file_log_id,
                )


    @staticmethod
    def packet_to_packet_log(packet, file_log_id):
        """
        Generate a packet log representation of the ROC database from a given packet dictionary.

        :param packet: packet dictionary to convert
        :param file_log_id: index of the corresponding file_log entry
        :return: packet log dictionary
        """

        data_field_header = packet.get('data_field_header', None)
        if data_field_header:
            packet_creation_time = str(packet['data_field_header'].time[0]) + ':' + str(packet['data_field_header'].time[1])
            sync_flag = packet['data_field_header'].time[2] == 0
        else:
            packet_creation_time = None
            sync_flag = None

        # Return a dictionary with expected fields for packet log representation
        return dict(
                packet_length = packet['header'].packet_length,
                packet_type = packet['type'],
                packet_category = packet['category'],
                packet_creation_time = packet_creation_time,
                sync_flag = sync_flag,
                utc_time = packet['utc_time'],
                name = packet['srdb_id'],
                palisade_id = packet['palisade_id'],
                raw_data = packet['binary'],
                ack_exe_state = packet.get('ack_exe_state', None),
                ack_acc_state = packet.get('ack_acc_state', None),
                sequence_name = packet.get('sequence_name', None),
                unique_id = packet.get('unique_id', None),
                file_log_id = file_log_id,
                )

    @staticmethod
    def packets_to_events(packet_list,
                            collection='IDB',
                            device='S_C',
                            palisade_version=None):
        """
        Build list of EventDescr from input packets list.

        :param packet_list: list of packet data dictionaries
        :param collection: Test event collection.
        :param device: Test event device.
        :param palisade_version: string containing the version of PALISADE IDB
        :return: events a list of dictionaries with expected eventdescr tag values
        """

        # Initialize output list
        nevent = len(packet_list)
        events = [None] * nevent

        # Get PALISADE metadata for current packet
        palisade_metadata_dict = palisade_metadata(
            palisade_version=palisade_version)

        # Loop over each packet
        nvalid = 0
        for i, current_packet in enumerate(packet_list):

            packet_name = current_packet['srdb_id']
            packet_type = current_packet['type']

            if not packet_name:
                logger.warning('#{0} - Unknown packet, skipping!'.format(packet_name))
                continue
            else:
                event_date = current_packet['utc_time'].strftime(TESTLOG_EVENTDATE_STRFORMAT)
                event_time = current_packet['utc_time'].strftime(TESTLOG_EVENTTIME_STRFORMAT)[:-3]
                if packet_type == 'TC':
                    type = 'TC_FEEDBACK'
                else:
                    type = 'TM'

                event = {'id':'0',
                         'EventType':type,
                         'Name':palisade_metadata_dict[packet_name]['palisade_id'],
                         'Category':palisade_metadata_dict[packet_name]['packet_category'],
                         'Data':current_packet['binary'],
                         'EventDate':event_date,
                         'EventTime':event_time,
                         'Collection':collection,
                         'Device': device,
                }

                if packet_type == 'TC':
                    event['Status'] = current_packet['ack_exe_state']

                events[i] = event
                nvalid += 1

        if nvalid < nevent:
            logger.warning(f'{nevent - nvalid} event(s) are not valid!')

        return events[0:nvalid]

    @classmethod
    def from_l0(cls, l0_path):
        """
        Parse input RPW L0 hd5 file and use the information
        to generate an instance of the Test class.

        :param l0_path:
        :param header_only:
        :return:
        """

        # Import L0 class to get list of packets
        from roc.film.tasks.l0 import L0

        l0_basename = os.path.basename(l0_path)
        test_name = os.path.splitext(l0_basename)[0]

        #Get L0 metadata
        l0_header = L0.extract_header(l0_path)

        data_version = l0_header['Data_version']
        try:
            test_uuid = l0_header['Test_uuid']
            description = l0_header['Test_description']
            launch_date = l0_header['Test_launched_date']
            terminated_date = l0_header['Test_terminated_date']
        except:
            logger.warning(f'No "Test_*" attribute found in {l0_path}')
            test_uuid = l0_header['File_ID']
            description = f'Generated by RGTS from {l0_basename}'
            launch_date = l0_header['TIME_MIN']
            terminated_date = l0_header['TIME_MAX']

        # Make sure that times are datetime.datetime object
        launch_date = dt.datetime.strptime(launch_date,
                                  TIME_ISO_STRFORMAT)
        terminated_date = dt.datetime.strptime(terminated_date,
                                      TIME_ISO_STRFORMAT)

        # Get list of packets in the input L0 file
        logger.info(f'Parsing {l0_path} ...')
        l0_packet_list = L0.l0_to_packet_list([l0_path],
                               no_data=True,
                               no_header=True,
                               ascending=True)

        events = [Test.l0_packet_to_event(current_packet, test_uuid)
                  for current_packet in l0_packet_list
                  if L0.is_valid_packet(current_packet)]

        # return the test
        return cls(test_name, launch_date,
                   test_uuid=test_uuid,
                   terminated_date=terminated_date,
                   description=description,
                   events=events,
                   version=data_version)

    @staticmethod
    def l0_packet_to_event(packet, test_uuid,
                            collection='IDB',
                            device='S_C'):
        """
        Convert a RPW L0 packet dictionary into a Test event.

        :param packet: RPW L0 packet dictionary
                       (as returned by roc.film.tasks.l0.L0.l0_to_packet_list method)
        :param test_uuid: UUID of the test
        :param collection: Test event collection
        :param device: MEB GSE event device
        :return: Corresponding Test event
        """

        if packet['palisade_id'].startswith('TC'):
            packet_type = 'TC_FEEDBACK'
        elif packet['palisade_id'].startswith('TM'):
            packet_type = 'TM'
        else:
            logger.error(f'Unknown input packet type ({packet})!')
            packet_type = 'UNKNOWN'

        try:
            if packet['tc_exe_state'] == 'NOT_APPLICABLE':
                status = 'Unknown'
            elif packet['tc_exe_state'] == 'FAILED':
                status = 'Failed'
            elif packet['tc_exe_state'] == 'IDLE':
                status = 'Pending'
            elif packet['tc_exe_state'] == 'PASSED':
                status = 'Terminated'
            else:
                status = 'Unknown'
        except:
            status = None

        event_date = packet['utc_time'].strftime(TESTLOG_EVENTDATE_STRFORMAT)
        event_time = packet['utc_time'].strftime(TESTLOG_EVENTTIME_STRFORMAT)[:-3]

        # Monkey patch due to bug in L0 (should be solved, but let as is in case of)
        try:
            category = packet['category']
            if packet['category'][0] != '/' :
                category = '/'+packet['category']
        except:
            category = None

        eventdescr = {'EventDate': event_date,
                      'EventTime': event_time,
                      'Name': packet['palisade_id'],
                      'Data': packet['binary'],
                      'Device': device,
                      'TestUUID': test_uuid,
                      'EventType': packet_type,
                      'EventID': None, # Not defined at this stage
                      'Category': category,
                      'Collection': collection,
                      'Status': status
                      }

        return eventdescr

def parse_ads_file(input_file,
                   remove_header=None):
    """
    Parse ADS GSE text file.

    :param input_file: input ADS text file containing the TM/TC packets
    :param remove_header: header in bytes to remove
    :returns: list of packets dictionary with 'binary' and 'utc_time' keywords
    """

    # Initialize outputs
    packets = []

    if not os.path.isfile(input_file):
        raise FileNotFoundError(f'{input_file} NOT FOUND, ABORTING!')

    # TODO - Add timemin, timemax

    # Open input file
    with open(input_file, 'r') as file_buffer:
        # And extract data
        for i, line in enumerate(file_buffer):
            items = line.split(' ')
            if len(items) != 2:
                logger.warning(f'Line #{i} is not well formatted, skip it! ({line})')
                continue

            # Get time
            time = items[0].strip()
            if time == INVALID_ADS_TIME:
                logger.warning(f'Invalid time at line #{i}, skip it!')
                continue
            else:
                utc_time = dt.datetime.strptime(time, INPUT_TIME_STRFORMAT)

            # Get tm packet in hexadecimal
            binary = items[1].strip()
            if remove_header:
                binary = bytearray.fromhex(binary)[remove_header:].hex()

            # Add binary_packet and corresponding time to the outputs
            packets.append({'binary': binary, 'utc_time': utc_time})

    return packets


def is_excluded(category, included_categories=['/RPW', ]):
    """
    Says if a category with its subcategory can be safely considered as
    excluded from the list of path for categories to exclude.
    """
    path = Path(category)

    # convert to path
    included_path_categories = map(lambda x: Path(x), included_categories)

    return not any(
        map(
            lambda x: x in path.parents or x == path,
            included_path_categories,
        )
    )

def to_test_log_repr(test_log, test_file, descriptor):
    """
    Create a test log representation given the XML target and
    the XML descriptor element to place values inside the representation of the
    test log.

    :param test_log: Test object to insert
    :param xml: string containing test log file
    :param descriptor: test descriptor XML
    :return: TestLog representation
    """

    general_info = descriptor.find('GeneralInfo')
    execution_info = descriptor.find('ExecutionInformation')
    description = general_info.find('LongDescription')
    author = general_info.find('Author')

    return TestLog(
        file_parent=os.path.basename(test_file),
        test_name=descriptor.get('TestName'),
        test_id=descriptor.get('TestUUID'),
        test_creation_date=general_info.find('CreationDate').text,
        test_descr=description.text if description is not None else None,
        test_author=author.text if author is not None else None,
        test_status=execution_info.find('Status').text,
        test_launched=execution_info.find('LaunchedDate').text,
        test_terminated=execution_info.find('TerminatedDate').text,
        test_sha=test_log.sha1,
        test_insert_date=dt.datetime.today().strftime(TESTLOG_STRFTIME),
    )
