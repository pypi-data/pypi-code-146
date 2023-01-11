"""Ingest progress reporter"""
import datetime as dt
import logging
import os
import sys
import time
import typing

import crayons
import tzlocal

from .. import config as root_config
from .. import util
from . import schemas as T
from .client.abstract import Client
from .config import ReporterConfig
from .container_tree import ContainerTree

log = logging.getLogger(__name__)


class Reporter:
    """Ingest progress reporter"""

    def __init__(self, client: Client, config: ReporterConfig):
        self._fh = sys.stdout
        self.client = client
        self.config = config
        self.mode = os.fstat(sys.stdout.fileno()).st_mode
        # state
        self.last_reported_status_idx = -1
        self.last_reported_status_name = None
        self.eta_report: typing.Optional[T.ReportETA] = None
        self.ingest: typing.Optional[T.IngestOut] = None
        self.progress: typing.Optional[T.Progress] = None

        self.max_status_length = max(len(s.name) for s in T.IngestStatus)
        self.last_update_time = time.time()

    def run(self):
        """Report progress"""
        self.update_progress()

        while not T.IngestStatus.is_terminal(self.ingest.status):
            self.update_progress()
            self.print_status_history()
            time.sleep(1)

        self.final_report()

    def update_progress(self):
        """Update ingest and ingest progress"""
        self.ingest = self.client.ingest
        if (
            self._has_to_update()
            or self.last_reported_status_name != self.ingest.status
        ):
            self.progress = self.client.progress
            self.last_update_time = time.time()

    def final_report(self):
        """Print final report"""
        self.update_progress()
        self.print_status_history(follow=False)
        self.print_final_report()
        log.debug("Ingest done, collecting logs...")
        self.save_reports()
        if (
            self.ingest.status == T.IngestStatus.finished
            and not self.client.report.errors
        ):
            sys.exit(0)
        else:
            sys.exit(1)

    def print_status_history(self, follow=True):
        """Print report of every status since previous status"""
        for idx, status in enumerate(self.ingest.history):
            self.eta_report = None  # reset repvious eta report
            if self.last_reported_status_idx >= idx:
                continue
            st_name, timestamp = status
            timestamp = dt.datetime.fromtimestamp(timestamp, tz=tzlocal.get_localzone())

            self.last_reported_status_idx = idx
            self.last_reported_status_name = st_name

            self.print_status_header(st_name, timestamp)
            report_method = getattr(self, f"report_{st_name}_status", None)
            if report_method:
                report_method(follow=follow)
            elif not T.IngestStatus.is_terminal(st_name):
                self.report_status(T.IngestStatus.get_item(st_name), follow=follow)
            self.print("")  # start new line

    def report_in_review_status(self, follow=True, max_nodes=100):
        """Print summary report of review stage"""
        self.print("Hierarchy:")

        if self.config.verbose:
            self.print(f"Maximum {max_nodes} containers are displayed.\n")
            container_factory = ContainerTree()
            for container in self.client.tree:
                container_factory.add_node(container)
                if len(container_factory.nodes) >= max_nodes:
                    break
            container_factory.print_tree(fh=self._fh)
            self.print("")  # new line

        summary = self.client.summary
        for k, v in summary.dict().items():
            if k in ["errors", "warnings"]:
                continue
            self.print(f"  {k.capitalize()}: {v}")

        self.print("")  # new line

        if summary.warnings:
            self.print("Warnings summary:")
            for error in summary.warnings:
                self.print(f"  {error.message} ({error.code}): {error.count}")
            self.print("")  # new line

        if summary.errors:
            self.print("Errors summary:")
            for error in summary.errors:
                self.print(f"  {error.message} ({error.code}): {error.count}")
            self.print("")  # new line

        if not follow or self.ingest.status != T.IngestStatus.in_review:
            # do not prompt if status is not in_review
            return

        fw = util.get_sdk_client_for_current_user()
        confirmation_prompt = f"Confirm upload to {fw.host}?"
        if self.config.assume_yes or util.confirmation_prompt(confirmation_prompt):
            self.client.review()
        else:
            self.client.abort()

    def report_status(self, status, follow=True):
        """Report progress of the given status until ingest is in that status"""
        # reset previous eta
        while follow and self.ingest.status == status:
            self.print_progress(status)
            self.update_progress()

            time.sleep(1)

        self.print_progress(status, last=True)
        print_status_summary = getattr(self, f"print_{status.name}_summary", None)
        if print_status_summary:
            print_status_summary()

    def print_progress(self, status, last=False):
        """Print progress of the given status"""

        def default_counts():
            progress = getattr(self.progress.stages, status.name, None)
            if not progress or not progress.total:
                return None, None
            return progress.completed, progress.total

        get_counts = getattr(self, f"get_{status.name}_progress_counts", default_counts)
        finished, total = get_counts()
        if not total:
            return
        msg = f"{round(finished/total*100, 2)}%"
        format_msg = getattr(self, f"format_{status.name}_progress", None)
        if format_msg:
            msg = format_msg(msg)

        elapsed_time = util.hrtime(self.get_status_elpased_time(status))

        if not last:
            eta = self.compute_eta(finished, total, status)
            eta = util.hrtime(eta) if eta is not None else "~"
            msg = f"{msg} (elapsed: {elapsed_time}|ETA: {eta})"
        else:
            msg = f"{msg} ({elapsed_time})"

        self.print(msg, replace=True)
        if last:
            self.print("")

    def get_scanning_progress_counts(self):
        """Get scanning progress counts (finished, total)"""
        finished = (
            self.progress.scans.finished + self.progress.stages.scanning.completed
        )
        total = self.progress.scans.total + self.progress.stages.scanning.total

        return finished, total

    def format_scanning_progress(self, msg):
        """Format scanning progress message"""
        finished, total = self.get_scanning_progress_counts()
        msg = f"{finished}/{total} files"
        if self.progress.bytes.total > 0:
            size = util.hrsize(self.progress.bytes.total)
            msg = f"{msg}, {size}"

        return msg

    def get_uploading_progress_counts(self):
        """Get uploading progress counts (finished, total)"""
        finished = self.progress.items.finished + self.progress.items.skipped
        total = self.progress.items.total
        return finished, total

    def print_uploading_summary(self):
        """Print upload summary"""
        exclude = ["finished"]
        for status, count in self.progress.items.dict().items():
            if count > 0 and status not in exclude:
                self.print(f"{status.capitalize()}: {count}")

    def format_uploading_progress(self, msg):
        """Format uploading progress message"""
        return f"{msg} - ({self.progress.items.failed} failed)"

    def print_final_report(self):
        """Print final report of the ingest"""
        self.print(str(crayons.magenta("Final report", bold=True)))
        report = self.client.report
        if report.errors or report.warnings:
            self.print("")  # new line
        if report.errors:
            self.print("The following errors happened:")
            for error in report.errors:
                self.print(f"{error.type}: {error.message} ({error.code})")
            self.print("")  # new line
        if report.warnings:
            self.print("The following warnings happened:")
            for error in report.warnings:
                self.print(f"{error.type}: {error.message} ({error.code})")
            self.print("")  # new line

        total_elapsed = 0
        for st_elapsed in report.elapsed.values():
            total_elapsed += st_elapsed

        self.print(f"Total elapsed time: {util.hrtime(total_elapsed)}")

    def print(self, msg, replace=False):
        """Print"""
        if replace:
            msg = f"\r{msg}\033[K"
        else:
            msg = f"{msg}\n"
        self._fh.write(msg)
        self._fh.flush()

    def print_status_header(self, status, timestamp):
        """Print status header"""
        status_name = (
            status.replace("_", " ").capitalize().ljust(self.max_status_length)
        )
        status_name = str(crayons.magenta(status_name, bold=True))
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        self.print(f"{status_name}[{timestamp}]")

    def save_reports(self):
        """Save audit/deid logs and subjects csv if it was requested"""
        for type_ in ("audit_logs", "deid_logs", "subjects"):
            path = getattr(self.config, f"save_{type_}")
            if not path:
                continue
            stream = getattr(self.client, type_)
            final_path = self.save_stream_to_file(stream, path, type_)
            self.print(f"Saved {type_.replace('_', ' ')} to {final_path}")

    @staticmethod
    def save_stream_to_file(stream, path, prefix, extension="csv"):
        """Save stream to file"""
        error = None
        try:
            path = util.get_filepath(path, prefix=prefix, extension=extension)
        except FileNotFoundError as exc:
            error = str(exc)
            path = util.get_filepath(root_config.LOG_FILE_DIRPATH, prefix=prefix)
        except FileExistsError:
            error = f"File already exists: {path}"
            path = util.get_incremental_filename(path)

        with open(path, "w", encoding="utf-8") as fp:
            for line in stream:
                fp.write(line)

        if error:
            msg = f"{error}. Fallback to: {path}"
            log.error(msg)

        return path

    def compute_eta(
        self, finished: int, total: int, status: T.IngestStatus
    ) -> typing.Optional[dt.timedelta]:
        """Compute ETA"""
        prev = self.eta_report
        if prev and finished == prev.finished and total == prev.total:
            # no changes so just reduce ETA with the elapsed time since the previous report
            report_time = time.time()
            new_eta = prev.eta - (report_time - prev.report_time)

            self.eta_report = T.ReportETA(
                eta=max(new_eta, 0),
                report_time=report_time,
                finished=prev.finished,
                total=prev.total,
            )
        else:
            elapsed_time = self.get_status_elpased_time(status)
            if not elapsed_time or not finished:
                # status is not in history
                return None

            remaining_time = (elapsed_time / finished) * (total - finished)

            self.eta_report = T.ReportETA(
                eta=remaining_time,
                report_time=time.time(),
                total=total,
                finished=finished,
            )

        return self.eta_report.eta

    def get_status_elpased_time(self, status: T.IngestStatus) -> int:
        """Return when the given status started"""
        for old, new in reversed(
            list(zip(self.ingest.history, self.ingest.history[1:]))
        ):
            # status has prev case
            old_status, old_timestamp = old
            _, new_timestamp = new
            if old_status == status:
                # status is not the last one
                return new_timestamp - old_timestamp
        try:
            last_status, last_timestamp = self.ingest.history[-1]
        except IndexError:
            return 0
        if last_status == status:
            # status is the last one
            return time.time() - last_timestamp
        return 0

    def _has_to_update(self) -> bool:
        if time.time() - self.last_update_time > self.config.refresh_interval:
            return True
        return False
