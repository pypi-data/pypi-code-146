import os
import shlex
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal

# http://web.archive.org/web/20141016185743/https://mail.python.org/pipermail/python-list/2007-May/460639.html

TeeFD = Literal["stdout", "stderr"]


class Tee(object):
    def __init__(self, fd_name: TeeFD, log_dir: str, mode="w"):
        self.path = self.__class__.path_for_fd(log_dir, fd_name)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        self.file = self.path.open(mode)
        self.fd_name = fd_name
        self.fd = getattr(sys, fd_name)

        setattr(sys, fd_name, self)

    @classmethod
    def path_for_fd(cls, log_dir, fd_name):
        return (Path(log_dir) / f"{os.getpid()}.{fd_name}.log").expanduser().resolve()

    @classmethod
    def tee_command(cls, log_dir, command):
        if isinstance(command, list):
            program = command[0]
            command = shlex.join(command)
        else:
            program = shlex.split(command)[0]
        stdout_path = cls.path_for_fd(log_dir, f"{program}.stdout")
        stderr_path = cls.path_for_fd(log_dir, f"{program}.stderr")
        return f"{command} > >(tee -a '{stdout_path}') 2> >(tee -a '{stderr_path}' >&2)"

    def close(self):
        if self.fd is not None:
            setattr(sys, self.fd_name, self.fd)
            self.fd = None

        if self.file is not None:
            if self.file.tell() == 0:
                self.path.unlink(missing_ok=True)
            else:
                self.file.write(
                    "\n".join(
                        [
                            "--",
                            f"Sym log file from {datetime.utcnow()}",
                            shlex.join(sys.argv or []),
                        ]
                    )
                )
                self.file.flush()
            self.file.close()
            self.file = None

    def write(self, data):
        self.file.write(data)
        self.fd.write(data)

    def flush(self):
        self.file.flush()
        self.fd.flush()

    def fileno(self):
        return self.fd.fileno()

    def __enter__(self):
        self.ref = self
        return self

    def __exit__(self, type, value, traceback):
        self.ref = None
        self.close()

    def __del__(self):
        self.close()


class TeeStdOut(Tee):
    def __init__(self, log_dir):
        super().__init__("stdout", log_dir)


class TeeStdErr(Tee):
    def __init__(self, log_dir):
        super().__init__("stderr", log_dir)
