"""Public API for interacting with Sciagraph."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Union
import logging
from dataclasses import dataclass, asdict
from os import PathLike, makedirs
from pathlib import Path
from ctypes import PyDLL, py_object
from contextlib import contextmanager
import sys

__all__ = ["ReportResult", "set_job_id"]

_LOGGER = logging.getLogger("sciagraph")


_DOWNLOAD_INSTRUCTIONS = """\
To download the report, run the following on Linux/Windows/macOS, Python 3.7+.

If you're inside a virtualenv:

    pip install --upgrade sciagraph-report

Otherwise:

    pip install --user --upgrade sciagraph-report

Then:

    python -m sciagraph_report download {download_key} {decryption_key}

If you have trouble installing sciagraph-report, please read the documentation:

https://sciagraph.com/docs/howto/reports/
"""

_FINAL_DOWNLOAD_INSTRUCTIONS = (
    """\
Successfully uploaded an encrypted Sciagraph profiling report.

Job start time: {job_time}
Job ID: {job_id}

{local_storage}"""
    + _DOWNLOAD_INSTRUCTIONS
)


_STORAGE_INSTRUCTIONS = """\
Successfully stored the Sciagraph profiling report.

Job start time: {job_time}
Job ID: {job_id}

The report was stored in {report_path}{addendum}
"""

_TRIAL_MODE_ADDENDUM = """

WARNING: You are running in trial mode, which limits you to profiling only the
first 60 seconds of a job. To profile jobs of unlimited length, read the docs
on setting up Sciagraph for production:

https://www.sciagraph.com/docs/howto/setup
"""


@dataclass
class ReportResult:
    """
    Information about how to download uploaded profiling report.

    This will get logged by Sciagraph when profiling is finished.
    """

    job_time: str
    job_id: str
    peak_memory_kb: int
    download_key: Optional[str]
    decryption_key: Optional[str]
    report_path: Optional[Path]
    # Private attribute for now, don't rely on it:
    _trial_mode: bool

    def __str__(self):
        if self.download_key is not None and self.decryption_key is not None:
            if self.report_path is not None:
                local_storage = (
                    f"The report was stored locally at path {self.report_path}\n\n"
                )
            else:
                local_storage = ""
            return _FINAL_DOWNLOAD_INSTRUCTIONS.format(
                **asdict(self), local_storage=local_storage
            )
        else:
            data = asdict(self)
            if self._trial_mode:
                data["addendum"] = _TRIAL_MODE_ADDENDUM
            else:
                data["addendum"] = ""
            return _STORAGE_INSTRUCTIONS.format(**data)


_UNKNOWN_JOB_ID = "Unknown, see docs to learn how to set this"


def _log_result(
    job_secs_since_epoch: int,
    job_id: Optional[str],
    download_key: Optional[str],
    decryption_key: Optional[str],
    report_path: Optional[Path],
    trial_mode: bool,
    peak_memory_kb: int,
):
    """Log a ``ReportResult``."""
    if job_id is None:
        job_id = _UNKNOWN_JOB_ID
    job_time = datetime.fromtimestamp(job_secs_since_epoch, timezone.utc).isoformat()
    report = ReportResult(
        job_time=job_time,
        job_id=job_id,
        download_key=download_key,
        decryption_key=decryption_key,
        report_path=report_path,
        _trial_mode=trial_mode,
        peak_memory_kb=peak_memory_kb,
    )
    _LOGGER.warning(report)


def _load_module(name: str):
    """Load a Python module from the pre-loaded Sciagraph shared library."""
    if name in sys.modules:
        return sys.modules[name]
    # The symbols in the current running process:
    this = PyDLL(None)
    try:
        f = getattr(this, f"PyInit_{name}")
    except AttributeError:
        # We're not running under Sciagraph:
        assert getattr(this, "sciagraph_initialize", None) is None
        return None
    f.restype = py_object
    module = f()
    sys.modules[name] = module
    return module


_sciagraph_jobs = _load_module("_sciagraph_jobs")


def _ensure_parent_process():
    """Using Sciagraph APIs from a child process is a bug in user code."""
    if _sciagraph_jobs:
        if not _sciagraph_jobs.is_parent_process():
            raise RuntimeError("Sciagraph APIs cannot be used from child processes")


def set_job_id(job_id: str):
    """
    Set the current job's ID; it will then be included in the resulting report
    and logged message.
    """
    _ensure_parent_process()
    if _sciagraph_jobs:
        _sciagraph_jobs.set_job_id(job_id)


def _start_job(job_id: str, output_path: Optional[Union[PathLike, str]] = None):
    """
    Start a new job.
    """
    _ensure_parent_process()
    if output_path is not None:
        output_path = str(output_path)
    if _sciagraph_jobs:
        if output_path is not None:
            makedirs(output_path, exist_ok=True)
        _sciagraph_jobs.start_job(job_id, output_path)


def _finish_job():
    """
    Finish the current job.
    """
    _ensure_parent_process()
    if _sciagraph_jobs:
        _sciagraph_jobs.finish_job()


@contextmanager
def profile_job(job_id: str, output_path: Union[PathLike, str]):
    """
    A context manager that starts a job on entry and finishes it on exit.
    """
    _start_job(job_id, output_path)
    try:
        yield
    finally:
        _finish_job()


@dataclass
class JobStatus:
    """The status of the current job, if any."""

    job_id: str
    download_key: str
    decryption_key: str
    peak_memory_kb: int

    def instructions(self) -> str:
        """Return download instructions."""
        if self.download_key == "N/A":
            return "No download instructions available at this time."
        return (
            "When this job finishes, a report will be uploaded.\n"
            + _DOWNLOAD_INSTRUCTIONS.format(**asdict(self))
        )

    @staticmethod
    def _empty():
        """Create an empty JobStatus."""
        return JobStatus("N/A", "N/A", "N/A", peak_memory_kb=0)


def job_status() -> JobStatus:
    """
    Return the status of the current job, if any.

    The download and decryption key may not be available immediately, until
    registration with the backend server succeeds.  If no job is currently
    running, the values will be meaningless.
    """
    if not _sciagraph_jobs:
        return JobStatus._empty()

    status_dict = _sciagraph_jobs.job_status()
    if not status_dict["in_job"]:
        return JobStatus._empty()

    return JobStatus(
        job_id=status_dict["id"],
        download_key=status_dict["download_key"],
        decryption_key=status_dict["decryption_key"],
        peak_memory_kb=status_dict["peak_memory_kb"],
    )
