# encoding: utf-8
"""
@project: PythonSuperMario-master->config
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 配置文件
@created_time: 2022/11/13 11:08
"""

import configparser
from configparser import ConfigParser
import os

from main.settings import BASE_DIR


class JConfig(ConfigParser):
    def __init__(self, *args, **kwargs):
        ConfigParser.__init__(self, *args, **kwargs)
        self.read()

    def read(self, filenames=BASE_DIR, encoding="utf-8-sig"):
        """获取配置文件，内容"""
        super().read(filenames, encoding)

    @staticmethod
    def get_section(path, section, encoding="utf-8-sig"):
        if not os.path.exists(path):
            return {}

        config = configparser.ConfigParser()
        config.read(path, encoding=encoding)
        if not config.has_section(section):
            return {}
        tuple_list = config.items(section)
        return {k: v for k, v in tuple_list}
