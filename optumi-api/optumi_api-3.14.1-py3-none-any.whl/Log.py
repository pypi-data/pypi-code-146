##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import os
from .utils import *

import optumi_core as optumi


class Log:
    def __init__(self, name: str, output: list):
        self._name = name
        self._output = output

    def download(self, path: str = None):
        f_name = optumi.utils.normalize_path(
            self._name.split("/")[-1] + ".log" if path is None else path
        )
        with open(f_name, "w+") as f:
            f.write(
                fixBackspace(fixCarriageReturn("".join([x[0] for x in self._output])))
            )
        print("Log saved to " + f_name)
