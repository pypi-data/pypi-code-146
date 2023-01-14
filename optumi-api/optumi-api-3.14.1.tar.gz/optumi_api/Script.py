##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .Executable import *


class Script(Executable):
    def __init__(self, path: str):
        super().__init__(path, ProgramType.PYTHON_SCRIPT)

    def __str__(self):
        return super().__str__()
