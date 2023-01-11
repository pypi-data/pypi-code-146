"""Provides a scanner for dicom files"""
import copy
import gzip
import itertools
import logging
import os
import sys

import fs
from flywheel_migration.dcm import DicomFile, DicomFileError
from pydicom.datadict import tag_for_keyword
from pydicom.tag import Tag

from .. import util
from .. import walker as walkers
from .abstract_importer import AbstractImporter
from .abstract_scanner import AbstractScanner
from .packfile import PackfileDescriptor

log = logging.getLogger(__name__)


class DicomSession:
    """Dicom session class"""

    # pylint: disable=too-few-public-methods
    def __init__(self, context):
        """Helper class that holds session properties and acquisitions"""
        self.context = context
        self.acquisitions = {}
        self.secondary_acquisitions = {}  # Acquisitions that we don't have all
        # of the info for yet


class DicomAcquisition:
    """Dicom acquisition class"""

    # pylint: disable=too-few-public-methods
    def __init__(self, context):
        """Helper class that holds acquisition properties and files"""
        self.context = context
        self.files = (
            {}
        )  # Map of primary_series_uids to maps of series uids to filepaths
        # So that the primary series uid can be used to group multiple dicom series into one acquisition
        self.filenames = {}  # A map of series uid to filenames


def _at_stack_id(related_acquisitions):
    if related_acquisitions:
        stop_tag = (0x3006, 0x0011)
    else:
        stop_tag = (0x0020, 0x9056)

    def f(tag, *args):  # pylint: disable=unused-argument
        return tag == stop_tag

    return f


class DicomScanner(AbstractScanner):
    """Dicom scanner class"""

    # The session label dicom header key
    session_label_key = "StudyDescription"

    def __init__(self, config):
        """Class that handles generic dicom import"""
        super().__init__(config)

        if config:
            self.deid_profile = config.deid_profile
            self.related_acquisitions = config.related_acquisitions
        else:
            self.deid_profile = None
            self.related_acquisitions = False

        self.profile = None  # Dicom file profile
        self.subject_map = None  # Provides subject mapping services
        self.get_subject_code = None
        if self.deid_profile:
            self.subject_map = self.deid_profile.map_subjects
            self.get_subject_code = (
                self.subject_map.get_code if self.subject_map else None
            )
            self.profile = self.deid_profile.get_file_profile("dicom")

        self.sessions = {}
        self.duplicates_fs = None

        self.dicom_utils = util.DicomUtils(
            deid_profile=self.profile, get_subject_code_fn=self.get_subject_code
        )

    def save_subject_map(self):
        """Save subject map"""
        if self.subject_map:
            self.subject_map.save()

    def discover(
        self, walker, context, container_factory, path_prefix=None, audit_log=None
    ):
        # pylint: disable=too-many-branches, too-many-statements, too-many-locals
        self.duplicates_fs = self._get_duplicates_fs(walker)
        tags = [
            Tag(tag_for_keyword(keyword)) for keyword in self.dicom_utils.required_tags
        ]

        # If we're mapping subject fields to id, then include those fields in the scan
        if self.subject_map:
            subject_cfg = self.subject_map.get_config()
            tags += [Tag(tag_for_keyword(keyword)) for keyword in subject_cfg.fields]
        if self.related_acquisitions:
            tags += [Tag(tag_for_keyword("ReferencedFrameOfReferenceSequence"))]

        # First step is to walk and sort files
        sys.stdout.write("Scanning directories...".ljust(80) + "\r")
        sys.stdout.flush()

        # Discover files first
        files = list(sorted(walker.files(subdir=path_prefix)))
        file_count = len(files)
        files_scanned = 0

        for path in files:
            sys.stdout.write(
                f"Scanning {files_scanned}/{file_count} files...".ljust(80) + "\r"
            )
            sys.stdout.flush()
            files_scanned = files_scanned + 1
            is_dicom = util.is_dicom_file(path)

            try:
                with walker.open(path, "rb", buffering=self.config.buffer_size) as f:
                    # Unzip gzipped files
                    _, ext = os.path.splitext(path)
                    if ext.lower() == ".gz":
                        f = gzip.GzipFile(fileobj=f)

                    # Don't decode while scanning, stop as early as possible
                    # TODO: will we ever rely on fields after stack id for subject mapping
                    dcm = DicomFile(
                        f,
                        parse=False,
                        session_label_key=self.session_label_key,
                        decode=self.related_acquisitions,
                        stop_when=_at_stack_id(self.related_acquisitions),
                        update_in_place=False,
                        specific_tags=tags,
                        force=is_dicom,
                    )
                    acquisition = self.resolve_acquisition(context, dcm)
                    sop_uid = self.dicom_utils.get_value(
                        dcm, "SOPInstanceUID", required=True
                    )
                    try:
                        self._before_add_instance(
                            path, sop_uid, context, walker, audit_log
                        )
                    except DuplicateSOPInstanceUID:
                        # skip file
                        continue
                    series_uid = self.dicom_utils.get_value(
                        dcm, "SeriesInstanceUID", required=True
                    )
                    if sop_uid in acquisition.files.setdefault(series_uid, {}):
                        orig_path = acquisition.files[series_uid][sop_uid]
                        if not util.files_equal(walker, path, orig_path):
                            message = (
                                f"DICOM conflicts with {orig_path}! Both files have the "
                                "same IDs, but contents differ!"
                            )
                            self.report_file_error(audit_log, path, msg=message)
                    else:
                        if self.config.check_unique_uids:
                            # store the SopInstanceUIDs on the global context object so we can check import wide
                            # that the current uid is unique
                            context.setdefault("sop_uids", []).append(sop_uid)
                        acquisition.files[series_uid][sop_uid] = path

                    # Add a filename for that series uid
                    if series_uid not in acquisition.filenames:
                        acquisition_timestamp = (
                            self.dicom_utils.determine_acquisition_timestamp(dcm)
                        )
                        series_label = self.dicom_utils.determine_acquisition_label(
                            acquisition.context,
                            dcm,
                            series_uid,
                            timestamp=acquisition_timestamp,
                        )
                        filename = self.dicom_utils.determine_dicom_zipname(
                            acquisition.filenames, series_label
                        )
                        acquisition.filenames[series_uid] = filename

            except DicomFileError as exc:
                if is_dicom:
                    self.report_file_error(
                        audit_log, path, exc=exc, msg=f"Not a DICOM - {exc}"
                    )
                else:
                    log.debug(f"Ignoring non-DICOM file: {path}")
            except Exception as exc:  # pylint: disable=broad-except
                self.report_file_error(audit_log, path, exc=exc)

        # Create context objects
        for session in self.sessions.values():
            session_context = copy.deepcopy(context)
            session_context.update(session.context)

            for acquisition in itertools.chain(
                session.acquisitions.values(), session.secondary_acquisitions.values()
            ):
                acquisition_context = copy.deepcopy(session_context)
                acquisition_context.update(acquisition.context)
                try:
                    self._before_resolve_acquisition(
                        acquisition, walker, container_factory.resolver, audit_log
                    )
                except DuplicateSeriesInstanceUID as exc:
                    # log message and skip this acquisition
                    log.debug(exc)
                    continue

                for series_uid, files in acquisition.files.items():
                    files = list(files.values())
                    filename = acquisition.filenames.get(series_uid)
                    try:
                        container = container_factory.resolve(acquisition_context)
                        self.add_files(
                            container,
                            files,
                            packfile=PackfileDescriptor(
                                "dicom", files, len(files), filename
                            ),
                        )
                    except ValueError as ex:
                        self.messages.append(("warn", str(ex)))

    def resolve_session(self, context, dcm):
        """Find or create a sesson from a dcm file."""
        subject_code = self.dicom_utils.determine_subject_code(context, dcm)

        session_uid = self.dicom_utils.get_value(dcm, "StudyInstanceUID", required=True)
        if session_uid not in self.sessions:
            session_timestamp = self.dicom_utils.get_timestamp(
                dcm, "StudyDate", "StudyTime"
            )

            # Create session
            self.sessions[session_uid] = DicomSession(
                {
                    "session": {
                        "uid": session_uid,
                        "label": self.dicom_utils.determine_session_label(
                            context, dcm, session_uid, timestamp=session_timestamp
                        ),
                        "timestamp": session_timestamp,
                        "timezone": str(util.DEFAULT_TZ),
                    },
                    "subject": {"label": subject_code},
                }
            )

        return self.sessions[session_uid]

    def resolve_acquisition(self, context, dcm):
        """Find or create an acquisition from a dcm file."""
        session = self.resolve_session(context, dcm)
        series_uid = self.dicom_utils.get_value(dcm, "SeriesInstanceUID", required=True)
        primary_acquisition_file = True
        if self.related_acquisitions and dcm.get("ReferencedFrameOfReferenceSequence"):
            # We need to add it to the acquisition of the primary series uid
            try:
                series_uid = (
                    dcm.get("ReferencedFrameOfReferenceSequence")[0]
                    .get("RTReferencedStudySequence")[0]
                    .get("RTReferencedSeriesSequence")[0]
                    .get("SeriesInstanceUID")
                )
                primary_acquisition_file = False
            except (TypeError, IndexError, AttributeError):
                log.warning(
                    "Unable to find related series for file {}. Uploading into its own acquisition"
                )

        if series_uid not in session.acquisitions:
            # full acquisition doesn't exists
            if (
                not primary_acquisition_file
                and series_uid in session.secondary_acquisitions
            ):
                # The secondary acquisition exists
                return session.secondary_acquisitions[series_uid]

            acquisition_timestamp = self.dicom_utils.determine_acquisition_timestamp(
                dcm
            )
            acquisition = DicomAcquisition(
                {
                    "acquisition": {
                        "uid": series_uid,
                        "label": self.dicom_utils.determine_acquisition_label(
                            context, dcm, series_uid, timestamp=acquisition_timestamp
                        ),
                        "timestamp": acquisition_timestamp,
                        "timezone": str(util.DEFAULT_TZ),
                    }
                }
            )

            if primary_acquisition_file:
                # Check for a secondary and add it the files and filenames to the primary
                if series_uid in session.secondary_acquisitions:
                    acquisition.files = session.secondary_acquisitions.get(
                        series_uid
                    ).files
                    acquisition.filenames = session.secondary_acquisitions.pop(
                        series_uid
                    ).filenames

                session.acquisitions[series_uid] = acquisition
                return session.acquisitions[series_uid]
            session.secondary_acquisitions[series_uid] = acquisition
            return session.secondary_acquisitions[series_uid]

        # Acquisition already exists
        return session.acquisitions[series_uid]

    def _before_add_instance(self, path, sop_uid, context, walker, audit_log):
        """
        Run before adding the given file to an acquisition.

        Verifies that the given SOPInstanceUID is unique, if not move the file to the duplicates folder.
        """
        if (
            sop_uid in context.get("sop_uids", [])
            and self.config.check_unique_uids
            and self.config.copy_duplicates
        ):
            message = (
                f"Copying to {self.config.duplicates_folder} because already processed "
                f"a DICOM instance with this SOPInstanceUID: {sop_uid}"
            )
            self.report_file_error(
                audit_log, path, msg=message, msg_prefix="Skipping file"
            )
            self.copy_file_to_duplicates(walker, path)
            raise DuplicateSOPInstanceUID(sop_uid)

    def _before_resolve_acquisition(self, acquisition, walker, resolver, audit_log):
        """
        Run before calling the container factory's resolve method.

        Verifies that the given SeriesInstanceUID is unique, if not moves all file in this acquisition to the duplicates folder.
        """
        acquisition_ctx = acquisition.context["acquisition"]
        if self.config.check_unique_uids and self.config.copy_duplicates:
            result = resolver.check_unique_uids(
                {"acquisitions": [acquisition_ctx["uid"]]}
            )
            if not acquisition_ctx["uid"] in result["acquisitions"]:
                return
            files_to_move = itertools.chain.from_iterable(
                map(lambda k__v: k__v[1].values(), acquisition.files.items())
            )
            for f in files_to_move:
                message = (
                    f"Copying to {self.config.duplicates_folder} because acquisition "
                    f"already exists with this SeriesInstanceUID: {acquisition_ctx['uid']}"
                )
                self.report_file_error(
                    audit_log, f, msg=message, msg_prefix="Skipping file"
                )
                self.copy_file_to_duplicates(walker, f)
            raise DuplicateSeriesInstanceUID(acquisition_ctx["uid"])

    def _get_duplicates_fs(self, walker):
        if not self.config.duplicates_folder:
            if isinstance(walker, walkers.PyFsWalker):
                parent_dir = fs.path.dirname(walker.src_fs.getsyspath("/").rstrip("/"))
                self.config.duplicates_folder = fs.path.combine(
                    parent_dir, "duplicates"
                )
            else:
                log.warning(
                    f"{walker.__class__.__name__} walker does not support copying files, duplicates won't be collected"
                )
                return None

        return fs.open_fs(self.config.duplicates_folder, create=True)

    def copy_file_to_duplicates(self, walker, file_path):
        """Copy file to duplicates"""
        if not self.duplicates_fs:
            log.debug("Filesystem for duplicates is not set")
            return
        dir_name = fs.path.dirname(file_path)
        self.duplicates_fs.makedirs(dir_name, recreate=True)
        fs.copy.copy_file(walker.src_fs, file_path, self.duplicates_fs, file_path)


class DicomScannerImporter(AbstractImporter):
    """Dicom scanner importer class"""

    # Archive filesystems are not supported, because zipfiles are not seekable
    support_archive_fs = False

    # Subject mapping is supported
    support_subject_mapping = True

    def __init__(
        self,
        group,
        project,
        config,
        context=None,
        subject_label=None,
        session_label=None,
    ):
        """Class that handles state for dicom scanning import.

        Arguments:
            group (str): The optional group id
            project (str): The optional project label or id in the format <id:xyz>
            config (Config): The config object
        """
        super().__init__(group, project, False, context, config)

        # Initialize the scanner
        self.scanner = DicomScanner(config)

        self.subject_label = subject_label
        self.session_label = session_label

    def before_begin_upload(self):
        # Save subject map
        self.scanner.save_subject_map()

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


class DuplicateSOPInstanceUID(Exception):
    """Duplicate SOPInstanceUID exception."""

    msg = "DICOM already exists with this SOPInstanceUID: {}"

    def __init__(self, uid):
        super().__init__(self.msg.format(uid))


class DuplicateSeriesInstanceUID(Exception):
    """Duplicate SeriesInstanceUID exception."""

    msg = "Acquisition already exists with this SeriesInstanceUID: {}"

    def __init__(self, uid):
        super().__init__(self.msg.format(uid))


class InvalidLabel(Exception):
    """Invalid label for container exception"""

    def __init__(self, container_type):
        self.msg = f"{container_type}.label '' not valid"
        super().__init__(self.msg)
