#!/usr/bin/env python
# -*- coding=utf-8 -*-
from __future__ import annotations

import logging
import time
from typing import Any, Callable, Dict, Iterable, List

from .shared_file_lock import SharedFileLock

logger = logging.getLogger("filelock4s")


class DumpableWorker(Dict[str, Any], dict):
    """worker对象"""

    def set_running(self, is_running: bool):
        """设置worker运行状态

        Args:
            is_running (bool): 运行状态
        """
        self.update(is_running=is_running)

    def is_running(self) -> bool:
        """获取worker运行状态

        Returns:
            bool: 运行状态
        """
        return self.get("is_running", False)


class DumpableWorkerMap(Dict[str, DumpableWorker], dict):
    """Worker Pool对象"""

    def __init__(self, *args, **kargs):
        dict.__init__(self, *args, **kargs)
        for k, v in list(self.items()):
            self.update({k: DumpableWorker(v)})

    def add_worker(self, name: str):
        """添加worker

        Args:
            name (str): worker名称
        """
        self.update({name: DumpableWorker()})

    def start_worker(self, name: str):
        """启动worker

        Args:
            name (str): worker名称
        """
        worker = self.get(name)
        if worker is not None:
            worker.set_running(True)

    def stop_worker(self, name: str):
        """停止worker

        Args:
            name (str): worker名称
        """
        worker = self.get(name)
        if worker is not None:
            worker.set_running(False)

    def is_worker_running(self, name: str):
        """worker是否在运行

        Args:
            name (str): worker名称

        Returns:
            bool: 是否在运行
        """
        worker = self.get(name)
        if worker is not None:
            return worker.is_running()
        return False


class WorkerLockPool(SharedFileLock):
    """基于文件锁实现的任务队列锁锁池"""

    def __init__(self, shared_filename: str, pool_name: str, timeout: float = -1, poll_interval: float = 3):
        super().__init__(shared_filename, timeout)
        self._pool_name = pool_name
        self._poll_interval = poll_interval
        self._current_lock_pool: DumpableWorkerMap = None

    def parse(self):
        super().parse()
        current_lock_pool = self.shared_lock_pools.get(self._pool_name)
        if current_lock_pool is None:
            self._current_lock_pool = DumpableWorkerMap()
        else:
            self._current_lock_pool = DumpableWorkerMap(current_lock_pool)
        self.shared_lock_pools[self._pool_name] = self._current_lock_pool

    def get_worker_names(self):
        """获取所有worker名称列表

        Returns:
            List[str]: worker名称列表
        """
        return list(self._current_lock_pool.keys())

    def is_worker_running(self, worker_name: str):
        """某worker是否运行中

        Args:
            worker_name (str): worker名称

        Returns:
            bool: True or False
        """
        return self._current_lock_pool.is_worker_running(worker_name)

    def add_worker(self, worker_name: str):
        """添加worker

        Args:
            worker_name (str): worker名称
        """
        self._current_lock_pool.add_worker(worker_name)
        self.mark_changed(True)

    def get_free_worker_names(self):
        """获取所有空闲worker名称列表

        Returns:
            List[str]: worker名称列表
        """
        result: List[str] = []
        for worker_name in self.get_worker_names():
            if not self.is_worker_running(worker_name):
                result.append(worker_name)
        return result

    def acquire_to_start_worker(self, select_worker_callback: Callable[[Iterable[str]], str]):
        """尝试申请锁并运行一个worker（阻塞）

        Args:
            select_worker_callback (Callable[[List[str]], str]): 选择worker回调方法

        Returns:
            AcquireReturnProxy: 锁返回代理（使用with语句调用本方法）
        """

        class AcquireReturnProxy:
            def __init__(self, lock: WorkerLockPool, worker_name: str):
                self.lock = lock
                self.worker_name = worker_name

            def __enter__(self) -> WorkerLockPool:
                return self.lock

            def __exit__(self, exc_type, exc_value, traceback):
                self.lock.stop_worker(self.worker_name)

        while True:
            with self.acquire():
                logger.info("trying to acquire lock group<{}> select worker callback by current counters{}".format(self._pool_name, self._current_lock_pool))
                worker_name = select_worker_callback(self.get_free_worker_names())
                logger.info(
                    "trying to acquire successfully lock group<{}> start worker<{}> by current counters{} ".format(
                        self._pool_name, worker_name, self._current_lock_pool
                    )
                )
                if worker_name:
                    self.start_worker(worker_name)
                    return AcquireReturnProxy(self, worker_name)
            time.sleep(self._poll_interval)

    def start_worker(self, worker_name: str):
        """运行一个worker

        Args:
            worker (str): worker名称
        """
        self._current_lock_pool.start_worker(worker_name)
        self.mark_changed(True)

    def stop_worker(self, worker_name: str):
        """停止一个worker

        Args:
            worker (str): worker名称
        """
        with self.acquire():
            logger.info(
                "trying to acquire successfully lock group<{}> stop worker<{}> by current counters{}".format(
                    self._pool_name, worker_name, self._current_lock_pool
                )
            )
            self._current_lock_pool.stop_worker(worker_name)
            self.mark_changed(True)
