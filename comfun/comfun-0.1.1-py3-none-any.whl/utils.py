#!/usr/bin/env python3

import logging
import os
from pathlib import Path
from typing import List, Tuple


def get_all_fpaths_by_extension(root_fdir: str, exts: Tuple[str, ...], recursive=True) -> List[str]:
    """
    Recursively extracts all file paths to files ending with the given extension down the folder hierarchy (i.e. it
    includes subfolders).
    :param root_fdir: str. Root directory from where to start searching
    :param exts: Tuple of extension strings. e.g. (".txt", "WAV")
    :param recursive:
    :return: sorted list of file paths
    """

    # Standardise the extensions tuple.
    exts = (ext.lower() for ext in exts)
    # Make sure they have a preceding period
    exts = tuple([ext if ext.startswith(".") else "." + ext for ext in exts])

    if recursive:
        file_paths = [str(path) for path in Path(root_fdir).rglob('*') if path.suffix.lower() in exts]
    else:
        file_paths = [os.path.join(root_fdir, fname) for fname in sorted(os.listdir(root_fdir)) if fname.endswith(exts)]
    return sorted(file_paths)
