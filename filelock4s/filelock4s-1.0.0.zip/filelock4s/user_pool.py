#!/usr/bin/env python
# -*- coding=utf-8 -*-
from __future__ import annotations

import logging
import os
import time
from datetime import datetime
from typing import Dict, Any

from filelock import FileLock

from .shared_file_lock import SharedFileLock

logger = logging.getLogger("filelock4s")


class DumpableUser(Dict[str, Any], dict):
    pass


class DumpableUserMap(Dict[str, DumpableUser], dict):
    pass


class UserPool(SharedFileLock):
    """用户信息池"""

    def __init__(self, shared_filename: str, timeout: float = -1, poll_interval: float = 3):
        """
        Args:
            shared_filename (str): 共享数据文件名
            timeout (float, optional): 获取锁时的超时时间. Defaults to -1.
        """
        super().__init__(shared_filename, timeout)
        self._poll_interval = poll_interval
        self._current_user_name = ""
        self._current_user_lock_filename = ""
        self._pool_name = "__user__"
        self._user_pool: DumpableUserMap = None
        self.__finalizers = []

    def parse(self):
        super().parse()
        user_pool = self.shared_lock_pools.get(self._pool_name)
        if user_pool is None:
            self._user_pool = DumpableUserMap()
        else:
            self._user_pool = DumpableUserMap(user_pool)
        self.shared_lock_pools[self._pool_name] = self._user_pool

    def get_user_lock_filename(self, user_name):
        return self.lock_file + "." + user_name.replace("/", "-")

    def acquire_to_add_current_user(self, extra_name="", **extra_infos):
        """获取文件锁，然后添加当前用户信息"""
        class AcquireReturnProxy:
            def __init__(self, lock: UserPool, user_name: str, user_lock: FileLock):
                self._lock = lock
                self._user_name = user_name
                self._user_lock = user_lock

            def __enter__(self):
                self._user_lock.acquire()
                return self._lock

            def __exit__(self, exc_type, exc_value, traceback):
                self._lock.remove_user(self._user_name)
                self._user_lock.release()
                try:
                    os.remove(self._user_lock.lock_file)
                except OSError:
                    pass

        with self.acquire():
            if self._user_pool is None:
                self._user_pool = DumpableUserMap()
            self._current_user_name = "%d" % os.getpid()
            if extra_name:
                self._current_user_name += "/" + extra_name
            self._user_pool[self._current_user_name] = DumpableUser(create_time=datetime.now().isoformat())
            self._user_pool[self._current_user_name].update(extra_infos)
            self._is_changed = True
            return AcquireReturnProxy(self, self._current_user_name, FileLock(self.get_user_lock_filename(self._current_user_name)))

    def remove_user(self, user_name: str):
        """移除用户"""
        with self.acquire():
            self._user_pool.pop(user_name)
            self._is_changed = True

    def has_users(self):
        """是否还有用户"""
        if self._user_pool:
            return True
        return False

    def cleanup_dead_users(self):
        """清理不存在的用户"""
        if self._user_pool is None:
            return
        for user_name in list(self._user_pool.keys()):
            user_lock = FileLock(self.get_user_lock_filename(user_name), timeout=3)
            try:
                with user_lock:
                    pass
            except TimeoutError:
                pass
            else:
                try:
                    os.remove(user_lock.lock_file)
                except OSError:
                    pass
                self._user_pool.pop(user_name)
                self._is_changed = True

    def add_finalizer(self, function, *args, **kargs):
        """添加用户退出后需要执行的方法（这些方法需要所有的用户已全部退出才会真正执行）"""
        self.__finalizers.append((function, args, kargs))

    def acquire_to_do_finalizer(self):
        """获取文件锁，然后执行退出后的方法（这些方法需要所有的用户已全部退出才会真正执行）"""
        if not self.__finalizers:
            return
        while True:
            with self.acquire():
                logger.info("trying to do finalizer by current users{}".format(self._user_pool))
                if not self.has_users():
                    while self.__finalizers:
                        function, args, kargs = self.__finalizers.pop()
                        function(*args, **kargs)
                    return
            time.sleep(self._poll_interval)
