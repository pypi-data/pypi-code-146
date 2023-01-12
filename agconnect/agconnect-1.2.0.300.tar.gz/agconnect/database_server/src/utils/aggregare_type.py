# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from enum import Enum


class AggregateType(str, Enum):
    AVG = 'Average',
    SUM = 'Sum',
    MAX = 'Max',
    MIN = 'Min',
    COUNT = 'Count'
