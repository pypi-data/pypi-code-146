# pylint: disable=too-few-public-methods,invalid-name
"""Pydantic ingest input and output schemas"""

import datetime
import enum
import typing as t
import uuid

from pydantic import (  # pylint: disable=E0611
    BaseModel,
    Field,
    root_validator,
    validator,
)

from .. import util
from . import config as cfg


class Schema(BaseModel):
    """Common base configured to play nice with sqlalchemy"""

    class Config:
        """Enable .from_orm() to load fields from attrs"""

        orm_mode = True
        allow_population_by_field_name = True


class Enum(enum.Enum):
    """Extended Enum with easy item lookup by instance, name or value"""

    @classmethod
    def get_item(cls, info: t.Any) -> "Enum":
        """Return enum item for given instance, name or value"""
        for item in cls:
            if info in (item, item.name, item.value):
                return item
        raise ValueError(f"Invalid {cls.__name__} {info}")

    @classmethod
    def has_item(cls, info: t.Any) -> bool:
        """Return True if info is a valid enum instance, name or value"""
        try:
            cls.get_item(info)
        except ValueError:
            return False
        return True


class Status(Enum):
    """Status enum with transition validation and terminality check"""

    @staticmethod
    def transitions():
        """Define allowed status transitions"""
        raise NotImplementedError

    @classmethod
    def validate_transition(cls, old, new) -> None:
        """Raise ValueError if old -> new is not a valid status transition"""
        old = cls.get_item(old).value if old else None
        new = cls.get_item(new).value
        if old and new not in cls.transitions()[old]:
            # NOTE allowing any status transition from old=None facilitates tests
            raise ValueError(f"Invalid {cls.__name__} transition {old} -> {new}")

    @classmethod
    def is_terminal(cls, info) -> bool:
        """Return True if 'has_item(info)' and the status has no transitions"""
        if cls.has_item(info):
            status = cls.get_item(info).value
            return cls.transitions()[status] == set()
        return False


# Ingests


class IngestStatus(str, Status):
    """Ingest status"""

    created = "created"
    configuring = "configuring"
    scanning = "scanning"
    resolving = "resolving"
    detecting_duplicates = "detecting_duplicates"
    in_review = "in_review"
    preparing = "preparing"
    preparing_sidecar = "preparing_sidecar"
    uploading = "uploading"
    finalizing = "finalizing"
    finished = "finished"
    failed = "failed"
    aborting = "aborting"
    aborted = "aborted"

    @staticmethod
    def transitions():
        """Define allowed transitions"""
        return {
            None: {"created"},
            "created": {"configuring", "aborting"},
            "configuring": {"scanning", "failed", "aborting"},
            "scanning": {"resolving", "failed", "aborting"},
            "resolving": {"detecting_duplicates", "in_review", "failed", "aborting"},
            "detecting_duplicates": {"in_review", "failed", "aborting"},
            "in_review": {"preparing", "aborting"},
            "preparing": {"uploading", "preparing_sidecar", "failed", "aborting"},
            "preparing_sidecar": {"uploading", "failed", "aborting"},
            "uploading": {"finalizing", "failed", "aborting"},
            "finalizing": {"finished", "failed", "aborting"},
            "finished": set(),
            "failed": set(),
            "aborting": {"aborted", "failed"},
            "aborted": set(),
        }


class IngestInAPI(Schema):
    """Ingest input schema for API"""

    config: cfg.IngestConfig
    strategy_config: cfg.StrategyConfig


class BaseIngestOut(Schema):
    """Base ingest output schema"""

    id: uuid.UUID
    label: str
    fw_host: str
    fw_user: str
    config: cfg.IngestConfig
    strategy_config: cfg.StrategyConfig
    status: IngestStatus
    history: t.List[t.Tuple[IngestStatus, int]]
    created: datetime.datetime


class IngestOutAPI(BaseIngestOut):
    """Ingest output schema for API"""


class IngestOut(BaseIngestOut):
    """Ingest output schema w/ api-key"""

    api_key: str


# Tasks


class TaskType(str, Enum):
    """Task type enum"""

    configure = "configure"
    scan = "scan"
    extract_uid = "extract_uid"
    resolve = "resolve"  # singleton
    detect_duplicates = "detect_duplicates"  # singleton
    prepare_sidecar = "prepare_sidecar"  # singleton
    prepare = "prepare"  # singleton
    upload = "upload"
    finalize = "finalize"  # singleton

    @classmethod
    def ingest_status(cls, info) -> IngestStatus:
        """Get the associated ingest status of a task type"""
        status = cls.get_item(info).value
        task_type_ingest_status_map = {
            "configure": IngestStatus.configuring,
            "scan": IngestStatus.scanning,
            "extract_uid": IngestStatus.scanning,
            "resolve": IngestStatus.resolving,
            "detect_duplicates": IngestStatus.detecting_duplicates,
            "prepare_sidecar": IngestStatus.preparing_sidecar,
            "prepare": IngestStatus.preparing,
            "upload": IngestStatus.uploading,
            "finalize": IngestStatus.finalizing,
        }
        return task_type_ingest_status_map[status]


class TaskStatus(str, Status):
    """Task status enum"""

    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    canceled = "canceled"

    @staticmethod
    def transitions():
        """Define allowed transitions"""
        return {
            None: {"pending"},
            "pending": {"running", "canceled"},  # cancel via ingest fail/abort
            "running": {"completed", "pending", "failed"},  # retry to pending
            "completed": set(),
            "failed": set(),  # NOTE this will get trickier with user retries
            "canceled": set(),
        }


class TaskIn(Schema):
    """Task input schema"""

    type: TaskType
    item_id: t.Optional[uuid.UUID]
    context: t.Optional[dict]
    status: TaskStatus = TaskStatus.pending


class TaskOut(TaskIn):
    """Task output schema"""

    id: uuid.UUID
    ingest_id: uuid.UUID
    status: TaskStatus
    history: t.List[t.Tuple[TaskStatus, int]]
    worker: t.Optional[str]
    error: t.Optional[str]
    created: datetime.datetime
    retries: int
    completed: t.Optional[int] = 0  # completed work unit
    total: t.Optional[int] = 0  # total number of work unit


# Containers


class SourceContainerContext(Schema):
    """Source container context schema, generally comes from the template/cli args/scanners"""

    id: t.Optional[str] = Field(None, alias="_id")
    label: t.Optional[str]
    info: t.Optional[t.Dict[str, t.Any]]
    uid: t.Optional[str]
    timestamp: t.Optional[datetime.datetime]
    timezone: t.Optional[str]

    age: t.Optional[int]
    weight: t.Optional[float]
    operator: t.Optional[str]
    cohort: t.Optional[str]
    mlset: t.Optional[str]
    ethnicity: t.Optional[str]
    firstname: t.Optional[str]
    lastname: t.Optional[str]
    race: t.Optional[str]
    sex: t.Optional[str]
    type: t.Optional[str]
    tags: t.Optional[t.List[str]]
    species: t.Optional[str]
    strain: t.Optional[str]

    @root_validator
    def id_or_label_provided(cls, values):  # pylint: disable=E0213
        """Verify that id or label is specified"""
        if not (values.get("id") or values.get("label")):
            raise ValueError("_id or label is required field")
        return values

    @validator("label")
    def sanitize_label(cls, v):  # pylint: disable=E0213
        """Sanitize label validator"""
        if not v:
            return v
        return util.sanitize_filename(v)


class SourceSubjectContext(SourceContainerContext):
    """Source subject context schema, generally comes from the template/cli args/scanners"""

    @root_validator(pre=True)
    def id_or_label_provided(cls, values):  # pylint: disable=E0213
        """Verify that id or label is specified"""
        if not (values.get("_id") or values.get("label")):
            raise ValueError(
                "_id or label is required field. Use the --subject flag to specify label"
            )
        return values


class SourceSessionContext(SourceContainerContext):
    """Source session context schema, generally comes from the template/cli args/scanners"""

    @root_validator(pre=True)
    def id_or_label_provided(cls, values):  # pylint: disable=E0213
        """Verify that id or label is specified"""
        if not (values.get("_id") or values.get("label")):
            raise ValueError(
                "_id or label is required field. Use the --session flag to specify label"
            )
        return values


class DestinationContainerContext(Schema):
    """Destination container context, represents an existing container in flywheel"""

    id: str = Field(..., alias="_id")
    label: t.Optional[str]
    info: t.Optional[t.Dict[str, t.Any]]
    uid: t.Optional[str]
    files: t.List[str] = []


class ContainerLevel(int, Enum):
    """Container level enum (int for simple ordering)"""

    group = 0
    project = 1
    subject = 2
    session = 3
    acquisition = 4


class Container(Schema):
    """Container schema"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    parent_id: t.Optional[uuid.UUID]
    path: str
    level: ContainerLevel
    src_context: SourceContainerContext
    dst_context: t.Optional[DestinationContainerContext]
    dst_path: t.Optional[str]
    existing: t.Optional[bool] = False
    error: t.Optional[bool] = False
    sidecar: t.Optional[bool] = False
    files_cnt: t.Optional[int]
    bytes_sum: t.Optional[int]
    dd_files: t.Optional[t.Dict[str, t.List[str]]] = {}


# Items


class ItemType(str, Enum):
    """Ingest item type enum"""

    file = "file"
    packfile = "packfile"


class Error(Schema):
    """Item error schema"""

    item_id: t.Optional[uuid.UUID]
    task_id: t.Optional[uuid.UUID]
    filepath: t.Optional[str]
    code: str
    message: t.Optional[str]
    conflict_path: t.Optional[str]


class PackfileContext(Schema):
    """Packfile context schema"""

    type: str
    name: t.Optional[str]
    flatten: bool = False
    zip: bool = True


class ItemContext(Schema):
    """Item context schema"""

    group: SourceContainerContext
    project: SourceContainerContext
    subject: t.Optional[SourceSubjectContext]
    session: t.Optional[SourceSessionContext]
    acquisition: t.Optional[SourceContainerContext]
    packfile: t.Optional[PackfileContext]


class Item(Schema):
    """Item schema"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    container_id: t.Optional[uuid.UUID]
    dir: str
    type: ItemType
    files: t.List[str]
    filename: str
    safe_filename: t.Optional[str]
    files_cnt: int
    bytes_sum: int
    context: ItemContext
    existing: t.Optional[bool] = False
    skipped: t.Optional[bool] = False
    fw_metadata: t.Optional[t.Dict[str, t.Any]]
    existing_in: t.Optional[str]

    @root_validator
    def validate_item_type(cls, values):  # pylint: disable=E0213
        """
        Validate that the item type is correct:
            - if files list contains more than one file the type has to be packfile
        """
        if len(values["files"]) > 1 and values["type"] == ItemType.file:
            raise ValueError("Found multiple files, type needs to be packfile")
        return values

    @validator("filename")
    def sanitize_filename(cls, v):  # pylint: disable=E0213
        """Sanitize filename validator"""
        return util.sanitize_filename(v)


class FWContainerMetadata(Schema):
    """FWContainerMetadata class"""

    path: str
    content: t.Dict[str, t.Any]


class ItemWithContainerPath(Schema):
    """Ingest item with container path for detect duplicates task"""

    id: uuid.UUID
    dir: str
    filename: str
    existing: t.Optional[bool]
    existing_in: t.Optional[str]
    container_path: t.Optional[str]


class ItemWithErrorCount(Schema):
    """Ingest item with error count for prepare task"""

    id: uuid.UUID
    existing: t.Optional[bool]
    error_cnt: int = 0
    container_error: t.Optional[bool]
    container_path: t.Optional[str]


# Ingest stats


class StageCount(Schema):
    """Work unit completed/total counts"""

    completed: int = 0
    total: int = 0


class StageProgress(Schema):
    """Work unit counts by ingest status"""

    configuring: StageCount = StageCount()
    scanning: StageCount = StageCount()
    resolving: StageCount = StageCount()
    detecting_duplicates: StageCount = StageCount()
    preparing: StageCount = StageCount()
    preparing_sidecar: StageCount = StageCount()
    uploading: StageCount = StageCount()
    finalizing: StageCount = StageCount()


class StatusCount(Schema):
    """Counts by status"""

    scanned: int = 0
    pending: int = 0
    running: int = 0
    failed: int = 0
    canceled: int = 0
    completed: int = 0
    skipped: int = 0
    finished: int = 0
    total: int = 0


class Progress(Schema):
    """Ingest progress with scan task and import- item/file/byte counts by status"""

    scans: StatusCount = StatusCount()
    items: StatusCount = StatusCount()
    files: StatusCount = StatusCount()
    bytes: StatusCount = StatusCount()
    stages: StageProgress = StageProgress()


class ErrorSummary(Schema):
    """Ingest error summary"""

    code: str
    message: str
    description: t.Optional[str]
    count: int


class Summary(Schema):
    """Ingest scan summary with hierarchy node and file counts"""

    groups: int = 0
    projects: int = 0
    subjects: int = 0
    sessions: int = 0
    acquisitions: int = 0
    files: int = 0
    packfiles: int = 0
    warnings: t.Optional[t.List[ErrorSummary]]
    errors: t.Optional[t.List[ErrorSummary]]


class TaskError(Schema):
    """Ingest task error"""

    task: uuid.UUID
    type: TaskType
    code: str
    message: str


class Report(Schema):
    """Final ingest report with status, elapsed times and list of errors"""

    status: IngestStatus
    elapsed: t.Dict[IngestStatus, int]
    errors: t.List[TaskError]
    warnings: t.List[TaskError]


# Review


class ReviewChange(Schema):
    """Review change"""

    path: str
    skip: t.Optional[bool]
    context: t.Optional[dict]


ReviewIn = t.List[ReviewChange]


# Logs


class AuditLogOut(Schema):
    """Audit log output schema"""

    id: uuid.UUID
    dir: str
    filename: str
    src_path: t.Optional[str]
    dst_path: t.Optional[str]
    existing: t.Optional[bool]
    skipped: t.Optional[bool]
    files_cnt: t.Optional[int]
    status: t.Optional[TaskStatus]
    error_code: t.Optional[str]
    error_message: t.Optional[str]
    container_error: t.Optional[bool]
    conflict_path: t.Optional[str]


class DeidLogIn(Schema):
    """Deid log input schema"""

    src_path: str
    tags_before: dict
    tags_after: dict


class DeidLogOut(DeidLogIn):
    """De-id log output schema"""

    id: uuid.UUID
    created: datetime.datetime


class SubjectOut(Schema):
    """Subject output schema"""

    code: str
    map_values: t.List[str]


# UID


class UIDIn(Schema):
    """UID input schema"""

    item_id: uuid.UUID
    filename: str
    study_instance_uid: str
    series_instance_uid: str
    sop_instance_uid: str
    acquisition_number: t.Optional[str]
    session_container_id: t.Optional[uuid.UUID]
    acquisition_container_id: t.Optional[uuid.UUID]


class UIDOut(UIDIn):
    """UID output schema"""

    id: uuid.UUID


class ItemWithUIDs(Schema):
    """Ingest item with UIDs"""

    item: Item
    uids: t.List[UIDIn]


class DetectDuplicateItem(Schema):
    """DetectDuplicateItem used in find_all_item_with_uid to return lightweight objects"""

    id: uuid.UUID
    item_id: uuid.UUID
    session_container_id: t.Optional[uuid.UUID]
    acquisition_container_id: t.Optional[uuid.UUID]
    study_instance_uid: t.Optional[str]
    series_instance_uid: t.Optional[str]


# Others


class ReportETA(Schema):
    """ETA report schema"""

    eta: int
    report_time: int
    finished: int
    total: int


class ContainerID(Schema):
    """Container ID for Item"""

    id: uuid.UUID
    container_id: uuid.UUID


class TaskStat(Schema):
    """TaskStat"""

    type: str = None
    ingest_id: uuid.UUID = None
    id: uuid.UUID = None
    pending: int = 0
    running: int = 0
    failed: int = 0
    canceled: int = 0
    completed: int = 0
    total: int = 0


class ItemStat(Schema):
    """ItemStat"""

    type: str = None
    ingest_id: uuid.UUID = None
    id: uuid.UUID = None
    total: int = 0
    completed: int = 0
    skipped: int = 0
    bytes_sum: int = 0
