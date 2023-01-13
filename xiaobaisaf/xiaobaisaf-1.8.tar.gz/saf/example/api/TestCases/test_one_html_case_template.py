#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/1/13 23:47
@File  : test_one_html_case_template.py
'''

import os
import pytest
from loguru import logger
from saf.utils.YamlUtils import yamlUtils
from saf.example.api.Config.config import log

''' 初始化日志 '''
logger.add(log.path() + 'info.log', level='INFO', rotation='1 days', retention='7 days', enqueue=True, encoding='UTF-8')
logger.add(log.path() + 'error.log', level='ERROR', rotation='1 days', retention='7 days', enqueue=True, encoding='UTF-8')

''' 获取当前脚本运行脚本的绝对路径，避免环境不同导致的脚本运行错误 '''
CUR_ABS_PATH = os.path.dirname(os.path.realpath(__file__)) + '\\' if os.name == 'nt' else '/'
YAML_FILE_PATH = os.path.realpath(CUR_ABS_PATH + '../data/') + '\\' if os.name == 'nt' else '/'

def setup_module(): pass

def teardown_module(): pass

class TestClass(object):
    ''' 解析测试数据文件*.yml|*.yaml '''
    case_list = [YAML_FILE_PATH + f for f in os.listdir(YAML_FILE_PATH) if os.path.splitext(f)[1] in ['.yml', '.yaml']]

    @pytest.mark.parametrize('filename', case_list)
    def test_case(self, filename):
        ''' 解析YAML文件 '''
        result = yamlUtils.read(files=filename)
        logger.info(f'{filename}解析结果：{result}')

        ''' 执行测试 '''
        logger.info('开始执行用例数据...')