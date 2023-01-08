#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# -----------------------------------------------

import yaml
from ._parse import _parse_dict


def load(stream) :
    '''
    对 yaml 的 safe_load 进行二次封装
    :param stream: yaml 文件读取流，例如 file.read()
    :return: yaml 配置字典
    '''
    settings = yaml.safe_load(stream)
    return _parse_dict(settings)




