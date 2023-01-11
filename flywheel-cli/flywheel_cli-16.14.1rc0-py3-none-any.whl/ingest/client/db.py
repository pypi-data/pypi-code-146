# pylint: disable=W0143
"""Client implementation using SQL database

Supported databases: sqlite, postgresql
"""

import copy
import functools
import inspect
import multiprocessing as mp
import os
import re
import typing
import uuid

import sqlalchemy as sqla

from ...models import FWAuth
from ...util import get_sdk_client_for_current_user
from .. import deid, errors
from .. import models as M
from .. import schemas as T
from .. import utils
from ..config import IngestConfig, StrategyConfig
from . import db_transactions
from .abstract import Client

S = typing.TypeVar("S")  # pylint: disable=C0103

# do not create lock instance in import time otherwise
# we will get leaked semaphores warnings in child processes
# when using spawn multiprocessing start method (default on windows)
sqlite_lock = None  # pylint: disable=C0103


def set_lock(lock) -> None:
    """
    Set lock object, used to have the same lock object
    in all processes even if using spawn process start method.
    """
    global sqlite_lock  # pylint: disable=W0603,C0103
    sqlite_lock = lock


class DBClient(Client):  # pylint: disable=R0904
    """Ingest DB client implementing crud interface"""

    method_names = {
        "batch_writer",
        "count_all",
        "find_one",
        "get",
        "get_all",
        "update",
    }

    batch_operations = {
        "insert",
        "update",
    }

    model_names = {
        "container": "Container",
        "deid_log": "DeidLog",
        "error": "Error",
        "item": "Item",
        "fw_container_metadata": "FWContainerMetadata",
        "task": "Task",
        "uid": "UID",
        "task_stat": "TaskStat",
    }

    def __init__(self, url: str):
        super().__init__(url)
        self.engine, self.sessionmaker = utils.init_sqla(url)

        if self.engine.name == "sqlite":
            if not sqlite_lock:
                set_lock(mp.Lock())
            with sqlite_lock:
                M.Base.metadata.create_all(self.engine)  # pylint: disable=no-member

    def __getattr__(self, name: str):
        """
        Return model-specific partial methods dynamically.
        Examples:
         * get_container(...) -> get('Container', ...)
         * batch_writer_insert_tasks(...) -> batch_writer('insert', 'Task', ...)
        """
        attr_err_msg = f"{type(self).__name__} object has no attribute {name}"
        for method_name in sorted(self.method_names, key=len, reverse=True):
            if name.startswith(method_name):
                method = getattr(self, method_name)
                model_name = name.replace(f"{method_name}_", "")
                break
        else:
            raise AttributeError(attr_err_msg)

        method_args = []

        # pylint: disable=undefined-loop-variable
        if method_name == "batch_writer":
            operation, model_name = model_name.split("_", maxsplit=1)
            if operation not in self.batch_operations:
                raise AttributeError(f"{attr_err_msg} (invalid operation {operation})")
            method_args.append(operation)

        if method_name.startswith("batch_") or method_name.endswith("_all"):
            model_name = model_name.rstrip("s")
        if model_name not in self.model_names:
            raise AttributeError(f"{attr_err_msg} (invalid model {model_name})")
        method_args.append(self.model_names[model_name])

        return functools.partial(method, *method_args)

    def check_connection(self):
        """Check whether or not the connection works"""
        try:
            # Test query
            self.engine.execute(sqla.text("SELECT 1"))
            return True
        except Exception:  # pylint: disable=broad-except
            return False

    def call_db(self, func: typing.Callable[..., S], *args, **kwargs) -> S:
        """Run the specified function in a transaction"""
        # pylint: disable=E1101
        session = self.sessionmaker()
        if session.bind.name == "sqlite":
            sqlite_lock.acquire()
        try:
            result = func(session, *args, **kwargs)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            if session.bind.name == "sqlite":
                sqlite_lock.release()
        return result

    # Non-ingest-bound methods

    def create_ingest(
        self,
        config: IngestConfig,
        strategy_config: StrategyConfig,
        fw_auth: typing.Optional[FWAuth] = None,
    ) -> T.IngestOutAPI:
        if not fw_auth:
            # TODO: probably this shouldn't be here
            fw_auth = get_sdk_client_for_current_user().auth_info
        ingest = M.Ingest(
            api_key=fw_auth.api_key,
            fw_host=fw_auth.host,
            fw_user=fw_auth.user_id,
            config=config.dict(exclude_none=True),
            strategy=strategy_config.strategy_name,
            strategy_config=strategy_config.dict(exclude_none=True),
            # TODO: user provided label from config
        )
        ingest_out = self.call_db(db_transactions.add, ingest)
        self.bind(ingest_out.id)
        self.create_ingest_stats()
        return T.IngestOutAPI(**ingest_out.dict())

    def list_ingests(
        self, api_key: typing.Optional[str] = None
    ) -> typing.Iterable[T.IngestOutAPI]:
        query = sqla.orm.Query(M.Ingest)
        if api_key:
            query = query.filter(M.Ingest.api_key == api_key)
        return self._iter_query(query, [M.Ingest.created], T.IngestOutAPI)

    def next_task(self, worker: str) -> typing.Optional[T.TaskOut]:
        """Get next pending task, assign to given worker and set status running"""
        return self.call_db(db_transactions.next_task, worker)

    def delete_ingest(self, ingest_id: uuid.UUID) -> None:
        ingest = self.call_db(db_transactions.get, M.Ingest, ingest_id)
        ingest = T.IngestOutAPI(**ingest.dict())
        if not T.IngestStatus.is_terminal(ingest.status):
            raise errors.IngestIsNotDeletable(
                f"Ingest status ({str(ingest.status)}) is not terminal"
            )

        # in case of abort for example the running tasks are not terminated
        if self.call_db(db_transactions.has_running_tasks, ingest_id):
            raise errors.IngestIsNotDeletable("Ingest has running tasks")

        self.call_db(db_transactions.delete_ingest, ingest_id)

    # Ingest-bound methods

    @property
    def ingest(self) -> T.IngestOutAPI:
        """Get ingest operation the client bind to"""
        ingest = self.call_db(db_transactions.get, M.Ingest, self.ingest_id)
        return T.IngestOutAPI(**ingest.dict())

    def load_subject_csv(self, subject_csv: typing.BinaryIO) -> None:
        """Load subject CSV file"""
        self.call_db(db_transactions.load_subject_csv, self.ingest_id, subject_csv)

    def start(self) -> T.IngestOutAPI:
        """Start ingest scanning"""
        ingest = self.call_db(db_transactions.start, self.ingest_id)
        return T.IngestOutAPI(**ingest.dict())

    def review(self, changes=None) -> T.IngestOutAPI:
        """Review (accept) ingest, add any changes and start importing"""
        ingest = self.call_db(db_transactions.review, self.ingest_id, changes)
        return T.IngestOutAPI(**ingest.dict())

    def abort(self) -> T.IngestOutAPI:
        """Abort ingest operation"""
        ingest = self.call_db(db_transactions.abort, self.ingest_id)
        return T.IngestOutAPI(**ingest.dict())

    @property
    def progress(self) -> T.Progress:
        """Get ingest scan task and item/file/byte counts by status"""
        return self.call_db(db_transactions.get_progress, self.ingest_id)

    @property
    def summary(self) -> T.Summary:
        """Get ingest hierarchy node and file count by level and type"""
        return self.call_db(db_transactions.get_summary, self.ingest_id)

    @property
    def report(self) -> T.Report:
        """Get ingest status, elapsed time per status and list of failed tasks"""
        return self.call_db(db_transactions.get_report, self.ingest_id)

    @property
    def tree(self) -> typing.Iterable[T.Container]:
        """Yield hierarchy nodes (containers)"""
        query = (
            sqla.orm.Query(
                [
                    M.Container.id,
                    M.Container.level,
                    M.Container.path,
                    M.Container.parent_id,
                    M.Container.src_context,
                    M.Container.dst_context,
                    M.Container.ingest_id,
                    sqla.sql.func.count(M.Item.id).label("files_cnt"),
                    sqla.sql.func.sum(M.Item.bytes_sum).label("bytes_sum"),
                ]
            )
            .outerjoin(M.Container.items)  # pylint: disable=E1101
            .filter(M.Container.ingest_id == self.ingest_id)
            .group_by(M.Container.id)
        )
        return self._iter_query(query, [M.Container.path], T.Container)

    @property
    def audit_logs(self) -> typing.Iterable[str]:
        """Yield audit log CSV lines"""
        # get sidecar project name
        sidecar_project_path = None
        try:
            # pylint: disable=C0121
            container = self.find_one_container(
                M.Container.level == T.ContainerLevel.project,
                M.Container.sidecar == True,
            )
            sidecar_project_path = container.path
        except sqla.orm.exc.NoResultFound:
            pass
        tasks_subq = (
            sqla.orm.Query([M.Task.item_id, M.Task.status])
            .filter(
                M.Task.ingest_id == self.ingest_id, M.Task.type == T.TaskType.upload
            )
            .subquery()
        )

        query = (
            sqla.orm.Query(
                [
                    M.Item.id,
                    M.Item.dir,
                    M.Item.filename,
                    M.Item.existing,
                    M.Item.skipped,
                    M.Item.files_cnt,
                    M.Container.path.label("src_path"),
                    M.Container.dst_path,
                    M.Container.error.label("container_error"),
                    tasks_subq.c.status,
                    M.Error.code.label("error_code"),
                    M.Error.message.label("error_message"),
                    M.Error.conflict_path.label("conflict_path"),
                ]
            )
            .outerjoin(M.Item.container, M.Item.errors)  # pylint: disable=E1101
            .outerjoin(
                tasks_subq,
                M.Item.id == tasks_subq.c.item_id,
            )
            .filter(M.Item.ingest_id == self.ingest_id)
        )
        filepath_errors = sqla.orm.Query(
            [M.Error.id, M.Error.code, M.Error.message, M.Error.filepath]
        ).filter(
            M.Error.ingest_id == self.ingest_id,
            M.Error.filepath.isnot(None),
        )

        fields = [
            "src_path",
            "dst_path",
            "status",
            "existing",
            "error_code",
            "error_message",
            "action_taken",
            "conflict_path",
        ]
        first = True
        for item in self._iter_query(
            query, [M.Item.dir, M.Error.code.label("error_code")], T.AuditLogOut
        ):
            if first:
                first = False
                header = ",".join(fields)
                yield f"{header}\n"

            # NOTE item.dir is a filename for single file, dir for multiple files
            src_path = f"{self.ingest.config.src_fs}{os.path.sep}{item.dir}"
            if item.files_cnt > 1:
                # NOTE log source dir (ending w/ sep) for packfiles
                src_path += os.path.sep
            src_path = re.sub(r"[/\\]+", re.escape(os.path.sep), src_path)

            values = dict(
                src_path=src_path,
                dst_path=f"{item.dst_path or item.src_path}/{item.filename}",
                status="skipped"
                if item.skipped or not item.status
                else item.status.name,
                existing=item.existing,
                conflict_path=item.conflict_path,
            )

            if item.error_code:
                error = errors.get_error_by_code(item.error_code)
                values["error_code"] = error.code
                values["error_message"] = item.error_message or error.message
            elif item.container_error:
                values["status"] = "skipped"
                values["error_code"] = errors.BaseIngestError.code
                values["error_message"] = "Skipped due to erroneous parent container"
            elif item.status == T.TaskStatus.failed:
                values["error_code"] = errors.BaseIngestError.code
                values["error_message"] = errors.BaseIngestError.message

            if item.skipped and item.status == T.TaskStatus.completed:
                values[
                    "action_taken"
                ] = f"Copied to Duplicates Project: [{sidecar_project_path}]"
            elif item.skipped:
                values["action_taken"] = "File Skipped"

            row = ",".join(_csv_field_str(values.get(field)) for field in fields)
            yield f"{row}\n"

        for filepath_error in self._iter_query(
            filepath_errors, [M.Error.created], T.Error
        ):
            if first:
                first = False
                header = ",".join(fields)
                yield f"{header}\n"

            values = dict(
                src_path=f"{self.ingest.config.src_fs}/{filepath_error.filepath}",
                status="skipped",
                error_code=filepath_error.code,
                error_message=filepath_error.message,
            )
            row = ",".join(_csv_field_str(values.get(field)) for field in fields)
            yield f"{row}\n"

    @property
    def deid_logs(self) -> typing.Iterable[str]:
        """Yield de-id log CSV lines"""
        ingest = self.ingest
        if not ingest.config.de_identify:
            # de-identify is false, so nothing to do
            return

        profile_name = ingest.config.deid_profile
        profiles = ingest.config.deid_profiles
        deid_profile = deid.load_deid_profile(profile_name, profiles)

        query = sqla.orm.Query(M.DeidLog).filter(M.DeidLog.ingest_id == self.ingest_id)
        yield from deid_logs(
            deid_profile, self._iter_query(query, [M.DeidLog.created], T.DeidLogOut)
        )

    @property
    def subjects(self) -> typing.Iterable[str]:
        """Yield subject CSV lines"""
        subject_config = self.ingest.config.subject_config
        if not subject_config:
            return
        query = sqla.orm.Query(M.Subject).filter(M.Subject.ingest_id == self.ingest_id)
        first = True
        for subject in self._iter_query(query, [M.Subject.code], T.SubjectOut):
            if first:
                first = False
                fields = [subject_config.code_format] + subject_config.map_keys
                header = ",".join(fields)
                yield f"{header}\n"
            values = [subject.code] + subject.map_values
            row = ",".join(_csv_field_str(value) for value in values)
            yield f"{row}\n"

    # Ingest-bound extra methods

    @property
    def api_key(self) -> str:
        """Get the associated api key of the ingest"""
        ingest = self.call_db(db_transactions.get, M.Ingest, self.ingest_id)
        return ingest.api_key

    def add(self, schema: T.Schema) -> T.Schema:
        """Add new task/container/item/deid-log to the ingest"""
        model_name = type(schema).__name__.replace("In", "")
        assert model_name in ("Task", "Container", "Item", "Error", "DeidLog")
        model_cls = getattr(M, model_name)
        model = model_cls(ingest_id=self.ingest_id, **schema.dict())
        return self.call_db(db_transactions.add, model)

    def get(self, model_name: str, model_id: uuid.UUID) -> T.Schema:
        """Get a task/container/item/deid-log by id"""
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        model_cls = getattr(M, model_name)
        return self.call_db(db_transactions.get, model_cls, model_id)

    def get_all(
        self, model_name: str, *conditions: typing.Any
    ) -> typing.Iterable[T.Schema]:
        """Get all ingests/tasks/containers/items/deid-logs by filters"""
        assert model_name in self.model_names.values()
        model_cls = getattr(M, model_name)
        order_by = _get_paginate_order_by_col(model_cls)
        query = sqla.orm.Query(model_cls).filter(model_cls.ingest_id == self.ingest_id)
        for condition in conditions:
            query = query.filter(condition)
        return self._iter_query(query, [order_by], model_cls.schema_cls())

    def get_items_sorted_by_dst_path(self) -> typing.Iterable[T.ItemWithContainerPath]:
        """Get items sorted by destination path including the filename.

        Primarily used in the detect duplicates task where sorting makes possible to
        find filepath conflicts without holding too much information in memory
        or overload the db backend with too much queries.
        """
        query = (
            sqla.orm.Query(
                [
                    M.Item.id,
                    M.Item.dir,
                    M.Item.filename,
                    M.Item.existing,
                    M.Item.existing_in,
                    M.Container.path.label("container_path"),
                ]
            )
            .join(M.Item.container)
            .filter(M.Item.ingest_id == self.ingest_id)
        )
        return self._iter_query(
            query,
            [M.Container.path.label("container_path"), M.Item.filename],
            T.ItemWithContainerPath,
        )

    def get_items_with_error_count(self) -> typing.Iterable[T.ItemWithErrorCount]:
        """Get all items with the number of realated errors"""
        query = (
            sqla.orm.Query(
                [
                    M.Item.id,
                    M.Item.existing,
                    sqla.sql.func.count(M.Error.id).label("error_cnt"),
                    sqla.sql.func.max(M.Container.error.cast(sqla.Integer))
                    .cast(sqla.Boolean)
                    .label("container_error"),
                    sqla.sql.func.max(M.Container.path).label("container_path"),
                ]
            )
            .outerjoin(M.Item.errors)  # pylint: disable=E1101
            .join(M.Item.container)
            .filter(M.Item.ingest_id == self.ingest_id)
            .group_by(M.Item.id)
        )

        return self._iter_query(query, [M.Item.id], T.ItemWithErrorCount)

    def count_all(self, model_name: str, *conditions: typing.Any) -> int:
        """Get count of tasks/containers/items/deid-logs"""
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        model_cls = getattr(M, model_name)
        conditions = (model_cls.ingest_id == self.ingest_id,) + conditions
        return self.call_db(db_transactions.count_all, model_cls, *conditions)

    def update(
        self, model_name: str, model_id: uuid.UUID, **updates: typing.Any
    ) -> T.Schema:
        """Update a task/container/item"""
        assert model_name in ("Task", "Container", "Item")
        model_cls = getattr(M, model_name)
        return self.call_db(db_transactions.update, model_cls, model_id, **updates)

    def update_ingest_config(self, config: IngestConfig) -> T.Schema:
        """Update ingest config"""
        return self.call_db(
            db_transactions.update,
            M.Ingest,
            self.ingest_id,
            config=config.dict(exclude_none=True),
        )

    def find_one(self, model_name: str, *conditions: typing.Any) -> typing.Any:
        """
        Get a task/container/item/deid-log by the specified key.

        Conditions need to specified in a way that uniquely identify an item.
        """
        assert model_name in self.model_names.values()
        assert conditions
        model_cls = getattr(M, model_name)
        conditions = (model_cls.ingest_id == self.ingest_id,) + conditions
        return self.call_db(db_transactions.find_one, model_cls, *conditions)

    def bulk(
        self, operation: str, model_name: str, mappings: typing.List[dict]
    ) -> None:
        """Bulk add/update tasks/containers/items"""
        assert operation in self.batch_operations
        assert model_name in self.model_names.values()
        model_cls = getattr(M, model_name)
        if operation == "insert":

            def _set_ingest_id(obj):
                obj = copy.copy(obj)
                obj["ingest_id"] = self.ingest_id
                return obj

            mappings = [_set_ingest_id(m) for m in mappings]
        self.call_db(db_transactions.bulk, operation, model_cls, mappings)

    def start_scanning(self) -> T.IngestOut:
        """Set ingest status to scanning and add scan task"""
        ingest = self.call_db(db_transactions.get, M.Ingest, self.ingest_id)
        if T.IngestStatus.is_terminal(ingest.status):
            return ingest
        if self.call_db(db_transactions.has_unfinished_tasks, self.ingest_id):
            return ingest

        return self.call_db(db_transactions.start_scanning, self.ingest_id)

    def start_resolving(self) -> T.IngestOut:
        """Set ingest status to resolving and add resolve task if all scans finished"""
        ingest = self.call_db(db_transactions.get, M.Ingest, self.ingest_id)
        if T.IngestStatus.is_terminal(ingest.status):
            return ingest
        if self.call_db(db_transactions.has_unfinished_tasks, self.ingest_id):
            return ingest

        return self.call_db(
            db_transactions.start_singleton, self.ingest_id, T.TaskType.resolve
        )

    def start_detecting_duplicates(self) -> T.IngestOut:
        """Start detecting duplicates"""
        return self.call_db(
            db_transactions.start_singleton,
            self.ingest_id,
            T.TaskType.detect_duplicates,
        )

    def resolve_subject(self, map_values: typing.List[str]) -> str:
        """Get existing or create new subject code based on the map values"""
        return self.call_db(db_transactions.resolve_subject, self.ingest_id, map_values)

    def start_finalizing(self) -> T.IngestOutAPI:
        """Set ingest status to finalizing and add finalize task if all uploads finished"""
        ingest = self.ingest
        if T.IngestStatus.is_terminal(ingest.status):
            return ingest
        # if ingest is in aborting status, create finalize task without status change
        if ingest.status == T.IngestStatus.aborting:
            return self.call_db(
                db_transactions.start_singleton_wo_status_check,
                self.ingest_id,
                T.TaskType.finalize,
            )
        if self.call_db(db_transactions.has_unfinished_tasks, self.ingest_id):
            return ingest
        return self.call_db(
            db_transactions.start_singleton, self.ingest_id, T.TaskType.finalize
        )

    def set_ingest_status(self, status: T.IngestStatus) -> T.IngestOut:
        """Set ingest status"""
        return self.call_db(db_transactions.set_ingest_status, self.ingest_id, status)

    def fail(self) -> T.IngestOut:
        """Set ingest status to failed and cancel pending tasks"""
        return self.call_db(db_transactions.fail_ingest, self.ingest_id)

    def batch_writer(self, *args, **kwargs) -> "BatchWriter":
        """Get batch writer which is bound to this client"""
        return BatchWriter(self, *args, **kwargs)

    def _iter_query(
        self,
        query: sqla.orm.Query,
        order_by_cols: typing.List[sqla.Column],
        schema: typing.Type[T.Schema],
        size: int = 10000,
    ) -> typing.Iterable[typing.Any]:
        """Get all rows of the given query using seek method"""
        id_col = _get_id_column_from_query(query)
        columns = []
        for col in order_by_cols:
            if isinstance(col, sqla.sql.elements.Label):
                columns.append(col.element)
            else:
                columns.append(col)
        query = seek_query = query.order_by(*order_by_cols, id_col)
        while True:
            count = 0
            item = None
            for item in self.call_db(
                db_transactions.get_all, seek_query.limit(size), schema
            ):
                count += 1
                yield item

            if count < size:
                break

            if item:
                values = []
                for col in order_by_cols:
                    values.append(getattr(item, col.name))
                seek_query = query.filter(
                    sqla.sql.tuple_(*order_by_cols, id_col) > (*values, item.id)
                )
            else:
                break

    # Detect duplicates

    def one_session_container_multiple_study_instance_uid_item_ids(
        self,
    ) -> typing.Set[uuid.UUID]:
        """Get Item IDs where 1 container has different StudyInstanceUIDs"""
        return self.call_db(
            db_transactions.one_container_multiple_uid_item_ids,
            self.ingest_id,
            uid_container_column=M.UID.session_container_id,
            uid_type_column=M.UID.study_instance_uid,
        )

    def one_study_instance_uid_multiple_session_container_item_ids(
        self,
    ) -> typing.Set[uuid.UUID]:
        """Get Item IDs where 1 StudyInstanceUIDs exists in multiple containers"""
        return self.call_db(
            db_transactions.one_uid_multiple_session_container_item_ids,
            self.ingest_id,
            uid_container_column=M.UID.session_container_id,
            uid_type_column=M.UID.study_instance_uid,
        )

    def study_instance_uids_in_new_session_container(self) -> typing.Set[str]:
        """Get StudyInstanceUIDs where the session containers in new"""
        return self.call_db(
            db_transactions.uids_in_new_session_container,
            self.ingest_id,
            uid_container_column=M.UID.session_container_id,
            uid_type_column=M.UID.study_instance_uid,
        )

    def one_acquisition_container_multiple_series_instance_uid_item_ids(
        self,
    ) -> typing.Set[uuid.UUID]:
        """Get Item IDs where 1 container has different SeriesInstanceUIDs"""
        return self.call_db(
            db_transactions.one_container_multiple_uid_item_ids,
            self.ingest_id,
            uid_container_column=M.UID.acquisition_container_id,
            uid_type_column=M.UID.series_instance_uid,
        )

    def one_series_instance_uid_multiple_acquisition_container_item_ids(
        self,
    ) -> typing.Set[uuid.UUID]:
        """Get Item IDs where 1 SeriesInstanceUIDs exists in multiple containers"""
        return self.call_db(
            db_transactions.one_uid_multiple_session_container_item_ids,
            self.ingest_id,
            uid_container_column=M.UID.acquisition_container_id,
            uid_type_column=M.UID.series_instance_uid,
        )

    def series_instance_uids_in_new_acquisition_container(self) -> typing.Set[str]:
        """Get SeriesInstanceUIDs where the acquisition containers in new"""
        return self.call_db(
            db_transactions.series_instance_uids_in_new_acquisition_container,
            self.ingest_id,
        )

    def find_all_items_with_uid(
        self, uid_condition: typing.Any
    ) -> typing.Iterable[T.Schema]:
        """Find item_ids for a given uid filter"""
        query = (
            sqla.orm.Query(
                [
                    M.UID.id,
                    M.UID.item_id,
                    M.UID.session_container_id,
                    M.UID.acquisition_container_id,
                    M.UID.study_instance_uid,
                    M.UID.series_instance_uid,
                ]
            )
            .filter(M.UID.ingest_id == self.ingest_id)
            .filter(uid_condition)
        )

        return self._iter_query(query, [], T.DetectDuplicateItem)

    def duplicated_sop_instance_uid_item_ids(self) -> typing.Set[uuid.UUID]:
        """Get Item IDs with duplicated SOPInstanceUIDs"""
        return self.call_db(
            db_transactions.duplicated_sop_instance_uid_item_ids, self.ingest_id
        )

    def find_all_containers_with_item_id(
        self, item_ids: typing.List
    ) -> typing.Iterable[T.Schema]:
        """Find all the item's containers"""
        query = (
            sqla.orm.Query([M.Item.id, M.Item.container_id])
            .filter(M.Item.ingest_id == self.ingest_id)
            .filter(M.Item.id.in_(item_ids))  # pylint: disable=E1101
        )

        return self._iter_query(query, [], T.ContainerID)

    def get_sidecar_items_with_container(self) -> typing.Iterable[T.Schema]:
        """Find all the item's containers"""
        # pylint: disable=E1101,C0121
        query = (
            sqla.orm.Query([M.Item.id, M.Item.container_id])
            .join(
                M.Error,
                sqla.and_(M.Error.item_id == M.Item.id, M.Error.code.notlike("DD%")),
                isouter=True,
            )
            .filter(M.Item.ingest_id == self.ingest_id)
            .filter(M.Item.skipped == True)
            .having(sqla.sql.func.count(M.Error.id) == 0)
            .group_by(M.Item.id, M.Item.container_id)
        )

        return self._iter_query(query, [M.Item.container_id], T.ContainerID)

    def create_ingest_stats(self):
        """Create TaskStat and ItemStat records"""
        for t_type in T.TaskType:
            stat = M.TaskStat(ingest_id=self.ingest_id, type=t_type.name)
            self.call_db(db_transactions.add, stat)

        stat = M.ItemStat(ingest_id=self.ingest_id)
        self.call_db(db_transactions.add, stat)

    def update_task_stat(self, type_: str, **updates: typing.Any):
        """update task stat"""
        return self.call_db(
            db_transactions.update_task_stat, self.ingest_id, type_, **updates
        )

    def update_item_stat(self, **updates: typing.Any):
        """update item stat"""
        return self.call_db(db_transactions.update_item_stat, self.ingest_id, **updates)

    def reset_task_status(self, task_id: uuid.UUID) -> None:
        """reset a running task's status back to pending"""
        task = self.find_one_task(M.Task.id == task_id)
        if task.status != T.TaskStatus.running:
            return

        self.call_db(
            db_transactions.update, M.Task, task_id, status=T.TaskStatus.pending
        )


class BatchWriter:
    """Batch insert/update writer of a given model"""

    def __init__(
        self,
        db: DBClient,
        operation: str,
        model_name: str,
        depends_on: "BatchWriter" = None,
        batch_size: int = 1000,
    ):
        self.db = db  # pylint: disable=C0103
        self.operation = operation
        self.model_name = model_name
        self.depends_on = depends_on
        self.batch_size = batch_size
        self.changes: typing.List[typing.Any] = []

    def push(self, change: typing.Any) -> None:
        """Push new change"""
        self.changes.append(change)
        if len(self.changes) >= self.batch_size:
            self.flush()

    def flush(self) -> None:
        """Flush all changes"""
        if self.depends_on:
            self.depends_on.flush()
        self.db.bulk(self.operation, self.model_name, self.changes)
        self.changes = []


def _get_id_column_from_query(query: sqla.orm.Query) -> sqla.Column:
    """Get id column from the given query's column descriptions.

    Used to always order rows by a unique column in _iter_query.
    """
    for col_desc in query.column_descriptions:
        if inspect.isclass(col_desc["expr"]):
            return col_desc["expr"].id
        if col_desc["name"] == "id":
            return col_desc["expr"]
    raise ValueError("No id column detected in query")


def _get_paginate_order_by_col(model_cls: M.Base) -> sqla.Column:
    """Determine the primary order by column for a given model.

    If the model has a compound index for the paginator then return the index's second column,
    otherwise the ID column.
    """
    for index in model_cls.__table__.indexes:
        if isinstance(index, sqla.Index) and index.name.endswith("_paginate"):
            col = index.columns.items()[1][1]
            return getattr(model_cls, col.name)
    return model_cls.id


def _csv_field_str(field):
    """Stringify csv fields"""
    value = "" if field is None else str(field)
    if "," in value:
        value = f'"{value}"'
    return value


def deid_logs(deid_profile, logs):
    """Create log output from deid logs"""
    # add fields from all deid file profiles
    fields = ["src_path", "type"]
    for file_profile in deid_profile.file_profiles:
        fields.extend(file_profile.get_log_fields())

    first = True
    for deid_log in logs:
        if first:
            first = False
            header = ",".join(_csv_field_str(field) for field in fields)
            yield f"{header}\n"

        before = {
            "src_path": deid_log.src_path,
            "type": "before",
            **deid_log.tags_before,
        }
        before_row = ",".join(_csv_field_str(before.get(field)) for field in fields)
        yield f"{before_row}\n"

        after = {
            "src_path": deid_log.src_path,
            "type": "after",
            **deid_log.tags_after,
        }
        after_row = ",".join(_csv_field_str(after.get(field)) for field in fields)
        yield f"{after_row}\n"


__all__ = ["DBClient"]
