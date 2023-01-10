#!/usr/bin/env python3
"""
Archive a work and send it to GB
"""

import argparse
import fileinput
import logging
import os
import queue
import sys
import tempfile
import threading
from zipfile import ZipFile
from datetime import datetime, timedelta
from pathlib import Path
import imghdr

from gb_lib import GbLib as lib
from gb_ocr.ftp_transfer import put_content
from log_ocr.AORunLog import AORunActivityLog


class GBAuditToolFailedError(Exception):
    pass



# Required globals

# For logging and recording. What is this operation's name?
activity: str = "content_upload"

# Loggers for runtime and activity
app_logger: AORunActivityLog

# For logging - what kind of material are we working on
dest_token: str = "content"
parsed_args: argparse.Namespace

# work queue
zip_queue: queue.Queue


def archive_upload_one(image_group_name: str, image_group_path: str) -> bool:
    """
    Archive an image group, filtering out unwanted files. Then upload it to the sftp site
    :param image_group_name:  identifier
    :param image_group_path: Path to one image group
    :return:
    """
    global app_logger

    log = app_logger.runtime_logger
    zip_home = tempfile.gettempdir()

    zip_path: Path = Path(zip_home, image_group_name + '.zip')
    log.debug(f"writing {image_group_name} to {zip_path}")
    image_file_count: int = 0
    non_image_file_count: int = 0
    ok: bool = False
    try:
        with ZipFile(zip_path, 'w', compresslevel=9) as outf:
            for each_thing in os.scandir(image_group_path):
                if each_thing.is_file():
                    if imghdr.what(each_thing.path):
                        image_file_count = image_file_count + 1
                        outf.write(each_thing.path, each_thing.name)
                    else:
                        non_image_file_count = non_image_file_count + 1
        log.info(f"zipped {str(zip_path)}")
        log.debug(
            f"{activity}:{image_group_name} Wrote image_file_count: {image_file_count} , non_image_file_count {non_image_file_count} to zip")

        return put_content(src=zip_path, logger=app_logger, dest=None, dry_run_p=parsed_args.dry_run)
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)


def dispatch(doing_queue: queue.Queue):
    """
      Thread worker to do one transfer
      Input: A queue of tuples, of (work_rid, image group name, image_group path)
      :param doing_queue:
      :return: None
      """

    up_rc: int = 1  # Preload error in case of exception
    image_group_path: str = "UNKNOWN_PATH"
    image_group_name: str = "UNKNOWN_IG"
    work_rid: str = "UNKNOWN_WORK"
    while True:
        try:

            # TODO: Handle case of some igs fail, some succeed.
            # Also handle case of audit tool failing
            item = doing_queue.get()
            work_rid = item[0]
            image_group_name = item[1]
            image_group_path = item[2]
            t0: datetime = datetime.now()
            app_logger.runtime_logger.info(f"uploading {item}")
            up_rc = 0 if archive_upload_one(image_group_name, image_group_path) else 1
            dt: timedelta = datetime.now() - t0
            et: datetime = datetime.utcfromtimestamp(dt.seconds)
            app_logger.runtime_logger.info(f"      Finished {item} - e.t. {et.strftime('%T')}")
            app_logger.activity_logger.info(f"{activity}:success:{item}")
        except:
            up_rc = -1
            ee = sys.exc_info()
            app_logger.runtime_logger.error(f"Failed {image_group_path} - {ee[0]}: {ee[1]}")

        try:
            app_logger.activity_db_logger.add_content_activity(work_rid, image_group_name, "upload",
                                                               datetime.now(),
                                                               up_rc)
        except:
            ee = sys.exc_info()
            app_logger.runtime_logger.error(f"Failed {image_group_path} - {ee[0]}: {ee[1]}: {ee[2]}")
        finally:
            doing_queue.task_done()


def work_image_group_paths(work_path: str) -> []:
    """
    Calculates paths to image groups of a work
    :param work_path: path to work.
    """
    igs: [] = []
    for a_dir in os.scandir(Path(work_path, 'images')):
        if a_dir.is_dir():
            igs.append(a_dir.path)
    return igs


def upload_archive_main():
    """
    Shell for uploading
    """

    global app_logger, parsed_args, zip_queue

    ap = lib.GbParserBase(
        description="uploads the images in a work to GB. Can upload all or some image groups (see --image_group option)")
    ap.add_argument("-g","--image_group", action='store_true' , help='True if paths are to image group')
    ap.add_argument("work_path", help="Path to work. Last node is work RID, or Image group, if -- is set", nargs='?',
                    default=lib.GbParserBase.NO_ARG_GIVEN)

    parsed_args = ap.init()

    app_logger = AORunActivityLog(prefix=activity, home=parsed_args.log_home, level=parsed_args.log_level)

    for quiet_logger in ['requests', 'urllib3', 'request', 'paramiko']:
        ql = logging.getLogger(quiet_logger)
        ql.setLevel(logging.CRITICAL)
        ql.propagate = True

    app_logger.runtime_logger.debug(f"args: {lib.print_args(parsed_args)}")

    # Turn on the worker threads - we only want 4 concurrent zips
    zip_queue = queue.Queue()
    for i in range(4):
        threading.Thread(target=dispatch, daemon=True, args=(zip_queue,)).start()

    try:
        if parsed_args.input_file:
            for work_path in fileinput.input(files=parsed_args.input_file):
                process_work(work_path.strip(), zip_queue, parsed_args.image_group)
        else:
            process_work(parsed_args.work_path, zip_queue, parsed_args.image_group)
    finally:
        zip_queue.join()


def audit_work(work_p):
    """Runs a special configuration of audit tool"""
    cmd: [] = ['audit-gb', work_p, app_logger.home]
    # TODO: capture SMS messaging of subshell here
    import subprocess
    at_out: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True)

    console_output: str = f"\n>>>stdout:\n{at_out.stdout.decode()}\n>>>stderr:\n{at_out.stderr.decode()}\nrc={at_out.returncode}"

    app_logger.runtime_logger.debug(f"upload content console: {console_output}")
    if at_out.returncode != 0:
        raise GBAuditToolFailedError(f"GB audit fail{console_output}")


def process_work(work_p: str, work_queue: queue.Queue, is_ig: bool  ):
    """
    Adds image groups in a work to the processing queue,
    IF they pass audit tool
    :param work_p:work path
    :param work_queue: handler
    :param is_ig: True if work_p points to imagr group
    :return:
    """

    if not is_ig:
        try:
            audit_work(work_p)
        except GBAuditToolFailedError as at_failed:
            app_logger.runtime_logger.error(f"{activity}:{at_failed}")
            app_logger.activity_logger.error(f"{activity}:error:GB Audit fail")
            return


    # was os.path.basename, which mishandles /blarg/slarti/bartfarst/
    if not is_ig:
        work_rid: str = Path(work_p).name
        for w_ig_path in work_image_group_paths(work_p):
            work_queue.put((work_rid, Path(w_ig_path).name, w_ig_path,))
    else:
        work_rid = Path(work_p).parent.parent.name
        work_queue.put((work_rid, Path(work_p).name, work_p,))


if __name__ == '__main__':
    upload_archive_main()
