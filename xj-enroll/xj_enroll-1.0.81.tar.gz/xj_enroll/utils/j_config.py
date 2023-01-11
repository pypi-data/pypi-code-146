# _*_coding:utf-8_*_
# 推荐工具JDict搭配使用
#  folder_path = root_config.IMAGE_UPLOAD_DIR or module_config.IMAGE_UPLOAD_DIR or "/upload/image/"
import configparser
import os


class JConfig(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    # 是否允许点操作符
    def allow_dotting(self, state=True):
        if state:
            self.__dict__ = self
        else:
            self.__dict__ = dict()

    # 当值不存在时返回None
    def __getattr__(self, *args):
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
