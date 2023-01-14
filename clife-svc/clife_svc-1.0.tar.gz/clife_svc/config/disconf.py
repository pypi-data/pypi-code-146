#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置中心
__author__ = 'andy.hu'
__mtime__ = '2021/07/09'

"""
import os
import sys

import requests

from clife_svc.libs.log import clogger
from clife_svc.libs import utils


_ENVIRONMENT = {
    0: {  # 开发环境
        'env_name': 'rd',
        'disconf_url': 'http://disconf.clife.net:8099/disconf-web/api'
    },
    1: {  # 测试环境
        'env_name': 'itest',
        'disconf_url': 'http://disconf.clife.net:8099/disconf-web/api'
    },
    2: {  # 生产环境
        'env_name': 'res',
        'disconf_url': 'http://disconf.clife.net:8099/disconf-web/api'
    },
    -1: {  # 本地环境
        'env_name': 'rd',
        'disconf_url': 'http://10.6.14.85:8099/disconf-web/api'
    },
}


class Disconf:
    """
    从 disconf 下载配置文件
    """

    def __init__(self, apps, version, keys: tuple):
        """ 构造函数
        :param apps: disconf配置app，多个使用逗号分隔
        :param version: 配置版本号
        :param keys: 配置文件名，缺省时只加载ai-commons.properties
        """
        __ENV = int(os.environ.get("ENVIRONMENT", -1))
        self.__ROOT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))

        self.__apps = self._split2list(apps)
        self.__sess = requests.session()
        self.__version = version
        self.__disconf_url = _ENVIRONMENT.get(__ENV).get('disconf_url')
        self.__env_name = _ENVIRONMENT.get(__ENV).get('env_name')
        # 下载disconf配置到根路径文件
        self.__disconf_path = os.path.join(self.__ROOT_DIR, 'local.properties')
        # 配置文件名称
        self.configs = ['ai-commons.properties', ] + self._split2list(keys)

        clogger.info('ROOT_PATH: {}'.format(self.__ROOT_DIR))
        clogger.info('ENVIRONMENT: {}'.format(__ENV))
        clogger.info('ENV_NAME: {}'.format(self.__env_name))
        clogger.info('DISCONF_URL: {}'.format(self.__disconf_url))

    @staticmethod
    def _split2list(keys):
        config_list = []
        if isinstance(keys, str):
            config_list.extend([_.strip() for _ in keys.replace('，', ',').split(',')])
        else:
            for key in keys:
                if isinstance(key, str):
                    config_list.extend([_.strip() for _ in key.replace('，', ',').split(',')])
                elif isinstance(key, list) or isinstance(key, tuple):
                    for _ in key:
                        config_list.append(_)
        return config_list

    def _download_file(self, app, key) -> dict:
        """
        从配置中心获取配置文件
        :param app: disconf配置app
        :param key: disconf配置文件的key（即配置文件名称）
        :return: 配置数据字典
        """

        url = self.__disconf_url + '/config/file'
        params = {
            'app': app,
            'version': self.__version,
            'env': self.__env_name,
            'key': key
        }
        try:
            resp = self.__sess.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                try:
                    return utils.format_multi_value(resp.text)
                except Exception as e:
                    clogger.error('Error format value：{}'.format(e))
                    raise e
            else:
                clogger.warning('Get disconf "{}" error, status_code:{}, response:{}'.format(key,
                                                                                             resp.status_code,
                                                                                             resp.text))
        except Exception as e:
            clogger.error('Get disconf error:{}'.format(e))
            raise e

    def get_disconf(self) -> dict:
        """
        获取当前项目下的所有配置数据字典
        :return:
        """
        clogger.info('Start downloading disconf files...')
        disconf_item = {}
        try:
            for app_name in self.__apps:
                for conf_key in self.configs:
                    item = self._download_file(app_name, conf_key)
                    if item:
                        disconf_item.update(item)
            self.__sess.close()

            if not disconf_item:
                clogger.error('Error download disconf from {}.'.format(self.__disconf_url))
                if os.path.exists(self.__disconf_path):
                    clogger.info('Try to load local disconf...')
                    with open(self.__disconf_path, 'r') as f:
                        disconf_item = utils.format_multi_value(f.read())
                    if not disconf_item:
                        clogger.info('Faild to load local disconf.')
                    else:
                        clogger.info('Load local disconf success.')
            else:
                clogger.info('Download disconf files finished.')

            for key, value in disconf_item.items():
                if any([_ in key for _ in ['secret', 'secret'.upper()]]):
                    clogger.info('disconf_item: {}=MD5({})'.format(key, utils.get_md5(value)))
                else:
                    clogger.info('disconf_item: {}={}'.format(key, value))
        except Exception as e:
            clogger.error('Error download disconf:{}'.format(e))
        finally:
            return disconf_item
