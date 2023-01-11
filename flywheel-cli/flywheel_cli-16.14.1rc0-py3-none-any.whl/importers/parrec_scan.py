"""Provides a scanner for PAR/REC files"""
import copy
import fnmatch
import logging
import sys

import fs
from flywheel_migration import parse_par_header, parse_par_timestamp

from .. import util
from .abstract_importer import AbstractImporter
from .abstract_scanner import AbstractScanner
from .packfile import PackfileDescriptor

log = logging.getLogger(__name__)


class ParRecSession:
    """PAR/REC session class"""

    # pylint: disable=too-few-public-methods
    def __init__(self, context):
        """Helper class that holds session properties and acquisitions"""
        self.context = context
        self.acquisitions = {}


class ParRecAcquisition:
    """PAR/REC acquisition class"""

    # pylint: disable=too-few-public-methods
    def __init__(self, context):
        """Helper class that holds acquisition properties and files"""
        self.context = context
        self.par_file = None


class ParRecScanner(AbstractScanner):
    """Class that handles generic PAR/REC import"""

    def __init__(self, config):
        super().__init__(config)
        self.sessions = {}

    def discover(
        self, walker, context, container_factory, path_prefix=None, audit_log=None
    ):
        # pylint: disable=too-many-locals
        # First step is to walk and sort files
        sys.stdout.write("Scanning directories...".ljust(80) + "\r")
        sys.stdout.flush()

        files = list(walker.files(subdir=path_prefix))
        file_count = len(files)
        files_scanned = 0

        rec_files = {}
        for path in files:
            sys.stdout.write(
                f"Scanning {files_scanned}/{file_count} files...".ljust(80) + "\r"
            )
            sys.stdout.flush()
            files_scanned = files_scanned + 1

            lpath = path.lower()
            real_path = path_prefix + path if path_prefix else path

            if fnmatch.fnmatch(lpath, "*.par"):
                # Parse par file
                try:
                    with walker.open(path, "r") as f:
                        par = parse_par_header(f)

                    acquisition = self.resolve_acquisition(context, par)
                    if acquisition.par_file and not util.files_equal(
                        walker, path, acquisition.par_file
                    ):
                        message = (
                            f'Conflicts with "{path}"! Both files appear to belong to '
                            "the same acquisition, but contents differ!"
                        )
                        self.report_file_error(audit_log, path, msg=message)

                    acquisition.par_file = real_path

                except Exception as exc:  # pylint: disable=broad-except
                    self.report_file_error(audit_log, real_path, exc=exc)
            elif fnmatch.fnmatch(lpath, "*.rec"):
                rec_files[real_path.lower()] = real_path
            else:
                log.debug(f"Ignoring unknown file: {real_path}")

        # Create context objects
        # Walk sessions, acquisitions, then try to find the matching rec file
        for session in self.sessions.values():
            session_context = copy.deepcopy(context)
            session_context.update(session.context)

            for acquisition in session.acquisitions.values():
                acquisition_context = copy.deepcopy(session_context)
                acquisition_context.update(acquisition.context)

                # Case-insensitive lookup for REC file
                root, _ = fs.path.splitext(acquisition.par_file)
                rec_path = rec_files.get(root.lower() + ".rec")
                if rec_path:
                    try:
                        files = [acquisition.par_file, rec_path]
                        container = container_factory.resolve(acquisition_context)
                        self.add_files(
                            container,
                            files,
                            packfile=PackfileDescriptor("parrec", files, 2),
                        )
                    except ValueError as ex:
                        self.messages.append(("warn", str(ex)))
                else:
                    log.warning(
                        f"Ignoring PAR file without matching REC file: {acquisition.par_file}"
                    )

    def resolve_session(self, context, par):
        """Find or create a sesson from a PAR header."""
        session_label = context.get("session", {}).get("label")

        session_timestamp = None
        if "exam_date" in par:
            session_timestamp = parse_par_timestamp(par["exam_date"])

        if not session_label:
            session_label = par.get("exam_name")
        if not session_label and session_timestamp:
            session_label = session_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Default to session label (no real subject code in PAR AFAIK)
        subject_label = context.get("subject", {}).get("label", session_label)

        session_key = (subject_label, session_label)
        if session_key not in self.sessions:
            self.sessions[session_key] = ParRecSession(
                {
                    "session": {
                        "label": session_label,
                        "timestamp": session_timestamp,
                        "timezone": str(util.DEFAULT_TZ),
                    },
                    "subject": {"label": subject_label},
                }
            )
        return self.sessions[session_key]

    def resolve_acquisition(self, context, par):
        """Find or create an acquisition from a PAR header."""
        session = self.resolve_session(context, par)

        # Prefix acquisition label with acquisition number, if available
        acq_label = par.get("protocol_name", "")
        acq_nr = par.get("acq_nr", "")
        if acq_nr:
            try:
                acq_nr = f"{int(acq_nr):02}"
            except ValueError:
                pass

        if acq_label and acq_nr:
            acq_label = f"{acq_nr} - {acq_label}"
        else:
            acq_label = acq_label or acq_nr

        if acq_label not in session.acquisitions:
            session.acquisitions[acq_label] = ParRecAcquisition(
                {"acquisition": {"label": acq_label}}
            )

        return session.acquisitions[acq_label]


class ParRecScannerImporter(AbstractImporter):
    """PAR/REC scanner importer class"""

    def __init__(
        self,
        group,
        project,
        config,
        context=None,
        subject_label=None,
        session_label=None,
    ):
        """Class that handles state for PAR/REC scanning import.

        Arguments:
            group (str): The optional group id
            project (str): The optional project label or id in the format <id:xyz>
            config (Config): The config object
        """
        super().__init__(group, project, False, context, config)

        # Initialize the scanner
        self.scanner = ParRecScanner(config)

        self.subject_label = subject_label
        self.session_label = session_label

    def initial_context(self):
        """Creates the initial context for folder import.

        Returns:
            dict: The initial context
        """
        context = super().initial_context()

        if self.subject_label:
            util.set_nested_attr(context, "subject.label", self.subject_label)

        if self.session_label:
            util.set_nested_attr(context, "session.label", self.session_label)

        return context

    def perform_discover(self, walker, context):
        """Performs discovery of containers to create and files to upload in the given folder.

        Arguments:
            walker (AbstractWalker): The filesystem to query
            context (dict): The initial context
        """
        self.scanner.discover(
            walker, context, self.container_factory, audit_log=self.audit_log
        )
        self.messages += self.scanner.messages
