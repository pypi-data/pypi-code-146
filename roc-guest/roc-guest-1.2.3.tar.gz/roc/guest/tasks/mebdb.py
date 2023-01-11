#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUEST plugin tasks related to MEB GSE database handling."""

import sys
from datetime import datetime
from threading import Thread
from queue import Queue

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import and_

try:
    from poppy.core.logger import logger
    from poppy.core.db.connector import Connector
    from poppy.core.db.handlers import get_or_create_with_info
    from poppy.core.task import Task
    from poppy.core.target import FileTarget, PyObjectTarget
    from poppy.core.db.dry_runner import DryRunner
except:
    sys.exit('POPPy framework seems to not be installed properly, exiting!')


from roc.guest.models.test import TestLog

from roc.guest.models.meb_gse_data.test import Descriptor
from roc.guest.models.meb_gse_data.packet import PacketType
from roc.guest.models.meb_gse_data.parser import ParserCollection
from roc.guest.models.meb_gse_data.event import Event
from roc.guest.models.meb_gse_data.device import Device
from roc.guest.exceptions import MebDbTransactionError
from roc.guest.constants import TESTLOG_STRFTIME
from roc.guest.guest import Test



__all__ = ['test_to_mebdb', 'mebdb_to_test']

class mebdb_to_test(Task):

    plugin_name = 'roc.guest'
    name = 'mebdb_to_test'

    def add_targets(self):
        self.add_output(target_class=PyObjectTarget,
                        identifier='test_descriptors')

    def set_filters(self):

        # If --Terminated option is set, only get Terminated tests
        if ('terminated' in self.pipeline.args and
                self.pipeline.args.Terminated is True):
            self.terminated = True
        else:
            self.terminated = False

        # If pattern option is set, retrieve
        # only tests that contain the pattern string
        if ('pattern' in self.pipeline.args and
                self.pipeline.args.pattern is not None):
            self.pattern = self.pipeline.args.pattern[0]
        else:
            self.pattern = None

        # If --time-max option is set, add an upper time limit
        if ('time_max' in self.pipeline.args and
                self.pipeline.args.time_max is not None):
            self.time_max = datetime.strptime(
                self.pipeline.args.time_max[0], TESTLOG_STRFTIME)
        else:
            self.time_max = None

        # If --time-min option is set, add an lower time limit
        if ('time_min' in self.pipeline.args and
                self.pipeline.args.time_min is not None):
            self.time_min = datetime.strptime(
                self.pipeline.args.time_min[0], TESTLOG_STRFTIME)
        else:
            self.time_min = None

    def run(self):

        """
        Task to generate an output XML file containing
        test log data retrieved from the MEB GSE database.

        :param task:
        :return:
        """

        # Set input filters
        self.set_filters()

        # Extract TestDescriptor of the requested test log data
        self.test_descriptors = self.extract_descriptors()

        # Set output target value
        self.outputs['test_descriptors'].value = self.test_descriptors


    @Connector.if_connected('MEB')
    def extract_descriptors(self):
        """
        Extract tests from the MEB GSE database.

        :param time_min: Get only test data after time_min (datetime object)
        :param time_max: Get only test data before time_max (datetime object)
        :param pattern: Get only test data with input pattern (MySQL regex string)
        :param terminated: if True only get test data for terminated test
        :return: Descriptor object filled with requested test data
        """

        # get the meb connector and get the database
        connector = Connector.manager['MEB']
        database = connector.get_database()

        # check the database is connected
        database.connectDatabase()

        # get the selected database from the MEB connector
        self.meb = connector.selected

        # connect to the database
        self.meb.connectDatabase()

        # check that the connection is made
        if not self.meb.connected:
            message = '{0} is not connected'.format(self.meb)
            logger.error(message)
            raise MebDbTransactionError(message)

        # Add input filters
        filters = []
        # If --Terminated option is set, only get Terminated tests
        if self.terminated == True:
            filters.append(Descriptor.Status == 'Terminated')

        # If pattern option is set, retrieve
        # only tests that contain the pattern string
        if self.pattern:
            filters.append(Descriptor.TestName.like(self.pattern))

        # If --time-max option is set, add an upper time limit
        if self.time_max:
            filters.append(Descriptor.TerminatedDate <= self.time_max)

        # If --time-min option is set, add an lower time limit
        if self.time_min:
            filters.append(Descriptor.Launched >= self.time_min)

        # get a session
        with self.meb.query_context() as session:
            # get list of tests in MEB GSE database
            try:
                return session.query(
                    Descriptor.TestName,
                    Descriptor.UUID,
                    Descriptor.XML,
                    Descriptor.Launched,
                    Descriptor.TerminatedDate,
                    Descriptor.Status,
                    Descriptor.CreationDate,
                    Descriptor.Description,
                    Descriptor.Author,
                ).filter(and_(*filters))
            except NoResultFound:
                logger.info('MEB GSE database query has returned no result!')
                return []

    def generator(self, loop):
        """Test log generator."""

        # reference to the pipeline
        pipeline = loop.pipeline

        # reference to the start task
        start_task = loop.start

        # reference to the end task
        end_task = loop.end

        # loop over tests into the MEB GSE database
        nextracted = 0

        for test_desc in loop.inputs['test_descriptors']:

            # check that the test is already present in the ROC database or not
            with self.meb.query_context() as session:
                if session.query(FileLog).filter_by(
                    file_id=test_desc.value.UUID,
                    file_name=test_desc.value.TestName,
                    is_test=True,
                ).count():
                    logger.info('{0} already loaded'.format(test_desc.value.TestName))
                    continue

            # set the test to parse
            logger.info('Extracting test {0}'.format(test_desc.value.TestName))
            self.test_descriptor = test_desc.value
            try:
                self.extract_events()
            except Exception as e:
                logger.error(f'Test {test_desc.value.TestName} ({test_desc.value.UUID}) has not event, skip it')
                continue
            else:
                test_desc.value = mebdb_to_test.to_test(self.test_descriptor, self.test_events)
                nextracted += 1

            # replace the 'raw_data' target by the test_desc instance
            test_desc.link('raw_data')

            yield

        if nextracted == 0:
            logger.info('All requested tests have been already extracted!')
            sys.exit(1)

    @Connector.if_connected('MEB')
    def extract_events(self):
        """
        A simple method that convert a test log from the
        MEB GSE database into an XML file.
        """

        # Initialize output test events list
        self.test_events = []

        if not self.test_descriptor:
            logger.error('No input test_descriptor defined!')
            return []

        # number of events
        logger.debug(
            'Counting number of events for test {0}'.format(
                self.test_descriptor.TestName
            )
        )
        with self.meb.query_context() as session:
            query = session.query(Event.XML).join(Descriptor).filter(
                Descriptor.TestName == self.test_descriptor.TestName and
                Descriptor.UUID == self.test_descriptor.UUID
            )
            nevents = query.count()
            logger.info(
                '{0} test events to retrieve'.format(nevents)
            )

        # create a queue to transfer data
        queue = Queue()

        # create a thread to request the data regularly from the database
        thread = Thread(
            target=self.worker,
            args=[self, queue, 10000, nevents],
        )

        # start the thread
        thread.start()

        # loop while there is data
        offset = 0
        event_list = []
        while (offset < nevents):
            # get the offset and the events
            logger.debug('Waiting data from thread')
            step, data = queue.get()
            logger.debug('Process events from thread')

            # increase offset
            offset = step

            # loop over events to add them into the xml
            for event in data:
                # read the xml in the string
                try:
                    event_list.append(event.XML)
                except:
                    logger.error("Can't convert test event into XML")
                    return []

            logger.debug('Events processed')

        # block until end
        thread.join()

        self.test_events = event_list

    @staticmethod
    def to_test(test_descriptor, test_events):
        """
        Convert input test_descriptor and test_events data
        into a Test class instance

        :return: Test class instance containing test_descriptor/test_events data
        """

        # Create Test instance with info in test_descriptor
        launched_date = datetime.strptime(test_descriptor.Launched, TESTLOG_STRFTIME)
        terminated_date = datetime.strptime(test_descriptor.TerminatedDate, TESTLOG_STRFTIME)
        creation_date = datetime.strptime(test_descriptor.CreationDate, TESTLOG_STRFTIME)

        test_instance = Test(
            test_descriptor.TestName, launched_date,
            test_uuid=test_descriptor.UUID,
            creation_date=creation_date,
            description=test_descriptor.Description,
            terminated_date=terminated_date,
            status=test_descriptor.Status,
            author=test_descriptor.Author,
        )

        # Generate the list of test events
        test_instance.events = [test_event for test_event in test_instance.events_from_string(test_events)]

        # return test instance
        return test_instance

    @staticmethod
    def worker(self, queue, step, nmax):
        """
        Worker in an other thread, to get the events by windows, in order to
        process it in the same time.
        """
        # init the offset
        offset = 0

        # loop while not reaching the end
        while (offset < nmax):
            # make the query to get events associated to the test. Do not use
            # the relationship of sqlalchemy since it keeps in memory the
            # attribute of events and doesn't allow it to be removed, else a
            # DELETE statement is performed on the database
            with self.meb.query_context() as session:
                query = session.query(Event.XML).join(Descriptor).filter(
                    Descriptor.TestName == self.test_descriptor.TestName and
                    Descriptor.UUID == self.test_descriptor.uuid
                )
                # query events in the window
                logger.debug('Get {0} events maximum from thread'.format(step))
                events = query.limit(step).offset(offset).all()

            # increase the offset
            offset += step

            # put the data in the queue
            logger.debug('Sending events to the queue')
            queue.put((offset, events))

@PyObjectTarget.output(identifier='raw_data')
@Task.as_task(plugin_name='roc.guest', name='test_to_mebdb')
@Connector.if_connected('MEB')
def test_to_mebdb(task):
    """
    Insert a test log object data into a MEB GSE database

    :param test_log: Test object to insert
    :return: True if correctly inserted, False otherwise
    """

    # Get input value
    test_log = task.outputs['raw_data'].value

    # get the meb connector and get the database
    connector = Connector.manager['MEB']
    database = connector.get_database()

    # check the database is connected
    database.connectDatabase()

    # get the selected database from the MEB connector
    meb = connector.selected

    # connect to the database
    meb.connectDatabase()

    # check that the connection is made
    if not meb.connected:
        message = '{0} is not connected'.format(meb)
        logger.error(message)
        raise MebDbTransactionError(message)

    # Insert test log TestDescriptor data into the MEB GSE database
    logger.info(f'Inserting test log [{test_log.name}, {test_log.uuid[:7]}] into {meb} ({len(test_log.events)} events to insert) ...')
    with meb.query_context() as session:

        descriptor, is_created = get_or_create_with_info(
            session,
            Descriptor,
            TestName=test_log.name,
            Status=test_log.status,
            Author=test_log.author,
            Description=test_log.description,
            CreationDate=test_log.creation_date,
            Launched=test_log.date,
            TerminatedDate=test_log.terminated_date,
            UUID=test_log.uuid,
            XML=test_log.descriptor_xml,
            OneShot=1
        )

    # If already found, then aborting
    if is_created == False:
        logger.info(f'Test {test_log.uuid} already found in the database')
        return False

    # Loop over test events
    logger.debug(f'test log description inserted')
    logger.debug(f'Inserting test event data ...')
    for event in test_log.events:

        with meb.query_context() as session:

            # Get all needed ID from MEB db

            query_collection = session.query(ParserCollection).filter(
                ParserCollection.CollectionName == event['Collection']
            )
            query_event = session.query(PacketType).filter(
                PacketType.Type == event['EventType']
            )
            query_desc = session.query(Descriptor).filter(
                Descriptor.TestName == test_log.name
            )
            query_device = session.query(Device).filter(
                Device.DeviceName == event['Device']
            )

            dic = [
                {'item_name': 'collection_id', 'query': query_collection, 'item_value' : event['Collection'] },
                {'item_name': 'event_id', 'query': query_event,'item_value': event['EventType']},
                {'item_name': 'descriptor_id', 'query': query_desc,'item_value' : test_log.name },
                {'item_name': 'device_id', 'query': query_device,'item_value' :event['Device'] }
            ]

            res = {}
            for item in dic:
                val = item['item_value']
                name = item['item_name']
                try:
                    res[name] = int(item['query'].one().ID)
                except NoResultFound:
                    logger.error(f'No {name} found for {val} in the MEB GSE database!')
                    break
                except MultipleResultsFound:
                    logger.error(f'More than one {name} found for { val } in the MEB GSE database!')
                    break

            # Insert test log event data into MEB GSE database
            event, is_created = get_or_create_with_info(
                session,
                Event,
                DateProduction=event['EventDate'] + 'T' + event['EventTime'],
                XML=event['XML'],
                Device=res['device_id'],
                PacketType=res['event_id'],
                AssociatedTest=res['descriptor_id'],
                Category=event['Category'],
                Name=event['Name'],
                Collection=res['collection_id'],
            )
            if is_created == False:
                logger.error(f'Current event not inserted: ({event})')
                logger.debug(
                    DateProduction=event['EventDate'] + 'T' + event['EventTime'],
                    XML=event['XML'],
                    Device=res['device_id'],
                    PacketType=res['event_id'],
                    AssociatedTest=res['descriptor_id'],
                    Category=event['Category'],
                    Name=event['Name'],
                    Collection=res['collection_id']
                )
                continue

    logger.debug(f'Test event data inserted')
    return True
