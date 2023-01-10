#!/usr/bin/env python3
"""
Create metadata
"""

import argparse
import fileinput
import logging
import os.path

import requests
import urllib3.poolmanager
import tempfile
from pathlib import Path

import gb_ocr.ftp_transfer
from gb_lib import GbLib as lib

# xmldocURL: str = "https://legacy.tbrc.org/xmldoc?rid="
marc_url: str = "https://purl.bdrc.io/resource/"
gb_param: str = "style=google_books"

# Required globals
activity: str = "buildMetadata"
app_logger: lib.AORunActivityLog
dest_token: str = "metadata"
parsed_args: argparse.Namespace


def create_one(work_rid: str, dry_run_p: bool = False):
    """
    Create and send one metadata
    :param work_rid: work id
    :param args: controls
    :return:
    """

    global app_logger
    #   curl -s -o $marcXMLdest "${marc_url}${w}.mrcx?${gbparam}"

    metadata_blob: Path = Path(tempfile.gettempdir(), f"marc-{work_rid}.xml")
    payload: str = os.path.basename(metadata_blob)

    get_marc_request_url = f'{marc_url}{work_rid}.mrcx?{gb_param}'
    resp = requests.get(get_marc_request_url)
    with open(metadata_blob, 'wb') as outf:
        # shutil.copyfileobj(resp.data, outf)
        outf.write(resp.data)
    try:
        app_logger.runtime_logger.info(f"created metadata {payload}from remote")
        ok = gb_ocr.ftp_transfer.put_metadata(metadata_blob, app_logger, None, dry_run_p)
    finally:
        os.remove(metadata_blob)

    if ok:
        app_logger.runtime_logger.info(f"sent {payload}")
        app_logger.activity_logger.info(f"{activity}:success:{payload}:metadata")
    else:
        app_logger.runtime_logger.error(f"failed to send {payload}")
        app_logger.activity_logger.error(f"{activity}:error:{payload}:metadata")


def create_main():
    """
    Create and send metadata
    :return:
    """
    global app_logger, parsed_args

    ap = lib.GbParserBase(
        description="Creates and sends metadata to gb")
    ap.add_argument("work_rid", help="Work ID", nargs='?')

    parsed_args = ap.init()

    app_logger = lib.AORunActivityLog(prefix=activity, home=parsed_args.log_home, level=parsed_args.log_level)

    for quiet_logger in ['requests', 'urllib3', 'request']:
        ql = logging.getLogger(quiet_logger)
        ql.setLevel(logging.CRITICAL)
        ql.propagate = True

    app_logger.runtime_logger.debug(f"args: {lib.print_args(parsed_args)}")
    if parsed_args.input_file:
        for work in fileinput.input(files=parsed_args.input_file):
            create_one(work, parsed_args.dry_run)
        return
    create_one(parsed_args.work_rid, parsed_args.dry_run)


if __name__ == '__main__':
    create_main()
