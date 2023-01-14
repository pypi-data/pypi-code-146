#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'andy.hu'
__mtime__ = '2021/07/09'

"""
import os
import sys

from loguru import logger as klogger

from clife_svc.libs.context import request_id


def _console_log_filter(record) -> bool:
    record['req_id'] = request_id.get()
    return True


def _format(record):
    if record['req_id']:
        return "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
               "<level>{level: <8}</level> | " \
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | " \
               "<cyan>{req_id}</cyan> | " \
               "<level>{message}</level>\n{exception}"
    else:
        return "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
               "<level>{level: <8}</level> | " \
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | " \
               "<level>{message}</level>\n{exception}"


klogger.remove(handler_id=None)
klogger.add(sys.stderr, filter=_console_log_filter, format=_format)
tlogger = klogger.bind(time=True)
clogger = klogger.bind(config=True)


def init_log(log_path: str, log_level='INFO'):
    """
    初始化服务日志模块
    :param log_path: 日志输出路径
    :param log_level: 日志级别，从低到高依次为 TRACE|DEBUG|INFO|SUCCESS|WARNING|ERROR|CRITICAL
    :return:
    """
    # 配置项日志
    klogger.add(os.path.join(log_path, 'config.log'), format=_format,
                filter=lambda record: record['extra'].get('config'))

    # 探针日志
    klogger.add(os.path.join(log_path, 'probe.log'), format=_format, retention='1 week',
                filter=lambda record: record['extra'].get('time'))
    # 通用日志
    klogger.add(os.path.join(log_path, '{time:YYYY-MM-DD}.log'),
                format=_format,
                level=log_level,
                enqueue=True,
                rotation='00:00',
                retention='10 days',
                encoding='utf-8',
                compression='zip',
                filter=lambda record: not record['extra'].get('time') and
                                      not record['extra'].get('config'))


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    print(os.path.dirname(os.path.dirname(__file__)))
    print(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    print(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
