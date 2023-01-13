#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/10 09:33
@Author  : WaveletAI-Product-Team Z
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : feature.py
@Desc    :
"""

import logging

_logger = logging.getLogger(__name__)


class Feature(object):

    def __init__(self, backend, id, name, desc, zone, type, json_data, create_time, create_user_id,
                 update_time, update_user_id):
        self._backend = backend
        self.id = id
        self.name = name
        self.desc = desc
        self.zone = zone
        self.type = type
        self.json_data = json_data
        self.create_time = create_time
        self.create_user_id = create_user_id
        self.update_time = update_time
        self.update_user_id = update_user_id
