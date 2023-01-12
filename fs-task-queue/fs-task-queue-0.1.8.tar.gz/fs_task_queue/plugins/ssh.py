import os
import uuid
import pathlib
import urllib.parse
from typing import Union

import paramiko
from paramiko.client import SSHClient

from fs_task_queue.core import Queue, JSONSerializer, DummyLock, Job, JobStatus
from fs_task_queue.utils import eval_boolean_env_var


class SSHJob(Job):
    @property
    def _meta(self):
        with self.queue._sftp_client.open(str(self.job_path), "rb") as f:
            return self.queue.job_serializer.loads(f.read())

    def get_status(self):
        for status in JobStatus:
            try:
                if self.queue._sftp_client.lstat(
                    str(self.queue.get_status_directory(status) / self.id)
                ):
                    return status
            except FileNotFoundError:
                pass

    # mutating operations not implemented for ssh interface
    def set_status(self):
        raise NotImplementedError()

    def claim(self):
        raise NotImplementedError()

    def __call__(self):
        raise NotImplementedError()

    @property
    def result(self):
        if self.get_status() in [JobStatus.FINISHED, JobStatus.FAILED]:
            with self.queue._sftp_client.open(
                str(self.queue.result_directory / self.id), "rb"
            ) as f:
                result_object = self.queue.result_serializer.loads(f.read())
                if result_object.get("exc_string") is not None:
                    raise Exception(result_object.get("exc_string"))
                else:
                    return result_object["return_value"]


class SSHQueue(Queue):
    def __init__(
        self,
        directory: Union[str, pathlib.Path],
        job_serializer_class=JSONSerializer,
        result_serializer_class=JSONSerializer,
        lock_class=DummyLock,
        job_class=SSHJob,
    ):
        directory = self._create_client(directory)
        super().__init__(
            directory=directory,
            job_serializer_class=job_serializer_class,
            result_serializer_class=result_serializer_class,
            lock_class=lock_class,
            job_class=job_class,
        )

    def _create_client(self, directory):
        if not directory.startswith("ssh://"):
            raise ValueError("directory must start with ssh://")

        p = urllib.parse.urlparse(directory)
        params = {
            "hostname": p.hostname,
            "port": int(p.port or 22),
            "username": p.username or os.getlogin(),
            "password": p.password,
            "key_filename": os.environ.get("PARAMIKO_SSH_KEYFILE"),
            "passphrase": os.environ.get("PARAMIKO_SSH_PASSPHRASE"),
            "allow_agent": eval_boolean_env_var("PARAMIKO_SSH_ALLOW_AGENT", True),
            "look_for_keys": eval_boolean_env_var("PARAMIKO_SSH_LOOK_FOR_KEYS", True),
            "path": p.path,
        }

        self._ssh_client = SSHClient()
        self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh_client.connect(
            hostname=params["hostname"],
            port=params["port"],
            username=params["username"],
            password=params["password"],
            look_for_keys=params["look_for_keys"],
            allow_agent=params["allow_agent"],
            key_filename=params["key_filename"],
            passphrase=params["passphrase"],
        )
        self._sftp_client = self._ssh_client.open_sftp()
        return pathlib.Path(params["path"])

    def ensure_directories(self):
        commands = []
        for directory in [
            self.job_directory,
            self.result_directory,
            self.worker_directory,
            self.queued_directory,
            self.finished_directory,
            self.failed_directory,
            self.started_directory,
        ]:
            commands.append(f"mkdir -p {directory}")
        commands.append('echo "done"')
        stdin, stdout, stderr = self._ssh_client.exec_command(" && ".join(commands))
        if stdout.read() != b"done\n":
            raise Exception(
                f'failed to create directories on remote machine with error {stderr.read().decode("utf-8")}'
            )

    def enqueue(self, func, *args, **kwargs):
        job_name = str(uuid.uuid4())
        job = self.job_class(queue=self, id=job_name)
        job_message = {
            "module": func.__module__,
            "name": func.__name__,
            "args": args,
            "kwargs": kwargs,
        }
        with self._sftp_client.open(str(job.job_path), "wb") as f:
            f.write(self.job_serializer.dumps(job_message))

        self._sftp_client.symlink(
            str(job.job_path), str(self.queued_directory / job.id)
        )
        return job

    def dequeue(self, timeout: float = 30, interval: int = 1):
        raise NotImplementedError()

    def stats(self):
        return {
            "queued": len(self._sftp_client.listdir(self.queued_directory)),
            "started": len(self._sftp_client.listdir(self.started_directory)),
            "finished": len(self._sftp_client.listdir(self.finished_directory)),
            "failed": len(self._sftp_client.listdir(self.failed_directory)),
        }
