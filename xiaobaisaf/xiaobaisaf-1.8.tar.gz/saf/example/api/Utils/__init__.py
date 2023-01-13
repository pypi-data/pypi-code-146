#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/1/13 23:47
@File  : __init__.py
'''

import os
def CUR_ABS_PATH():
    ''' 返回 当前运行脚本的绝对路径 '''
    return os.path.dirname(os.path.realpath(__file__)) + '\\' if os.name == 'nt' else '/'