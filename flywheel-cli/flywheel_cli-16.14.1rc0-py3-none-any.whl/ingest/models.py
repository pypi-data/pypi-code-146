"""SQLAlchemy DB models"""
# pylint: disable=E0213,W0613,R0903
import datetime
import json
import time
import typing
import uuid

import sqlalchemy as sqla
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator
from sqlalchemy_utils import UUIDType

from .. import util
from . import schemas as T
from . import utils as ingest_utils


class JSONType(TypeDecorator):  # pylint: disable=W0223
    """JSON type using JSONB for postgresql and UnicodeText otherwise"""

    impl = sqla.UnicodeText

    def load_dialect_impl(self, dialect):
        impl = JSONB() if dialect.name == "postgresql" else self.impl
        return dialect.type_descriptor(impl)

    def process_bind_param(self, value, dialect):
        if dialect.name == "postgresql":
            return value
        if value is not None:
            value = util.json_serializer(value)
        return value

    def process_result_value(self, value, dialect):
        if dialect.name == "postgresql":
            return value
        if value is not None:
            value = json.loads(value)
        return value


# NOTE constructor=None causes the models to use __init__
@sqla.ext.declarative.as_declarative(constructor=None)
class Base:
    """Mixin defining uuid primary key and schema serialization"""

    # column defaults to trigger validation during __init__
    init_defaults = {}

    def __init__(self, **kwargs):
        """Slightly customized initializer with init_defaults support"""
        for column, default in self.init_defaults.items():
            if column not in kwargs:
                kwargs[column] = default() if callable(default) else default
        self.update(**kwargs)

    @sqla.ext.declarative.declared_attr
    def id(cls):  # pylint: disable=no-self-argument, invalid-name
        """ID primary key column (default: python-generated random uuid)"""
        return sqla.Column(UUIDType, primary_key=True, default=uuid.uuid4)

    @sqla.ext.declarative.declared_attr
    def created(cls):  # pylint: disable=no-self-argument, invalid-name
        """Created timestamp column (default: python-generated current dt)"""
        # TODO switch datetimes to epochs (like status timestamps) to unify
        return sqla.Column(sqla.DateTime, index=True, default=datetime.datetime.utcnow)

    @classmethod
    def schema_cls(cls):
        """Get output schema class"""
        return getattr(T, f"{cls.__name__}Out", None) or getattr(T, f"{cls.__name__}")

    def schema(self):
        """Return sqla model as pydantic schema"""
        return self.schema_cls().from_orm(self)

    @property
    def columns(self) -> typing.Set[str]:
        """Return the set of mapper column names for the model"""
        return {col.key for col in sqla.inspect(self).mapper.column_attrs}

    def update(self, **kwargs: typing.Any) -> None:
        """Update model column attrs based on keyword arguments"""
        for column, value in kwargs.items():
            if column not in self.columns:
                message = (
                    f"{column} is an invalid keyword arg for {type(self).__name__}"
                )
                raise TypeError(message)
            setattr(self, column, value)


class IngestRefMixin:
    """Mixin defining many-to-one relationship to an ingest"""

    @sqla.ext.declarative.declared_attr
    def ingest_id(cls):
        """Ingest ID foreign key column"""
        return sqla.Column(UUIDType, sqla.ForeignKey("ingest.id"), index=True)

    @sqla.ext.declarative.declared_attr
    def ingest(cls):
        """Ingest relationship with (pluralized) backref"""
        return sqla.orm.relationship("Ingest", backref=f"{cls.__tablename__}s")


class StatusMixin:
    """
    Mixin adding status with validation and history.
    Important caveat: 'validate_status' (and history tracking with it)
    is only triggered when the status is set on an ORM model instance.
    """

    @property
    def status_enum(self):
        """Abstract property to be defined w/ the status enum class"""
        # NOTE not using abc to avoid interfering with model metaclass
        raise NotImplementedError

    @sqla.ext.declarative.declared_attr
    def status(cls):
        """Status column (string instead of enum to simplify migrations)"""
        return sqla.Column(sqla.String, index=True)

    @sqla.ext.declarative.declared_attr
    def timestamp(cls):
        """UTC epoch timestamp column of the last status change (int)"""
        return sqla.Column(sqla.Integer)

    @sqla.ext.declarative.declared_attr
    def history(cls):
        """JSON col of the status history (List[Tuple[status, timestamp]])"""
        return sqla.Column(sqla.JSON)

    @sqla.orm.validates("status")
    def validate_status(self, key, value):
        """Validate status change and update timestamp and history"""
        self.status_enum.validate_transition(self.status, value)
        new_status = self.status_enum.get_item(value).value
        new_timestamp = int(time.time())
        self.timestamp = new_timestamp
        self.history = self.history or []
        self.history.append((new_status, new_timestamp))
        # JSON cols don't detect modifications automatically
        sqla.orm.attributes.flag_modified(self, "history")
        self.on_status_update(new_status)
        return new_status

    def on_status_update(self, new_status: T.Status) -> None:
        """Status change callback for customization in subclasses"""


class Ingest(StatusMixin, Base):
    """Ingest operation model"""

    __tablename__ = "ingest"

    init_defaults = {"status": T.IngestStatus.created}

    label = sqla.Column(
        sqla.String, unique=True, default=ingest_utils.generate_ingest_label
    )
    api_key = sqla.Column(sqla.String)
    fw_host = sqla.Column(sqla.String)
    fw_user = sqla.Column(sqla.String)
    config = sqla.Column(sqla.JSON)
    strategy = sqla.Column(sqla.String)
    strategy_config = sqla.Column(sqla.JSON)
    total_time = sqla.Column(sqla.Integer)

    status_enum = T.IngestStatus

    def on_status_update(self, new_status: T.IngestStatus) -> None:
        """Set total_time when entering a terminal status"""
        if T.IngestStatus.is_terminal(new_status):
            timestamps = [hist[1] for hist in self.history]
            start, end = timestamps[0], timestamps[-1]
            self.total_time = end - start


class Task(IngestRefMixin, StatusMixin, Base):
    """Task model"""

    __tablename__ = "task"
    __table_args__ = (sqla.Index("ix_proc_stats", "ingest_id", "status"),)

    init_defaults = {"status": T.TaskStatus.pending}

    modified = sqla.Column(sqla.DateTime, onupdate=datetime.datetime.utcnow)
    item_id = sqla.Column(UUIDType, sqla.ForeignKey("item.id"), index=True)
    item = sqla.orm.relationship(
        "Item", backref=sqla.orm.backref("task", uselist=False)
    )
    type = sqla.Column(sqla.String)
    context = sqla.Column(sqla.JSON)
    worker = sqla.Column(sqla.String)
    retries = sqla.Column(sqla.Integer, default=0)
    completed = sqla.Column(sqla.Integer, default=0)
    total = sqla.Column(sqla.Integer, default=0)
    pending_time = sqla.Column(sqla.Integer)
    running_time = sqla.Column(sqla.Integer)

    status_enum = T.TaskStatus

    @sqla.orm.validates("type")
    def validate_type(self, key, value):
        """Validate task type"""
        return T.TaskType.get_item(value)

    def on_status_update(self, new_status: T.TaskStatus) -> None:
        """Set pending_time and running_time when entering a terminal status"""
        if T.TaskStatus.is_terminal(new_status):
            pending_ts = running_ts = terminal_ts = None
            for status, timestamp in self.history:
                # get pending timestamp of the last (re)try
                if status == T.TaskStatus.pending:
                    pending_ts = timestamp
                # get running timestamp of the last (re)try - may be None if canceled
                if status == T.TaskStatus.running:
                    running_ts = timestamp
                # get last (terminal) timestamp
                terminal_ts = timestamp
            # defensively handling None for tests with ad-hoc status histories
            if pending_ts is not None:
                self.pending_time = (running_ts or terminal_ts) - pending_ts
            if running_ts is not None:
                self.running_time = terminal_ts - running_ts


class Container(IngestRefMixin, Base):
    """Container model which represents nodes in the destination hierarchy"""

    __tablename__ = "container"
    __table_args__ = (
        sqla.Index("ix_scan_stats", "ingest_id", "level"),
        sqla.Index("ix_container_paginate", "ingest_id", "path", "id"),
    )
    parent_id = sqla.Column(UUIDType, sqla.ForeignKey("container.id"), index=True)
    parent = sqla.orm.relationship(
        "Container", remote_side="Container.id", backref="children"
    )
    level = sqla.Column(sqla.Integer)
    path = sqla.Column(sqla.String)
    src_context = sqla.Column(sqla.JSON)
    dst_context = sqla.Column(sqla.JSON)
    dst_path = sqla.Column(sqla.String)
    existing = sqla.Column(sqla.Boolean)
    error = sqla.Column(sqla.Boolean)
    sidecar = sqla.Column(sqla.Boolean)
    dd_files = sqla.Column(sqla.JSON)

    @sqla.orm.validates("level")
    def validate_level(self, key, value):
        """Validate container level"""
        return T.ContainerLevel.get_item(value)


class Item(IngestRefMixin, Base):
    """Ingest item model"""

    __tablename__ = "item"
    __table_args__ = (sqla.Index("ix_item_paginate", "ingest_id", "dir", "id"),)
    container_id = sqla.Column(UUIDType, sqla.ForeignKey("container.id"), index=True)
    container = sqla.orm.relationship("Container", backref="items")
    dir = sqla.Column(sqla.String)
    type = sqla.Column(sqla.String)
    files = sqla.Column(sqla.JSON)
    filename = sqla.Column(sqla.String)
    safe_filename = sqla.Column(sqla.String)
    files_cnt = sqla.Column(sqla.Integer)
    bytes_sum = sqla.Column(sqla.BigInteger)
    context = sqla.Column(sqla.JSON)
    existing = sqla.Column(sqla.Boolean)
    skipped = sqla.Column(sqla.Boolean)
    fw_metadata = sqla.Column(sqla.JSON)
    existing_in = sqla.Column(sqla.String)

    @sqla.orm.validates("type")
    def validate_type(self, key, value):
        """Validate item type"""
        return T.ItemType.get_item(value)


class FWContainerMetadata(IngestRefMixin, Base):
    """FWContainerMetadata model"""

    __tablename__ = "fw_container_metadata"
    __table_args__ = (sqla.Index("path_idx", "path"),)
    path = sqla.Column(sqla.String)
    content = sqla.Column(sqla.JSON)


class Review(IngestRefMixin, Base):
    """Review model"""

    __tablename__ = "review"
    path = sqla.Column(sqla.String)
    skip = sqla.Column(sqla.Boolean)
    context = sqla.Column(sqla.JSON)


class Subject(IngestRefMixin, Base):
    """Subject model"""

    __tablename__ = "subject"
    __table_args__ = (
        sqla.Index("ix_subject_paginate", "ingest_id", "code", "id"),
        sqla.Index("ix_subject_resolve", "ingest_id", "map_values"),
    )
    code = sqla.Column(sqla.String)
    map_values = sqla.Column(JSONType)


class DeidLog(IngestRefMixin, Base):
    """Deid log model"""

    __tablename__ = "deid_log"
    __table_args__ = (sqla.Index("ix_deidlog_paginate", "ingest_id", "created", "id"),)
    src_path = sqla.Column(sqla.String)
    tags_before = sqla.Column(sqla.JSON)
    tags_after = sqla.Column(sqla.JSON)


class Error(IngestRefMixin, Base):
    """Holds item related error"""

    __tablename__ = "item_error"
    __table_args__ = (
        sqla.Index("ix_item_error_paginate", "ingest_id", "created", "id"),
    )
    item_id = sqla.Column(UUIDType, sqla.ForeignKey("item.id"), index=True)
    item = sqla.orm.relationship("Item", backref="errors")
    task_id = sqla.Column(UUIDType, sqla.ForeignKey("task.id"), index=True)
    task = sqla.orm.relationship("Task", backref="errors")
    filepath = sqla.Column(sqla.String)
    code = sqla.Column(sqla.String)
    # allow to store unknown/dynamic error messages
    # mainly used in the asbtarct task error handle to capture any
    # unhandled exceptions
    message = sqla.Column(sqla.String)
    conflict_path = sqla.Column(sqla.String)


class UID(IngestRefMixin, Base):
    """UID model"""

    __tablename__ = "uid"
    item_id = sqla.Column(UUIDType, sqla.ForeignKey("item.id"))
    study_instance_uid = sqla.Column(sqla.String)
    series_instance_uid = sqla.Column(sqla.String)
    sop_instance_uid = sqla.Column(sqla.String)
    acquisition_number = sqla.Column(sqla.String)
    filename = sqla.Column(sqla.String)
    session_container_id = sqla.Column(UUIDType, sqla.ForeignKey("container.id"))
    acquisition_container_id = sqla.Column(UUIDType, sqla.ForeignKey("container.id"))


class TaskStat(IngestRefMixin, Base):
    """TaskStat model"""

    __tablename__ = "task_stat"
    type = sqla.Column(sqla.String)
    pending = sqla.Column(sqla.Integer, default=0)
    running = sqla.Column(sqla.Integer, default=0)
    failed = sqla.Column(sqla.Integer, default=0)
    canceled = sqla.Column(sqla.Integer, default=0)
    completed = sqla.Column(sqla.Integer, default=0)
    total = sqla.Column(sqla.Integer, default=0)


class ItemStat(IngestRefMixin, Base):
    """ItemStat model"""

    __tablename__ = "item_stat"
    scan_total = sqla.Column(sqla.Integer, default=0)
    scan_completed = sqla.Column(sqla.Integer, default=0)
    scan_bytes_sum = sqla.Column(sqla.BigInteger, default=0)

    upload_completed = sqla.Column(sqla.Integer, default=0)
    upload_skipped = sqla.Column(sqla.Integer, default=0)


sqla.orm.configure_mappers()  # NOTE create backrefs
