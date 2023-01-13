"""Provides IngestWorker class."""
import logging
import multiprocessing as mp
import signal
import sys
import time
import typing

from . import errors
from . import schemas as T
from .client import DBClient, db
from .config import WorkerConfig
from .tasks import create_task

log = logging.getLogger(__name__)


class WorkerPool:
    """Ingest worker pool"""

    def __init__(self, worker_config: WorkerConfig):
        self.worker_config = worker_config
        self.processes = []
        self.running = False
        self.lock = mp.Lock()

    def start(self):
        """Start the worker with N processes. Noop if the worker already started."""
        if self.running:
            return

        self.running = True
        for _ in range(self.worker_config.jobs):
            self._start_single_worker()

    def _start_single_worker(self):
        """Start a worker process."""
        p_name = f"{self.worker_config.worker_name}-{len(self.processes)}"
        shutdown_event = mp.Event()
        target = Worker(self.worker_config, p_name, shutdown_event, True).run
        proc = mp.Process(target=target, args=(self.lock,), name=p_name, daemon=True)
        proc.start()
        self.processes.append((proc, shutdown_event))

    def join(self):
        """Wait until all worker processes terminate"""
        for proc, _ in self.processes:
            proc.join()

    def shutdown(self):
        """Shutdown the executor.

        Send shutdown event for every worker processes and wait until all of them terminate.
        """
        for _, shutdown_event in self.processes:
            shutdown_event.set()
        self.join()


class Worker:  # pylint: disable=too-few-public-methods
    """Ingest worker, wait for task and execute it"""

    def __init__(
        self,
        config: WorkerConfig,
        name=None,
        shutdown=None,
        is_local_worker=False,
    ):
        self._db = None  # pylint: disable=C0103
        self.config = config
        self.name = name or config.worker_name
        self.shutdown = shutdown or mp.Event()
        self.is_local_worker = is_local_worker

        self.current_task_id = None

    @property
    def db(self):  # pylint: disable=C0103
        """
        Get db client instance. Database client is initialized lazely.

        Lazy mode is necessary to avoid pickle error
        when using spawn multiprocessing start method (default on windows).
        """
        if not self._db:
            self._db = DBClient(self.config.db_url)
        return self._db

    def run(self, lock: typing.Optional[mp.Lock] = None):
        """Run the worker"""
        orig_sigint_handler = signal.signal(
            signal.SIGINT, self.graceful_shutdown_handler
        )
        orig_sigterm_handler = signal.signal(
            signal.SIGTERM, self.graceful_shutdown_handler
        )
        if sys.platform != "win32":
            orig_alarm_handler = signal.signal(signal.SIGALRM, alarm_handler)
        if lock:
            db.set_lock(lock)
        try:
            log.debug(f"{self.name} worker started, wating for connection...")
            self.wait_for_db()
            log.debug(f"{self.name} worker connected, waiting for tasks...")
            self.consume_tasks()
        finally:
            signal.signal(signal.SIGINT, orig_sigint_handler)
            signal.signal(signal.SIGTERM, orig_sigterm_handler)
            if sys.platform != "win32":
                # SIGALRM is not implemented on windows
                signal.signal(signal.SIGALRM, orig_alarm_handler)

    def consume_tasks(self):
        """Consume ingest tasks, do the actual work"""
        force_consuming = False
        while not self.shutdown.is_set() or force_consuming:
            next_task = None
            try:
                next_task = self.db.next_task(self.name)
                # if it is a local worker it should run until ingest does not
                # reach a terminal status even if shutdown event is set this
                # makes sure that we always execute finalize task
                # also note that local workers only work on one ingest
                force_consuming = (
                    self.db.is_bound
                    and self.is_local_worker
                    and not T.IngestStatus.is_terminal(self.db.ingest.status)
                )

                if not next_task:
                    time.sleep(self.config.sleep_time)
                    continue

                self.current_task_id = next_task.id
                self.db.bind(next_task.ingest_id)
                self.run_task(next_task)
                self.current_task_id = None

            except Exception:  # pylint: disable=broad-except
                # catch any unhandled exceptions and fail the ingest if the
                # client is already bound to help find critical bugs
                # and handle them consciously
                if next_task:
                    self.db.bind(next_task.ingest_id)
                    self.db.fail()
                raise

        log.debug(f"{self.name} worker process exited gracefully")

    def run_task(self, task):
        """Run the task"""
        log.debug(f"{self.name} executing task {task}")
        task = create_task(self.db, task, self.config, is_local=self.is_local_worker)
        task.run()
        log.debug(f"{self.name} executing task completed")

    def wait_for_db(self):
        """Wait for database connection"""
        while not self.shutdown.is_set():
            if self.db.check_connection():
                break
            time.sleep(self.config.sleep_time)

    def graceful_shutdown_handler(self, signum, *_):
        """
        Set the shutdown event to not start any new tasks and give 15 seconds for the
        current task to finish. After 15s the task is failed using an alarm signal.
        """
        log.debug(f"{self.name} received {signum}, trying to shut down gracefully...")
        # next time shutdown will be forced
        signal.signal(signal.SIGINT, self.forced_shutdown_handler)
        signal.signal(signal.SIGTERM, self.forced_shutdown_handler)
        if not self.is_local_worker:
            # in case of a local ingest we has to ensure there is a worker that will run the finalize task
            self.shutdown.set()
        if sys.platform != "win32" and not self.is_local_worker:
            signal.alarm(self.config.termination_grace_period)

    def forced_shutdown_handler(self, signum, *_):
        """
        Immediately raise an exception to hard shutdown the worker.
        This handler fires for example when the user double press CTRL+c.
        """
        log.debug(f"{self.name} received {signum} forced shutdown")
        self._reset_task_status()
        raise errors.WorkerForcedShutdown

    def _reset_task_status(self):
        if self.current_task_id:
            self.db.reset_task_status(self.current_task_id)


def alarm_handler(signum, frame):
    """
    Custom alarm signal handler that raises a timeout exception to indicate that
    the worker couldn't terminate gracefully in the given amount of time
    """
    raise errors.WorkerShutdownTimeout
