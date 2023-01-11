"""Provides interface for multi-threaded task processing"""
import heapq
import itertools
import logging
import threading
from abc import ABC, abstractmethod

log = logging.getLogger(__name__)


class Task(ABC):
    """Abstract Task class"""

    __slots__ = ("group", "skipped")

    def __init__(self, group):
        self.group = group
        self.skipped = False

    @abstractmethod
    def execute(self):
        """Execute task"""

    @abstractmethod
    def get_bytes_processed(self):
        """Bytes processed by task"""

    @abstractmethod
    def get_desc(self):
        """Description of task"""

    @property
    def allow_retry(self):
        """Get whether retry is allowed or not"""
        return False


class WorkQueue:
    """Multi-threaded upload queue that reports progress"""

    def __init__(self, groups):
        """Initialize the work queue

        Arguments:
            groups (list): List of tuples of group tag to maximum concurrent tasks per group
        """
        # Queue of waiting tasks, by group
        self.waiting = {key: [] for key in groups.keys()}
        # Queue of pending tasks
        self.pending = []
        # Queue of completed tasks
        self.completed = []
        # List of errored tasks
        self.errors = []
        # Count of skipped tasks
        self.skipped = {group: 0 for group in groups.keys()}

        self.groups = groups

        self.running = False
        self._finish_called = False

        self._lock = threading.RLock()
        self._cond = {group: threading.Condition(self._lock) for group in groups.keys()}
        self._complete_cond = threading.Condition()

        self._work_threads = []
        self._counter = itertools.count()

    def start(self):
        """Start threads"""
        self.running = True
        self._finish_called = False

        for group, count in self.groups.items():
            work_fn = self._work_fn(group)
            for i in range(count):
                tname = f"{group}-worker-{i}"
                t = threading.Thread(  # pylint: disable=invalid-name
                    target=work_fn, name=tname
                )
                t.daemon = True
                t.start()
                self._work_threads.append(t)

    def enqueue(self, task, priority=10):
        """Enqueue task"""
        cond = self._cond[task.group]
        with cond:
            count = next(self._counter)
            heapq.heappush(self.waiting[task.group], (priority, count, task))
            cond.notify()

    def skip_task(self, task=None, group=None):
        """Skip task"""
        if group is None:
            group = task.group
        with self._lock:
            self.skipped[group] += 1

    def take(self, group):
        """Take one task"""
        result = None
        cond = self._cond[group]
        with cond:
            while self.running:
                queue = self.waiting[group]
                if queue:
                    _, _, result = heapq.heappop(queue)
                    break
                cond.wait()

            if not self.running:
                return None

            self.pending.append(result)
            return result

    def complete(self, task):
        """Append completed tasks list"""
        finished = False

        with self._lock:
            self.pending.remove(task)
            self.completed.append(task)

            if self._finish_called:
                # Check to see if we're done
                finished = not self.tasks_pending()

        if finished:
            with self._complete_cond:
                self._complete_cond.notify_all()

    def log_exception(self, task, exc_info):
        """Log exception"""
        with self._lock:
            log.error(f"{task.get_desc()} Error: {str(exc_info)}")
            log.debug("Details:", exc_info=exc_info)

    def has_errors(self):
        """Check if has errored tasks"""
        with self._lock:
            return bool(self.errors)

    def error(self, task):
        """Append errored tasks list"""
        finished = False

        with self._lock:
            self.pending.remove(task)
            self.errors.append(task)

            if self._finish_called:
                # Check to see if we're done
                finished = not self.tasks_pending()

        if finished:
            with self._complete_cond:
                self._complete_cond.notify_all()

    def tasks_pending(self):
        """Check if has pending tasks"""
        with self._lock:
            if self.pending:
                return True

            for queue in self.waiting.values():
                if queue:
                    return True
            return False

    def get_stats(self):
        """Get stats from every task and summarize"""
        results = {}

        with self._lock:
            for group in self.groups.keys():
                results[group] = {
                    "completed": 0,
                    "completed_bytes": 0,
                    "skipped": self.skipped[group],
                }

            for task in self.completed:
                stats = results[task.group]
                stats["completed"] = stats["completed"] + 1
                stats["completed_bytes"] = (
                    stats["completed_bytes"] + task.get_bytes_processed()
                )

            for task in self.pending:
                stats = results[task.group]
                stats["completed_bytes"] = (
                    stats["completed_bytes"] + task.get_bytes_processed()
                )

        return results

    def requeue_errors(self):
        """Requeue errored tasks"""
        errors = []
        with self._lock:
            self._finish_called = False
            errors = self.errors
            self.errors = []

        for task in errors:
            self.enqueue(task)

    def wait_for_finish(self):
        """Wait for finishing every pending task"""
        with self._complete_cond:
            self._finish_called = True

            while self.running and self.tasks_pending():
                self._complete_cond.wait(timeout=0.2)

    def shutdown(self):
        """Shutdown"""
        self.running = False
        for cond in self._cond.values():
            with cond:
                cond.notify_all()

        # Wait for threads
        for t in self._work_threads:  # pylint: disable=invalid-name
            t.join()

        self._work_threads = []

    def _work_fn(self, group):
        def do_work():
            self._do_work(group)

        return do_work

    def _do_work(self, group):
        this_thread = threading.current_thread()
        while self.running:
            task = self.take(group)
            if not task:
                log.debug(f"No task found, thread {this_thread.name} shutting down")
                return  # Shutdown

            try:
                next_task, priority = task.execute()
            except Exception as ex:  # pylint: disable=broad-except
                # Add to errors list
                self.log_exception(task, ex)
                self.error(task)
                continue

            if next_task:
                self.enqueue(next_task, priority=priority)

            # Complete the task
            log.debug(f"Thread {this_thread.name} completed task")
            self.complete(task)
