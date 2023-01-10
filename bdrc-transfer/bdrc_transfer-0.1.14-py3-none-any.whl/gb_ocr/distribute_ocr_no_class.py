#!/usr/bin/env python3
"""
Sends uploaded material to OCR
"""
import argparse
import fileinput
import logging
import queue
import threading

from datetime import datetime, timedelta
from pathlib import Path

import util_lib.GetFromBUDA
from archive_ops.Resolvers import Resolvers
from archive_ops.shell_ws import get_mappings

from gb_lib import GbLib as lib

# Required globals
activity: str = "to_s3"
run_log: logging
activity_log: logging
dest_token: str = "content"

# This will cover all the works in the initial cycle.
batch_id: str = "batch_2022"
#
# For this module only
S3_OCR_BUCKET_KEY: str = "s3_ocr_bucket"
S3_OCR_HOME_KEY: str = "s3_ocr_home"
output_source = "google_books"

s3_ocr_bucket: str
s3_ocr_home: str

fail_flag_lock: threading.Lock = threading.Lock()
had_fail: bool = False

s3_ocr_queue = queue.Queue()


def set_error(error_state: bool):
    """
    Sync lock the error flag
    :param error_state: state to set
    :return:
    """
    global had_fail, fail_flag_lock

    if fail_flag_lock.acquire():
        had_fail = error_state
    fail_flag_lock.release()

def get_if_any_error():
    """
    Sync lock the error flag
    :param error_state: state to set
    :return:
    """
    global had_fail, fail_flag_lock
    rc: bool = False

    if fail_flag_lock.acquire():
        rc = had_fail
    else:
        raise ValueError("Could not acquire fail flag lock")

    fail_flag_lock.release()
    return rc


def distribute_one(image_group_path: str, args: argparse.Namespace):
    """
    Distributes one image group
    :param image_group_path: path to one downloaded image group directory. The last element
    in the path is the work_rid-imagegroup_disk_rid pair
    :return:
    """
    global run_log
    import os

    # Per https://github.com/buda-base/archive-ops/issues/693, the proposed spec is
    #     # s3://ocr.bdrc.io/Works/{xx}/{work}/google_books/batch-id/{work-ig}/{work-ig}nnnn.suffix

    # {work-ig}
    ig_dir_name: str = Path(image_group_path).name

    # {work}
    work_name: str
    work_sep: str = '-'
    work_ig_rids: [] = ig_dir_name.split(work_sep)

    # Could be the initial uploads need to be redone, because their MARC records sent up Wxxxx-Innnn
    #  in the metadata, but We sent up Wxxxx-nnnn in the files, and their names, or perhaps just their names.
    # But it's OK, we roll up the disk image group names
    # If we're not dealing with a split, just pass it on through
    if len(work_ig_rids) > 1:
          work_ig_rids[1] = util_lib.GetFromBUDA.old_hack_get_ig_disk(work_ig_rids[1])

          #  Rebuild the corrected image group name
          ig_dir_name = work_sep.join(work_ig_rids)
    work_name = work_ig_rids[0]


    #
    # Get components (note - we're preparing for a boto s3 transfer, which takes the bucket
    # as an argument, so we don't need s3://bucketname. Just the path to the object.
    # Works/{xx}/Work
    work_dest_ig_path: str = get_mappings(s3_ocr_home, work_name, Resolvers.S3_BUCKET)

    global batch_id

    trans_message: str = f"{image_group_path}->s3://{s3_ocr_bucket}/{work_dest_ig_path}/{output_source}/{batch_id}/{ig_dir_name}"

    if args.log_after_fact:
        run_log.info(f"Simulating {activity} for {trans_message} :{dest_token}")
        activity_log.info(f"success:{activity}:{trans_message}:{dest_token}")
        return

    import boto3
    from botocore.exceptions import ClientError
    import os
    s3_client = boto3.client('s3')

    for (root, dirs, files) in os.walk(image_group_path):

        for f in files:
            object_src_path: str = str(Path(root, f))

            # Don't do this unless I need to. f.replace("0000", ig_name)
            object_dest_path=f"{work_dest_ig_path}/{output_source}/{batch_id}/{ig_dir_name}/{f}"

            # Cute. Unneeded.
            # list(map(lambda f: print(f"fp {str(Path(root, d, f))}"), files))

            try:
                s3_client.upload_file(object_src_path, s3_ocr_bucket, object_dest_path)
                run_log.debug(f"uploaded {object_src_path} to s3://{s3_ocr_bucket}/{object_dest_path}")
            except ClientError as e:
                run_log.error()
                set_error(True)

    if get_if_any_error():
        activity_log.error(f"{activity}:error:{trans_message}:{dest_token}")
    else:
        activity_log.info(f"{activity}:success:{trans_message}:{dest_token}")


def worker(doing_queue: queue.Queue, args: argparse.Namespace):
    """
    Thread worker to do one transfer
    :param doing_queue:
    :param args: options, from command line
    :return:
    """

    while True:
        try:
            item = doing_queue.get()
            t0: datetime = datetime.now()
            logging.info(f"distributing {item}")
            distribute_one(item, args)
            dt: timedelta = datetime.now() - t0
            et: datetime = datetime.utcfromtimestamp(dt.seconds)
            logging.info(f"      Finished {item} - e.t. {et.strftime('%T')}")
        finally:
            doing_queue.task_done()



def distribute_main():
    """
    :return:
    """

    ap = lib.GbParserBase(
        description="sends an OCR image group")
    ap.add_argument("image_group", help="path to image group directory", nargs='?',
                    default=lib.GbParserBase.NO_ARG_GIVEN)

    parsed_args: argparse.Namespace = ap.init()
    _app_logger = lib.AORunActivityLog(prefix=activity, home=parsed_args.log_home, level=parsed_args.log_level)

    global run_log, activity_log
    run_log = _app_logger.runtime_logger
    activity_log = _app_logger.activity_logger

    global s3_ocr_bucket, s3_ocr_home

    from gb_ocr.GRINConfig import GRINConfig
    config: GRINConfig().gb_sftp_config
    s3_ocr_bucket = config.get_value(S3_OCR_BUCKET_KEY)
    s3_ocr_home = config.get_value(S3_OCR_HOME_KEY)

    for quiet_logger in ['boto', 'botocore', 'boto3', 'requests', 'urllib3', 'request','s3transfer']:
        ql = logging.getLogger(quiet_logger)
        ql.setLevel(logging.CRITICAL)
        ql.propagate = True

    run_log.debug(f"args: {lib.print_args(parsed_args)}")

    # Turn-on the worker threads
    for i in range(5):
        threading.Thread(target=worker, daemon=True, args=(s3_ocr_queue, parsed_args,)).start()


    try:
        if parsed_args.input_file:
            for f in fileinput.input(files=parsed_args.input_file):
                s3_ocr_queue.put(f.strip())
        else:
            s3_ocr_queue.put(parsed_args.image_group)
        s3_ocr_queue.join()
    finally:
        s3_ocr_queue.join()



if __name__ == '__main__':
    distribute_main()
    print("Should get here")
