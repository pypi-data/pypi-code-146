#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/6 11:34
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : Sessions.py
@Desc    : 
"""
import logging

_logger = logging.getLogger(__name__)


class Session(object):
    """
    A class for running communication with WaveletAI.
    """
    def __init__(self, backend=None):
        self._backend = backend
