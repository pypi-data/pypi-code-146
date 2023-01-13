"""Integration for Celery."""

from typing import Callable, Optional
from os import environ
from functools import wraps
from pathlib import Path
from shutil import rmtree

from celery import current_task  # type: ignore

from ..api import profile_job as orig_profile_job

__all__ = ["profile"]


def _cleanup_reports(base_reports_path: Optional[Path], max_reports: int):
    """Delete old reports."""
    if base_reports_path is None:
        return

    # Find all reports:
    reports = []
    for report in base_reports_path.glob("*/*"):
        if report.is_dir() and (report / "peak-memory.prof").exists():
            reports.append(report)

    # Sort by modification time:
    reports.sort(key=lambda report: report.stat().st_mtime)

    # Delete all but max_reports:
    for report in reports[:-max_reports]:
        rmtree(report)


def profile(f: Callable):
    """
    Decorator for Celery tasks.  Make sure to use ``bind=True`` on the task.

    For example:

        @task
        @profile
        def your_task(self, x, y):
            return x + y

    Reports will be stored in directory in environment variable
    SCIAGRAPH_CELERY_REPORTS_PATH, in subdirectory ``<task name>/<task id>``.

    The environment variable SCIAGRAPH_CELERY_MAX_REPORTS sets how many reports
    will be kept over time, with the oldest deleted first. The default is 1000.
    """
    max_reports = int(environ.get("SCIAGRAPH_CELERY_MAX_REPORTS", 1000))
    assert max_reports > 0
    base_reports_path_orig = environ.get("SCIAGRAPH_CELERY_REPORTS_PATH", None)
    if base_reports_path_orig is not None:
        base_reports_path = Path(base_reports_path_orig).absolute()
    else:
        base_reports_path = None

    @wraps(f)
    def decorator(*args, **kwargs):
        task_id = str(current_task.request.id)
        task_name = str(current_task.name)
        job_id = f"{task_name}/{task_id}"
        report_path = (
            None
            if base_reports_path is None
            else base_reports_path / task_name / task_id
        )
        if report_path is not None:
            report_path.mkdir(parents=True, exist_ok=True)
        try:
            with orig_profile_job(job_id, report_path):
                return f(*args, **kwargs)
        finally:
            _cleanup_reports(base_reports_path, max_reports)

    return decorator
