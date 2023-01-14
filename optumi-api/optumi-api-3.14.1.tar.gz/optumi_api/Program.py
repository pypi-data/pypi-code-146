##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import os

import optumi_core as optumi


class Program:
    def __init__(self, name: str, run_num: str, program: str):
        self._name = name
        self._run_num = run_num
        self._program = program

    def download(self, path: str = None):
        extension = "." + self._name.split(".")[-1]
        f_name = optumi.utils.normalize_path(
            self._name.split("/")[-1].replace(
                extension, "-" + str(self._run_num) + extension
            )
            if path is None
            else path
        )
        with open(f_name, "w+") as f:
            f.write(self._program)
        print("Program saved to " + f_name)
