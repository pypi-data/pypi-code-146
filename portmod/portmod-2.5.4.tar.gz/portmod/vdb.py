# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
from contextlib import ContextDecorator
from typing import Optional

from .config import variable_data_dir
from .lock import vdb_lock


def vdb_path() -> str:
    """
    Returns the VDB path for the current prefix
    """
    return os.path.join(variable_data_dir(), "db")


class VDB(ContextDecorator):
    def __init__(self, commit_message: Optional[str] = None):

        self.lock = vdb_lock(write=True)
        self.message = commit_message

    def __enter__(self):
        # Slow import
        import git

        self.lock.__enter__()
        # Don't set the gitrepo until we have the write lock
        self.gitrepo = git.Repo.init(vdb_path())
        return self.gitrepo

    def __exit__(self, *_exc):
        if self.message is not None and (
            not self.gitrepo.heads or self.gitrepo.git.diff("HEAD", cached=True)
        ):
            self.gitrepo.git.commit(m=self.message)
        self.lock.__exit__()
        return False
