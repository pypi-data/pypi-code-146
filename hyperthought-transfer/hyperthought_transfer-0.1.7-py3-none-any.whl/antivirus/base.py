"""
antivirus/base.py

Abstract base class for AntiVirus Scanners.
"""

import abc
import collections
import os


class _NotAvailable:
    pass


class NotAvailableException(Exception):
    pass


class BaseAntivirus(abc.ABC):
    """
    Abstract base class for an AntiVirus scanner.

    The interface consists of an abstract method, scan, which will scan all
    paths provided to the constructor; paths and report_location properties
    which will store the same information passed to the constructor; and
    bad_files, paths to files in which malware was detected.

    Parameters
    ----------
    paths : list of str
        List of full paths to files/folders that need to be scanned.
    report_location : str
        A path to a directory where reports should be stored.
    """

    def __init__(self, paths, report_location):
        for path in paths:
            if not os.path.isfile(path) and not os.path.isdir(path):
                raise ValueError(f"{path} is not a valid path")

        if not os.path.isdir(report_location):
            raise ValueError(f"{report_location} is not a valid directory")

        self._report_location = report_location
        self._paths = [os.path.abspath(path) for path in paths]
        self._bad_files = _NotAvailable()

    @property
    def report_location(self):
        """Get the location for reports relating to the job/manifest."""
        return self._report_location

    @property
    def paths(self):
        """List all files in the manifest."""
        return self._paths

    @property
    def bad_files(self):
        if isinstance(self._bad_files, _NotAvailable):
            raise NotAvailableException("No antivirus scanning has been done.")

        return list(self._bad_files)

    @bad_files.setter
    def bad_files(self, value):
        if (
            not isinstance(value, collections.abc.Sequence)
            or
            isinstance(value, str)
        ):
            raise ValueError("bad_files must be a sequence")

        for bad_file in value:
            if not os.path.isfile(bad_file):
                raise ValueError(f"{bad_file} is not a file")

        self._bad_files = [os.path.abspath(file_) for file_ in value]

    @abc.abstractmethod
    def scan(self):
        pass
