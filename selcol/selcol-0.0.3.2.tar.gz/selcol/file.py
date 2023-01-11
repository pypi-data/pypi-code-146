import os
import uuid
from pathlib import Path


def default_pretrained_basepath() -> Path:
    import selcol

    default_path = Path(selcol.__file__).parent / "pretrained"
    assert default_path.exists()
    return default_path


def default_cache_basepath() -> Path:
    default_path = Path("~/.cache").expanduser() / "selcol"
    default_path.mkdir(exist_ok=True)
    return default_path


def default_datachunk_basepath() -> Path:
    base_path = Path("/tmp") / "selcol"
    chunk_base_path = base_path / str(uuid.uuid4())
    chunk_base_path.mkdir(exist_ok=True, parents=True)
    return chunk_base_path


def latest_detachunk_basepath() -> Path:
    base_path = Path("/tmp") / "selcol"
    dirs = list(base_path.iterdir())
    dirs_sorted = sorted(dirs, key=lambda x: os.stat(x).st_mtime)
    return dirs_sorted[-1]
