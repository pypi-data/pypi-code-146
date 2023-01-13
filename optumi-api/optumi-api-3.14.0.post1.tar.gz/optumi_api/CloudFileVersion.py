##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
import os, datetime, time
from uuid import uuid4


class CloudFileVersion:
    def __init__(
        self,
        path: str,
        hash: str,
        size: int,
        created: str,
        modified: str,
    ):
        self._path = path
        self._hash = hash
        self._size = size
        self._created = created
        self._modified = modified

    def download(self, wait=True):
        key = str(uuid4())
        print("Downloading file", self)
        optumi.core.download_files(
            key, [self._hash], [self._path], [self._size], False, None
        )

        if wait:
            while True:
                progress = optumi.core.get_download_progress([key])
                time.sleep(0.2)
                if progress[key]["progress"] < 0:
                    break

            print("...completed")

    def remove(self):
        print("Deleting file", self)
        optumi.core.delete_files([self._hash], [self._path], [self._created], "")

    @property
    def path(self):
        return self._path

    @property
    def hash(self):
        return self._hash

    @property
    def size(self):
        return self._size

    @property
    def created(self):
        return self._created

    @property
    def modified(self):
        return self._modified

    def __str__(self):
        return (
            self.path
            + " "
            + str(self.size)
            # + " "
            # + self.created
            + " "
            + self.modified
            # + " "
            # + self.hash
        )

    def __repr__(self):
        return self.__str__()
