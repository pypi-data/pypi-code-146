#!/usr/bin/env python3
"""
Sends uploaded material to OCR
"""

import argparse

import logging
import subprocess
from datetime import datetime
import io
import os
import shutil
from collections import namedtuple
from pathlib import Path
from zipfile import ZipFile

import boto3
import botocore
import gzip
import json

from archive_ops.Resolvers import Resolvers
from archive_ops.shell_ws import get_mappings

from gb_lib.GbLib import VolumeToWork, GbParserBase
from gb_ocr.GRINConfig import GRINConfig
from gb_ocr.unpack import Unpacker
from log_ocr.AORunLog import AORunActivityLog

# Required globals

activity: str = "distribute"
dest_token: str = "content"

# This will cover all the works in the initial cycle.
# These are specified in the spec (#archive-ops 694)
#
# For this module only.
# These are keys in the GRINConfig.GBSftpConfig
# TODO: Move them into the GRIN config / resources section
S3_OCR_BUCKET_KEY: str = "s3_ocr_bucket"
S3_OCR_HOME_KEY: str = "s3_ocr_home"
GB_SFTP_BATCH_ID_KEY = "batch_id"
GB_SFTP_OUTPUT_SOURCE = "output_source"

SourceList = namedtuple('sources', 'html images txt')

had_fail: bool = False


class AWSSyncFail(Exception):
    pass


class Distributor(GRINConfig):
    """
    Distributes an unpacked, downloaded object.
    According to https://buda-base/archive-ops/issues/694, as of 2022-X-12, the distribution destination is:
    s3://ocr.bdrc.ioWorks/{hash}/{wid}/{ocrmethod}/{batchid}/
    This value is 's3_work_root'
    where hash is the locate_archive -s output
    wid is the workRid
    ocrmethod is 'google-books'
    batchid is 'batch_2022'
    contents include:

    + s3_work_root/info.json - which is updated on every image group that gets uploaded (they get
    uploaded individually. this file only represents the time of the last upload)


    """

    _source_path: Path

    @property
    def source_path(self) -> Path:
        return self._source_path

    @source_path.setter
    def source_path(self, value):
        self._source_path = value

    _s3_dest_path: str

    @property
    def s3_dest_path(self):
        return self._s3_dest_path

    @s3_dest_path.setter
    def s3_dest_path(self, value):
        self._s3_dest_path = value

    def __init__(self, gb_package_path: Path, v2w: VolumeToWork):
        super().__init__(type_section="content")
        self.source_path = gb_package_path
        self.v_w = v2w
        self.log = AORunActivityLog(prefix=activity, home=self.cfg_log_dir, level=self.cfg_log_level,
                                    log_descriptor="content")
        self.s3 = boto3.client('s3')
        self.s3_dest_path: str = 'Not uploaded'

        # Har - because I'm a subclass of config
        self.image_file_exts: [] = self.get_value('image_file_exts')

    def distribute_image_group(self) -> str:
        """
        Distributes one image group to BDRC OCR.
        See ao-google-books README.md for structure definition
        :return: key of parent of all uploaded images (s3 image group)
        """
        import os

        # Make a holding tank. We will use the AWS CLI `aws s3 sync` shell script to actually move
        from tempfile import TemporaryDirectory

        batch_id: str = self.gb_sftp_config.get_value(GB_SFTP_BATCH_ID_KEY)
        output_source = self.gb_sftp_config.get_value(GB_SFTP_OUTPUT_SOURCE)

        with TemporaryDirectory(self.v_w.work_name) as buffer:
            # make the folders
            parent_dir: Path = Path(buffer, output_source, batch_id)
            os.makedirs(parent_dir)

            # create info.json
            info: {} = {
                "timestamp": datetime.strftime(datetime.now(), "%xT%X"),
                "html": "html.zip",
                "txt": "txt.zip",
                "images": "images.zip",
            }
            json_path: Path = Path(parent_dir, 'info.json')
            self.log.runtime_logger.debug(f"Creating {json_path}")
            with open(json_path, 'w') as oj:
                json.dump(info, oj)

            info_dir: Path = Path(parent_dir, 'info')
            info_work_dir: Path = Path(info_dir, self.v_w.volume_label)
            output_dir = Path(parent_dir, 'output', self.v_w.volume_label)
            os.makedirs(info_work_dir)

            os.makedirs(output_dir)

            self.log.runtime_logger.debug(
                f"Created dirs, creating  {str(Path(info_work_dir.name, 'gb-bdrc-map.json'))}")

            # Make the gb-bdrc-map
            GBDimensionsInfo("archive.tbrc.org", "Works", self.v_w.work_name, self.v_w.volume_label) \
                .write_image_list(info_work_dir / 'gb-bdrc-map.json')

            self.log.runtime_logger.debug(f"Copying manifest")
            # Copy the manifest from GB
            f_str = f"TBRC_{self.v_w.volume_label}.xml"
            shutil.copyfile(self.source_path / f_str, info_work_dir / f_str)

            buckets: SourceList = self.build_zip_lists()
            # zip up the outputs
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=3, thread_name_prefix='ARC') as executor:
                executor.submit(self.archive_path_func, Path(output_dir, 'images.zip'), buckets.images)
                executor.submit(self.archive_path_func, Path(output_dir, 'html.zip'), buckets.html)
                executor.submit(self.archive_path_func, Path(output_dir, 'txt.zip'), buckets.txt)

            self.sync(buffer)
            return f"{self.s3_dest_path}/{output_source}/{batch_id}/"

    def sync(self, source: Path):
        """
        Sync the source to the OCR destination
        :param source: OCR source, all processed
        sets the class variable self.s3_dest_path
        """
        aws_path: str = Unpacker.find_bin('aws')
        if not os.path.exists(aws_path):
            raise ValueError(f"aws program {aws_path} not present on system")
        s3_ocr_bucket = self.gb_sftp_config.get_value(S3_OCR_BUCKET_KEY)
        s3_ocr_home = self.gb_sftp_config.get_value(S3_OCR_HOME_KEY)
        s3_key = f"s3://{s3_ocr_bucket}/{s3_ocr_home}"
        self.s3_dest_path = get_mappings(s3_key, self.v_w.work_name, Resolvers.S3_BUCKET)

        aws_sync_cmd: [] = [
            aws_path,
            's3',
            'sync',
            '--no-progress',
            '--only-show-errors',
            source,
            self.s3_dest_path
        ]

        aws_sync_result: subprocess.CompletedProcess = subprocess.run(aws_sync_cmd, capture_output=True)
        self.log.runtime_logger.info(f"sync {source} to {self.s3_dest_path}")

        self.log.runtime_logger.info(f"aws sync rc:{aws_sync_result.returncode} command:{aws_sync_cmd}")
        self.log.runtime_logger.debug(
            f"stdout{aws_sync_result.stdout.decode()}\n stderr{aws_sync_result.stderr.decode()}")
        if aws_sync_result.returncode != 0:
            self.log.activity_db_logger.add_content_activity(self.v_w.work_name, self.v_w.volume_label,
                                                             "distribute_sync", datetime.now(), 1)
            raise AWSSyncFail(f"aws s3 sync failure from source:{source} to dest: "

                              f"{self.s3_dest_path} {aws_sync_result.stdout.decode()}\n"
                              f"{aws_sync_result.stderr.decode()}\n")

        self.log.activity_db_logger.add_content_activity(self.v_w.work_name, self.v_w.volume_label,
                                                         "distribute_sync", datetime.now(), 0)
    def build_zip_lists(self) -> SourceList:
        """
        Archives the files in a GB distribution
        :return: SourceList object
        """
        html: [] = []
        images: [] = []
        txt: [] = []

        for dir_entry in os.scandir(self.source_path):
            if not dir_entry.is_file():
                continue
            if dir_entry.name.endswith('.html'):
                html.append(dir_entry.path)
            elif dir_entry.name.endswith('.txt'):
                txt.append(dir_entry.path)
            else:
                _, ext = os.path.splitext(dir_entry.name)
                if ext.lower() in self.image_file_exts:
                    images.append(dir_entry.path)

        html.sort()
        images.sort()
        txt.sort()
        return SourceList(html=html, images=images, txt=txt)

    def archive_path_func(self, output_file: Path, sources: [str]):
        """
        Populates a zip file with paths. **IMPORTANT** Writes all the
        paths to a top level directory in the archive.
        /some/where/over/tatooine/bluebirds-fly.txt ==> bluebirds-fly.txt
        :param output_file: output archive
        :param sources: list of full paths to write
        :return:
        """
        with ZipFile(output_file, 'w') as zf:
            self.log.runtime_logger.debug(f"Creating archive {output_file}")
            for a_source in sources:
                # self.log.runtime_logger.debug(f"archiving {a_path}")
                a_path = Path(a_source)
                zf.write(a_path, a_path.name)


    def log_dip(self, distro_dir: str, comment: str = '', rc: int = 0) -> str:
        """
        Logs the S3 distribution to log-dip
        :param distro_dir: S3 destination
        :param comment:dip log log
        :param rc: return code to log (0 == success, anything else == failure)

        :return: log_dip id
        """

        from archive_ops.DipLog import DipLog

        from log_ocr.DrsContextBase import DrsDbContextBase
        now_now: datetime = datetime.now()

        # you want to pass None for no dip_id. Not str(None)
        # noinspection PyTypeChecker
        return DipLog(f"{DrsDbContextBase.bdrc_db_conf}:{str(self.cfg_db_config)}") \
            .set_dip('GB_OCR_S3_SENT', now_now, now_now, self.source_path, distro_dir,
                     self.v_w.work_name, None, rc, comment)


def iltogbinfo(imagelist) -> {}:
    """
    Translates image group file names into GB Output OCR filenames
    :param imagelist: json list of
    :return: dictionary of translated names
    """
    res = {}
    for i, imginfo in enumerate(imagelist):
        res["%08d" % (i + 1)] = imginfo["filename"]
    return res

class GBDimensionsError(Exception):
    pass

class GBDimensionsInfo:
    """
    Creates a mapping file between dimensions.json and the GB Info
    """

    def __init__(self, source_s3_bucket: str, source_s3_prefix: str, work_rid: str, ig_label: str):
        """
        :param source_s3_bucket: bucket of dimensions.json:
        :param source_s3_prefix: prefix for the dimensions.json:
        :param work_rid: work
        :param ig_label: image group
        """
        self.source_s3_bucket = source_s3_bucket
        self.source_s3_prefix = get_mappings(source_s3_prefix, work_rid, Resolvers.S3_BUCKET)
        self.work_name = work_rid
        self.volume_label = ig_label
        self.s3: boto3.client = boto3.client('s3')

    def write_image_list(self, dest_path: Path):
        """
        Creates and distributes a mapping between BUDA's manifest and the GB OCR output
        :param dest_path: local file
        :return:
        """
        image_list: [] = self.get_image_list()
        gb_info = iltogbinfo(image_list)
        with open(dest_path, 'w') as f:
            json.dump(gb_info, f, ensure_ascii=False)

    def get_image_list(self) -> [str]:
        """
        Gets the image list as defined by a dimensions.json
        :return: json data [ {filename: f1) ,....]
        """

        # We don't have to worry about the image group name disjunction hack - these works are
        # already resolved in S3

        s3_key = f"{self.source_s3_prefix}/images/{self.volume_label}/dimensions.json"
        blob = self.gets3blob(self.source_s3_bucket, s3_key)
        if blob is None or blob.getbuffer().nbytes == 0:
            raise GBDimensionsError(f"no dimensions.json found for {s3_key}")
        blob.seek(0)
        b = blob.read()
        ub = gzip.decompress(b)
        s = ub.decode('utf8')
        data = json.loads(s)
        return data

    def gets3blob(self, bucket: str, s3Key: str) -> io.BytesIO:
        """
        Returns a stream of bytes from an S3 object
        :param bucket:  S3 bucket
        :param s3Key: key rest of path
        :return:
        """
        import io
        f = io.BytesIO()
        try:
            self.s3.download_fileobj(bucket, s3Key, f)
            return f
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] != '404':
                raise
        return f



# noinspection PyBroadException
def distribute_service():
    """
    Main loop to get
    :return:
    """
    # TODO: implement
    from log_ocr.GbOcrTrack import GbOcrContext
    from gb_ocr.GRINConfig import GRINConfig
    from log_ocr.models.drs import GbReadyTrack, GbUnpack
    from sqlalchemy import select, delete
    from sqlalchemy.exc import SQLAlchemyError

    config: GRINConfig = GRINConfig()

    log = AORunActivityLog(prefix=activity, log_descriptor="content",
                           level=config.cfg_log_level, home=config.cfg_log_dir)
    with GbOcrContext() as ctx:
        get_ready_query = select(GbReadyTrack.target_id) \
            .where(GbReadyTrack.activity == 'distribute') \
            .order_by(GbReadyTrack.create_time)

        # Don't really need to split it out, but this way you can debu running the query as a query
        get_ready_subq = get_ready_query.subquery()

        get_ready_unpacked = select(GbUnpack).join(get_ready_subq, GbUnpack.id == get_ready_subq.c.target_id)
        yy = ctx.session.execute(get_ready_unpacked).all()
        log.runtime_logger.info(f" Got {len(yy)} unpacks ready to distribute")
        log.runtime_logger.debug(f"{yy}")

        target_unpack: GbUnpack

        ok_distributed: bool = False
        cur_distribution: Distributor
        cur_distribution_dir: str = "Unset"

        dip_comment: str = ''
        for download in yy:
            try:
                ok_distributed = False
                target_unpack: GbUnpack = download.GbUnpack

                # vvvvvvvvvv    dev       vvvvvvvvvv
                # test_dl_path = Path(os.path.expanduser(target_unpack.unpacked_path).replace('/mnt/','/Volumes/',1))
                # cur_distribution = Distributor(gb_package_path=test_dl_path,
                #                       v2w=VolumeToWork(target_unpack.volume.label))
                # ^^^^^^^   dev           ^^^^^^^^^^^^^^^^

                # vvvvvvvvvv   production       vvvvvvvvvv
                cur_distribution = Distributor(gb_package_path=Path(target_unpack.unpacked_path),
                                               v2w=VolumeToWork(target_unpack.volume.label))
                # ^^^^^^^^^^   production       ^^^^^^^^^^

                cur_distribution_dir = cur_distribution.distribute_image_group()
                ok_distributed = True
            except Exception as e:
                dip_comment = f"{e}"
                log.runtime_logger.error(e, exc_info=True)
            finally:
                if ok_distributed:
                    try:
                        log.runtime_logger.info(
                            f"success distributing {cur_distribution.source_path} to {cur_distribution_dir}")
                        cur_distribution.log_dip(cur_distribution_dir)

                        # Delete this from the gb_tracked
                        delete_one_track = delete(GbReadyTrack).where(GbReadyTrack.target_id == target_unpack.id)
                        ctx.session.execute(delete_one_track)
                        ctx.session.commit()
                    except SQLAlchemyError as sae:
                        ctx.session.rollback()
                        log.runtime_logger.error(sae, exc_info=True)
                else:
                    cur_distribution.log_dip(cur_distribution_dir, comment=dip_comment, rc=1)


def distribute_one(unpacked_path: Path, unpacked_ig_name: str, args: argparse.Namespace):
    """
    Distribute one image group - meant to be used in test harness or one-off call
    (distribute-main)
    :param unpacked_path: path to unpacked material
    :param unpacked_ig_name: workgroup to distribute
    :param args: command line config
    :return:
    """
    config: GRINConfig = GRINConfig()

    # override config with command line
    log_dir: str = config.cfg_log_dir if not args.log_home else args.log_home
    log_level: int = config.cfg_log_level if not args.log_level else logging.getLevelName(args.log_level)

    log = AORunActivityLog(prefix=activity, log_descriptor="content",
                           level=log_level, home=log_dir)

    cur_distribution = Distributor(gb_package_path=Path(unpacked_path),
                                   v2w=VolumeToWork(unpacked_ig_name))

    distro_path: str = "<NO UPLOAD>"
    log_comment: str = ""
    rc: int = 0
    # noinspection PyBroadException
    try:
        distro_path = str(cur_distribution.distribute_image_group())
    except Exception as e:
        log_comment = str(e)
        log.runtime_logger.error(e, exc_info=True)
        rc = 1

    dip_id: str = cur_distribution.log_dip(distro_path,  rc=rc, comment=log_comment)
    if rc == 0:
        log.runtime_logger.info(f"success:Distribute {unpacked_path} to {distro_path} Log_dip id: {dip_id}")
    else:
        log.runtime_logger.error(f"error:Distribute {unpacked_path}: {distro_path} Log_dip id: {dip_id}. Message {log_comment}")


def distribute_main():

    """
    :return:
    """

    ap = GbParserBase(
        description="sends an OCR image group")
    ap.add_argument("image_group", help="path to image group directory", nargs='?',
                    default=GbParserBase.NO_ARG_GIVEN)

    import argparse
    parsed_args: argparse.Namespace = ap.init()

    for quiet_logger in ['boto', 'botocore', 'boto3', 'requests', 'urllib3', 'request', 's3transfer']:
        ql = logging.getLogger(quiet_logger)
        ql.setLevel(logging.CRITICAL)
        ql.propagate = True

    if parsed_args.input_file:
        import fileinput
        for f in fileinput.input(files=parsed_args.input_file):
            ig_path: Path = Path(f.strip())
            distribute_one(ig_path, ig_path.name, parsed_args)
    else:
        ig_path: Path = Path(parsed_args.image_group)
        distribute_one(ig_path, ig_path.name, parsed_args)


if __name__ == '__main__':
    # distribute_service()
    distribute_main()

