##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .LocalFile import *

import optumi_core as optumi

import os, time
from uuid import uuid4
from typing import Union


STORAGE_TOTAL = 0
STORAGE_LIMIT = 1024 * 1024 * 1024 * 1024  # Assume the largest storage total


class LocalStorage(list):
    def __init__(self, files: Union[list, str] = []):
        _files = []
        if type(files) is str:
            _files.append(LocalFile(files))
        elif type(files) is LocalFile:
            _files.append(files)
        else:
            for f in files:
                if type(f) is str:
                    _files.append(LocalFile(f))
                else:
                    _files.append(f)
        super().__init__(_files)

    def upload(self, wait=True):
        if len(self) > 0:
            key = str(uuid4())
            print("Uploading", "files..." if len(self) > 1 else "file...")
            for f in self:
                print(f)
            optumi.core.upload_files(
                key,
                [x.path for x in self],
                True,
                STORAGE_TOTAL,
                STORAGE_LIMIT,
                True,
            )

            if wait:
                while True:
                    progress = optumi.core.get_upload_progress([key])
                    time.sleep(0.2)
                    if progress[key]["progress"] < 0:
                        break

                print("...completed")

    def __str__(self):
        return str([str(x) for x in self])
