"""
Tools for metamodern software development.

Design in accordance with the meta system.

"""

from .analysis import test
from .git import clone_repo, get_repo
from .pkg import (get_current_packages, get_current_project,
                  strip_local_dev_deps)

__all__ = [
    "clone_repo",
    "get_repo",
    "test",
    "get_current_project",
    "get_current_packages",
    "strip_local_dev_deps",
]
