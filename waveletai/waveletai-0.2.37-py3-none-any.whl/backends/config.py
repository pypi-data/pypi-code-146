#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/11 15:41
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : config.py
@Desc    : 
"""


class Config(object):

    def __init__(self, api_url, display_url, min_recommended_version, min_compatible_version, max_compatible_version):
        self._api_url = api_url
        self._display_url = display_url
        self._min_recommended_version = min_recommended_version
        self._min_compatible_version = min_compatible_version
        self._max_compatible_version = max_compatible_version

    @property
    def api_url(self):
        return self._api_url

    @property
    def display_url(self):
        return self._display_url

    @property
    def min_recommended_version(self):
        return self._min_recommended_version

    @property
    def min_compatible_version(self):
        return self._min_compatible_version

    @property
    def max_compatible_version(self):
        return self._max_compatible_version
