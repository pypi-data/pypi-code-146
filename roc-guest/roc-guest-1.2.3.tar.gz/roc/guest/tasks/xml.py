#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUEST plugin tasks related to MEB GSE test log XML handling."""

import os
import sys
import getpass
from shutil import copyfile as copy
from datetime import datetime

try:
    from poppy.core.logger import logger
    from poppy.core.db.connector import Connector
    from poppy.core.db.handlers import get_or_create_with_info
    from poppy.core.task import Task
    from poppy.core.target import FileTarget, PyObjectTarget
    from poppy.core.db.dry_runner import DryRunner
except:
    sys.exit('POPPy framework seems to not be installed properly!')

from roc.guest.guest import Test
from roc.guest.exceptions import ParseTestXmlError, GuestNoInputError
from roc.guest.constants import JENV, TESTLOG_TEMPLATE, TESTLOG_STRFTIME, \
    TESTLOG_EVENTDATE_STRFORMAT, TESTLOG_EVENTTIME_STRFORMAT

__all__ = ['xml_to_test', 'test_to_xml', 'copy_xml']

def get_test_log_xml(pipeline):
    # Pass the test_log_xml argument as the value of the input target test_log_xml of xml_to_test task
    try:
        return pipeline.args.test_log_xml[0]
    except:
        pass

@FileTarget.input(identifier='test_log_xml', filepath=get_test_log_xml)
@PyObjectTarget.output(identifier='raw_data')
@Task.as_task(plugin_name='roc.guest', name='xml_to_test')
def xml_to_test(task):
    """
    Parse test log XML and save content in a Test object.

    Parse header of the xml test log file
    """
    # Get test log file path

    test_file = task.inputs['test_log_xml'].filepath

    # Create test_log object
    test_log = Test.from_testlog_xml(test_file)

    # Check if test status is "Terminated"
    if ('terminated' in task.pipeline.args and
            task.pipeline.args.terminated == True and
            test_log.status != 'Terminated'):
        msg = '{0} is not terminated!'.format(test_file)
        logger.error(msg)
        raise ParseTestXmlError(msg)

    # TODO - improve this part to include packet_list setting into the Test class directly
    # raw data packets are stored in a list
    nevents = len(test_log.events)
    raw_binary_packets = [None] * nevents
    for i, event in enumerate(test_log.events):
        packet_type = event['EventType'][:2]

        # Only keep time for TC
        # (TM EventData-EventTime is not packet time creation in UTC)
        if packet_type == 'TM':
            utc_time = None
            ack_acc_state = None
            ack_exe_state = None
        else:
            utc_time = datetime.strptime(
                event['EventDate'] + 'T' + event['EventTime'],
                TESTLOG_EVENTDATE_STRFORMAT + 'T' + TESTLOG_EVENTTIME_STRFORMAT)
            if event.get('Status', 'UNKNOWN') == 'OK':
                ack_exe_state = 'PASSED'
                ack_acc_state = 'PASSED'
            elif event.get('Status', 'UNKNOWN') == 'NOK':
                ack_exe_state = 'FAILED'
                ack_acc_state = 'FAILED'
            else:
                ack_exe_state = 'UNKNOWN'
                ack_acc_state = 'UNKNOWN'

        raw_binary_packets[i] = {
            'binary': event['Data'],
            'palisade_id': event['Name'],
            # 'srdb_id': palisade_metadata[event["Name"]]['srdb_id'],
            'description': event['Name'],
            'category': event['Category'],
            'type': packet_type,
            'utc_time': utc_time,
            'ack_acc_state': ack_acc_state,
            'ack_exe_state': ack_exe_state,
        }

    # save the packet list in the test object
    test_log.packet_list = raw_binary_packets

    logger.info(f'{len(test_log.packet_list)} packets extracted from {test_file}')

    # Store test log in the pipeline
    task.outputs['raw_data'].value = test_log

@PyObjectTarget.input(identifier='raw_data')
@FileTarget.output(identifier='test_log_xml')
@Task.as_task(plugin_name='roc.guest', name='test_to_xml')
def test_to_xml(task):
    """
    Create an output XML file from the test log object stored in the pipeline properties
    :param task:
    :return:
    """

    # Retrieve input test log data
    try:
        # Get input test log object
        test_log = task.inputs['raw_data'].value
    except:
        logger.error('No input test_log data found for test_to_xml task!')
        return

    # Get data version (if any)
    data_version = task.pipeline.get('data_version', default=[None])[0]

    # Get overwrite argument or define it
    overwrite = task.pipeline.get('overwrite', default=False, args=True)

    if len(test_log.events) == 0 and len(test_log.packet_list) == 0:
        logger.warning('No event found in input raw_data')
    elif len(test_log.events) == 0 and len(test_log.packet_list) != 0:
        if test_log.packet_parser.idb_source == 'PALISADE':
            palisade_version = test_log.packet_parser.idb_version
        else:
            palisade_version = None
        test_log.events = Test.packets_to_events(test_log.packet_list,
                                                 palisade_version=palisade_version)

    # get output filepath
    xml_path = task.pipeline.get('test_log_xml',
                                 default=[None],
                                 args=True)[0]

    # if no file path, then generate it
    if xml_path is None:
        xml_path = test_log.file_name_format(
                task.pipeline,
                'solo_L0_rpw-mebgse-testlog',
                data_version=data_version,
                overwrite=overwrite) + '.xml'

    # Load GSE test log template
    template = JENV.get_template(TESTLOG_TEMPLATE)

    # Build the MEB GSE test log XML template render
    render = template.render(name=test_log.name,
                             uuid=test_log.uuid,
                             creation_date=test_log.creation_date.strftime(TESTLOG_STRFTIME),
                             author=getpass.getuser(),
                             description=test_log.description,
                             status=test_log.status,
                             launched=test_log.date.strftime(TESTLOG_STRFTIME),
                             terminated=test_log.terminated_date.strftime(TESTLOG_STRFTIME),
                             event_list=test_log.events,
                             )

    # Generate the XML
    # open a file with the name
    if os.path.isfile(xml_path) and not overwrite:
        logger.warning(f'{xml_path} already exists, aborting!')
    else:
        logger.info(f'Saving {xml_path}...')
        # Create output MEB GSE test log file
        with open(xml_path, 'w') as outfile:
            outfile.write(render)

    task.outputs['test_log_xml'].filepath = xml_path

@DryRunner.dry_run
@FileTarget.input(identifier='test_log_xml', filepath=get_test_log_xml)
@FileTarget.output(identifier='test_log_xml')
@Task.as_task(plugin_name='roc.guest', name='copy_xml')
def copy_xml(task):
    """
    Task to copy the input Test log LZ file into the output test directory
    with the ROC LZ filename convention (see ROC-TST-GSE-NTT-00017-LES doc.)
    (Use with from_xml command in dryrun mode only)

    :param task:
    :return:
    """

    # get the input target filepath
    input_testlog_xml = task.inputs['test_log_xml'].filepath

    # Create test log object
    test_log = Test.from_testlog_xml(input_testlog_xml)

    # Build the name of the output file
    output_testlog_xml = test_log.file_name_format(
        task,
        'solo_LZ_rpw-gse-test-log',
    ) + '.xml'

    # # Copy new test log into the output dir.
    logger.info('Copying {0} into {1}'.format(input_testlog_xml, output_testlog_xml))
    copy(input_testlog_xml, output_testlog_xml)
    if not os.path.isfile(output_testlog_xml):
        raise logger.error(
            'The test log file {0} has not been copied correctly in {1}!'.format(input_testlog_xml, output_testlog_xml))
    # else:
        #logger.debug("The test log file {0} has been copied correctly in {1}!".format(init_test_log, new_test_log))

    task.outputs['test_log_xml'].filepath = output_testlog_xml
