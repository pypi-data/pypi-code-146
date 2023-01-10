# encoding: utf-8
"""
@project: djangoModel->custom_merge
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户自定义 字典合并
@created_time: 2022/8/16 15:40
"""


class JoinList:
    @staticmethod
    def left_join(l_list, r_list, l_key="id", r_key="id"):
        r_map = {item[r_key]: item for item in r_list if r_key in item.keys()}
        return [item.update(r_map[item[l_key]]) for item in l_list if item[l_key] in r_map.keys()]
