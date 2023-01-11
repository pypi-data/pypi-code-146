"""File-system zip walker class"""
import tempfile

from .pyfs_walker import PyFsWalker
from .zip_walker_mixin import ZipWalkerMixin


class PyFsZipWalker(ZipWalkerMixin, PyFsWalker):
    """Walker that is implemented in terms of PyF and can extract files from zips"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._zip_meta = {}
        self.tmp_dir_path = tempfile.mkdtemp()

    def _read_chunk(self, path, offset, size=None):
        """read chunk"""
        f_bytes = bytearray()
        with self.src_fs.open(path, "rb") as file:
            file.seek(offset)
            while True:
                if size:
                    remaining_size = size - len(f_bytes)
                    read_size = min(remaining_size, 16384)
                else:
                    read_size = 16384

                chunk = file.read(read_size)
                if not chunk:
                    break
                f_bytes += bytearray(chunk)
                if size and len(f_bytes) >= size:
                    break

        return f_bytes
