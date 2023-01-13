"""Ingest related exceptions"""
# pylint: disable=C0111,R0903
from typing import List, Optional

from ..errors import BaseError


class WorkerShutdownTimeout(BaseError):
    message: str = "Worker shutdown grace period exceeded"


class WorkerForcedShutdown(BaseError):
    message: str = (
        "Forced worker to shutdown immediatly without waiting the grace period"
    )


class InvalidDeidProfile(BaseError):
    """Deid Profile Exception"""

    message: str = "Invalid deid profile"
    errors = None

    def __init__(self, msg: str, errors: Optional[List[str]] = None):
        super().__init__(msg)
        self.message = msg
        self.errors = errors

    def __str__(self):
        msg = self.message
        if self.errors:
            msg += f" ({' '.join(self.errors)})"
        return msg


class IngestIsNotDeletable(BaseError):
    """Deid Profile Exception"""

    message: str = "Could not delete ingest"


class BaseIngestError(BaseError):
    code: str = "UNKNOWN"
    message: str = "Unknown error"
    description: str = None
    is_warning = False

    def __init__(self, msg: Optional[str] = None, code: Optional[str] = None):
        super().__init__(msg)
        if code:
            self.code = code


class DuplicateFilepathInUploadSet(BaseIngestError):
    code = "DD01"
    message = "Multiple files have the same destination path"


class DuplicateFilepathInFlywheel(BaseIngestError):
    code = "DD02"
    message = "File name already exists in destination container"


class DifferentStudyInstanceUID(BaseIngestError):
    code = "DD03"
    message = "A single item contains multiple StudyInstanceUIDs"


class DuplicatedStudyInstanceUID(BaseIngestError):
    code = "DD04"
    message = "A single session contains multiple StudyInstanceUIDs"


class DuplicatedStudyInstanceUIDInContainers(BaseIngestError):
    code = "DD05"
    message = "Multiple sessions have the same StudyInstanceUID"


class StudyInstanceUIDExists(BaseIngestError):
    code = "DD06"
    message = "StudyInstanceUID already exists in a different session"


class DuplicatedSeriesInstanceUID(BaseIngestError):
    code = "DD07"
    message = "A single acquisition contains multiple SeriesInstanceUIDs"


class DuplicatedSeriesInstanceUIDInContainers(BaseIngestError):
    code = "DD08"
    message = "Multiple acquisitions have the same SeriesInstanceUID"


class DifferentSeriesInstanceUID(BaseIngestError):
    code = "DD09"
    message = "A single item contains multiple SeriesInstanceUIDs"


class SeriesInstanceUIDExists(BaseIngestError):
    code = "DD10"
    message = "SeriesInstanceUID already exists in a different acquisition"


class DuplicatedSOPInstanceUID(BaseIngestError):
    code = "DD11"
    message = "SOPInstanceUID occurs multiple times (image UIDs should be unique)"


class InvalidSourcePath(BaseIngestError):
    code = "SC01"
    message = "Invalid source path"


class InvalidDicomFile(BaseIngestError):
    code = "SC02"
    message = "Invalid DICOM - missing UID tag"


class ZeroByteFile(BaseIngestError):
    code = "SC03"
    message = "Zero byte file"
    is_warning = True


class NotEnoughPermissions(BaseIngestError):
    code = "SC04"
    message = "Can't perform ingest because of permission errors"


class ContainerDoesNotExist(BaseIngestError):
    code = "SC05"
    message = "The --require-project flag is set and group or project container does not exist"


class FilenameDoesNotMatchTemplate(BaseIngestError):
    code = "SC06"
    message = "Filename does not match to the specified template"


class InvalidFileContext(BaseIngestError):
    code = "SC07"
    message = "Extracted context is invalid"


class StopIngestError(BaseIngestError):
    code = "GE01"
    message = "Stop ingest because of fatal error"


class ProjectFileError(BaseIngestError):
    code = "GE02"
    message = "Project file upload is not enabled"


class ProjectDoesNotExistError(BaseIngestError):
    code = "GE03"
    message = "Detect duplicates project does not exist"
    is_warning = True


class S3AccessDeniedError(BaseIngestError):
    code = "GE04"
    message = "S3 Access denied"


class MultipleGroupOrProjectError(BaseIngestError):
    code = "GE05"
    message = (
        "The ingest would import into multiple groups or projects which is not allowed."
    )


class GroupOrProjectNotSetError(BaseIngestError):
    code = "GE06"
    message = "Group and project must be set explicitly. Use the 'group' and 'project' options."


class DeidConfigConflictError(BaseIngestError):
    code = "GE07"
    message = (
        "De-Identification Logging feature is enabled but no De-Id profile is configured. "
        "Set the De-Id profile on your project or specify the --de-identify and --deid-profile flags."
    )


def get_error_by_code(code: str):
    errors_map = {cls.code: cls for cls in BaseIngestError.__subclasses__()}
    error_cls = errors_map.get(code)
    if not error_cls:
        # pass requested error code to help debugging
        return BaseIngestError(code=code)
    return error_cls()


def get_error_is_warning(code: str):
    errors_map = {cls.code: cls for cls in BaseIngestError.__subclasses__()}
    error_cls = errors_map.get(code)
    if not error_cls:
        # default is error
        return False
    if hasattr(error_cls, "is_warning"):
        return error_cls.is_warning
    return False
