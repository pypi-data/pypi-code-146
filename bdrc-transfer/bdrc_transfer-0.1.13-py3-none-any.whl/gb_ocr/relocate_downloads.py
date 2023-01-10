#!/usr/bin/env python3
"""
Relocates downloads, to reduce directory load on Incoming/GoogleBooks/Downloads
"""
import logging
import os
import sys
from pathlib import Path

STD_SUFFIX = "tar.gz.gpg"
STD_PREFIX = "TBRC_"


def relocate_downloads_main():
    parent = Path(sys.argv[1])
    if not os.path.exists(parent):
        raise FileNotFoundError(parent)
    if not os.path.isdir(parent):
        raise NotADirectoryError(parent)

    for d_entry in os.scandir(parent):
        if not d_entry.is_file() or not d_entry.name.endswith(STD_SUFFIX):
            continue
        image_group: str = d_entry.name.replace(STD_SUFFIX, '').replace(STD_PREFIX, '')
        work: str = image_group.split('-')[0]
        new_dir: Path = Path(parent, work)
        if not os.path.exists(new_dir):
            logging.info(f"Creating {new_dir}")
            os.mkdir(new_dir)
        target = Path(parent, work, image_group + STD_SUFFIX)
        logging.info(f"moving {d_entry.path} to {target}")
        os.rename(d_entry.path, target)


if __name__ == "__main__":
    relocate_downloads_main()
