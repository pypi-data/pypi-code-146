# encoding: utf-8
"""
@project: djangoModel->custom_merge
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户自定义 字典合并
@created_time: 2022/8/16 15:40
"""


class JoinList:
    def __init__(self, l_list, r_list, l_key="id", r_key="id"):
        self.l_key = l_key
        self.r_key = r_key
        self.l_list = l_list
        self.r_list = r_list

    def join(self):
        r_map = {str(item.pop(self.r_key)): item for item in self.r_list}
        for item in self.l_list:
            if str(item[self.l_key]) in r_map.keys():
                item.update(r_map[str(item[self.l_key])])
        return self.l_list
