from pathlib import Path
from .conf import get_setting


def _get_lock_path(lockname: str) -> Path:
    cache_dir = get_setting("endi.static_tmp", default="/tmp")
    directory = Path(cache_dir)
    return directory.joinpath(f"{lockname}.lock")


def is_locked(lockname):
    p = _get_lock_path(lockname)
    return p.exists()


def acquire_lock(lockname):
    p = _get_lock_path(lockname)
    p.touch()


def release_lock(lockname):
    p = _get_lock_path(lockname)
    p.unlink()
