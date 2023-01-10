# pylint: disable=protected-access

import logging
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from fnmatch import fnmatch
from re import Pattern
from typing import Any, Dict, List, Optional, Set, Tuple

import icloudpy
import icloudpy.services.photos
import prometheus_client as prom
import yapx
from croniter import croniter
from tabulate import tabulate

from . import constants, exif_datetime
from .__version__ import __version__
from .exceptions import ICloudLoginRequiredError, PhotoDownloadError
from .logger import get_logger
from .photo_asset_ext import PhotoAssetExt
from .utils import build_target_path, download_media, send_webhook, wait_next

try:
    from typing_extensions import Literal
except ModuleNotFoundError:
    from typing import Literal

GLOBAL_ARGS: Dict[str, Any] = {}

STATS_REGISTRY = prom.CollectorRegistry()

ALBUM_PHOTO_COUNT = prom.Gauge(
    name="license_activation_sum",
    documentation="license activation sum",
    labelnames=["username", "album", "stage"],
    registry=STATS_REGISTRY,
)
MEDIA_DOWNLOADED = prom.Counter(
    name="media_downloaded",
    documentation="count of downloaded media assets",
    labelnames=["username", "album", "type"],
    registry=STATS_REGISTRY,
)
MEDIA_DOWNLOADED_BYTES = prom.Counter(
    name="media_downloaded_bytes",
    documentation="size of downloaded media assets",
    labelnames=["username", "album", "type"],
    registry=STATS_REGISTRY,
)
MEDIA_DELETED = prom.Counter(
    name="media_deleted",
    documentation="count of deleted media assets",
    labelnames=["username", "album", "type"],
    registry=STATS_REGISTRY,
)


def setup(
    username: str = yapx.arg(env="ICPD_USERNAME"),
    session_directory: str = yapx.arg("~/.icloudpy", env="ICPD_SESSION_DIR"),
):
    GLOBAL_ARGS["username"] = [
        u.strip() if "@" in u else f"{u.strip()}@{constants.DEFAULT_EMAIL_DOMAIN}"
        for u in username.split(",")
    ]
    GLOBAL_ARGS["session_directory"] = os.path.expanduser(session_directory)


def icloud_login(_extra_args: Optional[List[str]] = None) -> bool:
    return all(
        subprocess.run(
            [
                "icloud",
                "--username",
                u,
                "--session-directory",
                GLOBAL_ARGS["session_directory"],
                *(_extra_args if _extra_args else []),
            ],
            check=False,
        ).returncode
        == 0
        for u in GLOBAL_ARGS["username"]
    )


def _get_icloud_session(username: str):
    icloud: Optional[icloudpy.ICloudPyService] = icloudpy.ICloudPyService(
        apple_id=username,
        cookie_directory=GLOBAL_ARGS["session_directory"],
    )

    if (
        icloud.requires_2fa or icloud.requires_2sa or not icloud.is_trusted_session
    ) and not icloud_login(_extra_args=["--non-interactive"]):
        raise ICloudLoginRequiredError()

    return icloud


def icloud_download(
    album: str = yapx.arg("All Photos", env="ICPD_ALBUM"),
    directory: str = yapx.arg(
        os.getcwd(), env="ICPD_OUTPUT_DIR", flags=["-d", "--directory"]
    ),
    download_count: int = yapx.arg(
        -1, env="ICPD_DOWNLOAD_COUNT", flags=["-n", "--download-count"]
    ),
    keep_count: int = yapx.arg(-1, env="ICPD_KEEP_COUNT", flags=["--keep-count"]),
    keep_days: int = yapx.arg(-1, env="ICPD_KEEP_DAYS", flags=["--keep-days"]),
    convert_heic: bool = yapx.arg(False, env="ICPD_CONVERT_HEIC"),
    delete_after_download: bool = yapx.arg(
        False, env="ICPD_DELETE", flags=["-x", "--delete-after-download"]
    ),
    oldest_first: bool = yapx.arg(False, env="ICPD_OLDEST_FIRST"),
    name_filter: Optional[str] = yapx.arg(None, env="ICPD_FILTER", flags=["--name"]),
    skip_album: Optional[List[str]] = yapx.arg(None, env="ICPD_SKIP_ALBUM"),
    skip_favorites: bool = yapx.arg(False, env="ICPD_SKIP_FAVORITES"),
    skip_hidden: bool = yapx.arg(False, env="ICPD_SKIP_HIDDEN"),
    skip_lives: bool = yapx.arg(False, env="ICPD_SKIP_LIVES"),
    skip_videos: bool = yapx.arg(False, env="ICPD_SKIP_VIDEOS"),
    skip_stills: bool = yapx.arg(False, env="ICPD_SKIP_STILLS"),
    break_if_exists: bool = yapx.arg(False, env="ICPD_BREAK_IF_EXISTS"),
    folder_structure: str = yapx.arg("{:%Y/%m}", env="ICPD_FOLDER_STRUCTURE"),
    webhook_url: Optional[str] = yapx.arg(None, env="ICPD_WEBHOOK_URL"),
    webhook_method: Optional[str] = yapx.arg(None, env="ICPD_WEBHOOK_METHOD"),
    webhook_skip_verify: bool = yapx.arg(False, env="ICPD_WEBHOOK_METHOD"),
    pre_sh: Optional[str] = yapx.arg(None, env="ICPD_PRE_SH"),
    post_sh: Optional[str] = yapx.arg(None, env="ICPD_POST_SH"),
    dry_run: bool = False,
    schedule: Optional[str] = yapx.arg(None, env="ICPD_SCHEDULE"),
    metrics_port: Optional[int] = yapx.arg(None, env="ICPD_METRICS_PORT"),
    log_level: Literal[
        "info", "debug", "warning", "error", "critical", "fatal"
    ] = "info",
) -> None:
    logger = get_logger(__name__, getattr(logging, log_level.upper()))

    scheduler: Optional[croniter] = None
    if schedule:
        logger.debug("cron-schedule: %s", schedule)
        scheduler = croniter(schedule)

    directory = os.path.normpath(os.path.expanduser(directory))

    if metrics_port and metrics_port > 0:
        logger.info("exposing metrics on port %d", metrics_port)
        prom.start_http_server(port=metrics_port, registry=STATS_REGISTRY)

    exit_code: int = 0
    while exit_code == 0:
        if pre_sh:
            logger.info("invoking: %s", pre_sh)
            subprocess.run(pre_sh, shell=True, check=True)

        for u in GLOBAL_ARGS["username"]:
            icloud: icloudpy.ICloudPyService = _get_icloud_session(username=u)

            if keep_count >= 0 or keep_days >= 0:
                oldest_first = True
                delete_after_download = True

            # instantiate this now so we can get any album and retrieve photos oldest-first.
            photos: icloudpy.services.photos.PhotoAlbum = icloud.photos.albums[album]

            expose_metrics: bool = (
                not dry_run and metrics_port is not None and metrics_port > 0
            )

            if expose_metrics:
                ALBUM_PHOTO_COUNT.labels(username=u, album=album, stage="before").set(
                    len(photos)
                )

            if oldest_first:
                logger.info("Configured to process oldest photos first.")
                for folder_settings in icloud._photos._albums.values():
                    folder_settings.direction = "DESCENDING"

            if delete_after_download is True:
                logger.info(
                    "Configured to delete source photos from iCloud after downloading!"
                )

            logger.debug("Looking up all photos and videos from album: %s", album)

            skip_photo_ids: Set[str] = set()

            if skip_album:
                for a in skip_album:
                    logger.debug("Obtaining file IDs from album: '%s'", a)
                    this_list = [p.id for p in icloud.photos.albums[a]]
                    skip_photo_ids.update(this_list)
                    logger.debug("Found %d files", len(this_list))

            photo_total_count: int = len(photos)
            photo_download_limit: int = photo_total_count
            if keep_count >= 0:
                photo_download_limit = max(0, photo_download_limit - keep_count)
            if download_count >= 0:
                photo_download_limit = min(download_count, photo_download_limit)

            logger.info(
                "Preparing to download %d of %d photos.",
                photo_download_limit,
                photo_total_count,
            )

            break_at_date: Optional[datetime] = None
            if keep_days > 0:
                break_at_date = datetime.combine(
                    datetime.utcnow().date() - timedelta(days=keep_days),
                    datetime.min.time(),
                )
                logger.info("Will ignore media created >= %s", str(break_at_date))

            logger.info("Destination directory: %s", directory)

            pattern: Optional[Pattern] = (
                re.compile(pattern=name_filter, flags=re.IGNORECASE)
                if name_filter
                else None
            )

            c: int = 0
            for i, item in enumerate(photos):

                logger.info(
                    "*** iteration=%d; downloads=%d; limit=%d",
                    i + 1,
                    c,
                    photo_download_limit,
                )
                if c >= photo_download_limit:
                    logger.info("Download limit reached: %d", photo_download_limit)
                    break

                remote_file: PhotoAssetExt = PhotoAssetExt(item)

                if break_at_date and remote_file.created >= break_at_date:
                    logger.info(
                        "Download limit reached: observed=%s; limit=%s",
                        remote_file.created,
                        break_at_date,
                    )
                    break

                if dry_run:
                    logger.info("*** (DRY RUN)")

                logger.info("remote file name: %s", remote_file.filename)

                # only look for original size of photos and videos.
                remote_file_versions: Dict[str, Any] = {
                    name: v
                    for name, v in remote_file.largest_versions.items()
                    if name in constants.DOWNLOAD_FORMATS
                }

                # only download "medium video" version if it is not from the original record
                # (this will download rendered versions of special-effect videos, e.g., slo-mo,
                # but not unecessarily download "medium video" in other cases.)
                if (
                    constants.MEDIUM_VIDEO in remote_file_versions
                    and remote_file_versions[constants.MEDIUM_VIDEO]["source"]
                    == constants.MASTER_RECORD_TYPE
                ):
                    del remote_file_versions[constants.MEDIUM_VIDEO]

                skip: bool = False
                if not remote_file_versions:
                    skip = True
                    logger.warning("No URL found for file.")
                elif skip_favorites and remote_file.is_favorite:
                    skip = True
                    logger.info("Skipping favorite media.")
                elif skip_hidden and remote_file.is_hidden:
                    skip = True
                    logger.info("Skipping hidden media.")
                elif (
                    (skip_lives and remote_file.is_live)
                    or (skip_videos and remote_file.is_video)
                    or (skip_stills and remote_file.is_still)
                ):
                    skip = True
                    logger.info("Skipping media type: %s", remote_file.media_type)
                elif skip_photo_ids and remote_file.id in skip_photo_ids:
                    skip = True
                    logger.info("Skipping media from an ignored album: %s", skip_album)
                elif pattern and not pattern.search(remote_file.filename):
                    skip = True
                    logger.info("Skipping media not matching filter.")
                # elif not (remote_file.is_edited and remote_file.is_video):
                #     raise Exception("idk")
                #     skip = True

                if skip:
                    continue

                success: List[bool] = []
                target_exists: bool = False
                for version_name, version_details in remote_file_versions.items():

                    logger.info("version: %s", version_name)

                    target_file: str = build_target_path(
                        username=u,
                        file_name=version_details["filename"],
                        date_created=remote_file.created,
                        parent_directory=directory,
                        folder_structure=folder_structure,
                    )

                    target_exists = os.path.exists(target_file)
                    if target_exists:
                        file_size = os.path.getsize(target_file)
                        photo_size = version_details["size"]

                        if file_size != photo_size:
                            target_file = f"-{photo_size}.".join(
                                target_file.rsplit(".", 1)
                            )
                            target_exists = False

                    if not target_exists:
                        logger.info("Downloading: %s, ", target_file)

                        if not dry_run and not download_media(
                            icloud=icloud,
                            logger=logger,
                            photo=remote_file,
                            version=version_name,
                            target_file=target_file,
                        ):
                            raise PhotoDownloadError(target_file)

                        if expose_metrics:
                            MEDIA_DOWNLOADED_BYTES.labels(
                                username=u,
                                album=album,
                                type=remote_file.media_type,
                            ).inc(version_details["size"])

                    if not dry_run:
                        conversion_output_files: List[str] = (
                            convert_heic_to_jpg(target_file)
                            if convert_heic and target_file.upper().endswith(".HEIC")
                            else []
                        )
                        for f in conversion_output_files + [target_file]:
                            if f.upper().endswith(
                                (".JPG", ".JPEG")
                            ) and not exif_datetime.get_photo_exif(f):
                                # %Y:%m:%d looks wrong but it's the correct format
                                date_str = remote_file.created.strftime(
                                    "%Y:%m:%d %H:%M:%S"
                                )
                                exif_datetime.set_photo_exif(f, date_str=date_str)

                    if target_exists:
                        logger.warning("Target already exists: %s", target_file)
                        if break_if_exists:
                            break

                    success.append(True)

                if delete_after_download is True:
                    if len(success) != len(remote_file_versions) or not all(success):
                        logger.info("Not all media was downloaded; not deleting.")
                    elif not dry_run:
                        logger.info("Deleting source file from iCloud.")
                        remote_file.delete()

                        if expose_metrics:
                            MEDIA_DELETED.labels(
                                username=u,
                                album=album,
                                type=remote_file.media_type,
                            ).inc(1)

                if expose_metrics:
                    MEDIA_DOWNLOADED.labels(
                        username=u,
                        album=album,
                        type=remote_file.media_type,
                    ).inc(1)

                c += 1

                if target_exists and break_if_exists:
                    logger.info("Stopping early.")
                    break

            if expose_metrics:
                photos._len = None  # reset to not rely on cached count.
                ALBUM_PHOTO_COUNT.labels(username=u, album=album, stage="before").set(
                    len(photos)
                )

        if post_sh:
            logger.info("invoking: %s", post_sh)
            subprocess.run(post_sh, shell=True, check=True)

        logger.info("Done.")

        if webhook_url and not dry_run:
            send_webhook(
                url=webhook_url,
                method=webhook_method,
                skip_verify=webhook_skip_verify,
                data="complete",
            )

        if not scheduler:
            break
        if exit_code == 0:
            wait_next(scheduler, logger=logger)
    # END: while

    logger.debug("exit code: %d", str(exit_code))
    sys.exit(exit_code)


def convert_heic_to_jpg(path: str, quality: int = 100) -> List[str]:
    source_file_list: List[str] = (
        [
            os.path.join(dir_name, x)
            for dir_name, filter_to in [os.path.split(path)]
            for x in os.listdir(dir_name)
            if x.lower().endswith(".heic") and fnmatch(x, filter_to)
        ]
        if "*" in path
        else [path]
        if path.lower().endswith(".heic")
        else [
            os.path.join(path, x)
            for x in os.listdir(path)
            if x.lower().endswith(".heic")
        ]
        if os.path.isdir(path)
        else []
    )

    target_files: List[Tuple[str, str]] = [
        (x, os.path.splitext(x)[0] + ".jpg") for x in source_file_list
    ]

    for f, f_new in target_files:
        subprocess.run(
            ["heif-convert", "-q", str(quality), f, f_new],
            check=True,
        )
        p: subprocess.CompletedProcess = subprocess.run(
            ["exiftool", "-n", "-QuickTime:Rotation", f], check=False, text=True
        )

        exiftool_args: List[str] = [
            "exiftool",
            "-overwrite_original",
            "-P",
            "-n",
            "-ModifyDate<FileModifyDate",
        ]

        if p.returncode == 0:
            exiftool_args.append("-Orientation=1")
        subprocess.run(exiftool_args + [f_new], check=True)

    return [x for _, x in target_files]


def _list_albums(
    username: str,
    filter_to: Optional[str] = None,
    stats: bool = False,
    _icloud: Optional[icloudpy.ICloudPyService] = None,
) -> List[Dict[str, Any]]:
    if not _icloud:
        _icloud = _get_icloud_session(username=username)

    return [
        {"Album": str(v), "Photos": len(v)} if stats else {"Album": str(v)}
        for v in _icloud.photos.albums.values()
        if not filter_to or fnmatch(str(v), filter_to)
    ]


def list_albums(
    filter_to: Optional[str] = yapx.arg(None, flags=["--filter"]), stats: bool = False
) -> None:
    for u in GLOBAL_ARGS["username"]:
        print(
            tabulate(
                _list_albums(username=u, filter_to=filter_to, stats=stats),
                headers="keys",
                tablefmt="github",
            )
        )


def main() -> None:
    yapx.run(
        setup,
        **{
            "version": lambda: print(__version__),
            "login": icloud_login,
            "convert-heic": convert_heic_to_jpg,
            "albums": list_albums,
            "download": icloud_download,
        },
        _args=sys.argv[1:],
    )


if __name__ == "__main__":
    main()
