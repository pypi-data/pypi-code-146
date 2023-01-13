# -*- coding: utf-8 -*-
# @Time : 2022/3/25 13:52
# @Author : Zhan Yong
import json
import numpy as np


class Encoder(json.JSONEncoder):
    """
    labelme数据保存编码实现类
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(Encoder, self).default(obj)
