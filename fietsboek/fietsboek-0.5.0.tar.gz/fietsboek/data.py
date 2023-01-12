"""Data manager for fietsboek.

Data are objects that belong to a track (such as images), but are not stored in
the database itself. This module makes access to such data objects easier.
"""
import datetime
import logging
import random
import shutil
import string
import uuid
from pathlib import Path
from typing import BinaryIO, List, Optional

import brotli
import gpxpy
from filelock import FileLock

from .util import secure_filename

LOGGER = logging.getLogger(__name__)


def generate_filename(filename: Optional[str]) -> str:
    """Generates a safe-to-use filename for uploads.

    If possible, tries to keep parts of the original filename intact, such as
    the extension.

    :param filename: The original filename.
    :return: The generated filename.
    """
    if filename:
        good_name = secure_filename(filename)
        if good_name:
            random_prefix = "".join(random.choice(string.ascii_lowercase) for _ in range(5))
            return f"{random_prefix}_{good_name}"

    return str(uuid.uuid4())


class DataManager:
    """Data manager.

    The data manager is usually provided as ``request.data_manager`` and can be
    used to access track's images and other on-disk data.

    :ivar data_dir: Path to the data folder.
    """

    def __init__(self, data_dir: Path):
        self.data_dir: Path = data_dir

    def _track_data_dir(self, track_id):
        return self.data_dir / "tracks" / str(track_id)

    def initialize(self, track_id: int) -> "TrackDataDir":
        """Creates the data directory for a track.

        :raises FileExistsError: If the directory already exists.
        :param track_id: ID of the track.
        :return: The manager that can be used to manage this track's data.
        """
        path = self._track_data_dir(track_id)
        path.mkdir(parents=True)
        return TrackDataDir(track_id, path)

    def purge(self, track_id: int):
        """Forcefully purges all data from the given track.

        This function logs errors but raises no exception, as such it can
        always be used to clean up after a track.
        """
        TrackDataDir(track_id, self._track_data_dir(track_id)).purge()

    def open(self, track_id: int) -> "TrackDataDir":
        """Opens a track's data directory.

        :raises FileNotFoundError: If the track directory does not exist.
        :param track_id: ID of the track.
        :return: The manager that can be used to manage this track's data.
        """
        path = self._track_data_dir(track_id)
        if not path.is_dir():
            raise FileNotFoundError(f"The path {path} is not a directory") from None
        return TrackDataDir(track_id, path)


class TrackDataDir:
    """Manager for a single track's data."""

    def __init__(self, track_id: int, path: Path):
        self.track_id: int = track_id
        self.path: Path = path

    def lock(self) -> FileLock:
        """Returns a FileLock that can be used to lock access to the track's
        data.

        :return: The lock responsible for locking this data directory.
        """
        return FileLock(self.path / "lock")

    def purge(self):
        """Purge all data pertaining to the track.

        This function logs errors but raises no exception, as such it can
        always be used to clean up after a track.
        """

        def log_error(_, path, exc_info):
            LOGGER.warning("Failed to remove %s", path, exc_info=exc_info)

        if self.path.is_dir():
            shutil.rmtree(self.path, ignore_errors=False, onerror=log_error)

    def gpx_path(self) -> Path:
        """Returns the path of the GPX file.

        This file contains the (brotli) compressed GPX data.

        :return: The path where the GPX is supposed to be.
        """
        return self.path / "track.gpx.br"

    def compress_gpx(self, data: bytes, quality: int = 4):
        """Set the GPX content to the compressed form of data.

        If you want to write compressed data directly, use :meth:`gpx_path` to
        get the path of the GPX file.

        :param data: The GPX data (uncompressed).
        :param quality: Compression quality, from 0 to 11 - 11 is highest
            quality but slowest compression speed.
        """
        compressed = brotli.compress(data, quality=quality)
        self.gpx_path().write_bytes(compressed)

    def decompress_gpx(self) -> bytes:
        """Returns the GPX bytes decompressed.

        :return: The saved GPX file, decompressed.
        """
        return brotli.decompress(self.gpx_path().read_bytes())

    def engrave_metadata(
        self, title: str, description: str, author_name: str, time: datetime.datetime
    ):
        """Engrave the given metadata into the GPX file.

        Note that this will erase all existing metadata in the given fields.

        :param title: The title of the track.
        :param description: The description of the track.
        :param creator: Name of the track's creator.
        :param time: Time of the track.
        """
        gpx = gpxpy.parse(self.decompress_gpx())
        # First we delete the existing metadata
        for track in gpx.tracks:
            track.name = None
            track.description = None

        # Now we add the new metadata
        gpx.author_name = author_name
        gpx.name = title
        gpx.description = description
        gpx.time = time

        self.compress_gpx(gpx.to_xml().encode("utf-8"))

    def backup(self):
        """Create a backup of the GPX file."""
        shutil.copy(self.gpx_path(), self.backup_path())

    def backup_path(self) -> Path:
        """Path of the GPX backup file.

        :return: The path of the backup file.
        """
        return self.path / "track.bck.gpx.br"

    def images(self) -> List[str]:
        """Returns a list of images that belong to the track.

        :param track_id: Numerical ID of the track.
        :return: A list of image IDs.
        """
        image_dir = self.path / "images"
        if not image_dir.exists():
            return []
        images = [image.name for image in image_dir.iterdir()]
        return images

    def image_path(self, image_id: str) -> Path:
        """Returns a path to a saved image.

        :raises FileNotFoundError: If the given image could not be found.
        :param image_id: ID of the image.
        :return: A path pointing to the requested image.
        """
        image = self.path / "images" / secure_filename(image_id)
        if not image.exists():
            raise FileNotFoundError("The requested image does not exist")
        return image

    def add_image(self, image: BinaryIO, filename: Optional[str] = None) -> str:
        """Saves an image to a track.

        :param image: The image, as a file-like object to read from.
        :param filename: The image's original filename.
        :return: The ID of the saved image.
        """
        image_dir = self.path / "images"
        image_dir.mkdir(parents=True, exist_ok=True)

        filename = generate_filename(filename)
        path = image_dir / filename
        with open(path, "wb") as fobj:
            shutil.copyfileobj(image, fobj)

        return filename

    def delete_image(self, image_id: str):
        """Deletes an image from a track.

        :raises FileNotFoundError: If the given image could not be found.
        :param image_id: ID of the image.
        """
        # Be sure to not delete anything else than the image file
        image_id = secure_filename(image_id)
        if "/" in image_id or "\\" in image_id:
            return
        path = self.image_path(image_id)
        path.unlink()
