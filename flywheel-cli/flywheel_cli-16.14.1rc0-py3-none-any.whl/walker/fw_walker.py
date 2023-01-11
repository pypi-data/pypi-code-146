"""Flywheel Walker"""

import json
import logging
import os
import tempfile

import fs

from .. import util
from ..sync.fw_threaded_src import FWThreadedSource, get_container_file_response
from .abstract_walker import AbstractWalker, FileInfo

log = logging.getLogger(__name__)

CHUNKSIZE = 8 << 20


class FWFileInfo(FileInfo):  # pylint: disable=too-few-public-methods
    """Extended FileInfo class for regular files."""

    def __init__(self, full_path, size, filename, container_id):
        super().__init__(name=full_path, is_dir=False, size=size)
        self.filename = filename
        self.container_id = container_id


class FWMetaFileInfo(FileInfo):  # pylint: disable=too-few-public-methods
    """Extended FileInfo class for files containing metainformation."""

    def __init__(self, full_path, size, content):
        super().__init__(name=full_path, is_dir=False, size=size)
        self.content = content


class FWWalker(AbstractWalker):
    """
    Flywheel Walker class

    It's only used by ingest, therefore, only the list_files and open methods are
    implemented.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        fs_url: str,
        api_key,
        ignore_dot_files=True,
        follow_symlinks=False,
        filter=None,  # pylint: disable=redefined-builtin
        exclude=None,
        filter_dirs=None,
        exclude_dirs=None,
    ):
        project_path = fs_url.replace("fw://", "")
        # Root will be the project path.
        super().__init__(project_path)
        self._fw_client = util.get_sdk_client(api_key)

        """
        NamedTemporaryFile on windows is problematic
        https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile
        """
        # pylint: disable=consider-using-with
        self._tmp_file = tempfile.NamedTemporaryFile(delete=False)

    def list_files(self, subdir=None):
        project = self._fw_client.lookup(util.parse_resolver_path(self.root))
        fw_src = FWThreadedSource(self._fw_client, project["_id"], metadata=True)
        for f in fw_src:
            if f.is_metadata:
                metadata_str = f.file.read().decode("utf-8")
                yield FWMetaFileInfo(
                    full_path=f.name,
                    size=f.size,
                    content=json.loads(metadata_str) if metadata_str else None,
                )
            else:
                yield FWFileInfo(
                    full_path=f.name,
                    size=f.size,
                    filename=f.filename,
                    container_id=f.container_id,
                )

    def _listdir(self, path):
        raise NotImplementedError()

    def get_fs_url(self):
        raise NotImplementedError()

    def open(self, path: str, mode="rb", **kwargs):
        container_id, filename = path.split("/")

        resp = get_container_file_response(self._fw_client, container_id, filename)
        # on windows one have to close the file before able to open it
        self._tmp_file.close()
        with open(self._tmp_file.name, "wb") as f:
            data = resp.raw.read(CHUNKSIZE)
            while data:
                f.write(data)
                data = resp.raw.read(CHUNKSIZE)
        try:
            # pylint: disable=consider-using-with, unspecified-encoding
            return open(self._tmp_file.name, mode, **kwargs)
        except fs.errors.ResourceNotFound as ex:
            raise FileNotFoundError(f"File '{path}' not found.") from ex

    def close(self):
        self._tmp_file.close()
        os.remove(self._tmp_file.name)
