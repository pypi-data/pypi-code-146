#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/6/29 13:01
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : async.py
@Product: WaveletAI
"""

from threading import Thread


def async_call(f):
    """
    异步注解
    :param f:
    :return:
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
