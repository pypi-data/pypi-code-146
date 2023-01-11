"""Sync queue module"""
import datetime
import logging
import os
import sys
import tempfile
import threading

import fs.filesize

from ..importers.progress_reporter import ProgressReporter
from ..importers.work_queue import Task, WorkQueue
from ..util import confirmation_prompt

log = logging.getLogger(__name__)


# If the file size is less than this threshold, download it rather than
# querying zip members
ZIP_INFO_DOWNLOAD_THRESHOLD = int(
    os.environ.get("FW_ZIP_INFO_DOWNLOAD_THRESHOLD", "5242880")
)


class SyncQueue(WorkQueue):
    """Queue class"""

    def __init__(self, dst, jobs, assume_yes=False, dry_run=False, unpack=False):
        super().__init__({"store": jobs, "delete": 1})
        self.dst = dst
        self.assume_yes = assume_yes
        self.dry_run = dry_run
        self.cleanup = False
        self.unpack = unpack
        self.report = SyncProgressReporter(self)
        self.report.add_group("store", "Syncing", 0)
        self.report.add_group("delete", "Deleting", 0)
        # pylint:disable=consider-using-with
        self.audit_log_fp = tempfile.TemporaryFile(mode="rb+")
        self.audit_log_fp.write(
            b"src_path,dest_path,status,existing,error_message,action_taken\n"
        )

    def store(self, src_file):
        """Add a store task to queue for a source file"""
        self.enqueue(StoreTask(self, src_file))
        self.report.groups["store"].total_bytes += src_file.size

    def delete(self, dst_file):
        """Add a delete task to queue for a destination file"""
        self.enqueue(DeleteTask(self, dst_file))
        self.cleanup = True

    def enqueue(self, task, priority=10):
        super().enqueue(task, priority=priority)
        self.report.groups[task.group].total_count += 1

    def confirm_replace(self, filename):
        """Confirm file replacement"""
        if self.assume_yes or self.dry_run:
            return True
        with self._lock:
            self.report.suspend()
            message = f'Are you sure you want to replace "{filename}"?'
            confirm = confirmation_prompt(message)
            self.report.resume()
            return confirm

    def start(self):
        super().start()
        self.report.start()

    def shutdown(self):
        if self.cleanup:
            self.dst.cleanup()
        super().shutdown()
        self.report.shutdown()
        self.report.final_report()

    def write_audit_log(
        self, src_path, dest_path, status, existing, error_message, action_taken
    ):
        with self._lock:
            self.audit_log_fp.write(
                f"{src_path},{dest_path},{status},{existing},{error_message},{action_taken}\n".encode()
            )


class StoreTask(Task):
    """Store task class"""

    __slots__ = ("queue", "src_file", "bytes_read", "event", "filename")

    def __init__(self, queue, src_file):
        super().__init__("store")
        self.queue = queue
        self.src_file = src_file
        self.bytes_read = 0
        self.event = None
        self.filename = src_file.name

    def execute(self):
        """Compare src and dst (if it exists) and create/update(prompt)/skip as appropriate"""
        # Perform zip storing
        name = self.src_file.name
        log.debug(f"StoreTask for {name} started")
        this_thread = threading.current_thread()
        if self.queue.unpack and self.src_file.is_packed:
            out_path = os.path.dirname(self.queue.dst.file(self.src_file.name).filepath)
            out_exists = os.path.exists(out_path)
            log.debug(
                f"{this_thread.name} Unpacking {self.src_file.name}, exists={out_exists}, size={self.src_file.size}"
            )
            use_local = (
                not out_exists or self.src_file.size < ZIP_INFO_DOWNLOAD_THRESHOLD
            )

            members = self.src_file.get_members(use_local)
            results = set()
            for member in members:
                task_result = self.execute_one(member)
                results.add(task_result)

            self.event = StoreTask.aggregate_status(results)

            log.debug(
                f"{this_thread.name} Done unpacking {len(list(members))} zip members"
            )
        else:
            log.debug(f"{this_thread.name} Storing {self.src_file.name}")
            self.event = self.execute_one(self.src_file)

        if self.event.startswith("skip/"):
            self.skip()

        self.src_file.cleanup()
        self.src_file = None

        log.debug(f"StoreTask for {name} done")

        return None, None

    def execute_one(self, src_file):
        """Execute a single file extraction"""
        dst_file = self.queue.dst.file(src_file.name)
        if not dst_file.stat():
            self.store(src_file, dst_file)
            self.queue.write_audit_log(
                src_path=src_file.name,
                dest_path=dst_file.name,
                status="completed",
                existing="False",
                error_message="",
                action_taken="Created file on destination",
            )
            return "store/create"

        if src_file.size == dst_file.size and src_file.modified <= dst_file.modified:
            self.queue.write_audit_log(
                src_path=src_file.name,
                dest_path=dst_file.name,
                status="skipped",
                existing="True",
                error_message="",
                action_taken="",
            )
            return "skip/stat"

        if self.queue.confirm_replace(src_file.name):
            self.store(src_file, dst_file)
            self.queue.write_audit_log(
                src_path=src_file.name,
                dest_path=dst_file.name,
                status="completed",
                existing="True",
                error_message="",
                action_taken="Updated file on destination",
            )
            return "store/update"

        self.queue.write_audit_log(
            src_path=src_file.name,
            dest_path=dst_file.name,
            status="canceled",
            existing="",
            error_message="",
            action_taken="",
        )
        return "skip/user"

    def store(self, src_file, dst_file):
        """Store source file contents to destination file"""
        if self.queue.dry_run:
            self.bytes_read = src_file.size
        else:
            dst_file.store(src_file)
            self.bytes_read = src_file.bytes_read

    def skip(self):
        """Skip task and notify queue"""
        self.skipped = True
        self.queue.skip_task(task=self)

    def get_bytes_processed(self):
        """Return number of bytes read from the source (equals bytes written to destination)"""
        return self.bytes_read

    def get_desc(self):
        """Return 'store path/to/file'"""
        return f"{self.group} {self.filename}"

    @staticmethod
    def aggregate_status(results):
        """Return the actual status given multiple results"""
        # If any files were created or updated, then it's an update
        if results == {"store/create"}:
            return "store/create"
        if results == {"skip/stat"}:
            return "skip/stat"
        if "store/update" in results:
            return "store/update"
        return "skip/user"


class DeleteTask(Task):
    """Delete task"""

    __slots__ = ("queue", "dst_file")

    def __init__(self, queue, dst_file):
        super().__init__("delete")
        self.queue = queue
        self.dst_file = dst_file

    def execute(self):
        """Delete file on destination"""
        name = self.dst_file.name
        log.debug(f"DeleteTask for {name} started")
        if not self.queue.dry_run:
            self.dst_file.delete()
        self.dst_file = None
        self.queue.write_audit_log(
            src_path="",
            dest_path=name,
            status="completed",
            existing="",
            error_message="",
            action_taken="Deleted from destination",
        )
        log.debug(f"DeleteTask for {name} done")
        return None, None

    def get_bytes_processed(self):
        """Return one (representing a single file instead of bytes)"""
        return 1

    def get_desc(self):
        """Return 'delete path/to/file'"""
        return f"{self.group} {self.dst_file.name}"


class SyncProgressReporter(ProgressReporter):
    """Sync progress reporter class"""

    def report(self, newline="\r"):
        messages = []
        compare_total = compared_count = 0
        for name, group in self.groups.items():
            compare_total += group.total_count
            compared_count += group.completed
            unskipped_count = group.total_count - group.skipped
            if unskipped_count > 0:
                if group.completed == group.total_count:
                    speed_str = "DONE"
                elif name == "store":
                    speed_str = fs.filesize.traditional(group.bytes_per_sec) + "/s"
                elif name == "delete":
                    # NOTE reusing group.bytes_per_sec for tracking deleted / sec
                    # TODO in-depth subclassing of WorkQueue for appropriate attribute name
                    speed_str = f"{group.bytes_per_sec:.2f}/s"
                messages.append(
                    f"{group.desc} {group.completed}/{group.total_count} - {speed_str}"
                )
        if self.queue.dry_run:
            if compared_count == compare_total:
                status_str = "DONE"
            else:
                status_str = f"{compared_count}/{compare_total}"
            message = f"Comparing source and destination - {status_str}"
        elif messages:
            message = ", ".join(messages)
        else:
            return
        sys.stdout.write(message.ljust(self.columns) + newline)
        sys.stdout.flush()

    def final_report(self):
        self.sample()
        self.report(newline="\n")

        create_count = update_count = 0
        for task in self.queue.completed:
            if isinstance(task, StoreTask) and task.event == "store/create":
                create_count += 1
            elif isinstance(task, StoreTask) and task.event == "store/update":
                update_count += 1
        delete_count = self.groups["delete"].completed
        skip_count = self.groups["store"].skipped
        cancel_count = sum(
            group.total_count - group.completed for group in self.groups.values()
        )
        transfer_bytes = self.groups["store"].completed_bytes
        if transfer_bytes > 0:
            xfer_bytes = fs.filesize.traditional(transfer_bytes)
            xfer_files = create_count + update_count
            if self.queue.dry_run:
                xfer_msg = f"Would transfer {xfer_bytes} across {xfer_files} files"
            else:
                xfer_time = self.format_timedelta(
                    datetime.datetime.now() - self._start_time
                )
                xfer_msg = (
                    f"Transferred {xfer_bytes} across {xfer_files} files in {xfer_time}"
                )
            print(xfer_msg.ljust(self.columns))
        messages = []
        if create_count > 0:
            messages.append(f"create {create_count}")
        if update_count:
            messages.append(f"update {update_count}")
        if delete_count:
            messages.append(f"delete {delete_count}")
        if skip_count:
            messages.append(f"skip {skip_count}")
        if cancel_count:
            messages.append(f"cancel {cancel_count}")
        message = ", ".join(messages)
        print(f"Sync summary: {message}".ljust(self.columns))

    @staticmethod
    def format_timedelta(timedelta):
        """Return human-readable str given a datetime.timedelta"""
        seconds = timedelta.total_seconds()
        if seconds < 60:
            return f"{seconds:.2f} seconds"
        return str(datetime.timedelta(seconds=int(seconds)))
