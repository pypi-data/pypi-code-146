"""
McAfee Antivirus scanner.  Uses the McAfee command line client.
"""

import os
import subprocess

from .base import BaseAntivirus


class McAfee(BaseAntivirus):
    """
    McAfee Antivirus scanner.  Uses the McAfee command line client, called
    from a subprocess.

    Parameters
    ----------
    n_threads : int
        The number of threads to be used by McAfee for virus scanning.

    See base class for specification of other constructor parameters.
    """

    def __init__(self, n_threads=10, *args, **kwargs):
        if not isinstance(n_threads, int):
            raise ValueError("n_threads must be an integer")

        super().__init__(*args, **kwargs)
        self._n_threads = n_threads

    def scan(self):
        """Use McAfee CLI AV scanner to scan all paths."""
        # Create a directory for McAfee-related input files and reports.
        mcafee = os.path.join(self.report_location, "McAfee")

        if not os.path.exists(mcafee):
            os.makedirs(mcafee)

        # Get file list and store in checklist file.
        checklist = os.path.abspath(os.path.join(mcafee, "checklist.txt"))

        def ensure_newline(str):
            """Make sure a string ends with a newline."""
            if not str.endswith("\n"):
                return str + "\n"
            else:
                return str

        lines = [ensure_newline(path) for path in self.paths]

        with open(checklist, "w") as file_handle:
            file_handle.writelines(lines)

        # Specify badlist.  This is where paths to bad files will be appended
        # by McAfee.
        badlist = os.path.abspath(os.path.join(mcafee, "badlist.txt"))

        # Specify the path to the full McAfee report.
        report = os.path.abspath(os.path.join(mcafee, "report.xml"))

        # Invoke McAfee CLI.
        parameters = [
            "SCAN",
            "/ALL",
            "/SECURE",
            "/ALLOLE",
            "/STREAMS",
            "/DOHSM",
            "/MIME",
            "/NOBREAK",
            "/NOMEM",
            "/NOEXPIRE",
            "/RECURSIVE",
            "/SUB",
            "/SHOWCOMP",
            "/SHOWENCRYPTED",
            "/RPTOBJECTS",
            "/BADLIST",
            badlist,
            "/APPENDBAD",
            f"/XMLPATH={report}",
            "/RPTALL",
            "/CHECKLIST",
            checklist,
            "/THREADS",
            str(self._n_threads),
            "/SILENT",
        ]
        process = subprocess.Popen(parameters, shell=True)
        process.wait()

        # Set self._bad_files based on files in badlist.
        if not os.path.exists(badlist):
            self.bad_files = []
        else:
            with open(badlist, "r") as file_handle:
                self.bad_files = file_handle.readlines()
