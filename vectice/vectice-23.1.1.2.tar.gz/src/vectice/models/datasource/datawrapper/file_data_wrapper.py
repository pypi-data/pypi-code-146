from __future__ import annotations

import datetime
import glob
import hashlib
import logging
import os

from vectice.models.datasource.datawrapper.data_wrapper import DataWrapper
from vectice.models.datasource.datawrapper.metadata import DatasetSourceUsage, File, FilesMetadata, SourceOrigin

_logger = logging.getLogger(__name__)


class FileDataWrapper(DataWrapper):
    """Wrap columnar data and its metadata in a local file.

    Implements :py:class:`DataWrapper`.

    """

    def __init__(
        self,
        path: str,
        name: str,
        usage: DatasetSourceUsage | None = None,
        inputs: list[int] | None = None,
        capture_code: bool = True,
    ):
        """
        :param usage: The usage of the dataset
        :param name: The name of the :py:class:`DataWrapper`
        :param inputs: The list of dataset ids to create a new dataset from
        :param capture_code: Automatically capture active commit in .git folder
        """
        self.path = path
        super(FileDataWrapper, self).__init__(name, usage, inputs, capture_code)
        _logger.info(f"File: {path} wrapped successfully.")

    def _fetch_data(self) -> dict[str, bytes]:
        datas = {}
        for file in self.metadata.files:
            with open(file.name, "rb") as opened_file:
                datas[file.name] = opened_file.read()
        return datas

    def _build_metadata(self, path: str | None = None) -> FilesMetadata:
        if self.path is None:
            raise ValueError("Path can not be None.")
        files, total_size = self._file_visitor_list_builder(self.path, [])
        files_count = len(files)
        metadata = FilesMetadata(
            size=total_size, origin=SourceOrigin.OTHER, files_count=files_count, files=files, usage=self.usage
        )
        return metadata

    def _file_visitor_list_builder(self, path: str, files: list[File]) -> tuple[list[File], int]:
        total_size = 0
        if not os.path.exists(path):
            raise FileNotFoundError
        if os.path.isfile(path):
            file: File = self._build_file_from_path(path)
            total_size += file.size
            files.append(file)
        else:
            for entry_path in glob.glob(f"{path}/**", recursive=True):
                if os.path.isfile(entry_path):
                    glob_file: File = self._build_file_from_path(entry_path)
                    total_size += glob_file.size
                    files.append(glob_file)
        return files, total_size

    def _build_file_from_path(self, path: str) -> File:
        entry_stats: os.stat_result = os.stat(path)
        name = path.split("\\")[-1]
        return File(
            name=name,
            size=entry_stats.st_size,
            fingerprint=self._compute_digest_for_path(path),
            updated_date=self._convert_date_to_iso(entry_stats.st_mtime),
            created_date=self._convert_date_to_iso(self._get_created_date(entry_stats)),
            uri=f"file://{os.path.abspath(path)}",
        )

    @staticmethod
    def _get_created_date(entry_stats: os.stat_result) -> float:
        try:
            return float(entry_stats.st_birthtime)  # type: ignore[attr-defined]
        except AttributeError:
            return entry_stats.st_ctime

    @staticmethod
    def _compute_digest_for_path(path: str) -> str:
        sha = hashlib.sha256()
        bytes_array = bytearray(128 * 1024)
        mv = memoryview(bytes_array)
        with open(path, "rb", buffering=0) as file:
            n = file.readinto(mv)
            while n:
                sha.update(mv[:n])
                n = file.readinto(mv)
        return sha.hexdigest()

    @staticmethod
    def _convert_date_to_iso(timestamp: float) -> str:
        return datetime.datetime.fromtimestamp(timestamp).isoformat()
