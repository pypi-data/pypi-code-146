from pathlib import Path
from enum import Enum

from bitia.logger import logger
from bitia.checksumdir import filehash


def sha256sum(infile: Path) -> str:
    """Compute sha256sum of a file."""
    return filehash(infile, "sha256")


def dir_info(user_dir: Path) -> dict:
    """Check if directory is in good condition."""
    files = [f.resolve() for f in user_dir.glob("**/*") if f.is_file()]
    size_in_mb = sum(f.stat().st_size / 1024.0 / 1024.0 for f in files)
    if size_in_mb > 25.0:
        logger.warning(
            "The size of pipeline is >25MB ({size_in_mb} MB)."
            " You should try to reduce the size of the pipeline. TODO: See this link."
        )
    return dict(size_in_mb=size_in_mb, num_files=len(files), files=files)
