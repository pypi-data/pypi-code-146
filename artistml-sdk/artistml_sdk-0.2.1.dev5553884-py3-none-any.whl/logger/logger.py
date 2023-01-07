# coding=utf-8

import json
import logging
import os
import re
import sys
import threading
import time
from functools import wraps
from logging import Formatter
from logging import StreamHandler

import psutil

LOGGER_NAME = "artistml_log"

DEFAULT_LINE_FORMAT = "%(asctime)s %(levelname)-8s %(threadName)-30s " \
                   "[%(filename)s:%(module)s#%(lineno)d]: %(message)s"
DEFAULT_DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

artistml_logger = logging.getLogger(LOGGER_NAME)


def get_logger():
    """get the global logger for artistml_log"""
    return artistml_logger


def set_logger(logger):
    """set the global logger for artistml_log"""
    global artistml_logger
    artistml_logger = logger


def configure_logger(level, stream=None, line_format=None, date_format=None):
    """configure logging"""
    logger = get_logger()

    # Don't add handler twice
    if not logger.handlers:
        stream_handler = StreamHandler(stream or sys.stdout)
        formatter = Formatter(
            fmt=line_format or DEFAULT_LINE_FORMAT,
            datefmt=date_format or DEFAULT_DATE_FORMAT,
        )
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    logger.setLevel(level)

    return logger


def log_invoke(logger=None,
               level=logging.DEBUG,
               module=None,
               summary=True,
               independent=False,
               result_adapter=None,
               memory=False):
    #
    # log the invoke-status for a function
    # :param logger:
    #     - 使用的 logger-handler
    # :param summary:
    #     - true 同时记录调用参数和返回结果，
    #     - false 只记录调用参数
    # :param level
    #     - 日志级别，如果小于配置的展示级别，则无计算无记录
    # :param module
    #     - 被调用方法所属模块（建议: __name__ ）
    # :param independent:
    #     - 是否是独立方法/静态函数，默认 false
    # :param result_adapter:
    #     - default:None
    #     - 返回结果适配器（提炼返回结果的精简/有效内容）
    # :param memory:
    #     - default:False
    #     - 监控内存
    # :return: A function that wraps the function being decorated.
    # e.g.
    # - @log_invoke(summary=True, independent=True)
    # - def add(a,b):
    # -     return a+b
    # -
    # - add(2,b=8)
    # -------------------
    # - log:
    # - 2022/03/22 11:08:23 DEBUG MainThread [test.py:test#8]: call add(2, b=8) ---> (10)
    #
    class MemoryMonitor(threading.Thread):
        """内存监控线程"""

        def __init__(self):
            super(MemoryMonitor, self).__init__()
            self.__pid = os.getpid()
            self.__finished = False
            self.__start = 0
            self.__min = 0
            self.__max = 0
            self.__end = 0
            self.__average = 0
            self.__loop_times = 0
            self.start()

        def run(self):
            """不断监控内存变化"""
            while not self.__finished:
                p = psutil.Process(self.__pid)
                m = int(p.memory_full_info().uss / 1024 / 1024)
                if self.__max == 0 or m > self.__max:
                    self.__max = m
                if self.__min == 0 or m < self.__min:
                    self.__min = m
                if self.__start == 0:
                    self.__start = m
                self.__end = m
                self.__average = ((self.__loop_times * self.__average) +
                                  m) / (self.__loop_times + 1)
                self.__loop_times += 1
                if self.__loop_times >= 3600 * 4:
                    log_handler().log(logging.WARNING, "内存监控运行超过2小时")
                    break
                time.sleep(0.5)

        def close(self):
            """结束监控"""
            self.__finished = True

        def get_current_report(self):
            return "内存-启动(%dM),结束(%dM),最小(%dM),最大(%dM),平均(%dM)" % (
                self.__start, self.__end, self.__min, self.__max,
                self.__average)

    def log_handler():
        return logger or get_logger()

    def to_str(arg):
        """将任意类型的变量转化为 str 格式"""
        if arg is None:
            return "None"
        try:
            return json.dumps(arg)
        except TypeError:
            pass

        if isinstance(arg, list):
            list_inner_strs = [to_str(node) for node in arg]
            return '[' + ', '.join(list_inner_strs) + ']'
        if isinstance(arg, tuple):
            tuple_inner_strs = [to_str(node) for node in arg]
            return '(' + ', '.join(tuple_inner_strs) + ')'
        if isinstance(arg, dict):
            dict_inner_strs = [
                '%s: %s' % (to_str(k), to_str(v)) for (k, v) in arg.items()
            ]
            return '{' + ', '.join(dict_inner_strs) + '}'

        if hasattr(arg, "__name__"):
            return '%s|Type' % arg.__name__
        if hasattr(arg, "__class__"):
            try:
                arg_json = json.dumps(arg,
                                      sort_keys=True,
                                      indent=4,
                                      default=lambda o: o.__dict__
                                      if hasattr(o, "__dict__") else repr(o))
                return '%s|%s' % (arg.__class__.__name__, arg_json)

            except TypeError:
                pass
            return '%s|Instance' % arg.__class__.__name__
        return repr(arg)

    def arg_formatter(*args, **kwargs):
        """
        将参数格式化
         - 对于 sum = get_sum(1, 2, 3, d=4, e=5)
         - 返回"1, 2, 3, d=4, e=5"
        @param args:
        @param kwargs:
        @return:
        """
        unnamed_part = [
            to_str(args[i]) for i in range(0 if independent else 1, len(args))
        ]
        named_part = ["%s=%s" % (k, to_str(v)) for (k, v) in kwargs.items()]
        return ", ".join(unnamed_part + named_part)

    def result_formatter(result):
        """
        将返回结果格式化，允许自定义精简方法
        @param result:
        @return:
        """

        if result_adapter is not None:
            result = result_adapter(result)
        return to_str(result)

    def get_callee(func, args):
        """
        获取调用名，格式:
        - [module]::[class name (非独立方法才有) ]::[method name]
        @param func:
        @param args:
        @return:
        """
        callee = func.__name__
        if module is not None:
            if (not independent) and len(args) > 0:
                if hasattr(args[0], "__name__"):
                    callee = "%s::%s" % (args[0].__name__, callee)
                elif hasattr(args[0], "__class__"):
                    callee = "%s::%s" % (args[0].__class__.__name__, callee)
            callee = "%s::%s" % (module, callee)
        return callee

    def log(msg):
        """记录日志，去掉换行，适配调用栈层数"""
        msg = re.sub(r'(\r\n)|(\r)|(\n)|(\t)[hg]', '', msg)
        while True:
            tmp = msg.replace("  ", " ")
            if msg == tmp:
                break
            msg = tmp
        log_handler().log(level, msg, stacklevel=4)

    def decorator(func):
        """装饰器，记录调用日志，执行实际调用"""

        def log_summary(start_time, callee_str, args_str, result_str,
                        memory_monitor):
            time_str = "{:.2f}秒".format(time.time() - start_time)
            memory_str = "No memory monitor"
            if memory_monitor is not None:
                memory_str = memory_monitor.get_current_report()
                memory_monitor.close()
            log("%s | %s | call %s(%s) ---> (%s)" %
                (memory_str, time_str, callee_str, args_str, result_str))

        @wraps(func)
        def invoker(*args, **kwargs):
            # 如果展示日志级别 小于 要输出的日志级别，则跳过日志逻辑。

            need_log = level >= log_handler().level
            callee_str = ""
            args_str = ""
            if need_log:
                callee_str = get_callee(func=func, args=args)
                args_str = arg_formatter(*args, **kwargs) or ""

            start_time = time.time()
            memory_monitor = None
            if memory and need_log:
                memory_monitor = MemoryMonitor()
            try:
                result = func(*args, **kwargs)
                if need_log:
                    result_str = "(no-summary)"
                    if summary:
                        result_str = result_formatter(result)
                    # 同时记录调用参数和返回结果的日志
                    log_summary(start_time, callee_str, args_str, result_str,
                                memory_monitor)
                return result
            except Exception as e:
                result_str = "报错：%s" % (str(e))
                log_summary(start_time, callee_str, args_str, result_str,
                            memory_monitor)
                raise e

        return invoker

    return decorator
