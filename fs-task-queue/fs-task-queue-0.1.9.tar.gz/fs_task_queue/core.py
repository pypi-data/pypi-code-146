import sys
import logging
import enum
import pathlib
import json
import uuid
import contextlib
import importlib
import traceback
import time
from typing import Union

from fs_task_queue import utils


logger = logging.getLogger(__name__)


class JobStatus(enum.Enum):
    QUEUED = "queued"
    FINISHED = "finished"
    FAILED = "failed"
    STARTED = "started"


class JSONSerializer:
    def loads(self, message: bytes):
        return json.loads(message)

    def dumps(self, data: bytes):
        return json.dumps(data).encode("utf-8")


class DummyLock:
    @contextlib.contextmanager
    def aquire(self, path: Union[str, pathlib.Path]):
        yield


class Job:
    def __init__(
        self,
        queue: "Queue",
        id: str,
    ):
        self.queue = queue
        self.id = id

    def __str__(self):
        meta = self._meta
        return f"<{self.__class__.__name__} {meta['module']}.{meta['name']}(*{meta['args']}, **{meta['kwargs']})>"

    @property
    def job_path(self):
        return self.queue.job_directory / self.id

    @property
    def lock_path(self):
        return (self.queue.job_directory / self.id).with_suffix(".lock")

    @property
    def _meta(self):
        with self.job_path.open("rb") as f:
            return self.queue.job_serializer.loads(f.read())

    def get_status(self):
        for status in JobStatus:
            if (self.queue.get_status_directory(status) / self.id).is_symlink():
                return status

    def claim(self):
        """Returns True/False depending on if job claim succeeded"""
        with self.queue.lock.aquire(self.lock_path):
            current_status = self.get_status()
            if current_status == JobStatus.QUEUED:
                self._set_status(JobStatus.STARTED)
                return True
            else:
                return False

    def set_status(self, status: JobStatus = JobStatus.QUEUED):
        with self.queue.lock.aquire(self.lock_path):
            self._set_status(status)

    def _set_status(self, status: JobStatus = JobStatus.QUEUED):
        current_status = self.get_status()

        if current_status == status:
            return

        if current_status:
            (self.queue.get_status_directory(current_status) / self.id).unlink()
        (self.queue.get_status_directory(status) / self.id).symlink_to(self.job_path)

    def __call__(self):
        meta = self._meta
        func = getattr(importlib.import_module(meta["module"]), meta["name"])
        args = meta["args"]
        kwargs = meta["kwargs"]

        try:
            self.set_status(JobStatus.STARTED)
            result = func(*args, **kwargs)
            self.set_status(JobStatus.FINISHED)
            with (self.queue.result_directory / self.id).open("wb") as f:
                f.write(
                    self.queue.result_serializer.dumps(
                        {
                            "return_value": result,
                            "exc_string": None,
                        }
                    )
                )
        except Exception:
            self.set_status(JobStatus.FAILED)
            with (self.queue.result_directory / self.id).open("wb") as f:
                f.write(
                    self.queue.result_serializer.dumps(
                        {"return_value": None, "exc_string": traceback.format_exc()}
                    )
                )

    @property
    def result(self):
        if self.get_status() in [JobStatus.FINISHED, JobStatus.FAILED]:
            with (self.queue.result_directory / self.id).open("rb") as f:
                result_object = self.queue.result_serializer.loads(f.read())
                if result_object.get("exc_string") is not None:
                    raise Exception(result_object.get("exc_string"))
                else:
                    return result_object["return_value"]

    def wait(self, timeout: float = 30, interval: int = 1):
        start_time = time.time()
        while True:
            if (time.time() - start_time) > timeout:
                raise TimeoutError(f"Waiting for job {self.id}")
            elif self.get_status() in [JobStatus.FINISHED, JobStatus.FAILED]:
                return self.result
            time.sleep(interval)


class Queue:
    def __init__(
        self,
        directory: Union[str, pathlib.Path],
        job_serializer_class=JSONSerializer,
        result_serializer_class=JSONSerializer,
        lock_class=DummyLock,
        job_class=Job,
    ):
        self.directory = pathlib.Path(directory)
        self.job_serializer = job_serializer_class()
        self.result_serializer = result_serializer_class()
        self.lock = lock_class()
        self.job_class = job_class
        self.ensure_directories()

    def __repr__(self):
        return f"<Queue directory={self.directory}>"

    def ensure_directories(self):
        self.job_directory.mkdir(exist_ok=True)
        self.result_directory.mkdir(exist_ok=True)
        self.worker_directory.mkdir(exist_ok=True)
        self.queued_directory.mkdir(exist_ok=True)
        self.finished_directory.mkdir(exist_ok=True)
        self.failed_directory.mkdir(exist_ok=True)
        self.started_directory.mkdir(exist_ok=True)

    def enqueue(self, func, *args, **kwargs):
        job_name = str(uuid.uuid4())
        job = self.job_class(queue=self, id=job_name)
        job_message = {
            "module": func.__module__,
            "name": func.__name__,
            "args": args,
            "kwargs": kwargs,
        }
        with job.job_path.open("wb") as f:
            f.write(self.job_serializer.dumps(job_message))

        job.set_status(JobStatus.QUEUED)
        return job

    def dequeue(self, timeout: float = 30, interval: int = 1):
        start_time = time.time()
        while True:
            if (time.time() - start_time) > timeout:
                raise TimeoutError("Failed to dequeue job")

            for filename in self.queued_directory.iterdir():
                job_name = filename.name
                job = Job(queue=self, id=job_name)
                if job.claim():
                    return job
            time.sleep(interval)

    @property
    def job_directory(self):
        return self.directory / "tasks"

    @property
    def result_directory(self):
        return self.directory / "results"

    @property
    def worker_directory(self):
        return self.directory / "workers"

    @property
    def queued_directory(self):
        return self.directory / JobStatus.QUEUED.value

    @property
    def finished_directory(self):
        return self.directory / JobStatus.FINISHED.value

    @property
    def failed_directory(self):
        return self.directory / JobStatus.FAILED.value

    @property
    def started_directory(self):
        return self.directory / JobStatus.STARTED.value

    def get_status_directory(self, status: JobStatus):
        if status == JobStatus.QUEUED:
            return self.queued_directory
        elif status == JobStatus.STARTED:
            return self.started_directory
        elif status == JobStatus.FINISHED:
            return self.finished_directory
        elif status == JobStatus.FAILED:
            return self.failed_directory

    def stats(self):
        return {
            "queued": len(list(self.queued_directory.iterdir())),
            "started": len(list(self.started_directory.iterdir())),
            "finished": len(list(self.finished_directory.iterdir())),
            "failed": len(list(self.failed_directory.iterdir())),
        }


class Worker:
    def __init__(
        self,
        queue: Queue,
        id: str = None,
    ):
        self.queue = queue
        self.id = id or str(uuid.uuid4())
        self.job_check_interval = 1
        self.heartbeat_interval = 30

    @property
    def worker_path(self):
        return self.queue.worker_directory / self.id

    def register_worker(self):
        self.worker_path.touch()

    def unregister_worker(self):
        self.worker_path.unlink(missing_ok=True)

    def check_shutdown(self):
        if not self.worker_path.exists():
            logger.info(f"Stopping worker {self.id} due to shutdown command")
            sys.exit(0)

    def send_heartbeat(self):
        self.worker_path.touch()

    def run(self):
        logger.info(f"Starting worker {self.id} on queue={self.queue}")
        try:
            self.register_worker()
            while True:
                self.check_shutdown()
                # must send heartbeat after shutdown check
                # since heartbeat will create file if it doesn't exist
                self.send_heartbeat()
                try:
                    job = self.queue.dequeue()
                    with utils.timer(logger, str(job)):
                        job()
                except TimeoutError:
                    pass
        finally:
            self.unregister_worker()
