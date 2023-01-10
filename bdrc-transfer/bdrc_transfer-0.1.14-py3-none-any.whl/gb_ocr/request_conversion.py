#!/usr/bin/env python3
"""
Requests conversion of an image group. Will have to fill in with gb auth.
Note that a network trace of the POST data for selecting some barcodes and clicking submit
gives:
(target URL is /libraries/TBRC/_process
Document_process
1 / 7 requests
3.6 kB / 47.5 kB transferred
3.6 kB / 122 kB resources
Finish: 611 ms
DOMContentLoaded: 406 ms
Load: 501 ms
process_format=html
&barcodes=W1PD159424-I3PD77
&barcodes=W1PD159424-I3PD80
&barcodes=W1PD159424-I3PD87
&barcodes=W1PD159424-I3PD89
&barcodes=W1PD159424-I3PD90
&table_result_count=%2Flibraries%2FTBRC%2F_available%3Fresult_count%3D50
(decoded: /libraries/TBRC/_available?result_count=50)
"""
import argparse
import fileinput
import logging
from datetime import datetime

from gb_lib.GbLib import VolumeToWork
from gb_ocr.GRINConfig import GRINConfig
from log_ocr.AORunLog import AORunActivityLog
from gb_ocr.grin_lib.GRINOps import GRINGet, GRINProcessRequest

from gb_lib import GbLib as lib

activity: str = "request_conversion"
dest_token: str = "content"

log: AORunActivityLog


def request_one(image_group: str, args: argparse.Namespace):
    """

    :param image_group: image group to request
    :param args:
    :return: system settings
    """

    # Seriously, hurl if this doesn't work
    v_w: VolumeToWork = VolumeToWork(image_group)
    a_rc: int = -1
    try:
        if args.log_after_fact:
            log.runtime_logger.info(f"Simulating {activity} for {image_group}:{dest_token}")
            a_rc = 0
        else:
            request_conversion([image_group])
            a_rc = 0
    finally:
        log.activity_db_logger.add_content_activity(
            work_rid=v_w.work_name, activity=activity,
            image_group_label=image_group, activity_rc=a_rc, start_time=datetime.now())
        log.activity_logger.info(f"success:{activity}:{image_group}:{dest_token}")


# This set of headers is deduced from observation of the web page
# Don't include 'Barcode' and 'Scanned Date' we separate those out.
books_available_to_convert_extra_headers = ['Processed Date', 'Analyzed Date', 'OCR''d Date',
                                            'Google Books']


def parse_available_return(grin_text_return: [str]) -> [{}]:
    """
    Parse GRIN return from available
    :param grin_text_return:
    Choice of scanned date is arbitrary - to provide a unique index based on volume id and time
    :return: [ { 'Barcode' : volumeid , 'Scanned Date': datetime gb_data: { 	'Processed Date': ... ,
    'Analyzed Date':...,	'OCR Date':...,	'Google Books':...} } ]
    """
    out_data: [{}] = []
    for a_text in grin_text_return:
        a_text_data = a_text.split('\t')
        barcode: str = a_text_data[0]
        scanned_date: str = a_text_data[1]
        available_row = dict(zip(books_available_to_convert_extra_headers, a_text_data[3:]))
        log.runtime_logger.debug(
            f"Raw return: {a_text} . barcode: {barcode} scanned_date: {scanned_date} Parsed row: {available_row}")
        out_data.append({'Barcode': barcode, 'Scanned Date': scanned_date, 'gb_data': available_row})

    return out_data


def request_conversion(volumes: [str]):
    """
    Requests the GRINserver to process a list of volumes
    """
    if not volumes:
        return

    gb = GRINProcessRequest()

    request_start: datetime = datetime.now()

    # Make the request to process
    processed_volumes: [] = gb.process_volumes(volumes)
    # Drop the first row of output- it's just a banner
    for pv in processed_volumes[2:]:
        work_name = pv[0].split('-')[0]
        log.runtime_logger.info(f"Process  {activity} for {pv[0]}:{work_name}")
        # log.activity_logger.info(f"success:{activity}:{image_group}:{dest_token}")
        # work_rid: str, image_group_label: str, activity: str,
        #                              start_time: datetime, Dupload_rc: int) -> int
        log.activity_db_logger.add_content_activity(work_rid=work_name, image_group_label=pv[0], activity=activity,
                                                    start_time=request_start, activity_rc=0)


def available_conversions_service():
    """
    main loop for conversion request monitoring and processing. Run this on a timer, once or twice per day
    Expected format from books.google.com/libraries/UOM/_available
    'Barcode' 'Scanned Date'	'Processed Date'	'Analyzed Date'	'OCR Date'	'Google Books'
    :return:
    """
    global log
    cfg: GRINConfig = GRINConfig('')
    log = AORunActivityLog(prefix=activity, log_descriptor="content", home=cfg.cfg_log_dir,
                           level=logging.INFO)
    log.runtime_logger.info("Getting available")
    available_to_convert: [str] = GRINGet().get("_available")

    tracking_data: [{}] = parse_available_return(available_to_convert)
    log.runtime_logger.info(f"Got {len(tracking_data)} objects")
    import json

    # TODO: Logging fails here because only record W:W here.
    for td in tracking_data:
        obs_date: datetime = datetime.strptime(td['Scanned Date'], "%Y/%m/%d %H:%M")
        log.activity_db_logger.add_content_state(td['Barcode'].split('-')[0], td['Barcode'], obs_date, '_available',
                                                 json.dumps(td['gb_data']),
                                                 )
        # ? Unconditional, or test for something?

    to_process = [td['Barcode'] for td in tracking_data]
    request_conversion(to_process)


def request_conversion_main():
    """
    Standalone command line utility to request a conversion for a designated image group
    :return:
    """
    global log

    ap = lib.GbParserBase(
        description="Requests conversion of an uploaded content image group")
    ap.add_argument("image_group", help="workRid-ImageGroupRid - no file suffixes", nargs='?',
                    default=lib.GbParserBase.NO_ARG_GIVEN)

    parsed_args: argparse.Namespace = ap.init()

    global log
    cfg: GRINConfig = GRINConfig('')
    log = AORunActivityLog(prefix=activity, log_descriptor="content", home=cfg.cfg_log_dir,
                           level=logging.INFO)
    log.runtime_logger.debug(f"args: {lib.print_args(parsed_args)}")

    if parsed_args.input_file:
        for f in fileinput.input(files=parsed_args.input_file):
            request_one(f.strip(), parsed_args)
        return

    request_one(parsed_args.image_group, parsed_args)


if __name__ == "__main__":
    # request_conversion_main()
    available_conversions_service()
