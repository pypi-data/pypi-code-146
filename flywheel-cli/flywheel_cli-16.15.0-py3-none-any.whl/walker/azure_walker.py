"""Azure Storage Walker Module"""
import logging
import os

import fs
from fw_storage import get_storage
from fw_storage.errors import FileNotFound

from .abstract_walker import AbstractWalker, FileInfo

logging.getLogger("azure").setLevel(logging.getLogger().level)


class AzureWalker(AbstractWalker):
    """Walker that is implemented in terms of Azure
    The path delimiter is always '/'."""

    def __init__(
        self,
        fs_url,
        ignore_dot_files=True,
        follow_symlinks=False,
        filter=None,  # pylint: disable=redefined-builtin
        exclude=None,
        filter_dirs=None,
        exclude_dirs=None,
    ):
        """Initialize the abstract walker

        Args:
            fs_url (str): The starting directory for walking
            ignore_dot_files (bool): Whether or not to ignore files starting with '.'
            follow_symlinks(bool): Whether or not to follow symlinks
            filter (list): An optional list of filename patterns to INCLUDE
            exclude (list): An optional list of filename patterns to EXCLUDE
            filter_dirs (list): An optional list of directories to INCLUDE
            exclude_dirs (list): An optional list of patterns of directories to EXCLUDE
        """
        super().__init__(
            "/",
            ignore_dot_files=ignore_dot_files,
            follow_symlinks=follow_symlinks,
            filter=filter,
            exclude=exclude,
            filter_dirs=filter_dirs,
            exclude_dirs=exclude_dirs,
        )

        self.client = get_storage(fs_url)
        self.fs_url = fs_url
        self.separator = "/"
        self.prev_opened = None

    def get_fs_url(self):
        return self.fs_url

    def close(self):
        self.client.cleanup()

    def open(self, path, mode="rb", **kwargs):
        if mode != "rb":
            raise ValueError(f"Invalid file mode: {mode} (expected rb)")

        path = path.lstrip("/")
        try:
            return self.client.get(path, "rb")
        except FileNotFound as exc:
            print(type(exc))
            raise FileNotFoundError(f"File {path} not found") from exc

    def _listdir(self, path):
        raise NotImplementedError()

    def _list_files(self, subdir):
        """List files using blob paginator"""
        if subdir in ("/", ""):
            sub_prefix = ""
        else:
            sub_prefix = subdir.strip("/") + "/"

        for prefix in self._get_filtering_prefixes(sub_prefix):
            for blob in self.client.ls(prefix):
                relpath = self.client.abspath(blob.path)
                dirpath = fs.path.combine(sub_prefix, fs.path.dirname(relpath))
                if not self._include_dir(dirpath):
                    continue
                fileinfo = FileInfo(
                    blob.path, False, modified=blob.modified, size=blob.size
                )
                if self._should_include_file(fileinfo):
                    yield fileinfo

    def _get_filtering_prefixes(self, subdir_prefix):
        prefixes = []
        if self._include_dirs:
            for pattern in self._include_dirs:
                pattern_prefix = os.path.join(*pattern).strip("/")
                # only include pattern prefixes which start with subdir_prefix
                if pattern_prefix.startswith(subdir_prefix):
                    prefixes.append(pattern_prefix)
                elif subdir_prefix.startswith(pattern_prefix):
                    prefixes.append(subdir_prefix)

        else:
            prefixes.append(subdir_prefix)
        return prefixes

    def _include_dir(self, dirpath):
        """Check if the given directory should be included"""
        for part in dirpath.split(self.separator):
            if self._ignore_dot_files and part.startswith("."):
                return False

            if self._exclude_dirs is not None and self.match(self._exclude_dirs, part):
                return False

        return True
