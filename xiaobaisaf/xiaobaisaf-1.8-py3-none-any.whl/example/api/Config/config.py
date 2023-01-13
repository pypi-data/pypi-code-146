#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/1/13 23:47
@File  : config.py
'''

# 执行环境、报告路径、日志路径、邮件信息
import sys
import os
from configparser import ConfigParser

CUR_ABS_PATH = os.path.dirname(os.path.realpath(__file__)) + '\\' if os.name == 'nt' else '/'

Config = ConfigParser()
Config.read(CUR_ABS_PATH + 'config.ini', encoding='UTF-8')

class host(object):
    @staticmethod
    def test():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)

    @staticmethod
    def pro():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)

    @staticmethod
    def current():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return Config.get(__class__.__name__, Config.get(__class__.__name__, sys._getframe(0).f_code.co_name))

class report(object):
    @staticmethod
    def html_path():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return os.path.realpath(CUR_ABS_PATH + Config.get(__class__.__name__, sys._getframe(0).f_code.co_name))

    @staticmethod
    def allure_data_path():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return CUR_ABS_PATH + Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)

class email(object):
    @staticmethod
    def smtp():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)

    @staticmethod
    def port():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)

    @staticmethod
    def to():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)

    @staticmethod
    def username():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)

    @staticmethod
    def password():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)

    @staticmethod
    def subject():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)

    @staticmethod
    def content():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)

    @staticmethod
    def files():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return os.path.realpath(CUR_ABS_PATH + Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)) + '\\' if os.name == 'nt' else '/'


class log(object):
    @staticmethod
    def path():
        '''
        __class__.__name__                  获取所在类的类名
        sys._getframe(0).f_code.co_name     获取所在函数的函数名
        :return:
        '''
        return os.path.realpath(CUR_ABS_PATH + Config.get(__class__.__name__, sys._getframe(0).f_code.co_name)) + '\\' if os.name == 'nt' else '/'
