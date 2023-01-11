"""Zipwalker mixin and utils"""
import os
import shutil
import zipfile
from io import BytesIO, IOBase

import fs

from ..util import is_dicom_file


class ZipWalkerMixin:
    """Mixin class for local/S3 zip walker"""

    def list_files(self, subdir=None):
        for fileinfo in super().list_files(subdir):
            self._zip_meta[fileinfo.name] = [fileinfo.size, []]
            yield fileinfo

    def get_archive_members(self, path):
        """get members from archive"""
        o_path = fs.path.join(self.tmp_dir_path, path)
        with zipfile.ZipFile(super().open(path, "rb")) as z_file:
            z_file.extractall(o_path)

        for path_, _, files in os.walk(o_path):
            for name in files:
                yield os.path.relpath(fs.path.join(path_, name), self.tmp_dir_path)

    def open(self, path, mode="rb", **kwargs):  # pylint: disable=unused-argument
        """
        If the path ends with .zip the first DICOM is opened(ot the first file in case of extensionless files)
        Othervise the file should be an extracted file in the tmp_dir
        """
        try:
            if path.lower().endswith(".zip"):
                # zip file, get first dicom
                dicom_path = self._get_dicom_file_from_archive(path)
                # pylint: disable=consider-using-with, unspecified-encoding
                return open(dicom_path, mode, **kwargs)
            if os.path.exists(fs.path.join(self.tmp_dir_path, path)):
                # file in extracted zip
                # pylint: disable=consider-using-with, unspecified-encoding
                return open(fs.path.join(self.tmp_dir_path, path), mode, **kwargs)

            raise FileNotFoundError(f"File {path} not found")
        except fs.errors.ResourceNotFound as exc:
            raise FileNotFoundError(f"File {path} not found") from exc

    def close(self):
        super().close()
        if self.tmp_dir_path is not None:
            shutil.rmtree(self.tmp_dir_path)
            self.tmp_dir_path = None

    def _read_chunk(self, path, offset, size=None):
        """read chunk"""
        raise NotImplementedError()

    def _get_dicom_file_from_archive(self, path):
        """get DICOM from archive without downloading the full archive"""
        key = path
        if not key in self._zip_meta:
            key = fs.path.basename(path)
            if not key in self._zip_meta:
                raise ValueError(f"{path} not found in zip meta")

        size = self._zip_meta[key][0]
        file_like = ChunkedBytesIO(size)

        # last 512k
        start_byte = max(size - 512 * 1024, 0)
        content = self._read_chunk(path, start_byte)

        file_like.add_chunk(content, size - len(content))
        filelist = None

        with zipfile.ZipFile(file_like) as z_file:
            filelist = z_file.infolist()

        member = None
        # try to find a file with DICOM extension
        for file in filelist:
            if not file.is_dir() and is_dicom_file(file.filename):
                member = file
                break
        # if no dicom found fallback to first file
        if not member:
            for file in filelist:
                if not file.is_dir():
                    member = file
                    break

        if not member:
            return None

        offset = max(member.header_offset - 1024, 0)
        size = min(member.compress_size + 2048, size)

        content = self._read_chunk(key, offset, size)
        file_like.add_chunk(content, offset)
        o_path = fs.path.join(self.tmp_dir_path, key)
        with zipfile.ZipFile(file_like) as z_file:
            z_file.extract(member, o_path)

        return fs.path.join(self.tmp_dir_path, key, member.filename)


class ChunkedBytesIO(IOBase):
    """ChunkedBytesIO only tell, seek, read"""

    def __init__(self, length):
        super().__init__()
        self._length = length
        self._real_pos = 0
        self._chunks = []

    def add_chunk(self, initial_bytes, offset):
        """add chunk"""
        self._chunks.append(
            [offset, offset + len(initial_bytes), BytesIO(initial_bytes)]
        )

    def seek(self, pos, whence=0):
        """seek"""
        try:
            pos_index = pos.__index__
        except AttributeError as ex:
            raise TypeError(f"{pos!r} is not an integer") from ex
        else:
            pos = pos_index()
        if whence == 0:
            # absolute
            if pos < 0:
                raise ValueError(f"negative seek position {pos}")
            self._real_pos = pos
        elif whence == 1:
            # relative to the current position
            self._real_pos = max(0, self._real_pos + pos)
        elif whence == 2:
            # relative to the file's end.
            self._real_pos = max(0, self._length + pos)
        else:
            raise ValueError("unsupported whence value")

        valid_chunk = None
        for chunk in self._chunks:
            if self._real_pos >= chunk[0] and self._real_pos <= chunk[1]:
                valid_chunk = chunk
                break

        if not valid_chunk:
            raise ValueError(f"no valid chunk found for seek {pos}, {whence}")

        valid_chunk[2].seek(self._real_pos - valid_chunk[0], 0)
        return self._real_pos

    def tell(self):
        """tell"""
        return self._real_pos

    def read(self, size=-1):
        """read"""
        valid_chunk = None
        for chunk in self._chunks:
            if self._real_pos >= chunk[0] and self._real_pos <= chunk[1]:
                valid_chunk = chunk
                break
        if not valid_chunk:
            raise ValueError("no valid chunk found")

        r_bytes = valid_chunk[2].read(size)
        self._real_pos = min(self._length, self._real_pos + size)
        return r_bytes
