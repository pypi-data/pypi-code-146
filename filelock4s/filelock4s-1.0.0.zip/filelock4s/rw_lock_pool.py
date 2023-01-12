#!/usr/bin/env python
# -*- coding=utf-8 -*-
from __future__ import annotations

import logging
import time
from typing import Dict, Iterable, List

from .shared_file_lock import SharedFileLock

logger = logging.getLogger("filelock4s")


class DumpableRWCounter(Dict[str, int], dict):
    """读写计数器"""

    def get_reader_count(self):
        """获取当前的读计数

        Returns:
            int: 当前读计数
        """
        return self.get("reader", 0)

    def get_writer_count(self):
        """获取当前的写计数

        Returns:
            int: 当前写计数
        """
        return self.get("writer", 0)

    def increase_reader(self):
        """增加1个读计数"""
        self.update({"reader": self.get("reader", 0) + 1})

    def decrease_reader(self):
        """减少1个读计数"""
        self.update({"reader": self.get("reader", 0) - 1})

    def increase_writer(self):
        """增加1个写计数"""
        self.update({"writer": self.get("writer", 0) + 1})

    def decrease_writer(self):
        """减少1个写计数"""
        self.update({"writer": self.get("writer", 0) - 1})


class DumpableRWCounterMap(Dict[str, DumpableRWCounter], dict):
    """读写计数器集合，key为锁名称，value为计数器"""

    def __init__(self, *args, **kargs):
        dict.__init__(self, *args, **kargs)
        for k, v in list(self.items()):
            self.update({k: DumpableRWCounter(v)})

    def get_names(self):
        """获取所有计数器名称列表

        Returns:
            List[str]: 计数器名称列表
        """
        return list(self.keys())

    def get_reader_count(self, name: str):
        """获取某个计数器当前的读计数

        Args:
            name (str): 计数器名称

        Returns:
            int: 当前读计数
        """
        counter = self.get(name)
        if counter is None:
            return 0
        return counter.get_reader_count()

    def get_writer_count(self, name: str):
        """获取某个计数器当前的写计数

        Args:
            name (str): 计数器名称

        Returns:
            int: 当前写计数
        """
        counter = self.get(name)
        if counter is None:
            return 0
        return counter.get_writer_count()

    def increase_reader(self, name: str):
        """某个计数器增加1个读计数

        Args:
            name (str): 计数器名称
        """
        counter = self.get(name)
        if counter is None:
            self.update({name: DumpableRWCounter()})
        self.get(name).increase_reader()

    def decrease_reader(self, name: str):
        """某个计数器减少1个读计数

        Args:
            name (str): 计数器名称
        """
        counter = self.get(name)
        if counter is None:
            self.update({name: DumpableRWCounter()})
        self.get(name).decrease_reader()
        if self.get_reader_count(name) == 0 and self.get_writer_count(name) == 0:
            self.pop(name)

    def increase_writer(self, name: str):
        """某个计数器增加1个写计数

        Args:
            name (str): 计数器名称
        """
        counter = self.get(name)
        if counter is None:
            self.update({name: DumpableRWCounter()})
        self.get(name).increase_writer()

    def decrease_writer(self, name: str):
        """某个计数器减少1个写计数

        Args:
            name (str): 计数器名称
        """
        counter = self.get(name)
        if counter is None:
            self.update({name: DumpableRWCounter()})
        self.get(name).decrease_writer()
        if self.get_reader_count(name) == 0 and self.get_writer_count(name) == 0:
            self.pop(name)


class RWLockPool(SharedFileLock):
    """基于文件锁实现的读写锁锁池"""

    def __init__(self, shared_filename: str, pool_name: str, timeout: float = -1, poll_interval: float = 3):
        super().__init__(shared_filename, timeout)
        self._pool_name = pool_name
        self._poll_interval = poll_interval
        self._current_lock_pool: DumpableRWCounterMap = None

    def parse(self):
        super().parse()
        current_lock_pool = self.shared_lock_pools.get(self._pool_name)
        if current_lock_pool is None:
            self._current_lock_pool = DumpableRWCounterMap()
        else:
            self._current_lock_pool = DumpableRWCounterMap(current_lock_pool)
        self.shared_lock_pools[self._pool_name] = self._current_lock_pool

    def get_names(self):
        """获取所有锁名称列表

        Returns:
            List[str]: 锁名称列表
        """
        return self._current_lock_pool.get_names()

    def get_reader_count(self, name: str):
        """获取某个锁当前的读计数

        Args:
            name (List[str]): 锁名称，为None时返回所有

        Returns:
            int: 当前读计数
        """
        return self._current_lock_pool.get_reader_count(name)

    def get_writer_count(self, name: str):
        """获取某个锁当前的写计数

        Args:
            name (List[str]): 锁名称，为None时返回所有

        Returns:
            int: 当前写计数
        """
        return self._current_lock_pool.get_writer_count(name)

    def acquire_to_increase_readers(self, names: Iterable[str]):
        """锁增加1个读计数（阻塞）

        Args:
            name (List[str]): 锁名称列表
        """

        class AcquireReturnProxy:
            def __init__(self, lock: RWLockPool, names: Iterable[str]):
                self.lock = lock
                self.names = names

            def __enter__(self) -> RWLockPool:
                return self.lock

            def __exit__(self, exc_type, exc_value, traceback):
                self.lock.decrease_readers(self.names)

        while True:
            with self.acquire():
                logger.info("trying to acquire increase lock group<{}> readers{} by current counters{}".format(self._pool_name, names, self._current_lock_pool))
                if all(self.get_writer_count(name) == 0 for name in names):
                    logger.info(
                        "trying to acquire successfully increase lock group<{}> readers{} by current counters{}".format(
                            self._pool_name, names, self._current_lock_pool
                        )
                    )
                    for name in set(names):
                        self._current_lock_pool.increase_reader(name)
                    self.mark_changed(True)
                    return AcquireReturnProxy(self, names)
            time.sleep(self._poll_interval)

    def decrease_readers(self, names: Iterable[str]):
        """锁减少1个读计数（阻塞）

        Args:
            name (str): 锁名称列表
        """
        with self.acquire():
            logger.info(
                "trying to acquire successfully decrease lock group<{}> readers{} by current counters{}".format(self._pool_name, names, self._current_lock_pool)
            )
            for name in set(names):
                self._current_lock_pool.decrease_reader(name)
            self.mark_changed(True)

    def acquire_to_increase_writers(self, names: Iterable[str]):
        """锁增加1个写计数（阻塞）

        Args:
            name (str): 锁名称列表
        """

        class AcquireReturnProxy:
            def __init__(self, lock: RWLockPool, names: Iterable[str]):
                self.lock = lock
                self.names = names

            def __enter__(self) -> RWLockPool:
                return self.lock

            def __exit__(self, exc_type, exc_value, traceback):
                self.lock.decrease_writers(self.names)

        while True:
            with self.acquire():
                logger.info("trying to acquire increase lock group<{}> writers{} by current counters{}".format(self._pool_name, names, self._current_lock_pool))
                if all(self.get_writer_count(name) == 0 and self.get_reader_count(name) == 0 for name in names):
                    logger.info(
                        "trying to acquire successfully increase lock group<{}> writers{} by current counters{}".format(
                            self._pool_name, names, self._current_lock_pool
                        )
                    )
                    for name in set(names):
                        self._current_lock_pool.increase_writer(name)
                    self.mark_changed(True)
                    return AcquireReturnProxy(self, names)
            time.sleep(self._poll_interval)

    def decrease_writers(self, names: Iterable[str]):
        """锁减少1个写计数（阻塞）

        Args:
            name (str): 锁名称列表
        """
        with self.acquire():
            logger.info(
                "trying to acquire successfully decrease lock group<{}> writers{} by current counters{}".format(self._pool_name, names, self._current_lock_pool)
            )
            for name in set(names):
                self._current_lock_pool.decrease_writer(name)
            self.mark_changed(True)


class ReentrantRWLockPool(RWLockPool):
    """基于文件锁实现的可重入读写锁锁池"""

    def __init__(self, shared_filename: str, pool_name: str, timeout: float = -1, poll_interval: float = 3):
        super().__init__(shared_filename, pool_name, timeout, poll_interval)
        self._current_writers: List[str] = []
        self._current_readers: List[str] = []

    def acquire_to_increase_writers(self, names: Iterable[str]):
        """锁增加1个写计数（阻塞）

        Args:
            name (str): 锁名称列表
        """

        class AcquireReturnProxy:
            def __init__(self, lock: ReentrantRWLockPool, names: Iterable[str]):
                self.lock = lock
                self.names = names
                self.lock._current_writers.extend(self.names)

            def __enter__(self) -> ReentrantRWLockPool:
                return self.lock

            def __exit__(self, exc_type, exc_value, traceback):
                for name in self.names:
                    self.lock._current_writers.remove(name)
                self.lock.decrease_writers(self.names)

        while True:
            with self.acquire():
                logger.info("trying to acquire increase lock group<{}> writers{} by current counters{}".format(self._pool_name, names, self._current_lock_pool))
                if all(
                    self.get_writer_count(name) == self._current_writers.count(name) and self.get_reader_count(name) == self._current_readers.count(name)
                    for name in names
                ):
                    logger.info(
                        "trying to acquire successfully increase lock group<{}> writers{} by current counters{}".format(
                            self._pool_name, names, self._current_lock_pool
                        )
                    )
                    for name in set(names):
                        self._current_lock_pool.increase_writer(name)
                    self.mark_changed(True)
                    return AcquireReturnProxy(self, names)
            time.sleep(self._poll_interval)

    def acquire_to_increase_readers(self, names: Iterable[str]):
        """锁增加1个读计数（阻塞）

        Args:
            name (List[str]): 锁名称列表
        """

        class AcquireReturnProxy:
            def __init__(self, lock: ReentrantRWLockPool, names: Iterable[str]):
                self.lock = lock
                self.names = names
                self.lock._current_readers.extend(self.names)

            def __enter__(self) -> ReentrantRWLockPool:
                return self.lock

            def __exit__(self, exc_type, exc_value, traceback):
                for name in self.names:
                    self.lock._current_readers.remove(name)
                self.lock.decrease_readers(self.names)

        while True:
            with self.acquire():
                logger.info("trying to acquire increase lock group<{}> readers{} by current counters{}".format(self._pool_name, names, self._current_lock_pool))
                if all(self.get_writer_count(name) == self._current_writers.count(name) for name in names):
                    logger.info(
                        "trying to acquire successfully increase lock group<{}> readers{} by current counters{}".format(
                            self._pool_name, names, self._current_lock_pool
                        )
                    )
                    for name in set(names):
                        self._current_lock_pool.increase_reader(name)
                    self.mark_changed(True)
                    return AcquireReturnProxy(self, names)
            time.sleep(self._poll_interval)
