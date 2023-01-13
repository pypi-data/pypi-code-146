##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from enum import Enum
from typing import Union


class GpuType(Enum):
    UNSPECIFIED = "U"
    NVIDIA_K80 = "K80"
    NVIDIA_M60 = "M60"
    NVIDIA_P100 = "P100"
    NVIDIA_P40 = "P40"
    NVIDIA_V100 = "V100"
    NVIDIA_T4 = "T4"


class Resource:
    def __init__(self, gpu: Union[bool, GpuType] = True):
        self._gpu = gpu

    @property
    def gpu(self):
        return self._gpu

    def __str__(self):
        return "gpu=" + str(self.gpu)
