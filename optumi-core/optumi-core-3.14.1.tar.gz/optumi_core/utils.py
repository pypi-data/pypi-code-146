##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##


import os, hashlib

from pathlib import Path

# Get a windows path in a format we can use on linux
def split_drive(path):
    # Split the path and return drive, path tuple
    # Normalize the path first just to make sure we have the right format
    return os.path.splitdrive(normalize_path(path))


def hash_file(fileName):
    if os.path.isfile(fileName):
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        with open(fileName, "rb") as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest().upper()
    return str(None)


def normalize_path(path, strict=True):
    if not path:
        if strict:
            raise FileNotFoundError("Path is empty")
        else:
            return path

    # Expand "~" and relative paths
    # Retrieve correct case from file system in windows paths
    # Replace "\" with "/"
    # strict=True will throw an exception if the file does not exist
    return str(Path(path).expanduser().resolve(strict=strict)).replace("\\", "/")


def replace_home_with_tilde(path):
    # Normalize the path first just to make sure we have the right format
    return normalize_path(path).replace(normalize_path(os.path.expanduser("~")), "~")


def hash_string(string):
    hasher = hashlib.md5()
    hasher.update(string)
    return hasher.hexdigest().upper()
