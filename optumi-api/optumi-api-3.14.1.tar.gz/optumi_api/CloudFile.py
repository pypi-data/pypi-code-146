##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

import os, datetime
from uuid import uuid4


class CloudFile:
    def __init__(self, path: str, versions: list):
        if not versions:
            raise OptumiException("Missing CloudFile versions")
        self._path = path
        # Sort files by newest to oldest modification time
        self._versions = sorted(versions, key=lambda version: version.modified)
        # Make sure all versions have the proper path
        for v in versions:
            if v.path != path:
                raise OptumiException("CloudFile has inconsistent versions")

    def download(self):
        # Download newest version
        self._versions[0].download()

    def remove(self):
        # Remove all versions of the file
        print("Removing file", self)
        optumi.core.delete_files(
            [x.hash for x in self._versions],
            [x.path for x in self._versions],
            [x.created for x in self._versions],
            "",
        )

    @property
    def versions(self):
        return self._versions

    @property
    def path(self):
        return self._path

    def __str__(self):
        return (
            self._path
            + " ("
            + str(len(self._versions))
            + (" versions)" if len(self._versions) > 1 else " version)")
        )
