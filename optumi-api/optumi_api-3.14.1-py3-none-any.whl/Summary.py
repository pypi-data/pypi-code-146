##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import os
from .utils import *

import optumi_core as optumi


class ProgressMessage:
    def __init__(self, updates: list = []):
        self._updates = updates


class Summary:
    def __init__(
        self,
        name: str,
        initializing_lines: list,
        preparing_lines: list,
        running_lines: list,
    ):
        self._name = name
        self._initializing_lines = initializing_lines
        self._preparing_lines = preparing_lines
        self._running_lines = running_lines

    def download(self, path: str = None):
        f_name = optumi.utils.normalize_path(
            self._name.split("/")[-1] + ".summary" if path is None else path
        )
        with open(f_name, "w+") as f:
            f.write(
                collapseUpdates(
                    self._initializing_lines
                    + self._preparing_lines
                    + self._running_lines
                )
            )
        print("Summary saved to " + f_name)

    def __str__(self):
        return str(self._name)
