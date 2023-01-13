#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUEST plugin tasks related to ROC database."""

import sys

from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from roc.guest.exceptions import ClearTestError, RocDbTransactionError

try:
    from poppy.core.logger import logger
    from poppy.core.db.connector import Connector
    from poppy.core.db.handlers import get_or_create_with_info
    from poppy.core.task import Task
    from poppy.core.target import FileTarget, PyObjectTarget
    from poppy.core.db.dry_runner import DryRunner
    from poppy.core.conf import settings
except:
    print('POPPy framework seems to not be installed properly!')

from roc.guest.models.test import TestLog
from roc.guest.models.packet import PacketLog
from roc.guest.guest import Test

__all__ = ['test_to_rocdb', 'clear_test']

# get the task test_to_db
@PyObjectTarget.input(identifier='raw_data')
@Task.as_task(plugin_name='roc.guest', name='test_to_rocdb')
@Connector.if_connected(settings.PIPELINE_DATABASE)
def test_to_rocdb(task):
    """
    To put into the ROC database a given Test object.
    """
    # get the test instance
    test_log = task.inputs['raw_data'].value

    # get the database session
    session = task.pipeline.db.session

    # Create file log entry in the ROC database from test log data
    file_log, created = get_or_create_with_info(
        session,
        TestLog,
        test_id=str(test_log.uuid),
        create_method_kwargs=test_log.to_testlog_repr(),
    )

    # If test log already saved in the database, skip the insertion
    if created == False:
        logger.info(f'Test {test_log.name} ({test_log.uuid}) already inserted into the database')
        return None

    try:
        file_log_id = file_log.id_file_log
    except:
        logger.error(f'Inserting test {test_log.name} ({test_log.uuid}) has failed!')
        return None

    # Extract test events as PacketLog entries
    if len(test_log.packet_list) > 0:
        # If packet_list exists, insert it
        packets = [Test.packet_to_packet_log(packet, file_log_id) for packet in test_log.packet_list]
    else:
        # Else just insert events as retrieved from test log
        logger.info(f'Inserting "as is" events from test {test_log.name} ({test_log.uuid})')
        packets = [Test.event_to_packet_log(event, file_log_id) for event in test_log.events]


    # commit to database if there are events to insert (those with data)
    if len(packets) > 0:
        engine = session.bind
        engine.execute(
            PacketLog.__table__.insert(),
            packets,
        )


@DryRunner.dry_run
@Task.as_task(plugin_name='roc.guest', name='clear_test')
@Connector.if_connected(settings.PIPELINE_DATABASE)
def clear_test(task):
    """
    Clear a test from the ROC database given a name and an UUID.
    """
    # get a session from the ROC database
    database = task.pipeline.db.get_database()

    # check the database is connected
    database.connectDatabase()

    # check that the connection is made
    if not database.connected:
        message = '{0} is not connected'.format(database)
        logger.error(message)
        raise RocDbTransactionError(message)

    # get the arguments
    filters = []

    if ('clear_all' in task.pipeline.args and
            task.pipeline.args.clear_all is True):
        filters.append(TestLog.test_name.like('%'))
    else:
        if task.pipeline.args.test_name is not None:
            filters.append(TestLog.test_name ==
                           task.pipeline.args.test_name[0])
        elif ('pattern' in task.pipeline.args and
                task.pipeline.args.pattern is not None):
            filters.append(TestLog.test_name.like(
                task.pipeline.args.pattern[0]))

        if task.pipeline.args.test_uuid is not None:
            filters.append(TestLog.test_id ==
                           task.pipeline.args.test_uuid[0])

        # If --end-time option is set, add an upper time limit
        if ('end_time' in task.pipeline.args and
                task.pipeline.args.end_time is not None):
            filters.append(TestLog.test_terminated <= task.pipeline.args.end_time[0])

        # If --start-time option is set, add an lower time limit
        if ('start_time' in task.pipeline.args and
                task.pipeline.args.start_time is not None):
            filters.append(TestLog.test_launched >= task.pipeline.args.start_time[0])

    # get the test(s) from the database
    with database.query_context() as session:
        try:
            tests = session.query(TestLog).filter(
                and_(*filters)).all()
        except NoResultFound:
            pass
        except:
            logger.exception(f'Removing test [{filters}] from ROC database has failed!')
            raise RocDbTransactionError

        if len(tests) == 0:
            logger.warning('No test found with input criteria in the ROC database!')
            return

        # now remove the test(s)
        for test in tests:
            logger.info('Removing test {0} from the ROC database...'.format(
                test[0].test_name))
            # from the database
            session.delete(test[0])
            session.commit()
