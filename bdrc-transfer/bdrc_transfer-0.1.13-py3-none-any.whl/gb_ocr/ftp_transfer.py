#!/usr/bin/env python3

"""
SFTP upload specific to Google Books
"""
import argparse
import os
import pathlib
from pathlib import Path
import logging
from gb_lib import GbLib as lib
from log_ocr.AORunLog import AORunActivityLog

run_logger_name = 'upload_logger'

# Globals

dest_token: str
run_log: logging
activity_log: logging
_app_logger: AORunActivityLog
dry_run: bool
transfer_setup_args: {} = {}
sftp_conn: lib.GbSftp


def set_globals(app_logger: AORunActivityLog, op_type: str, dry_run_p: bool = False):
    """
    Sets globals for operations
    :param app_logger: loggers
    :param op_type: content or metadata
    :param dry_run_p: simulate by logging
    :return:
    """
    global dest_token, run_log, activity_log, dry_run, transfer_setup_args, sftp_conn
    dest_token = op_type
    run_log = app_logger.runtime_logger
    activity_log = app_logger.activity_logger
    if not run_log.isEnabledFor(logging.DEBUG):
        logging.getLogger('paramiko').setLevel(logging.ERROR)

    dry_run = dry_run_p

    transfer_setup_args = {
        'content_type': dest_token,
        'dry_run': dry_run
    }
    sftp_conn = lib.GbSftp(**transfer_setup_args)


def put_metadata(src: Path, logger: AORunActivityLog, dest: str = None, dry_run_p: bool = False) -> bool:
    """
    Puts an object of metadata. Meant for use by clients
    :param src:
    :param logger:
    :param dest: optional target on remote site, if none, copy filename of src_path
    to login folder of dest
    :param dry_run_p: True if simulating
    :return: success state of operation
    """
    set_globals(logger, "metadata", dry_run_p)
    return put(src_path=src, dest_path=dest)


def put_content(src: Path, logger: AORunActivityLog, dest: str = None, dry_run_p: bool = False) -> bool:
    """
    Puts an object of content. Meant for use by clients
    :param src:
    :param logger:
    :param dest: optional target on remote site, if none, copy filename of src_path
    to login folder of dest
    :param dry_run_p: True if simulating
    :return: success state of operation
    """
    set_globals(logger, "content", dry_run_p)
    return put(src_path=src, dest_path=dest)


def get(src: str, dest_str: str = None) -> bool:
    """
    Gets one file
    :param src: Remote file
    :param dest_str: optional location to store file (./src file name)
    :return:
    """
    # TODO:implement, when needed
    global run_log, activity_log
    dest_dir = os.path.dirname(dest_str) if dest_str else '.'
    if not os.access(dest_dir, os.W_OK):
        raise PermissionError(f"{dest_dir} not found or not writable")
    return False


def put(src_path: Path, dest_path: str = None) -> bool:
    """
    Puts one file
    :param src_path: source to put
    :param dest_path: Optional full path to output
    :return: success status of underlying sftp call
    """

    global dest_token
    if not pathlib.Path.exists(src_path):
        run_log.error(f"put:Errno 2: source {src_path} not found or not readable")
        activity_log.error("error:put:source %s not found or readable:%s", src_path, dest_token)
        raise FileNotFoundError(str(src_path))
    # Put to same name (or directory) on dest, if nothing given
    dest: str = Path(src_path).name if dest_path is None else dest_path

    return sftp_conn.put(str(src_path), dest)


def ftp_transfer_main():
    ap = lib.GbParserBase(
        description="Uploads a file to a specific partner server, defined by a section in the config file")
    destinations = ap.add_mutually_exclusive_group()
    destinations.add_argument("-m", "--metadata", help="Act on metadata target", action="store_true")
    destinations.add_argument("-c", "--content", help="Act on the content target", action="store_true")
    ap.add_argument_group(destinations)

    directions = ap.add_mutually_exclusive_group()
    directions.add_argument("-p", "--put", help="send to", action="store_true")
    directions.add_argument("-g", "--get", help="get from (NOT IMPLEMENTED)", action="store_true")
    ap.add_argument_group(directions)

    ap.add_argument("src", help="source file for transfer")
    ap.add_argument("dest", help='[Optional] destination file - defaults to basename of source', nargs='?')

    parsed_args: argparse.Namespace = ap.init()

    set_globals(
        app_logger=AORunActivityLog(prefix="transfer",
                                    home=parsed_args.log_home, level=parsed_args.log_level),
        op_type="metadata" if parsed_args.metadata else "content",
        dry_run_p=parsed_args.dry_run)

    run_log.debug(f"args: {lib.print_args(parsed_args)}")

    op: str = lib.GbFtpOps.PUT_OP if parsed_args.put else lib.GbFtpOps.GET_OP

    if parsed_args.log_after_fact:
        activity_log.info(f"{op}:success:%s:%s", parsed_args.src, dest_token)
        return

    if parsed_args.put:
        allOk = put(Path(parsed_args.src), parsed_args.dest)
    else:
        allOk = get(parsed_args.src, parsed_args.dest)

    if allOk:
        run_log.info(f"{op} success %s:%s", parsed_args.src, dest_token)
        if not parsed_args.dry_run:
            activity_log.info(f"{op}:success:%s:%s", parsed_args.src, dest_token)
    else:
        run_log.error(f"{op} failed %s:%s", parsed_args.src, dest_token)
        if not parsed_args.dry_run:
            activity_log.error(f"{op}:error:%s:%s:", parsed_args.src, dest_token)


if __name__ == "__main__":
    ftp_transfer_main()
