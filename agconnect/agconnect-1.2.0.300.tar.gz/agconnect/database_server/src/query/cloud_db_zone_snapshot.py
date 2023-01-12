# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from __future__ import annotations
from typing import TypeVar, Generic, List

T = TypeVar('T')


class CloudDBZoneSnapshot(Generic[T]):
    __snapshot_objects: List[T]

    def __init__(self, snapshots_objects: List[T]):
        self.__snapshot_objects = snapshots_objects

    def get_snapshot_objects(self) -> List[T]:
        return self.__snapshot_objects
