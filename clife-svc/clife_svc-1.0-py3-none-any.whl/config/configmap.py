#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ConfigMap工具
__author__ = 'YAnho.wen'
__mtime__ = '2021/12/28'

"""
import os

from clife_svc.libs import utils
from clife_svc.libs.log import clogger


class ConfigMap:
    """
    从 ConfigMap 挂载文件获取配置
    """

    def __init__(self):
        self.__configmap_path = os.path.join(os.getcwd(), 'configmap')
        clogger.info('CONFIGMAP_PATH: {}'.format(self.__configmap_path))

        clogger.info('Start loading configmap files...')
        self.configmap = self._load_configmap_file()
        clogger.info('Load configmap files finished.')
        self._log_all_conf()

    def get(self, key):
        """
        获取ConfigMap文件的配置内容
        """
        return self.get_all().get(key)

    def get_all(self):
        """
        获取所有ConfigMap
        """
        config_map = self._load_configmap_file()
        if self.configmap != config_map:
            clogger.info('The ConfigMap has been updated.')
            self.configmap = config_map
            self._log_all_conf()
        return config_map

    def _log_all_conf(self):
        for key, value in self.configmap.items():
            if any([_ in key for _ in ['secret', 'secret'.upper()]]):
                clogger.info('configmap_item: {}=MD5({})'.format(key, utils.get_md5(value)))
            else:
                clogger.info('configmap_item: {}={}'.format(key, value))

    def _load_configmap_file(self):
        """
        获取最新的ConfigMap文件内容
        """
        config_map = {}
        if os.path.exists(self.__configmap_path):
            for file_name in os.listdir(self.__configmap_path):
                file_path = os.path.join(self.__configmap_path, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        items = utils.format_multi_value(f.read())
                    config_map.update(items)
        return config_map
