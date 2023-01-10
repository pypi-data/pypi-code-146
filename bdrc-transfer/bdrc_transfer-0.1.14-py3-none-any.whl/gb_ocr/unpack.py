#!/usr/bin/env python3
"""
Marshals arguments for shelling out to GPG and, unzipping and unpacking an image group
"""
import argparse
import fileinput
import json
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from tarfile import TarFile

from gb_lib.GbLib import VolumeToWork, GbParserBase, print_args, no_suffix
from log_ocr.AORunLog import AORunActivityLog
from log_ocr.GbOcrTrack import GbOcrContext
from gb_ocr.GRINConfig import GRINConfig
from log_ocr.models.drs import GbDownload, GbReadyTrack, GbUnpack, Volumes
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

log: AORunActivityLog

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


class ChecksumFailedError(Exception):
    pass


# region unpacker class
class Unpacker(GRINConfig):
    """
    Unpacks a downloaded file
    """

    def __init__(self, gb_package_path: Path, v2w: VolumeToWork):
        super().__init__(type_section="content")
        self.source_path = gb_package_path
        self.v_w = v2w
        self.log = AORunActivityLog(prefix="receive", home=self.cfg_log_dir, level=self.cfg_log_level,
                                    log_descriptor="content")
        self._result_path = None

    _v_w: VolumeToWork

    @property
    def v_w(self) -> VolumeToWork:
        return self._v_w

    @v_w.setter
    def v_w(self, value: VolumeToWork):
        self._v_w = value

    _source_path: Path

    @property
    def source_path(self):
        return self._source_path

    @source_path.setter
    def source_path(self, value):
        self._source_path = value

    _log: AORunActivityLog

    @property
    def log(self) -> AORunActivityLog:
        return self._log

    @log.setter
    def log(self, value: AORunActivityLog):
        self._log = value

    @property
    def run_log(self):
        return self.log.runtime_logger

    @property
    def act_log(self):
        return self.log.activity_logger

    @property
    def db_log(self):
        return self.log.activity_db_logger

    @property
    def result_path(self) -> Path:
        return self._result_path

    @result_path.setter
    def result_path(self, value: Path):
        self._result_path = value

    def do_unpack(self) -> object:
        self.unpack_one(self.source_path)
        return self

    def unpack_one(self, src: Path):
        """
        Complete unpacking process. Derives the work name from  the filename of src. Unpack files into
        dirname(src)/WorkName/basename(src)
        :param src: Path of source to unpack
        :return: sources on disk
        """

        job_step: str = "gpg"
        # noinspection PyBroadException
        try:
            gunz: Path = self.do_gpg(src)

            lm: {} = {'src': str(src), "dest": str(gunz)}
            lms = json.dumps(lm)  # LogMessageString
            self.run_log.info(f"decrypted {src} to {gunz}")
            self.db_log.add_content_activity(self.v_w.work_name, self.v_w.volume_label, job_step, datetime.now(), 0,
                                             lms)

            #
            # jimk - save the decrypted file to the internal archive

            job_step = "extract"
            self.result_path = self.extract(gunz)
            self.db_log.add_content_activity(self.v_w.work_name, self.v_w.volume_label, job_step, datetime.now(),
                                             0, json.dumps({'src': str(gunz), "dest": str(self.result_path)}))
            job_step = "checksum validate"
            validated: bool = self.do_checksum_validate(self.result_path, "checksum.md5")
            self.run_log.info(f"MD5 {job_step} {validated} {self.result_path}")
            self.db_log.add_content_activity(self.v_w.work_name, self.v_w.volume_label, job_step, datetime.now(),
                                             0 if validated else 1, json.dumps({'src': str(self.result_path)}))
            if not validated:
                raise ChecksumFailedError(
                    f"Checksums on object {self.result_path} failed. Possible Corruption. Cannot continue.")
        except Exception:
            ei = sys.exc_info()
            unpack_error_string: str = f"{job_step} failed: {ei[1]}"
            self.run_log.error(unpack_error_string)
            self.db_log.add_content_activity(self.v_w.work_name, self.v_w.volume_label, job_step, datetime.now(), 1)
            raise

    def do_gpg(self, src: Path) -> Path:
        """
        Decrypts a gpg file
        :param src: Path to source file
        :return: the pathname of the decrypted file
        """
        gpg_exec = self.find_bin("gpg")
        if not os.path.exists(gpg_exec):
            raise ValueError(f"gpg binary not present on system")
        # make the output file
        output_file: Path = Path(os.path.splitext(src)[0])
        if Path.exists(output_file):
            os.remove(output_file)
        gpg_command: [] = [
            gpg_exec,
            '--batch',
            '--passphrase',
            f"{self.gb_sftp_config.gpg_passphrase}",
            '-o',
            output_file,
            '--decrypt',
            src
        ]
        if self.cfg_log_level == logging.DEBUG:
            gpg_command.insert(2, '-v')
        gpg_out: subprocess.CompletedProcess = subprocess.run(gpg_command, capture_output=True)

        self.run_log.debug(
            f"unpack console: stdout{gpg_out.stdout.decode()}\n stderr{gpg_out.stderr.decode()} "
            f"rc={gpg_out.returncode}")

        if gpg_out.returncode != 0:
            raise GPGFailedError(f"decrypt failure {src} {gpg_out.stdout.decode()}\n{gpg_out.stderr.decode()}")
        return output_file

    def extract(self, src: Path) -> Path:
        """
        GUnzip and untar the source
        :param src: path to file to unzip
        :return:
        """
        import tarfile

        # Put the output next to the source file. It should be a dir
        # with the work name
        output_dir: Path = src.parent / self.v_w.work_name / self.v_w.volume_label

        try:
            if Path.exists(output_dir):
                shutil.rmtree(output_dir)
            else:
                os.makedirs(output_dir, exist_ok=True)

            tf: TarFile = tarfile.open(src, mode='r:gz')
            tf.extractall(output_dir)

        except:
            ei = sys.exc_info()
            raise GunzipFailedError(f"decompress failure on src {ei[1]} ")
        return output_dir

    # region Obsolete
    def do_gunz_shell(self, src: Path) -> Path:
        """
        GUnzip the source
        :param src: path to file to unzip
        :return:
        """
        gunzip_bin = self.find_bin("gunzip")
        if not os.path.exists(gunzip_bin):
            raise ValueError(f"gunzip binary not present on system")
        # make the output file
        output_file: Path = Path(os.path.splitext(src)[0])

        if Path.exists(output_file):
            os.remove(output_file)

        gunzip_command: [] = [
            gunzip_bin,
            src
        ]
        if self.cfg_log_level == logging.DEBUG:
            gunzip_command.insert(1, '-v')
        self.run_log.debug(f"{gunzip_command}")

        gunz_out: subprocess.CompletedProcess = subprocess.run(gunzip_command, capture_output=True)

        self.run_log.debug(
            f"unpack console: stdout{gunz_out.stdout.decode()}\n stderr{gunz_out.stderr.decode()} "
            f"rc={gunz_out.returncode}")

        if gunz_out.returncode != 0:
            raise GunzipFailedError(
                f"decompress failure {src} {gunz_out.stdout.decode()}\n{gunz_out.stderr.decode()}")
        return output_file

    def do_tar(self, src: Path, output_dir: Path) -> Path:
        """
        Extracts the uncompressed tar file
        :param src: source file.
        :param output_dir: extraction destination
        :return: the full path of the output directory
        """
        tar_bin = self.find_bin("tar")
        if not os.path.exists(tar_bin):
            raise ValueError(f"tar binary not present on system")

        self.run_log.debug(f"{'tar':>8}:creating {output_dir}")

        # Really shouldn't exist
        os.makedirs(output_dir)

        tar_command: [] = [
            tar_bin,
            '--extract',
            f"--file={src}",
            f"--directory={output_dir}"
        ]

        if self.cfg_log_level == logging.DEBUG:
            tar_command.insert(1, '-v')

        tar_out: subprocess.CompletedProcess = subprocess.run(tar_command, capture_output=True)

        self.run_log.debug(
            f"unpack console: stdout{tar_out.stdout.decode()}\n stderr{tar_out.stderr.decode()} "
            f"rc={tar_out.returncode}")

        if tar_out.returncode != 0:
            raise TarFailedError(
                f"extraction failure {src} {tar_out.stdout.decode()}\n{tar_out.stderr.decode()}")
        return output_dir

    def do_rename(self, orig_path: Path):
        """
        Backs up an existing path to a sibling directory
        :param orig_path:
        :return:
        """
        bk_part = "-backup-"

        # Relocate existing
        limit: int = 5
        if os.path.exists(orig_path):
            pass1: int = 1

            # Find an available slot
            while os.path.exists(str(orig_path) + f"{bk_part}{pass1}") and pass1 < limit:
                self.run_log.debug(f"{'tar':>8}:output exists: {orig_path}{bk_part}{pass1}")
                pass1 = pass1 + 1

            # none? Make some room. pass1 is the next available slot
            if pass1 == limit:
                self.run_log.debug(f"{'tar':>8}:Max backups reached. Removing oldest..")
                # Remove the first one
                shutil.rmtree(str(orig_path) + f"{bk_part}{limit - 1}")

                # Rename the rest
                for pass2 in range(limit - 1, 1, -1):
                    self.run_log.debug(f"{'tar':>8}:pushing up {orig_path}{bk_part}{pass2 - 1} to {pass2} ")
                    os.rename(str(orig_path) + f"{bk_part}{pass2 - 1}", str(orig_path) + f"{bk_part}{pass2}")
                pass1 = 1
            self.run_log.debug(f"{'tar':>8}:pushing {orig_path} to {bk_part}{pass1}")
            os.rename(orig_path, f"{orig_path}{bk_part}{pass1}")

    # endregion

    @classmethod
    def find_bin(cls, base_bin: str) -> str:
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

    def do_checksum_validate(self, sources_path: Path, sum_file_name: str) -> bool:
        """
        Checks md5 sums of each file in the manifest.
        :return: true if all files match their md5 checksum in the sum_file_name
        """
        import hashlib
        rc: [] = []
        with open(sources_path / sum_file_name, 'r') as sums:
            for line in sums.readlines():
                d = line.strip().split()
                transmitted_checksum = d[0]
                file_path: Path = Path(sources_path, d[1])
                # build a list of each file's md5
                received_checksum = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                rc.append(
                    {
                        "file": d[1],
                        "match": received_checksum == transmitted_checksum,
                        "transmitted_checksum": transmitted_checksum,
                        "received_checksum": received_checksum
                    })

        fails: [] = list(filter(lambda x: not x["match"], rc))

        list(map(lambda x: self.run_log.error(f"{x}") if not x["match"] else None, fails))
        # If there were no files to read, call it a failure
        # Otherwise return failures (second column in each list)
        return len(fails) == 0 if len(rc) > 0 else False


def parse_args() -> argparse.Namespace:
    ap = GbParserBase(
        description="Unpacks an artifact")
    ap.add_argument("src", help="xxx.tar.gz.gpg file to unpack", nargs='?',
                    default=GbParserBase.NO_ARG_GIVEN)
    return ap.init()


def unpack_main():
    """
    Unpacks a gpg file. We do this in the shell, because we want the result to be a file, not a stream
    :return:
    """

    global log, run_log, activity_log
    unpack_main_args: argparse.Namespace = parse_args()
    log = AORunActivityLog(prefix=activity, home=unpack_main_args.log_home,
                           level=unpack_main_args.log_level, log_descriptor=dest_token)
    run_log = log.runtime_logger

    run_log.debug(f"args: {print_args(unpack_main_args)}")

    try:

        if unpack_main_args.input_file:
            for f in fileinput.input(files=unpack_main_args.input_file):
                unpack_one(f.strip(), unpack_main_args)
            return
        unpack_one(unpack_main_args.src, unpack_main_args)

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


def unpack_one(to_unpack: str, args: argparse.Namespace):
    """
    Unpack one work
    :param to_unpack: filename to unpack
    :param args: command line params
    :return:
    """

    if args.log_after_fact:
        run_log.info(f"Simulating {activity} for {to_unpack}:{dest_token}")
        activity_log.info(f"success:{activity}:{to_unpack}->{to_unpack}:{dest_token}")
        return
    if args.dry_run:
        run_log.info(f"(dry_run):success:unpack:{to_unpack}:")
        return
    # noinspection PyBroadException
    ok_unpack: bool = False
    unpack_path: Path = Path(os.path.expanduser(to_unpack))
    ig_label: str = no_suffix(unpack_path.name)
    cur_unpack = Unpacker(unpack_path, VolumeToWork(ig_label))
    try:
        cur_unpack.do_unpack()
        ok_unpack = True
    except:
        run_log.error(f" Could not unpack {unpack_path} : Error {sys.exc_info()[1]}")
    finally:
        if ok_unpack:
            with GbOcrContext() as ctx:
                try:
                    v_w: VolumeToWork = VolumeToWork(ig_label)
                    vol: Volumes = ctx.get_or_create_volume(v_w.work_name, v_w.volume_label)
                    run_log.info(f"success unpack {cur_unpack.source_path} to {cur_unpack.result_path}")
                    new_unpack = GbUnpack(unpack_time=datetime.now(), unpacked_path=cur_unpack.result_path,
                                          unpack_object_name=str(unpack_path),
                                          volume_id=vol.volumeId)

                    ctx.session.add(new_unpack)
                    ctx.session.flush()
                    ctx.session.add(GbReadyTrack(target_id=new_unpack.id, activity='distribute'))
                except SQLAlchemyError:
                    run_log.error(f"could not record unpack in DB. error: {sys.exc_info()[1]}  path:{unpack_path}")
                    ctx.session.rollback()
                finally:
                    ctx.session.commit()


def unpack_service():
    """
    Polls the database for downloads to unpack
    """

    config: GRINConfig = GRINConfig()

    log = AORunActivityLog(prefix=activity, log_descriptor="content",
                           level=logging.INFO, home=config.cfg_log_dir)

    # Get records marked "Ready for unpack" (download activity marks it ready)
    with GbOcrContext() as ctx:
        get_ready_query = select(GbReadyTrack.target_id) \
            .where(GbReadyTrack.activity == 'unpack') \
            .order_by(GbReadyTrack.create_time)

        get_readys_subq = get_ready_query.subquery()

        get_ready_downloads = select(GbDownload).join(get_readys_subq, GbDownload.id == get_readys_subq.c.target_id)
        yy = ctx.session.execute(get_ready_downloads).all()

        ok_unpack: bool = False
        cur_unpack: Unpacker

        # TODO:  Unpack them all
        for download in yy:
            try:
                ok_unpack = False
                target_dl = download.GbDownload

                # vvvvvvvvvv    dev    vvvvvvvvvv
                # test_dl_path = str(target_dl.download_path).replace('/mnt/','/Volumes/',1)
                # cur_unpack = Unpacker(Path(os.path.expanduser(test_dl_path)),
                #                       VolumeToWork(target_dl.volume.label))
                # # Test ONLY
                # cur_unpack.result_path = cur_unpack.source_path
                # ^^^^^^^      dev     ^^^^^^^^^^^^^

                # vvvvvvvvvv    Production   vvvvvvvvvv
                cur_unpack = Unpacker(Path(os.path.expanduser(target_dl.download_path)),
                                      VolumeToWork(target_dl.volume.label))
                cur_unpack.do_unpack()
                # ^^^^^^^^^^    Production   ^^^^^^^^^^
                ok_unpack = True
            except  GPGFailedError:
                log.runtime_logger.error(sys.exc_info()[1])
            except GunzipFailedError:
                log.runtime_logger.error(sys.exc_info()[1])
            except TarFailedError:
                log.runtime_logger.error(sys.exc_info()[1])
            except ChecksumFailedError:
                log.runtime_logger.error(sys.exc_info()[1])
            finally:
                if ok_unpack:
                    try:
                        log.runtime_logger.info(f"success unpack {cur_unpack.source_path} to {cur_unpack.result_path}")
                        new_unpack = GbUnpack(unpack_time=datetime.now(), unpacked_path=cur_unpack.result_path,
                                              unpack_object_name=target_dl.download_object_name,
                                              volume_id=target_dl.volume_id)

                        ctx.session.add(new_unpack)
                        ctx.session.flush()

                        # Mark the object ready to distribute
                        ctx.session.add(GbReadyTrack(target_id=new_unpack.id, activity='distribute'))

                        # Delete this from the gb_tracked
                        delete_one_track = delete(GbReadyTrack).where(GbReadyTrack.target_id == target_dl.id)
                        ctx.session.execute(delete_one_track)
                        ctx.session.commit()
                    except SQLAlchemyError as sqle:
                        log.runtime_logger.error(sqle, exc_info=True)
                        ctx.session.rollback()


if __name__ == '__main__':
    # unpack_service()
    unpack_main()
