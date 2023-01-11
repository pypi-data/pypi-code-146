#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/9
"""
import time
import sys
import os

from fast_tracker import config


def lower_case_name(text):
    """
    将驼峰命名转为小写下划线命名
    :param text:
    :return:
    """
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)

    return "".join(lst).lower()


def log(text, *args, level=1):
    """
    log日志标准输出
    :param text: 日志内容（含替换符）
    :param args: 替换符对应的数据
    :param int level: 日志级别, 数字越高，打印信息越多，为0表示不打印日志。暂定级别有：0，1，2，3，4 可对应为logging的日志级别
    :return:
    """
    startup_debug = config.debug
    debug_level = config.debug_level
    if startup_debug and debug_level >= level:
        text = text % args
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sys.stdout.write("FAST: %s (%d) - %s\n" % (timestamp, os.getpid(), text))
        sys.stdout.flush()
