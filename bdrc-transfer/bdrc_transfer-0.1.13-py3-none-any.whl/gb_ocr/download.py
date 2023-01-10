#!/usr/bin/env python3
"""
Requests download of an OCR'd image group
"""
import argparse
import fileinput
import logging
import os
import sys
from pathlib import Path

from gb_lib.GbLib import VolumeToWork, no_suffix
from gb_ocr.grin_lib.GRINOps import GRINGet
from log_ocr.AORunLog import AORunActivityLog
from datetime import datetime

from gb_lib import GbLib as lib
from log_ocr.GbOcrTrack import GbOcrContext

activity: str = "download"
dest_token: str = "content"
STANDARD_SUFFIX: str = ".tar.gz.gpg"

log: AORunActivityLog

# This set of headers is deduced from observation of the web page
# Don't include 'FileName'
books_available_to_download_extra_headers = ['Scanned Date', 'Converted Date', 'Downloaded Date',
                                             'Google Books']


def parse_converted_return(grin_text_return: [str], header_list: [str]) -> [{}]:
    """
    Parse GRIN return from available
    :param grin_text_return:
    :param header_list:  List of expected headers - these are mostly passed into the gb_data dictionary
    Choice of scanned date is arbitrary - to provide a unique index based on volume id and time
    :return: [ { 'Filename' : Work-ImageGroup.tar.gz.pgp ,  gb_data: { 	'Processed Date': ... ,
    'Analyzed Date':...,	'OCR Date':...,	'Google Books':...} } ]
    """
    out_data: [{}] = []
    for a_text in grin_text_return:
        a_text_data = a_text.split('\t')
        filename: str = a_text_data[0]
        available_row = dict(zip(header_list, a_text_data[2:]))
        log.runtime_logger.debug(
            f"Raw return: {a_text} . filename: {filename}  Parsed row: {available_row}")

        out_data.append({'Filename': filename, 'gb_data': available_row})

    return out_data


# noinspection PyBroadException
def request_download(to_download: [str], download_to: str, mark_only: bool):
    """
    Requests the GRINserver to download a list of books
    :param to_download: list of volume (image group) labels
    :param download_to: destination
    :param mark_only: log post activity
    """

    global log
    ok_down: bool = False
    for vp in to_download:
        request_start: datetime = datetime.now()
        # Remove the file suffixes, and create a work+volume structure
        v_w = VolumeToWork(no_suffix(vp))
        download_source: str = vp
        dest_path: Path = Path(download_to, download_source)

        try:
            ok_down = False
            if not mark_only:
                os.makedirs(download_to, exist_ok=True)
                gb = GRINGet()
                gb.get_download(download_source, dest_path)
            ok_down = True
        except:
            si = sys.exc_info()
            log.runtime_logger.error(f"Could not download {download_source}. error {si[1]} ")
        finally:
            db_log_rc = 0 if ok_down else 1
            if ok_down:
                log.runtime_logger.info(
                    f"Process  {activity} for {v_w.volume_label} {'success' if ok_down else 'fail'}")

            log_data: {} = {'payload': str(dest_path)}
            log.activity_db_logger.add_content_activity(work_rid=v_w.work_name, image_group_label=v_w.volume_label,
                                                        activity=activity, start_time=request_start,
                                                        activity_rc=db_log_rc, log_data=str(log_data))
            with GbOcrContext() as ctx:
                from log_ocr.models.drs import Volumes, GbDownload, GbReadyTrack
                vol: Volumes = ctx.get_or_create_volume(v_w.work_name, v_w.volume_label)
                from log_ocr.models.drs import GbDownload
                down_record = GbDownload(
                    volume=vol,
                    download_time=datetime.now(),
                    download_path=str(dest_path),
                    download_object_name=v_w.volume_label)
                ctx.session.add(down_record)
                ctx.session.flush()
                ctx.session.add(GbReadyTrack(target_id=down_record.id, activity=activity))
                ctx.session.commit()


def flush_download_backlog():
    """
    Transfer records of all downloads into GbReadyTrack
    """
    from log_ocr.models.drs import GbReadyTrack
    with GbOcrContext() as ctx:
        downloads = ctx.get_downloads()
        for dl in downloads:
            ctx.session.add(GbReadyTrack(target_id=dl.GbDownload.id, activity='download'))
        ctx.session.commit()


def available_downloads_service():
    """
    main loop for available download monitoring and processing. Run this on a timer, once or twice per day
    Expected format from books.google.com/libraries/UOM/_
    'Filename' 'Scanned Date'	'Converted Date'	'Downloaded Date' 'Google Books'
    :return:
    """

    from gb_ocr.GRINConfig import GRINConfig

    global log
    config: GRINConfig = GRINConfig()
    log = AORunActivityLog(prefix=activity, log_descriptor="content",
                           level=logging.INFO, home=config.cfg_log_dir)
    log.runtime_logger.info("Getting available")

    available_to_download: [str] = GRINGet().get("_converted")
    tracking_data: [{}] = parse_converted_return(available_to_download, books_available_to_download_extra_headers)
    log.runtime_logger.info(f"Got {len(tracking_data)} objects")

    register_content_state(tracking_data)

    # Get the actual payload: the names of the files to download
    to_process = [td['Filename'] for td in tracking_data]
    #
    # For limited testing
    request_download(to_process, config.cfg_download_dir, False)
    # request_download(to_process, config.cfg_download_dir,False)


def register_content_state(tracking_data):
    import json
    with GbOcrContext() as gbt:
        obs_date: datetime = datetime.now()
        for td in tracking_data:
            # Strip all the file extensions (expecting Wxxxxx-Iggggg.tar.gz.gpg')
            v_w: VolumeToWork = VolumeToWork(td['Filename'].split('.')[0])
            gbt.add_content_state(v_w.work_name, v_w.volume_label, obs_date, '_converted',
                                  json.dumps(td['gb_data']),
                                  )


def download_main():
    from gb_ocr.GRINConfig import GRINConfig
    _to: Path = GRINConfig().cfg_download_dir
    ap = lib.GbParserBase(
        description="Downloads an OCR'd content image group")
    ap.add_argument("image_group", help="workRid-ImageGroupRid - no file suffixes", nargs='?',
                    default=lib.GbParserBase.NO_ARG_GIVEN)
    ap.add_argument("download_to", help="overrides config path", nargs='?',
                    default=_to)

    parsed_args: argparse.Namespace = ap.init()

    global log
    log = AORunActivityLog(prefix=activity, home=parsed_args.log_home, level=parsed_args.log_level,
                           log_descriptor='content')

    log.runtime_logger.debug(f"args: {lib.print_args(parsed_args)}")

    req_args: [] = []
    if parsed_args.input_file:
        for f in fileinput.input(files=parsed_args.input_file):
            req_args.append(f)
    else:
        req_args.append(parsed_args.image_group)

    request_download(req_args, parsed_args.download_to, parsed_args.log_after_fact)


if __name__ == "__main__":
    # download_main()
    flush_download_backlog()
    # available_downloads_service()
