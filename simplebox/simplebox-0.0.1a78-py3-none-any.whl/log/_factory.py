#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import traceback
from functools import wraps
from logging import StreamHandler, Formatter, Logger, Handler, Filter, LoggerAdapter
from logging.handlers import RotatingFileHandler
from pathlib import Path
from threading import current_thread, Lock

from .. import _local_var, banner
from .._internal import _V
from ..classes import ForceType
from ..config import LogConfig, LogLevel
from ..utils import StringUtils, ObjectsUtils


class _LoggerWrapper(Logger):
    """
    Log wrapper.
    Provides logging processing.
    """
    __level = ForceType(LogLevel)
    __level_file = ForceType(LogLevel)
    __level_console = ForceType(LogLevel)

    def __init__(self, name: str, level: LogLevel, level_file: LogLevel, level_console: LogLevel):
        self.__level = level
        self.__level_file = level_file
        self.__level_console = level_console
        super().__init__(name, self.__level.value)
        self.__initialize()

    def __initialize(self):
        log_dir: Path = Path(LogConfig.dir)
        if not log_dir.exists():
            log_dir.mkdir(parents=True)
        if not LogConfig.off:
            for handler_type in ["ch", "fh"]:
                if handler_type == "fh" and LogConfig.off_file:
                    continue
                elif handler_type == "ch" and LogConfig.off_console:
                    continue
                self.addHandler(self.__handler__(handler_type))
        self.setLevel(self.__level.value)

    def __handler__(self, handler_type: str) -> Handler:
        if "ch" == handler_type:
            handler = StreamHandler()
            level_filter = Filter()
            level: LogLevel = self.__level_console if self.__level_console else LogLevel.CRITICAL
            level_filter.filter = lambda record: record.levelno <= level.value
            handler.addFilter(level_filter)
        elif "fh" == handler_type:
            handler = RotatingFileHandler(filename=str(LogConfig.path),
                                          encoding=LogConfig.coding,
                                          maxBytes=LogConfig.max_bytes,
                                          backupCount=LogConfig.backup_count)
            level_filter = Filter()
            level: LogLevel = self.__level_file if self.__level_file else LogLevel.CRITICAL
            level_filter.filter = lambda record: record.levelno <= level.value
            handler.addFilter(level_filter)
        else:
            raise Exception(f"unknown handler type: {handler_type}")

        handler.setLevel(LogConfig.level.value)
        handler.setFormatter(Formatter(LogConfig.format))
        return handler


class _LoggerAdapterWrapper(LoggerAdapter):

    def process(self, msg, kwargs):
        key = current_thread().ident
        thread_local = _local_var.__dict__
        if key not in thread_local or thread_local[key] is None:
            msg = f": {msg}"
            return msg, kwargs
        msg = f"[{thread_local[key]}]: {msg}"
        return super().process(msg, kwargs)

    def trace(self, value: _V = None):
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                if not value:
                    _value = ObjectsUtils.generate_random_str(16)
                else:
                    _value = value
                set_ok = self.__set(_value)
                try:
                    return func(*args, **kwargs)
                except BaseException as e:
                    if issubclass(type(e), OSError):
                        if hasattr(e, "strerror"):
                            origin_strerror = getattr(e, "strerror")
                            setattr(e, "strerror", f"[TRACE {self.get_trace_id()}] {origin_strerror}")
                    else:
                        e.__init__(f"[TRACE {self.get_trace_id()}] {str(e)}")
                    msg = f"\nEXCEPTION TRACE: {self.get_trace_id()}\n{'EXCEPTION STACK'.center(35, '*')}"
                    self.error(f"{msg}\n{traceback.format_exc()}")
                    raise
                finally:
                    if set_ok:
                        self.__remove()

            return __wrapper

        return __inner

    @staticmethod
    def __set(value: _V) -> bool:
        key = current_thread().ident
        if key and key not in _local_var.__dict__:
            _local_var.__dict__[key] = value
            return True
        return False

    @staticmethod
    def get_trace_id(default: _V = None) -> _V:
        key = current_thread().ident
        thread_local = _local_var.__dict__
        if key in thread_local:
            return thread_local[key]
        return default

    @staticmethod
    def __remove():
        key = current_thread().ident
        thread_local = _local_var.__dict__
        if key in thread_local:
            del thread_local[key]


class _LoggerFactory(object):
    __lock = Lock()
    __instance = None

    def __new__(cls, *args, **kwargs):
        with cls.__lock:
            if not cls.__instance:
                cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__rename_log()
        self.__show_banner()

    def __show_banner(self):
        if StringUtils.to_bool(os.getenv("SB_BANNER_OFF"), False):
            return
        if not LogConfig.banner:
            return
        log = self.get_logger()
        content = banner
        from .._internal import _banner
        for info in getattr(_banner, "__build_frame_banner_infos")():
            init_len = 160
            split_len = 32
            key_len = 20
            value_len = 0
            left_len = 4
            logo = info['title']
            logo_len = len(logo)
            content += f"""
{''.center(init_len, "#")}
{'#'.ljust(int((init_len - logo_len) / 2), " ")}{logo}{'#'.rjust(int((init_len - logo_len) / 2), " ")}
"""
            banner_dict = info['properties']
            for k, v in banner_dict.items():
                v_ = str(v)
                line = f"{k.ljust(key_len)}{'=>'.center(split_len, ' ')}{v_.rjust(value_len)}"
                content += f"{'#'.ljust(left_len, ' ')}{line}{'#'.rjust(init_len - len(line) - left_len, ' ')}\n"

            content += f"{''.center(init_len, '#')}"
        log.info(content)

    @staticmethod
    def get_logger(name: str = "root", level: LogLevel = LogConfig.level, level_file: LogLevel = LogConfig.level_file,
                   level_console: LogLevel = LogConfig.level_console) -> '_LoggerAdapterWrapper':
        if StringUtils.is_empty(name):
            name_ = "root"
        else:
            name_ = name
        if not issubclass(type(level), LogLevel):
            level_ = LogConfig.level
        else:
            level_ = level
        if not issubclass(type(level_file), LogLevel):
            level_file_ = LogConfig.level_file
        else:
            level_file_ = level_file
        if not issubclass(type(level_console), LogLevel):
            level_console_ = LogConfig.level_console
        else:
            level_console_ = level_console
        log = _LoggerWrapper(name_, level_, level_file_, level_console_)
        return _LoggerAdapterWrapper(log, {})

    @staticmethod
    def __rename_log():
        if LogConfig.cut:
            tmp = LogConfig.path
            index = 1
            while True:
                if tmp.exists():
                    new_name = f"{tmp.stem}-{index}{tmp.suffix}"
                    new_path = tmp.parent.joinpath(new_name)
                    if not new_path.exists():
                        tmp.rename(new_path)
                        break
                else:
                    break
                index += 1


LoggerFactory = _LoggerFactory()

__all__ = [LoggerFactory]
