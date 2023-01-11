#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by ty 2021/4/6
"""

import logging

from fast_tracker import config


def getLogger(name=None):
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s [%(threadName)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    # 设置流式处理器为日志处理器
    logger.addHandler(ch)
    # propagate
    # 如果此属性为true，则除了附加到此记录器的任何处理程序之外，记录到该记录器的事件还将传递到更高级别（祖先）记录器的处理程序。
    # 消息直接传递给祖先记录器的处理程序-既不考虑所讨论的祖先记录器的级别也没有过滤器。
    # 如果此结果为false，则不会将日志记录消息传递给祖先记录器的处理程序。
    logger.propagate = False

    return logger


logger = getLogger('fast_tracker')


def init():
    # CRITICAL ERROR WARNING  INFO    DEBUG    NOTSET
    logging.addLevelName(logging.CRITICAL + 10, 'OFF')
    logger.setLevel(logging.getLevelName(config.logging_level))
