import logging
import os
import socket
import time
from datetime import datetime
from typing import Optional

import requests
from croniter import croniter
from icloudpy import ICloudPyService
from icloudpy.exceptions import ICloudPyAPIResponseException
from icloudpy.services.photos import PhotoAsset
from requests.exceptions import ConnectionError  # pylint: disable=redefined-builtin

from icpd import constants


def wait_next(scheduler: croniter, logger: Optional[logging.Logger] = None) -> None:
    next_time: float = scheduler.get_next()
    sleep_sec: float = next_time - time.time()
    while sleep_sec <= 0:
        next_time = scheduler.get_next()
        sleep_sec = next_time - time.time()

    if logger:
        logger.info(
            "sleeping until %d (%d seconds)", round(next_time), round(sleep_sec)
        )

    remaining_sec: float = next_time - time.time()
    while remaining_sec > 0:
        time.sleep(3)
        remaining_sec = next_time - time.time()


def send_webhook(url: str, method: Optional[str], skip_verify: bool, data: str) -> None:
    verify: bool = not skip_verify
    if method and method.lower() == "get":
        resp = requests.get(url, verify=verify, timeout=10)
    else:
        resp = requests.post(
            url,
            verify=verify,
            json={
                "priority": 1,
                "title": "icpd cycle complete",
                "message": data,
            },
            timeout=10,
        )

    if not (200 <= resp.status_code < 400):
        raise Exception("error sending webhook; http error " + str(resp.status_code))


def download_media(
    icloud: ICloudPyService,
    logger: logging.Logger,
    photo: PhotoAsset,
    version: str,
    target_file: str,
) -> bool:
    """Download the photo to path, with retries and error handling"""

    download_dir: str = os.path.dirname(target_file)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir, exist_ok=True)

    for retries in range(constants.MAX_RETRIES):
        try:
            photo_response = photo.download(version)
            if photo_response:
                temp_download_path = target_file + ".part"
                with open(temp_download_path, "wb") as file_obj:
                    for chunk in photo_response.iter_content(chunk_size=1024):
                        if chunk:
                            file_obj.write(chunk)
                temp_file_size = os.path.getsize(temp_download_path)
                if photo.versions[version]["size"] != temp_file_size:
                    raise Exception(
                        f"source file size ({photo.size}) != destination file size"
                        f" ({temp_file_size})"
                    )
                os.rename(temp_download_path, target_file)
                return True

            logger.error(
                "Could not find URL to download %s for size %s!",
                photo.filename,
                version,
            )
            break

        except (ConnectionError, socket.timeout, ICloudPyAPIResponseException) as ex:
            if "Invalid global session" in str(ex):
                logger.debug("Session error, re-authenticating...")
                if retries > 0:
                    # If the first reauthentication attempt failed,
                    # start waiting a few seconds before retrying in case
                    # there are some issues with the Apple servers
                    time.sleep(constants.WAIT_SECONDS)

                icloud.authenticate()
            else:
                # you end up here when p.e. throttling by Apple happens
                wait_time = (retries + 1) * constants.WAIT_SECONDS
                logger.error(
                    "Error downloading %s, retrying after %d seconds...",
                    photo.filename,
                    wait_time,
                )
                time.sleep(wait_time)
    else:
        raise Exception(
            "Could not download %s! Please try again later." % photo.filename
        )

    return False


def build_target_path(
    username: str,
    file_name: str,
    date_created: datetime,
    parent_directory: str,
    folder_structure: Optional[str] = None,
) -> str:
    date_path: str = ""
    if folder_structure:
        date_path = (
            folder_structure.format(date_created)
            if folder_structure.startswith("{") and folder_structure.endswith("}")
            else folder_structure
        )

    username_safe = "".join(x for x in username if x.isalnum())

    download_dir = os.path.normpath(
        os.path.join(parent_directory, username_safe, date_path)
    )

    return os.path.join(download_dir, file_name)
