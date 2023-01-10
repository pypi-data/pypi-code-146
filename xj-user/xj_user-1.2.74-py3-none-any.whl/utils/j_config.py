# _*_coding:utf-8_*_
# 推荐工具JDict搭配使用
#  folder_path = root_config.IMAGE_UPLOAD_DIR or module_config.IMAGE_UPLOAD_DIR or "/upload/image/"
# 简易用法
# from main.settings import BASE_DIR
# root_config = JConfig.get_section(str(BASE_DIR) + '/config.ini', 'xj_user', encode='utf-8-sig')

import configparser
import os


class JConfig(dict):
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get_section(path, section, encode="utf-8-sig"):
        if not os.path.exists(path):
            return {}

        config = configparser.ConfigParser()
        config.read(path, encoding=encode)
        if not config.has_section(section):
            return {}
        tuple_list = config.items(section)
        return {k: v for k, v in tuple_list}
