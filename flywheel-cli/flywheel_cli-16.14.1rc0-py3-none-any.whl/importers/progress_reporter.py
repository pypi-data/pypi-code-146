"""Provides progress reporter for threaded jobs"""
import collections
import sys
import threading
from abc import ABC
from datetime import datetime

import fs.filesize


class GroupStats:
    """GroupStats class"""

    # pylint: disable=too-few-public-methods
    def __init__(self, desc, total_count):
        self.desc = desc
        self.total_count = total_count
        self.total_bytes = 0
        self.completed = 0
        self.completed_bytes = 0
        self.skipped = 0

        self.samples = collections.deque()
        self.bytes_per_sec = 0


class ProgressReporter(ABC):
    """Thread that prints upload progress"""

    def __init__(self, queue, average_samples=10, sample_time=0.5, columns=80):
        self.queue = queue

        self.groups = collections.OrderedDict()

        self.completed_bytes = 0
        self.total_bytes = 0
        self.uploaded_files = 0
        self.pending_filename = ""

        self.sample_time = sample_time
        self.average_samples = average_samples
        self.columns = columns

        self._suspended = False
        self._running = False
        self._thread = None
        self._shutdown_event = threading.Event()
        self._start_time = datetime.now()

    def add_group(self, name, desc, total_count):
        """Initialize GroupStats for a group and adds it to groups"""
        self.groups[name] = GroupStats(desc, total_count)

    def start(self):
        """Starts progress report thread"""
        self._running = True
        self._suspended = False
        self._thread = threading.Thread(target=self.run, name="progress-report-thread")
        self._thread.daemon = True
        self._thread.start()

    def suspend(self):
        """Suspend progress report thread"""
        self._suspended = True

        message = " " * self.columns + "\r"
        sys.stdout.write(message)
        sys.stdout.flush()

    def resume(self):
        """Resume suspended progress report thread"""
        self._suspended = False

    def shutdown(self):
        """Shut down progress report thread"""
        self._running = False
        self._shutdown_event.set()
        self._thread.join()

    def run(self):
        """Report progress"""
        while True:
            self._shutdown_event.wait(self.sample_time)
            if not self._running:
                return

            self.sample()
            if not self._suspended:
                self.report()

    def sample(self):
        """Takes a sample from a group's stats"""
        # Get current stats
        current_stats = self.queue.get_stats()
        sample_time = datetime.now()

        for group, stats in current_stats.items():
            # Take a sample from each group for averaging
            group_stats = self.groups[group]
            group_stats.skipped = stats.get("skipped", 0)
            group_stats.completed = stats.get("completed", 0)
            group_stats.completed_bytes = stats.get("completed_bytes", 0)
            group_stats.samples.append((sample_time, group_stats.completed_bytes))

            # Prune older samples
            while len(group_stats.samples) > self.average_samples:
                group_stats.samples.popleft()

            # Calculate the average between the oldest and newest
            if len(group_stats.samples) > 1:
                t1, s1 = group_stats.samples[0]
                t2, s2 = group_stats.samples[-1]

                dt = (t2 - t1).total_seconds()
                ds = s2 - s1

                group_stats.bytes_per_sec = ds / dt

    def report(self, newline="\r"):
        """Progress report"""
        messages = []

        for group in self.groups.values():
            total_count = group.total_count - group.skipped
            if total_count > 0:
                if group.completed == total_count:
                    bps = "DONE"
                else:
                    bps = fs.filesize.traditional(group.bytes_per_sec) + "/s"
                messages.append(f"{group.desc} {group.completed}/{total_count} - {bps}")

        message = ", ".join(messages).ljust(self.columns) + newline

        sys.stdout.write(message)
        sys.stdout.flush()

    def final_report(self):
        """Final summarized report"""
        elapsed = datetime.now() - self._start_time

        # Take a final sample
        self.sample()

        # Write the report line a final time, with a newline
        self.report(newline="\n")

        # Then write a summary of time elapsed
        print(f"Finished in {elapsed.total_seconds():.2f} seconds")

    @staticmethod
    def log_process_info(work_threads, upload_threads, packfile_jobs):
        """Logs information about processes"""
        if packfile_jobs > 0:
            print(
                f"Using up to {work_threads} worker thread(s) and {upload_threads} transfer thread(s)."
            )
        else:
            print(f"Using up to {upload_threads} transfer thread(s).")
