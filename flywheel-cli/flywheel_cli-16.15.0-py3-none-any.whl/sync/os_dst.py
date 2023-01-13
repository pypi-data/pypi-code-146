"""OS destination module for syncing files to a directory"""
import io
import os

CHUNKSIZE = 8 << 20  # 8 MB


class OSDestination:
    """Filesystem directory sync destination"""

    def __init__(self, dirpath):
        self.dirpath = dirpath

    def __iter__(self):
        """Yield `OSFile`s for files found walking the destination dir"""
        for dirpath, _, filenames in os.walk(self.dirpath):
            for filepath in (f"{dirpath}/{filename}" for filename in filenames):
                yield self.file(os.path.relpath(filepath, self.dirpath))

    def check_perms(self):
        """Create/stat/delete a permcheck file - raise `PermissionError` on error"""
        try:
            file = self.file("permcheck")
            file.store(io.BytesIO(b"permcheck"))  # (dir creation and) file write perms
            file.stat()  # os.stat
            file.delete()  # os.remove
            os.listdir(self.dirpath)  # dir listing
        except PermissionError as exc:
            raise PermissionError(f"Destination perm-check failed ({exc})") from exc

    def file(self, relpath):
        """Return an `OSFile` for a given path relative to the destination dir"""
        return OSFile(self, relpath)

    def cleanup(self):
        """Remove any empty dirs within the destination dir recursively"""
        for dirpath, dirnames, filenames in os.walk(self.dirpath):
            if not dirnames and not filenames:
                os.rmdir(dirpath)


class OSFile:
    """Filesystem file sync target"""

    __slots__ = ("name", "size", "modified", "filepath")

    def __init__(self, osdst, relpath):
        self.name = relpath
        self.filepath = f"{osdst.dirpath}/{relpath}"

    def stat(self):
        """Set self.size and modified via os.stat - return bool(file exists)"""
        try:
            stat = os.stat(self.filepath)
        except FileNotFoundError:
            return False
        self.size, self.modified = (  # pylint: disable=attribute-defined-outside-init
            stat.st_size,
            stat.st_mtime,
        )
        return True

    def store(self, src_file):
        """Write file with content read from `src_file`"""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "wb") as dst:
            data = src_file.read(CHUNKSIZE)
            while data:
                dst.write(data)
                data = src_file.read(CHUNKSIZE)

    def delete(self):
        """Delete file"""
        os.remove(self.filepath)
