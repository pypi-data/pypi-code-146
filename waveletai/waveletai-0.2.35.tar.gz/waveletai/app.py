#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/5/31 11:47
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : app.py
@Desc    : 应用实体
"""

import logging

_logger = logging.getLogger(__name__)


class App(object):

    def __init__(self, backend, id, name, desc, create_time, create_user_id, update_time, update_user_id):
        self._backend = backend
        self.id = id
        self.name = name
        self.desc = desc
        self.create_time = create_time
        self.create_user_id = create_user_id
        self.update_time = update_time
        self.update_user_id = update_user_id

    def update(self, name=None, tags=None, desc=None):
        """
        更新模型基础信息
        :param tags:应用标签
        :param name:应用名称
        :param desc:应用备注
        :return: Class `app` Object
        """
        return self._backend.update_app(name, tags, desc)

    def delete(self):
        """
        删除当前应用
        :return:
        """
        return self._backend.delete_app()

    def list_models(self):
        """
        获取应用下模型对象列表
        :return: List of Class `Model` Object
        """
        return self._backend.list_models()

    def create_model(self, name, desc='', auth_id='', git_url='', http_url=''):
        """
        当前应用下创建模型
        :param http_url: http地址 默认空
        :param auth_id: auth_id 默认空
        :param git_url: git地址 默认空
        :param name:模型名称
        :param desc:模型备注
        :return: List of Class `Model` Object
        """
        return self._backend.create_model(name, desc, auth_id, git_url, http_url)
