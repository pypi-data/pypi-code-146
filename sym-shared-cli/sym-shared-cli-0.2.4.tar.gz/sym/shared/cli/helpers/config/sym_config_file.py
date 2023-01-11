import hashlib
import json
import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import ClassVar

from portalocker.exceptions import AlreadyLocked, LockException

from ..io import TruncatingStringIO
from ..os import create_lock, read_lock, read_write_lock


class _Config:
    dir_name: ClassVar[str]


def init(dir_name):
    _Config.dir_name = dir_name


def xdg_config_home() -> Path:
    try:
        return Path(os.environ["XDG_CONFIG_HOME"]).expanduser().resolve()
    except KeyError:
        return Path.home() / ".config"


def sym_config_file(file_name: str) -> Path:
    return (xdg_config_home() / _Config.dir_name / file_name).resolve()


def get_dir_name() -> str:
    return _Config.dir_name


class SymConfigFile:
    def __init__(self, *, file_name: str, uid_scope: bool = True, **dependencies):
        path = Path()

        if dependencies:
            key = json.dumps(dependencies, sort_keys=True).encode("utf-8")
            md5 = hashlib.md5(key).hexdigest()
            path = path / md5

        path = path / file_name

        if uid_scope:
            path = Path("uid") / str(os.getuid()) / path
        else:
            path = Path("default") / path

        self.path = sym_config_file(path)

        self.read_lock = read_lock(self.path)
        self.write_lock = create_lock(self.path)
        self.update_lock = read_write_lock(self.path)

        self.value = None

    def __enter__(self):
        self.mkparents()
        try:
            # acquire read lock, hold across context
            fh = self.read_lock.acquire()
            fh.seek(0)  # reentrant
            self.value = fh.read()
        except FileNotFoundError:
            self.value = None
        self.file = TruncatingStringIO(initial_value=self.value)
        return self.file

    def __exit__(self, type, value, traceback):
        self.read_lock.release()  # release read lock
        if value:
            return
        if self.file.tell() == 0:
            return
        if self.value != (value := self.file.getvalue()):
            with self.exclusive_access() as f:
                f.write(value)

    def __str__(self):
        return str(self.path)

    def mkparents(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def put(self, s: str):
        with self as f:
            f.write(s)

    def read(self):
        if self.value:
            return self.value
        with self.read_lock.acquire() as fh:
            fh.seek(0)
            return fh.read()

    def _throwaway_write(self):
        with NamedTemporaryFile(mode="w+") as f:
            yield f

    @contextmanager
    def exclusive_access(self):
        try:
            with self.write_lock as f:  # acquire write lock
                yield f
        except AlreadyLocked:  # another thread is writing same value
            yield from self._throwaway_write()

    @contextmanager
    def exclusive_create(self):
        self.mkparents()
        if self.path.exists():
            yield from self._throwaway_write()
        else:
            with self.exclusive_access() as f:
                yield f

    @contextmanager
    def update(self, fail_ok=False):
        self.mkparents()
        try:
            with self.update_lock as f:
                f.seek(0)  # reentrant
                yield f
        except LockException:
            if fail_ok:
                yield TruncatingStringIO(initial_value=self.read())
            else:
                raise
