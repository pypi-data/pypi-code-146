"""Provides AbstractScanner class"""

import logging
from abc import ABC, abstractmethod

import fs

from .. import errors
from .. import schemas as T

log = logging.getLogger(__name__)


class AbstractScanner(ABC):
    """Provides common interface for scanners"""

    def __init__(  # pylint: disable=R0913
        self,
        ingest_config,
        strategy_config,
        worker_config,
        walker,
        opts=None,
        context=None,
        get_subject_code_fn=None,
        report_progress_fn=None,
    ):
        self.ingest_config = ingest_config
        self.strategy_config = strategy_config
        self.worker_config = worker_config
        self.walker = walker
        self.opts = opts
        self.context = context
        self.get_subject_code_fn = get_subject_code_fn
        self.report_progress_fn = report_progress_fn
        self.file_errors = []

    @abstractmethod
    def _scan(self, subdir):
        """Scanner specific implementation"""

    def _initialize(self):
        """Initialize scanner"""

    def scan(self, dirpath):
        """Run scan"""
        self._initialize()

        yield from self._scan(dirpath)

        for error in self.file_errors:
            yield error

    def iter_files(self, dirpath, report_progress=False):
        """Yield files from the given dir and filter out zero byte files"""
        if report_progress:
            # make progress report optional since we don't want to slow down for example
            # a template scanner which doesn't download any files
            files_count = len(list(self.walker.list_files(dirpath)))
            # set total file count
            self.report_progress(total=files_count)

        for fileinfo in self.walker.list_files(dirpath):
            if fileinfo.size == 0:
                filepath = fs.path.join(dirpath, fileinfo.name)
                log.debug(f"Skipped zero byte file: {filepath}")
                self.file_errors.append(
                    T.Error(
                        code=errors.ZeroByteFile.code,
                        message=errors.ZeroByteFile.message,
                        filepath=filepath,
                    )
                )
            else:
                yield fileinfo

            if report_progress:
                # update progress
                self.report_progress(completed=1)

    def report_progress(self, *args, **kwargs):
        """
        Report progress by calling report progress function passed in the constructor.

        If no report progress function, it is a noop.
        """
        if callable(self.report_progress_fn):
            self.report_progress_fn(*args, **kwargs)

    @staticmethod
    def context_merge_subject_and_session(context):
        """Merge session & subject labels"""
        merged = False
        if "session" in context and "label" in context["session"]:
            context.setdefault("subject", {})["label"] = context["session"]["label"]
            merged = True
        if not merged and "subject" in context and "label" in context["subject"]:
            context.setdefault("session", {})["label"] = context["subject"]["label"]
            merged = True
        return merged

    @staticmethod
    def validate_opts(opts):
        """Validate the scanner options, raising a ValueError if invalid"""
