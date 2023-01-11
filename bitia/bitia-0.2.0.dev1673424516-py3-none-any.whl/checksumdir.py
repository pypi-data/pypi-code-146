"""
Function for deterministically creating a single hash for a directory of files,
taking into account only file contents and not filenames.

dirhash('/path/to/directory', 'md5')

Orignally from
https://raw.githubusercontent.com/SubconsciousCompute/checksumdir/master/checksumdir/__init__.p
y
"""

import hashlib
import typing as T
import os
import re
from pathlib import Path

HASH_FUNCS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


def dirhash(
    dirname: Path,
    hashfunc: str = "sha256",
    excluded_files: T.List[Path] = [],
    ignore_hidden: bool = False,
    followlinks: bool = False,
    excluded_extensions: T.List[str] = [],
):
    hash_func = HASH_FUNCS[hashfunc]
    assert dirname.is_dir(), "{} is not a directory.".format(dirname)
    hashvalues = []
    for r_dir, dirs, files in os.walk(dirname, topdown=True, followlinks=followlinks):
        if ignore_hidden and re.search(r"/\.", r_dir):
            continue
        root = Path(r_dir)
        dirs.sort()
        files.sort()
        for fname in files:
            if ignore_hidden and fname.startswith("."):
                continue

            if Path(fname).suffix in excluded_extensions:
                continue

            if fname in excluded_files:
                continue

            hashvalues.append(filehash(root / fname, hashfunc))

    return _reduce_hash(hashvalues, hash_func)


def filehash(filepath: Path, hashfunc: str = "sha256"):
    """Compute checksum of a file"""
    hasher = HASH_FUNCS[hashfunc]()
    blocksize = 64 * 1024
    assert filepath.is_file(), f"{filepath} is not a file"
    with filepath.open("rb") as fp:
        while True:
            data = fp.read(blocksize)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def _reduce_hash(hashlist, hashfunc):
    hasher = hashfunc()
    for hashvalue in sorted(hashlist):
        hasher.update(hashvalue.encode("utf-8"))
    return hasher.hexdigest()
