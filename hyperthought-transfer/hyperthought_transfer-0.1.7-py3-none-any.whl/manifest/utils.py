"""
General utility functions.
"""

import hashlib
import os
from typing import List
import uuid


N_END_BYTES = 20


def clean_path(path: str) -> str:
    """Get a path having consistent path delimiters."""
    return path.replace("/", os.path.sep).replace("\\", os.path.sep)


def generate_id() -> str:
    """Generate a random uuid."""
    return str(uuid.uuid4())


def get_end_bytes(path: str, n_bytes: int = N_END_BYTES) -> List[int]:
    """
    Read the last n bytes from file.

    Parameters
    ----------
    path : str
        Path to file of interest.
    n_bytes : int
        Number of bytes to read from end of file.

    Returns
    -------
    An integer array corresponding to the last n_bytes bytes.

    Exceptions
    ----------
    A ValueError will be thrown if the file does not exist.
    A PermissionError will be thrown if the file cannot be read because
    another process is writing to it.
    A generic Exception may be thrown if something unexpected happens.
    """
    if not os.path.exists(path):
        raise ValueError(f"path {path} does not exist")

    file_size = os.path.getsize(path)

    if not file_size:
        return []

    with open(path, "rb") as file_handle:
        file_handle.seek(0, os.SEEK_END)

        if file_size != file_handle.tell():
            raise Exception("unexpected file size mismatch")

        # Don't try to read more bytes than the file has.
        n_bytes = min(file_size, n_bytes)
        file_handle.seek(file_size - n_bytes)
        end_bytes = file_handle.read(n_bytes)

    return [int(byte_) for byte_ in end_bytes]


def get_hash(file_name: str) -> str:
    """Get a file hash for a file."""
    hash_object = hashlib.md5()
    chunk_size = 2**20  # 1 MB

    with open(file_name, "rb") as f:
        chunk = f.read(chunk_size)

        while chunk:
            hash_object.update(chunk)
            chunk = f.read(chunk_size)

    hash = hash_object.hexdigest()
    return hash
