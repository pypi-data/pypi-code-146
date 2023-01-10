from remotemanager.logging import LoggingMixin
from remotemanager.storage import SendableMixin

import os


class TrackedFile(LoggingMixin, SendableMixin):

    __slots__ = ('_remote_path', '_local_path', '_file')

    def __init__(self, local_path, remote_path, file):

        self._remote_path = remote_path
        self._local_path = local_path
        self._file = file

    def __str__(self):
        return self.local

    @property
    def name(self):
        return self._file

    @property
    def remote(self):
        return os.path.join(self._remote_path, self.name)

    @property
    def local(self):
        return os.path.join(self._local_path, self.name)

    @property
    def remote_dir(self):
        return self._remote_path

    @property
    def local_dir(self):
        return self._local_path
