#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from collections import defaultdict
'''
Author: Gan Jun
Date: 2022.8
Usage: 生成yaml表格
'''

# yaml记得要先open
def yaml_write_str(yaml, input_strg, level = 0):
    """以yaml格式写入str

    :Args:
        * input_strg: string
        * level: 缩进级别, 4个空格为1级
    """
    space = int(level) * 4 * " "
    yaml.write("%s%s\n" %(space, input_strg))

def yaml_write_list(yaml, input_list, level = 0):
    """以yaml格式写入list

    :Args:
        * input_list: list
        * level: 缩进级别, 4个空格为1级
    """
    space = int(level) * 4 * " "
    for i in input_list:
        yaml.write("%s- %s\n" %(space, i))

def yaml_write_dict(yaml, input_dict, level = 0):
    """以yaml格式写入dict

    :Args:
        * input_dict: The dictionary
        * level: 缩进级别, 4个空格为1级
    """
    space = int(level) * 4 * " "
    for k in input_dict:
        if not k: continue
        yaml.write("%s%s:\n"%(space, k))
        if type(input_dict[k]) in [str,int,float]:
            yaml_write_str(yaml, input_dict[k], level + 1)
        elif type(input_dict[k]) == list:
            yaml_write_list(yaml, input_dict[k], level + 1)
        elif type(input_dict[k]) == dict or type(input_dict[k]) == type(defaultdict()):
            yaml_write_dict(yaml, input_dict[k], level + 1)
