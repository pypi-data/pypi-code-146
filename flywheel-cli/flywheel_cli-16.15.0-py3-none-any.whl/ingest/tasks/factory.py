"""Provides factory method to create tasks."""

from .configure import ConfigureTask
from .detect_duplicates import DetectDuplicatesTask
from .extract_uid import ExtractUIDTask
from .finalize import FinalizeTask
from .prepare import PrepareTask
from .prepare_sidecar import PrepareSidecarTask
from .resolve import ResolveTask
from .scan import ScanTask
from .upload import UploadTask

TASK_MAP = {
    "configure": ConfigureTask,
    "scan": ScanTask,
    "extract_uid": ExtractUIDTask,
    "resolve": ResolveTask,
    "detect_duplicates": DetectDuplicatesTask,
    "prepare": PrepareTask,
    "prepare_sidecar": PrepareSidecarTask,
    "upload": UploadTask,
    "finalize": FinalizeTask,
}


def create_task(client, task, worker_config, is_local):
    """Create executable task from task object"""
    task_cls = TASK_MAP.get(task.type)
    if not task_cls:
        raise Exception(f"Invalid task type: {task.type}")
    return task_cls(client, task, worker_config, is_local)
