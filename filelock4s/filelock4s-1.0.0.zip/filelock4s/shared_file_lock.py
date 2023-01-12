#!/usr/bin/env python
# -*- coding=utf-8 -*-
from __future__ import annotations

import json
import logging
import os
from typing import Dict, Any

from filelock import FileLock

logger = logging.getLogger("filelock4s")


class SharedFileLock(FileLock):
    """共享文件锁（所有锁记录到一个共享数据文件中）"""

    def __init__(self, shared_filename: str, timeout: float = -1):
        """
        Args:
            shared_filename (str): 共享数据文件名
            timeout (float, optional): 获取锁时的超时时间. Defaults to -1.
        """
        FileLock.__init__(self, shared_filename + ".lock", timeout)
        self._shared_filename = shared_filename
        self._is_changed = False
        self._shared_lock_pools: Dict[str, Any] = None

    def parse(self):
        """读取并解析数据文件"""
        self._is_changed = False
        if not os.path.exists(self._shared_filename):
            self._shared_lock_pools = {}
        else:
            with open(self._shared_filename) as f:
                self._shared_lock_pools = json.load(f)

    def save(self):
        with open(self._shared_filename, "w") as f:
            json.dump(self._shared_lock_pools, f, indent=2)

    @property
    def is_changed(self):
        """数据内容是否变化（根据数据内容是否变化判断是否需要对文件进行一次写入）"""
        return self._is_changed

    def mark_changed(self, is_changed: bool):
        """标记数据内容已变化"""
        self._is_changed = is_changed

    @property
    def shared_lock_pools(self):
        """共享锁池"""
        return self._shared_lock_pools

    @property
    def shared_filename(self):
        """共享文件名"""
        return self._shared_filename

    def acquire(self):
        """获取文件锁"""
        result = super().acquire()
        self.parse()
        return result

    def release(self, force: bool = False):
        """释放文件锁"""
        if self._is_changed:
            self.save()
            self._is_changed = False
        super().release(force)

    def __str__(self):
        return self._shared_lock_pools.__str__()

    def __enter__(self):
        self.acquire()
        return self
