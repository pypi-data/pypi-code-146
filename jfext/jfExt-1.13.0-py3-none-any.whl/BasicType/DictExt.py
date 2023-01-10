# -*- coding: utf-8 -*-
"""
jf-ext.BasicType.DictExt.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018-2022 by the Ji Fu, see AUTHORS for more details.
:license: MIT, see LICENSE for more details.
"""

import json
from jfExt.EncryptExt import generate_md5


def dict_get_and_insert(dic, key, default):
    """
    >>> 字典: 获取字段, 未找到直接插入
    :param {dictionary} dic: 待处理字典
    :param {String} key: 键
    :param {Any} default: 默认插入值
    """
    if not dic.get(key, None):
        dic[key] = default
    return


def dict_flatten(obj):
    """
    >>> 字典拍平
    """
    from jfExt.BasicType.ListExt import list_to_string
    if not isinstance(obj, dict):
        return False
    new_obj = dict()
    for i in obj.keys():
        # 字典类型展开
        if isinstance(obj[i], dict):
            for j in obj[i].keys():
                tmp = list_to_string(obj[i][j])
                new_obj["{}_{}".format(i, j)] = tmp
            continue
        if isinstance(obj[i], list):
            new_obj[i] = list_to_string(obj[i])
            continue
        new_obj[i] = obj[i]
    return new_obj


def dict_gen_md5_by_model(source):
    """
    >>> 字典生成md5 by model对象
    """
    source['md5'] = ''
    source['update_time'] = ''
    return dict_gen_md5(source)


def dict_check_md5_by_model(source, md5):
    """
    >>> 字典检测md5值是否匹配 by model对象
    """
    source['md5'] = ''
    source['update_time'] = ''
    return dict_check_md5(source, md5)


def dict_gen_md5(source):
    """
    >>> 字典生成md5
    :param {Dictionary} source: 数据源
    :return {String}: md5字符串
    """
    if not isinstance(source, dict):
        return None
    source_json = json.dumps(source)
    return generate_md5(source_json)


def dict_check_md5(source, md5):
    """
    >>> 字典检测md5值是否匹配
    :param {Dictionary} source: 数据源
    :param {String} md5: 待检测md5值
    :return {Boolean}: 是否匹配
    """
    if not isinstance(source, dict):
        return False
    source_md5 = dict_gen_md5(source)
    if source_md5 == md5:
        return True
    else:
        return False
