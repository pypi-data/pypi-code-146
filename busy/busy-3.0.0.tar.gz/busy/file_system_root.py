from pathlib import Path
from tempfile import TemporaryDirectory
import os
import subprocess

from .file import File
from .busyqueue import BusyQueue


class FilesystemRoot:

    def __init__(self, path=None):
        if path:
            self._path = Path(path) if isinstance(path, str) else path
            assert isinstance(self._path, Path) and self._path.is_dir()
        else:
            env_var = os.environ.get('BUSY_ROOT')
            self._path = Path(env_var if env_var else Path.home() / '.busy')
            if not self._path.is_dir():
                self._path.mkdir()
        is_git = self.git('rev-parse', check=False)
        if is_git.returncode > 0:
            self.git('init')
        self._files = {}
        self._queues = {}

    @property
    def _str_path(self):
        return str(self._path.resolve())

    def git(self, command, **kwargs):
        return subprocess.run(f'git -C {self._str_path} {command}'.split(), capture_output=True, **kwargs)

    def get_queue(self, key=None):
        key = key or BusyQueue.default_key
        if key not in self._queues:
            queueclass = BusyQueue.subclass(key)
            queuefile = File(self._path / f'{key}.txt')
            self._files[key] = queuefile
            items = queuefile.read(queueclass.itemclass)
            self._queues[key] = queueclass(self, items)
        return self._queues[key]

    def save(self):
        changed = False
        while self._queues:
            key, queue = self._queues.popitem()
            if queue.changed:
                items = queue.all()
                self._files[key].save(*items)
                changed = True
        # if changed:
        #     self.git('add -A')
        #     self.git('commit -m change')

    @property
    def queue_names(self):
        filenames = list(self._path.glob('*.txt'))
        keys = [Path(f).stem for f in filenames]
        return keys
