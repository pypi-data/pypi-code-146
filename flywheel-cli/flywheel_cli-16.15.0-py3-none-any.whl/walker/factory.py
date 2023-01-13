"""Factory functions to create a file walker"""
from urllib.parse import urlparse

from .. import util
from .azure_walker import AzureWalker
from .fw_walker import FWWalker
from .gcs_walker import GCSWalker
from .pyfs_walker import PyFsWalker
from .pyfs_zip_walker import PyFsZipWalker
from .s3_walker import S3Walker
from .s3_zip_walker import S3ZipWalker


def create_walker(
    fs_url,
    ignore_dot_files=True,
    follow_symlinks=False,
    include=None,
    exclude=None,
    include_dirs=None,
    exclude_dirs=None,
    fw_walker_api_key=None,
    zip_walker=False,
):  # pylint: disable=redefined-builtin, too-many-arguments
    """Create a walker from a filesystem url

    Args:
        fs_url (str): The filesystem url
        ignore_dot_files (bool): Whether or not to ignore files starting with '.'
        follow_symlinks(bool): Whether or not to follow symlinks
        include (list): An optional list of filename patterns to INCLUDE
        exclude (list): An optional list of filename patterns to EXCLUDE
        include_dirs (list): An optional list of directories to INCLUDE
        exclude_dirs (list): An optional list of patterns of directories to EXCLUDE

    Returns:
        AbstractWalker: fs_url opened as a walker
    """

    scheme, *_ = urlparse(fs_url)

    if scheme == "fw":
        return FWWalker(
            fs_url,
            fw_walker_api_key,
            ignore_dot_files=ignore_dot_files,
            follow_symlinks=follow_symlinks,
            filter=include,
            exclude=exclude,
            filter_dirs=include_dirs,
            exclude_dirs=exclude_dirs,
        )

    if zip_walker:
        if scheme == "s3":
            cls = S3ZipWalker
        else:
            cls = PyFsZipWalker
    else:
        if scheme == "s3":
            cls = S3Walker
        elif scheme == "gs":
            cls = GCSWalker
        elif scheme == "az":
            cls = AzureWalker
        else:
            cls = PyFsWalker

    return cls(
        fs_url,
        ignore_dot_files=ignore_dot_files,
        follow_symlinks=follow_symlinks,
        filter=include,
        exclude=exclude,
        filter_dirs=include_dirs,
        exclude_dirs=exclude_dirs,
    )


def create_archive_walker(walker, path):
    """Open the given path as a walker

    Arguments:
        walker (AbstractWalker): The source walker instance
        path (str): The path to the file to open

    Returns:
        AbstractWalker: Path opened as a sub walker
    """
    archive_fs = None

    if util.is_tar_file(path):
        import fs.tarfs  # pylint: disable=import-outside-toplevel

        archive_fs = fs.tarfs.TarFS(walker.open(path, "rb"))
    if util.is_zip_file(path):
        import fs.zipfs  # pylint: disable=import-outside-toplevel

        archive_fs = fs.zipfs.ZipFS(walker.open(path, "rb"))

    if archive_fs:
        return PyFsWalker(path, src_fs=archive_fs)
    return None
