#!/usr/bin/env python3
"""
Marshals arguments for shelling out to GPG and, unzipping and unpacking an image group
"""
import argparse
import fileinput
import os
import shutil
import subprocess
import sys
from pathlib import Path
import logging
from datetime import datetime
from gb_lib import GbLib as lib
from gb_ocr.GRINConfig import GRINConfig
from log_ocr.AORunLog import AORunActivityLog

run_log: logging
activity_log: logging

activity: str = "unpack"
dest_token: str = "content"

# Used in relocating
STD_SUFFIX: str = ".tar.gz.gpg"
STD_PREFIX: str = "TBRC_"


class GPGFailedError(Exception):
    pass


class GunzipFailedError(Exception):
    pass


class TarFailedError(Exception):
    pass


# endregion
# region Non-class
def parse_args() -> argparse.Namespace:
    ap = lib.GbParserBase(
        description="Unpacks an artifact")
    ap.add_argument("src", help="xxx.tar.gz.gpg file to unpack", nargs='?',
                    default=lib.GbParserBase.NO_ARG_GIVEN)
    return ap.init()


def do_gpg(_config, src: str, log_level: int) -> str:
    """
    Decrypts a gpg file
    :param _config:controls from config file
    :param src: controls from arguments
    :param log_level:
    :return: the pathname of the decrypted file
    """
    gpg_exec = find_bin("gpg")
    if not os.path.exists(gpg_exec):
        raise ValueError(f"gpg binary not present on system")
    # make the output file
    output_file: str = os.path.splitext(src)[0]
    gpg_command: [] = [
        gpg_exec,
        '--batch',
        '--passphrase',
        f"{_config.gpg_passphrase}",
        '-o',
        output_file,
        '--decrypt',
        src
    ]
    if log_level == logging.DEBUG:
        gpg_command.insert(2, '-v')
    gpg_out: subprocess.CompletedProcess = subprocess.run(gpg_command, capture_output=True)

    run_log.debug(
        f"unpack console: stdout{gpg_out.stdout.decode()}\n stderr{gpg_out.stderr.decode()} rc={gpg_out.returncode}")

    if gpg_out.returncode != 0:
        raise GPGFailedError(f"decrypt failure {src} {gpg_out.stdout.decode()}\n{gpg_out.stderr.decode()}")
    return output_file


def do_tar(src: str, log_level: int) -> str:
    """
    Extracts the uncompressed tar file
    :param src: source file. The file name (before the suffix) becomes the output directory
    :param log_level: log level
    :return: the full path of the output directory
    """
    tar_bin = find_bin("tar")
    if not os.path.exists(tar_bin):
        raise ValueError(f"tar binary not present on system")
    # make the output directory
    output_dir: str = os.path.splitext(src)[0]
    bk_part = "-backup-"

    # Relocate existing
    limit: int = 5
    if os.path.exists(output_dir):
        pass1: int = 1

        # Find an available slot
        while os.path.exists(output_dir + f"{bk_part}{pass1}") and pass1 < limit:
            run_log.debug(f"{'tar':>8}:output exists: {output_dir}{bk_part}{pass1}")
            pass1 = pass1 + 1

        # none? Make some room. pass1 is the next available slot
        if pass1 == limit:
            run_log.debug(f"{'tar':>8}:Max backups reached. Removing oldest..")
            # Remove the first one
            shutil.rmtree(output_dir + f"{bk_part}{limit - 1}")

            # Rename the rest
            for pass2 in range(limit - 1, 1, -1):
                run_log.debug(f"{'tar':>8}:pushing up {output_dir}{bk_part}{pass2 - 1} to {pass2} ")
                os.rename(output_dir + f"{bk_part}{pass2 - 1}", output_dir + f"{bk_part}{pass2}")
            pass1 = 1
        run_log.debug(f"{'tar':>8}:pushing {output_dir} to {bk_part}{pass1}")
        os.rename(output_dir, f"{output_dir}{bk_part}{pass1}")

    run_log.debug(f"{'tar':>8}:creating {output_dir}")
    os.mkdir(output_dir)

    # if not os.path.exists(output_dir):
    #     os.mkdir(output_dir)

    tar_command: [] = [
        tar_bin,
        '--extract',
        f"--file={src}",
        f"--directory={output_dir}"
    ]

    if log_level == logging.DEBUG:
        tar_command.insert(1, '-v')

    tar_out: subprocess.CompletedProcess = subprocess.run(tar_command, capture_output=True)

    run_log.debug(
        f"unpack console: stdout{tar_out.stdout.decode()}\n stderr{tar_out.stderr.decode()} rc={tar_out.returncode}")

    if tar_out.returncode != 0:
        raise TarFailedError(
            f"extraction failure {src} {tar_out.stdout.decode()}\n{tar_out.stderr.decode()}")
    return output_dir


def do_gunz(src: Path, log_level: int) -> str:
    """
    GUnzip the source
    :param src: path to file to unzip
    :param log_level:
    :return:
    """
    gunzip_bin = find_bin("gunzip")
    if not os.path.exists(gunzip_bin):
        raise ValueError(f"gunzip binary not present on system")
    # make the output file
    output_file: str = os.path.splitext(src)[0]
    gunzip_command: [] = [
        gunzip_bin,
        src
    ]
    if log_level == logging.DEBUG:
        gunzip_command.insert(1, '-v')
    run_log.debug(f"{gunzip_command}")

    gunz_out: subprocess.CompletedProcess = subprocess.run(gunzip_command, capture_output=True)

    run_log.debug(
        f"unpack console: stdout{gunz_out.stdout.decode()}\n stderr{gunz_out.stderr.decode()} rc={gunz_out.returncode}")

    if gunz_out.returncode != 0:
        raise GunzipFailedError(
            f"decompress failure {src} {gunz_out.stdout.decode()}\n{gunz_out.stderr.decode()}")
    return output_file


def unpack_main():
    """
    Unpacks a gpg file. We do this in the shell, because we want the result to be a file, not a stream
    :return:
    """

    uper = Unpacker(Path(os.path.expanduser('~/dev/tmp/Projects/google-books/TBRC_W12827-2072.tar.gz.gpg')),
                    VolumeToWork('W12827-2072'))
    uper.do_unpack()
    return

    global run_log, activity_log
    unpack_main_args: argparse.Namespace = parse_args()
    unpack_main_app_logger = AORunActivityLog(prefix=activity, home=unpack_main_args.log_home,
                                              level=unpack_main_args.log_level)
    run_log = unpack_main_app_logger.runtime_logger
    activity_log = unpack_main_app_logger.activity_logger

    run_log.debug(f"args: {lib.print_args(unpack_main_args)}")

    _config = GRINConfig().gb_sftp_config

    # MyOut = subprocess.Popen(['ls', '-l', '.'],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.STDOUT)
    # stdout, stderr = MyOut.communicate()
    #

    try:

        if unpack_main_args.input_file:
            for f in fileinput.input(files=unpack_main_args.input_file):
                unpack_one(_config, f.strip(), unpack_main_args)
            return
        unpack_one(_config, unpack_main_args.src, unpack_main_args)

    except (GPGFailedError, GunzipFailedError, TarFailedError):
        label = "unknown"
        ei = sys.exc_info()
        if ei[0] is GPGFailedError:
            label = "gpg"
        if ei[0] is GunzipFailedError:
            label = "gunzip"
        if ei[0] is TarFailedError:
            label = "tar"
        run_log.error(f"{label} failed, {ei[1]}")
        activity_log.error(f"{label}:error: {ei[1]}")


def do_check(sources_path: str, sum_file_name: str) -> bool:
    """
    Checks md5 sums of each file in the manifest.
    :return: true if all files match their md5 checksum in the sum_file_name
    """
    rc: [] = []
    with open(Path(sources_path, sum_file_name), 'r') as sums:
        for line in sums.readlines():
            d = line.strip().split()

            transmitted_checksum = d[0]
            file_path: Path = Path(sources_path, d[1])
            import hashlib
            # build a list of each file's md5
            received_checksum = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            rc.append(
                {
                    "file": d[1],
                    "match": received_checksum == transmitted_checksum,
                    "transmitted_checksum": transmitted_checksum,
                    "received_checksum": received_checksum
                }
            )

    fails: [] = list(filter(lambda x: not x["match"], rc))

    list(map(lambda x: run_log.error(f"{x}") if not x["match"] else None, fails))
    # If there were no files to read, call it a failure
    # Otherwise return failures (second column in each list)
    return len(fails) == 0 if len(rc) > 0 else False


def do_relocation(source_gpg: str) -> bool:
    """
    Relocates the directory TBRC_WorkRID_IMAGEGROUP to WORKRID/WORKRID-ImageGroup
    uses the chain of unpacking which has:
    TBRC_WORKRID_IMAGEGROUPRID.tar.gz.gpg creating:
    TBRC_WORKRID_IMAGEGROUPRID.tar.gz
    TBRC_WORKRID_IMAGEGROUPRID.tar
    TBRC_WORKRID_IMAGEGROUPRID/ (folder)
    Moves intermediate files into the work's directroy
    :param original source file: TBRC_WorkRID_ImageGroupRID.tar.gz.gpg
    :return:
    """

    orig_path: Path = Path(source_gpg)

    unpacked_folder_name: str = orig_path.name.replace(STD_SUFFIX, '')
    image_group: str = unpacked_folder_name.replace(STD_PREFIX, '')
    work: str = image_group.split('-')[0]

    work_dir: Path = Path(orig_path.parent, work)
    if not os.path.exists(work_dir):
        logging.info(f"Creating {work_dir}")
        os.mkdir(work_dir)
    #
    # build the image group directory name
    target = Path(orig_path.parent, work, image_group)

    # Move the output folder
    unpacked_folder_path: Path = Path(orig_path.parent, unpacked_folder_name)
    logging.info(f"moving {unpacked_folder_path} to {target}")
    os.rename(unpacked_folder_path, target)

    # Move the intermediate files into the work
    logging.debug(f"{os.getcwd()}")
    shutil.move(source_gpg, work_dir)
    # The "gunzip" step removed the ".gz" file
    # Move the tar
    shutil.move(source_gpg.replace(".gz.gpg", ""), work_dir)


def unpack_one(_config, src: str, args: argparse.Namespace):
    """
    Operate on one file
    :param _config: control through environment
    :param src: operand
    :param args: command line controls
    :return:
    """

    if args.log_after_fact:
        run_log.info(f"Simulating {activity} for {src}:{dest_token}")
        activity_log.info(f"success:{activity}:{src}->{src}:{dest_token}")
        return
    if args.dry_run:
        run_log.info(f"(dry_run):success:unpack:{src}:")
        return
    # noinspection PyBroadException
    try:
        gunz: str = do_gpg(_config, src, args.log_level)
        run_log.info(f"decrypted {src} to {gunz}")
        tar: str = do_gunz(gunz, args.log_level)
        run_log.info(f"decompressed {gunz} to {tar}")
        result: str = do_tar(tar, args.log_level)
        run_log.info(f"{result} checksum validation")
        validated: bool = do_check(result, "checksum.md5")
        run_log.info(f"MD5 checksum validates {validated}")
        result_tag: str = "success" if validated else "fail"
        relo_dir = do_relocation(src)

        run_log.info(f"relocated to {relo_dir}")
        activity_log.info(f"unpack:{result_tag}:{src}->{result}:{dest_token}")
    except Exception:
        ei = sys.exc_info()
        run_log.error(f"unpack failed: {ei[1]}")
        activity_log.error("{activity}:error:{ei[1]}")


def find_bin(base_bin: str) -> str:
    """
    Tries to find a binary
    :param base_bin:
    :return:
    """
    bin_path: str = shutil.which(base_bin)
    #
    # gah - stupid hack - doesnt work under pycharm debugger, should work when built
    if bin_path is None:
        bin_path = str(Path("/usr/local/bin", base_bin))
    return bin_path


# endregion
if __name__ == '__main__':
    unpack_main()
    #
    # this tests just unpacking
    # parsed_args: argparse.Namespace = parse_args()
    # _app_logger = AORunActivityLog(prefix=activity, home=parsed_args.log_home, level=parsed_args.log_level)
    # run_log = _app_logger.runtime_logger
    # activity_log = _app_logger.activity_logger
    # run_log.info(f"checking {do_check(parsed_args.src, 'checksum.md5')}")
