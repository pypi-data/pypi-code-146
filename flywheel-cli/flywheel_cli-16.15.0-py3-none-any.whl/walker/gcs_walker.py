"""Google Storage Walker Module"""
import os
import shutil
import tempfile
from urllib.parse import urlparse

import fs
from google.cloud import storage

from .abstract_walker import AbstractWalker, FileInfo

TMP_CACHE: bool = os.getenv("FLYWHEEL_CLI_GCS_TMP_CACHE", "true").lower() == "true"


class GCSWalker(AbstractWalker):
    """Walker that is implemented in terms of GCS
    By default, use '/' for GCS list objects path delimiter"""

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
        _, bucket, path, *_ = urlparse(fs_url)

        super().__init__(
            "/",
            ignore_dot_files=ignore_dot_files,
            follow_symlinks=follow_symlinks,
            filter=filter,
            exclude=exclude,
            filter_dirs=filter_dirs,
            exclude_dirs=exclude_dirs,
        )
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(bucket)
        self.fs_url = fs_url
        self.prefix = "" if path == "/" else path.strip("/") + "/"
        self.tmp_dir_path = tempfile.mkdtemp()
        self.separator = "/"
        self.prev_opened = None
        self.tmp_cache = TMP_CACHE

    def get_fs_url(self):
        return self.fs_url

    def close(self):
        if self.tmp_dir_path is not None:
            shutil.rmtree(self.tmp_dir_path)
            self.tmp_dir_path = None

    def open(self, path, mode="rb", **kwargs):
        file_path = os.path.join(
            self.tmp_dir_path, self.prefix.lstrip("/"), path.lstrip("/")
        )

        if not self.tmp_cache and self.prev_opened and self.prev_opened != file_path:
            os.remove(self.prev_opened)

        self.prev_opened = file_path

        if not os.path.isfile(file_path):
            file_dir = fs.path.dirname(file_path)
            os.makedirs(file_dir, exist_ok=True)

            object_name = os.path.join(self.prefix.lstrip("/"), path.lstrip("/"))
            blob = self.bucket.get_blob(object_name)
            if blob is None:
                raise FileNotFoundError(f"File {path} not found")
            blob.download_to_filename(file_path)

        try:
            # pylint: disable=consider-using-with, unspecified-encoding
            return open(file_path, mode, **kwargs)
        except fs.errors.ResourceNotFound as exc:
            self.prev_opened = None
            raise FileNotFoundError(f"File {path} not found") from exc

    def _listdir(self, path):
        if path in ("/", ""):
            prefix_path = ""
        else:
            prefix_path = path.lstrip("/").rstrip("/") + "/"
        prefix_path = os.path.join(self.prefix, prefix_path)

        blobs = self.client.list_blobs(self.bucket, prefix=prefix_path, delimiter="/")
        for prefix in blobs.prefixes:
            dir_name = prefix if prefix_path == "" else prefix.split(prefix_path)[1]
            yield FileInfo(dir_name, True)

        for blob in blobs:
            file_name = (
                blob.name if prefix_path == "" else blob.name.split(prefix_path)[1]
            )
            yield FileInfo(file_name, False, modified=blob.time_created, size=blob.size)

    def _list_files(self, subdir):
        """List files using blob paginator"""
        if subdir in ("/", ""):
            sub_prefix = ""
        else:
            sub_prefix = subdir.strip("/") + "/"

        full_prefix = os.path.join(self.prefix, sub_prefix)
        for prefix in self._get_filtering_prefixes(sub_prefix):
            for blob in self.client.list_blobs(
                self.bucket, prefix=prefix, delimiter=None
            ):
                relpath = (
                    blob.name if full_prefix == "" else blob.name.split(full_prefix)[1]
                )
                dirpath = fs.path.combine(sub_prefix, fs.path.dirname(relpath))
                if not self._include_dir(dirpath):
                    continue
                fileinfo = FileInfo(
                    relpath, False, modified=blob.time_created, size=blob.size
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
                    prefixes.append(os.path.join(self.prefix, pattern_prefix))
                elif subdir_prefix.startswith(pattern_prefix):
                    prefixes.append(os.path.join(self.prefix, subdir_prefix))

        else:
            prefixes.append(os.path.join(self.prefix, subdir_prefix))
        return prefixes

    def _include_dir(self, dirpath):
        """Check if the given directory should be included"""
        for part in dirpath.split(self.separator):
            if self._ignore_dot_files and part.startswith("."):
                return False

            if self._exclude_dirs is not None and self.match(self._exclude_dirs, part):
                return False

        return True
