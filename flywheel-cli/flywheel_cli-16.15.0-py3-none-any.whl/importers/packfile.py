"""Provides functions for creating packfiles"""
import logging

import fs
import fs.copy
import fs.path
from fs.zipfs import ZipFS

from .. import util

log = logging.getLogger(__name__)


class PackfileDescriptor:
    # pylint: disable=too-few-public-methods
    """PackfileDescriptor class"""

    def __init__(self, packfile_type, path, count, name=None):
        """Descriptor object for creating a packfile"""
        self.packfile_type = packfile_type
        self.path = path
        self.count = count
        # property fields
        self._name = util.sanitize_filename(name)

    @property
    def name(self):
        """Name getter"""
        return self._name

    @name.setter
    def name(self, val):
        """Name setter that sanitize the value"""
        self._name = util.sanitize_filename(val)


def create_zip_packfile(dst_file, walker, packfile_type, compression=None, **kwargs):
    """Create a zipped packfile for the given packfile_type and options, that writes a ZipFile to dst_file

    Arguments:
        dst_file (file): The destination path or file object
        walker (AbstractWalker): The source walker instance
        packfile_type (str): The packfile type, or None
        subdir (str): The optional packfile subdirectory
        paths (list(str)): The list of paths to add to the packfile
        progress_callback (function): Function to call with byte totals
        deid_profile: The de-identification profile to use
    """
    if compression is None:
        import zipfile  # pylint: disable=import-outside-toplevel

        compression = zipfile.ZIP_DEFLATED

    with ZipFS(dst_file, write=True, compression=compression) as dst_fs:
        zip_member_count, deid_log = create_packfile(
            walker, dst_fs, packfile_type, **kwargs
        )

    return zip_member_count, deid_log


def create_packfile(  # pylint: disable=too-many-arguments, too-many-branches
    walker,
    dst_fs,
    packfile_type,
    subdir=None,
    paths=None,
    progress_callback=None,
    deid_profile=None,
    flatten=False,
    create_deid_log=False,
):
    """Create a packfile by copying files from walker to dst_fs, possibly validating and/or de-identifying

    Arguments:
        walker (AbstractWalker): The source walker instance
        write_fn (function): Write function that takes path and bytes to write
        progress_callback (function): Function to call with byte totals
        deid_profile: The de-identification profile to use
        create_deid_log: Create deid log payload or not
    """
    progress = {"total_bytes": 0}

    # Report progress as total_bytes
    if callable(progress_callback):

        def progress_fn(dst_fs, path):
            progress["total_bytes"] += dst_fs.getsize(path)
            progress_callback(progress["total_bytes"])

    else:
        progress_fn = None

    if not paths:
        # Determine file paths
        paths = []
        for root, _, files in walker.walk(subdir=subdir):
            for file_info in files:
                paths.append(walker.combine(root, file_info.name))
    # Attempt to de-identify using deid_profile first
    if deid_profile.name != "none":
        deid_log_payload = None
        if create_deid_log:
            deid_logger = get_deid_payload_logger(deid_profile)
        if deid_profile.process_packfile(
            packfile_type, walker, dst_fs, paths, callback=progress_fn
        ):
            if create_deid_log:
                deid_log_payload = deid_logger.logs.get(paths[0])
            return len(paths), deid_log_payload  # Handled by de-id

    # Otherwise, just copy files into place
    for path in paths:
        # Ensure folder exists
        target_path = path
        if subdir:
            target_path = walker.remove_prefix(subdir, path)
        if flatten:
            target_path = fs.path.basename(path)
        folder = fs.path.dirname(target_path)
        dst_fs.makedirs(folder, recreate=True)
        with walker.open(path, "rb") as src_file:
            dst_fs.upload(target_path, src_file)
        if callable(progress_fn):
            progress_fn(dst_fs, target_path)
    return len(paths), None


def get_deid_payload_logger(deid_profile):
    """Get the deid logger, or add one if not yet added"""

    # pylint: disable=import-outside-toplevel
    from ..ingest.deid import DeidLogPayloadLogger

    def get_logger(deid_profile):
        for file_profile in deid_profile.file_profiles:
            if file_profile.log:
                for logger in file_profile.log:
                    if isinstance(logger, DeidLogPayloadLogger):
                        return logger
        return None

    deid_logger = get_logger(deid_profile)
    if not deid_logger:
        deid_logger = DeidLogPayloadLogger()

        for file_profile in deid_profile.file_profiles:
            loggers = file_profile.log
            if not loggers:
                loggers = []
            elif not isinstance(loggers, list):
                loggers = [loggers]

            loggers.append(deid_logger)
            file_profile.set_log(loggers)

    return deid_logger
