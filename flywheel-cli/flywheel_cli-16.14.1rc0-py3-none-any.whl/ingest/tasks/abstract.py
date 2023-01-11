"""Provides the abstract Task class."""
import datetime
import json
import logging
import os
import sys
import time
import traceback
import typing
from abc import ABC, abstractmethod

import flywheel
from fs import errors as fs_errors

from ... import errors as base_errors
from ... import util
from .. import config, errors
from .. import schemas as T
from ..client import DBClient

log = logging.getLogger(__name__)


class Task(ABC):
    """Abstract ingest task interface"""

    # task can be retried or not in case of failure
    can_retry = False

    def __init__(
        self,
        db: DBClient,
        task: T.TaskOut,
        worker_config: config.WorkerConfig,
        is_local: bool,
    ):
        self.db = db  # pylint: disable=C0103
        self.task = task
        self.worker_config = worker_config
        self.ingest = self.db.ingest
        self.ingest_config = self.ingest.config
        self.strategy_config = self.ingest.strategy_config
        self.walker = None
        self.last_report = {
            "time": None,
            "completed": self.task.completed,
            "total": self.task.total,
        }
        self.is_local = is_local

    @abstractmethod
    def _run(self):
        """Task specific implementation."""

    def _initialize(self):
        """Initialize the task before execution."""

    def _on_success(self):
        """Called when the task completed successfully"""

    def _on_error(self):
        """Called when the task ultimately failed"""

    def _on_aborting(self):
        """Called when ingest is in aborting status."""
        self.db.start_finalizing()

    def run(self):
        """Execute the task."""
        try:
            self.walker = self.ingest_config.create_walker()
            self._initialize()
            self._run()
            self.report_progress(force=True)
            self.db.update_task(self.task.id, status=T.TaskStatus.completed)
            if self.db.ingest.status == T.IngestStatus.aborting:
                self._on_aborting()
            else:
                self._on_success()

        except Exception as exc:  # pylint: disable=broad-except
            exc_type, _, exc_tb = sys.exc_info()
            filename, linenum, _, _ = traceback.extract_tb(exc_tb)[-1]

            trace = []
            for frame in traceback.extract_tb(exc_tb):
                head, tail = os.path.split(frame.filename)
                trace.append(
                    f"{os.path.basename(head)}/{os.path.splitext(tail)[0]}:{frame.lineno}"
                )
            trace = "->".join(trace)

            exc_details_dict = {
                "filename": filename,
                "line number": linenum,
                "type": exc_type.__qualname__,
                "message": str(exc),
                "timestamp": datetime.datetime.utcnow().isoformat(),
            }

            if isinstance(exc, flywheel.ApiException):
                # pylint: disable=no-member
                log.debug(
                    f"Got ApiException: {exc.body}",
                    exc_info=True,
                )
                try:
                    response = json.loads(exc.body)  # pylint: disable=no-member
                    if isinstance(response, dict) and response.get("request_id", None):
                        exc_details_dict[
                            "message"
                        ] += f", Request ID: {response.get('request_id')}"
                except json.JSONDecodeError:
                    pass

            exc_details = ", ".join([f"{k}: {v}" for k, v in exc_details_dict.items()])

            if self.should_retry(exc):
                self.db.update_task(
                    self.task.id,
                    status=T.TaskStatus.pending,
                    retries=self.task.retries + 1,
                )
                exc_type = exc.__class__.__name__
                log.debug(
                    f"Task failed {exc_details}, retrying later ({self.task.retries + 1})",
                    exc_info=True,
                )
            else:
                log.debug("Task failed", exc_info=True)
                self.db.update_task(self.task.id, status=T.TaskStatus.failed)
                self.add_task_error(exc_details, exc, trace)
                self._on_error()
        finally:
            # always close the walker to cleanup tempfolder
            # TODO: cache scanned files and reuse during upload
            if self.walker:
                # only close the walker if we could open it
                self.walker.close()

    def add_task_error(self, exc_details: str, exc: Exception, trace: str):
        """Add task error"""
        if isinstance(exc, fs_errors.CreateFailed):
            error = errors.InvalidSourcePath
            msg = str(exc)
        elif isinstance(exc, errors.BaseIngestError):
            error = exc
            msg = exc.message
        elif isinstance(exc, base_errors.S3AccessDeniedError):
            error = errors.S3AccessDeniedError
            if self.is_local:
                msg = f"User {exc.s3_user} cannot perform scan on {exc.s3_location} "
            else:
                msg = f"Access denied. The specified cluster does not have permission to access: {exc.s3_location}"
        else:
            error = errors.BaseIngestError
            msg = exc_details
            msg += f"[{trace}]"
        self.db.add(
            T.Error(
                task_id=self.task.id,
                item_id=self.task.item_id,
                code=error.code,
                message=msg,
            )
        )

    def report_progress(
        self,
        completed: typing.Optional[int] = None,
        total: typing.Optional[int] = None,
        force: typing.Optional[bool] = False,
    ):
        """Report task progress"""
        last_time = self.last_report["time"]
        last_completed = self.last_report["completed"]
        last_total = self.last_report["total"]
        if completed:
            self.task.completed += completed
        if total:
            self.task.total += total
        if self.task.completed > self.task.total:
            self.task.total = self.task.completed
        if self.task.completed == last_completed and self.task.total == last_total:
            # no update needed
            return
        if not last_time or time.time() - last_time > 1 or force:
            self.db.update_task(
                self.task.id, completed=self.task.completed, total=self.task.total
            )

            self.last_report.update(
                {
                    "time": time.time(),
                    "completed": self.task.completed,
                    "total": self.task.total,
                }
            )

    def should_retry(self, exc):
        """Determine that task should be retried or not"""
        should_retry = self.can_retry
        if isinstance(exc, flywheel.ApiException):
            # we should not retry for example in case of a 400 Bad Request
            should_retry = should_retry and exc.status in (429, 502, 503, 504)
        return should_retry and self.task.retries < self.ingest_config.max_retries

    def _set_deid_profile(self, profile):
        if self.ingest_config.de_identify and self.ingest_config.deid_profile:
            raise errors.BaseIngestError(
                "Deid-profile is configured on the server, can't override."
            )

        if "name" not in profile:
            profile["name"] = "server_deid_profile"

        self.ingest_config.de_identify = True
        self.ingest_config.deid_profile = profile["name"]
        self.ingest_config.deid_profiles = [profile]
        self.ingest_config.deid_is_from_server = True

        self.db.update_ingest_config(self.ingest_config)

    @property
    def fw(self):
        """Get flywheel SDK client"""
        return util.get_sdk_client(self.db.api_key)
