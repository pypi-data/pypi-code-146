#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUEST plugin tasks related to ADS GSE ASCII file handling."""

import sys
import os
import uuid

from edds_process.response.make import make_tmraw_xml, make_tcreport_xml

try:
    from poppy.core.logger import logger
    from poppy.core.db.connector import Connector
    from poppy.core.db.handlers import get_or_create_with_info
    from poppy.core.task import Task
    from poppy.core.target import FileTarget, PyObjectTarget
    from poppy.core.db.dry_runner import DryRunner
except:
    sys.exit("POPPy framework seems to not be installed properly!")


from roc.guest.guest import Test
from roc.guest.guest import parse_ads_file

__all__ = ['raw_to_txt', 'test_to_txt', 'txt_to_test']

# time format in the ADS GSE ASCII file (e.g. 2019-11-06T10:53:35.195Z)
ADS_STRFTIME = '%Y-%m-%dT%H:%M:%S.%f'

@PyObjectTarget.input(identifier='raw_data')
@FileTarget.output(identifier='ads_gse_txt')
@Task.as_task(plugin_name='roc.guest', name='raw_to_txt')
def raw_to_txt(task):
    # get the raw data from pipeline properties
    try:
        raw_data = task.inputs['raw_data'].value
    except:
        logger.error("No input RawData object defined, aborting!")
        return

    # Get output file path from input argument
    output_file = task.pipeline.args.ads_gse_txt

    logger.info(f'Writing {output_file}...')
    with open(output_file, 'w') as out_file:
        for current_packet in raw_data.packet_list:
            utc_time = current_packet['utc_time'].strftime(ADS_STRFTIME)[:-3] + 'Z'

            out_file.write(" ".join([utc_time,
                           current_packet['binary']]) + "\n")

    if os.path.isfile(output_file):
        logger.info("{0} saved".format(output_file))
    else:
        logger.error(f'Writing {output_file} has failed!')

    task.outputs['ads_gse_txt'].filepath = output_file

def get_ads_gse_txt(pipeline):
    """
    Get path of the ads gse txt file

    :param pipeline:
    :return:
    """
    return pipeline.args.ads_gse_txt


@DryRunner.dry_run
@FileTarget.input(identifier='ads_gse_txt', filepath=get_ads_gse_txt)
@PyObjectTarget.output(identifier='raw_data')
@Task.as_task(plugin_name='roc.guest', name='txt_to_test')
def txt_to_test(task):
    """
    Generate a Test instance from an input ADS GSE Text file.

    :param task:
    :return:
    """

    # Get --remove-header keyword value, if set
    try:
        header = task.pipeline.args.remove_header
    except:
        header = None

    # Parse ads file
    ads_gse_txt = task.inputs['ads_gse_txt'].filepath
    logger.info("Parsing {0}...".format(ads_gse_txt))
    raw_binary_packets = parse_ads_file(ads_gse_txt,
                                        remove_header=header)

    # Get packet times to compute min/max
    packet_times = [pkt['utc_time'] for pkt in raw_binary_packets]

    # Create test object from ADS text file...
    launched_date = min(packet_times)
    terminated_date = max(packet_times)
    test_log = Test(
        os.path.basename(os.path.splitext(ads_gse_txt)[0]),
        launched_date,
        test_uuid=str(uuid.uuid4()),
        creation_date=launched_date, # we assume that creation_date = launched_date
        description="Test created from {0}".format(ads_gse_txt),
        terminated_date=terminated_date,
        status='Terminated',
        file_path=ads_gse_txt,
    )

    # Add packet list to test object
    test_log.packet_list = raw_binary_packets

    logger.info(f'{len(raw_binary_packets)} packets retrieved from {ads_gse_txt}')

    # And insert it into the pipeline
    task.outputs['raw_data'].value = test_log

@FileTarget.input(identifier='txt_ads_file')
@FileTarget.output(identifier='dds_response_xml')
@Task.as_task(plugin_name='roc.guest', name='txt_to_dds')
def txt_to_dds(task):
    """
    Convert an input ADS GSE ASCII file into a MOC DDS response XML file.

    :param task:
    :return:
    """

    # Get --remove-header keyword value, if set
    try:
        header = task.pipeline.args.remove_header
    except:
        header = None

    # Get DDS XML filepath from output_file input argument
    try:
        output_file = task.pipeline.args.dds_response_xml
    except:
        logger.error('No output filename passed as argument, aborting')
        return None

    # Parse ads file
    ads_gse_txt = task.inputs['ads_gse_txt'].filepath
    logger.info("Parsing {0}...".format(ads_gse_txt))
    packet_times, raw_binary_packets = parse_ads_file(ads_gse_txt,
                                                     remove_header=header)
    # Generate output DDS XML
    # FIXME - Must filter between TM and TC data
    if make_tmraw_xml(raw_binary_packets, task.pipeline.properties.output_file,
                    overwrite=task.pipeline.properties.overwrite):
        logger.info("{0} saved".format(output_file))
    else:
        logger.error(f'Writing {output_file} has failed!' )

    # Set filepath value of output target
    task.outputs["dds_response_xml"].filepath = output_file

@DryRunner.dry_run
@PyObjectTarget.input(identifier='raw_data')
@FileTarget.output(identifier='ads_gse_txt')
@Task.as_task(plugin_name='roc.guest', name='test_to_txt')
def test_to_txt(task):
    """

    :param task:
    :return:
    """

    # Get test log raw data
    test_log = task.inputs['raw_data'].value

    # Get output file path
    output_file = task.pipeline.args.ads_gse_txt

    try:
        nevents = 0
        with open(output_file, "w") as file_out:
            # parse input test log XML and iterate on each EventDescr tag
            for event in test_log.events:
                time = "T".join([event["EventDate"], event["EventTime"]]) + "Z"
                row = " ".join([time, event["Data"]]) + "\n"
                file_out.write(row)
                logger.debug("Saving {0} into {1}".format(row, output_file))
                nevents += 1
    except Exception as e:
        logger.error(f'Writing {output_file} has failed: {e}')
    else:
        # events found
        if nevents == 0:
            logger.info("No event found in the input file, output file is empty!")
        else:
            logger.info("{0} event(s) saved into {1}".format(nevents, output_file))
    finally:
        task.outputs['ads_gse_txt'].filepath = output_file







