#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/1/13 23:47
@File  : YamlUtils.py
'''

''' 解析 *.YAML / *.YML文件 '''
from yaml import full_load
from typing import Union
from os import path as os_path, listdir, name

class yamlUtils(object):
    @staticmethod
    def read(files: Union[str, list] = None, dir_path: Union[str] = None):
        '''解析指定yaml文件(或者指定文件夹内的所有yaml文件)
        :param files: 指定单个（*.yml/*.yaml）文件或者存储在列表中的多个（*.yml/*.yaml）文件
        :param dir_path:  指定文件夹路径，解析其内的所有（*.yml/*.yaml）文件
        实例：
            yamlUtils.read(files='a.yml')
            yamlUtils.read(files='a.yaml')
            yamlUtils.read(files=['a.yml','b.yml'])
            yamlUtils.read(files=['a.yml','b.yaml'])
            yamlUtils.read(dir_path='../data')
            yamlUtils.read(dir_path='D:\\data')
        '''
        if files:
            if type(files) == str and os_path.isfile(files) and os_path.splitext(files)[1] in ['.yml', '.yaml']:
                ''' 单文件场景 '''
                files = [files]
            elif type(files) == list:
                ''' 多文件场景 '''
                ''' 过滤非法文件 '''
                files = [i for i in files if os_path.splitext(i)[1] in ['.yml', '.yaml'] and os_path.isfile(i)]
            else:
                raise TypeError('您输入的内容不支持！')
        elif dir_path:
            ''' 提供文件夹路径场景 '''
            step = '\\' if name == 'nt' else '/'
            files = [dir_path + step + i for i in listdir(dir_path) if os_path.splitext(i)[1] in ['.yml', '.yaml']]
        else:
            ''' 参数异常场景 '''
            raise ValueError('参数值有误！')
        if len(files) > 0:
            result = list()
            for file in files:
                result.append(full_load(open(file, 'r', encoding='UTF-8')))
            return result
        return []