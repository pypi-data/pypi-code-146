#!/usr/bin/env python
# -*- coding=utf-8 -*-
from __future__ import annotations

import logging
import time
from collections import namedtuple
from typing import Callable, Dict, Iterable, Optional

from .shared_file_lock import SharedFileLock

logger = logging.getLogger("filelock4s")


class DumpableSemaphoreCounter(Dict[str, int], dict):
    """信号量锁计数"""

    def set_init_count(self, count: int):
        """初始化信号量数值

        Args:
            count (int): 信号量数值
        """
        self.update(init=count)

    def get_init_count(self):
        """获取初始化信号量数值

        Returns:
            int: 初始化信号量数值
        """
        return self.get("init", 0)

    def get_used_count(self):
        """获取已使用的信号量数值

        Returns:
            int: 已使用的信号量数值
        """
        return self.get("used", 0)

    def increase_used(self, count=1):
        """申请count个信号量"""
        self.update(used=self.get("used", 0) + count)

    def decrease_used(self, count=1):
        """释放count个信号量"""
        self.update(used=self.get("used", 0) - count)


class DumpableSemaphoreCounterMap(Dict[str, DumpableSemaphoreCounter], dict):
    def __init__(self, *args, **kargs):
        dict.__init__(self, *args, **kargs)
        for k, v in list(self.items()):
            self.update({k: DumpableSemaphoreCounter(v)})

    def get_names(self):
        """获取所有计数器名称列表

        Returns:
            List[str]: 计数器名称列表
        """
        return list(self.keys())

    def set_sem_init_count(self, sem: str, count: int):
        """初始化某个锁信号量数值

        Args:
            sem (str): 锁名称
            count (int): 信号量数值
        """
        counter = self.get(sem)
        if counter is None:
            self.update({sem: DumpableSemaphoreCounter(init=count)})
        else:
            counter.set_init_count(count)

    def get_sem_init_count(self, sem: str):
        """获取某个锁初始化信号量数值

        Args:
            sem (str): 锁名称

        Returns:
            int: 初始化信号量数值
        """
        counter = self.get(sem)
        if counter is not None:
            return counter.get_init_count()
        return 0

    def get_sem_used_count(self, sem: str):
        """获取某个锁已使用的信号量数值

        Args:
            sem (str): 锁名称

        Returns:
            int: 已使用的信号量数值
        """
        counter = self.get(sem)
        if counter is not None:
            return counter.get_used_count()
        return 0

    def increase_sem_used(self, sem: str, count=1):
        """非阻塞方式的尝试申请某个锁count个信号量

        Args:
            sem (str): 锁名称

        Returns:
            bool: 申请成功时返回True，失败则返回False
        """
        counter = self.get(sem)
        if counter is None:
            self.update({sem: DumpableSemaphoreCounter()})
        return self.get(sem).increase_used(count)

    def decrease_sem_used(self, sem: str, count=1):
        """释放某个锁count个信号量"""
        counter = self.get(sem)
        if counter is None:
            self.update({sem: DumpableSemaphoreCounter()})
        return self.get(sem).decrease_used(count)


SemaphoreCount = namedtuple("SemaphoreCount", ["sem_name", "count"])


class SemaphoreLockPool(SharedFileLock):
    """基于文件锁实现的信号量锁锁池"""

    def __init__(self, shared_filename: str, pool_name: str, timeout: float = -1, poll_interval: float = 3):
        super().__init__(shared_filename, timeout)
        self._pool_name = pool_name
        self._poll_interval = poll_interval
        self._current_lock_pool: DumpableSemaphoreCounterMap = None

    def parse(self):
        super().parse()
        current_lock_pool = self.shared_lock_pools.get(self._pool_name)
        if current_lock_pool is None:
            self._current_lock_pool = DumpableSemaphoreCounterMap()
        else:
            self._current_lock_pool = DumpableSemaphoreCounterMap(current_lock_pool)
        self.shared_lock_pools[self._pool_name] = self._current_lock_pool

    def get_sem_names(self):
        """获取所有锁名称列表

        Returns:
            List[str]: 锁名称列表
        """
        return self._current_lock_pool.get_names()

    def set_sem_init_count(self, sem_name: str, count: int):
        """初始化某个锁信号量数值

        Args:
            sem_name (str): 锁名称
            count (int): 信号量数值
        """
        self._current_lock_pool.set_sem_init_count(sem_name, count)
        self.mark_changed(True)

    def get_sem_init_count(self, sem_name: str):
        """获取某个锁初始化信号量数值

        Args:
            sem_name (str): 锁名称

        Returns:
            int: 初始化信号量数值
        """
        return self._current_lock_pool.get_sem_init_count(sem_name)

    def get_sem_used_count(self, sem_name: str):
        """获取某个锁已使用的信号量数值

        Args:
            sem_name (str): 锁名称

        Returns:
            int: 已使用的信号量数值
        """
        return self._current_lock_pool.get_sem_used_count(sem_name)

    def get_free_sem_count_infos(self):
        return [
            SemaphoreCount(sem_name=sem_name, count=self.get_sem_init_count(sem_name) - self.get_sem_used_count(sem_name)) for sem_name in self.get_sem_names()
        ]

    def acquire_to_use_sem(self, to_acquire_sem_callback: Callable[[Iterable[SemaphoreCount]], Optional[Iterable[SemaphoreCount]]]):
        """尝试申请某个锁1个信号量（阻塞）

        Args:
            sem (str): 锁名称

        Returns:
            bool: 申请成功时返回True，失败则返回False
        """

        class AcquireReturnProxy:
            def __init__(self, lock: SemaphoreLockPool, to_acquire_sem_counts: Iterable[SemaphoreCount]):
                self.lock = lock
                self.to_acquire_sem_counts = to_acquire_sem_counts

            def __enter__(self) -> SemaphoreLockPool:
                return self.lock

            def __exit__(self, exc_type, exc_value, traceback):
                self.lock.decrease_sem_used(self.to_acquire_sem_counts)

        while True:
            with self.acquire():
                logger.info("trying to acquire lock group<{}> sems callback by current counters{}".format(self._pool_name, self._current_lock_pool))
                to_acquire_sem_counts = to_acquire_sem_callback(self.get_free_sem_count_infos())
                if to_acquire_sem_counts is not None:
                    logger.info(
                        "trying to acquire successfully lock group<{}> increase sems{} by current counters{}".format(
                            self._pool_name, to_acquire_sem_counts, self._current_lock_pool
                        )
                    )
                    for sem_count in to_acquire_sem_counts:
                        self._current_lock_pool.increase_sem_used(sem_count.sem_name, sem_count.count)
                        self.mark_changed(True)
                    return AcquireReturnProxy(self, to_acquire_sem_counts)
            time.sleep(self._poll_interval)

    def decrease_sem_used(self, sem_count_infos: Iterable[SemaphoreCount]):
        """释放某个锁1个信号量"""
        with self.acquire():
            logger.info(
                "trying to acquire successfully lock group<{}> decrease sems{} by current counters{}".format(
                    self._pool_name, sem_count_infos, self._current_lock_pool
                )
            )
            for sem_count in sem_count_infos:
                self._current_lock_pool.decrease_sem_used(sem_count.sem_name, sem_count.count)
                self.mark_changed(True)
