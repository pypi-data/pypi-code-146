# -*- coding: utf-8 -*-
# @Time : 2022/3/25 13:53
# @Author : Zhan Yong
from ccdt.dataset.base_labelme.label_infos import LabelInfo
from collections import Iterable


class ShowTool(object):
    def __init__(self, datasets):
        if isinstance(datasets, Iterable):
            self.datasets = datasets
        else:
            self.datasets = datasets
        self.data = None
        self.label_info = None

    def total_single_print(self):
        """
        所有数据集总打印处理
        """
        from ccdt import TotalLabelmeInfos
        data_info = TotalLabelmeInfos(self.datasets)
        for data in data_info:
            pass
        return data_info

    def deal_with(self, label2label_info):
        """
        shape_type属性打印实列化
        :param label2label_info:
        """
        label_info = LabelInfo(label2label_info)
        for label in label_info:
            pass
        self.label_info = label_info

    @staticmethod
    def clear_update(data):
        data.label2label_info.clear()  # 清空处理前的变量
        data.update_property()  # 更新属性

    def before_after(self, conditions):
        """
        所有打印筛选前后条件判断
        :param conditions:
        """
        if isinstance(self.datasets, Iterable):
            for data in self.datasets:
                if conditions == 1:  # 筛选前打印shapes属性判断条件
                    self.deal_with(data.label2label_info)
                elif conditions == 2:  # 筛选后打印shapes属性判断条件
                    self.clear_update(data)
                    self.deal_with(data.label2label_info)
                elif conditions == 3:  # 筛选前打印数量判断条件
                    self.clear_update(data)
                    self.data = data
                elif conditions == 4:  # 筛选后打印数量判断条件
                    data.update_property()
                    self.data = data
        else:
            if conditions == 1:
                self.deal_with(self.datasets.label2label_info)
            elif conditions == 2:
                self.clear_update(self.datasets)
                self.deal_with(self.datasets.label2label_info)
            elif conditions == 3:
                self.clear_update(self.datasets)
                self.data = self.datasets
            elif conditions == 4:
                self.datasets.update_property()
                self.data = self.datasets

    def shapes_before_attribute(self):
        """
        打印筛选前shapes属性，label_name（标签类别）、shape_type_name（标注形状）、flags_name（标注类别属性）
        """
        shapes_before = 1
        self.before_after(shapes_before)
        return self.label_info

    def shapes_after_attribute(self):
        """
        打印筛选出来后的shapes属性，label_name（标签类别）、shape_type_name（标注形状）、flags_name（标注类别属性）
        """
        shapes_after = 2
        self.before_after(shapes_after)
        return self.label_info

    def data_before_treatment(self):
        """
        打印筛选处理前，num_images（图片数量）、num_labelme（json文件数量）、num_background（有图片但没有标注的数量）
        """
        data_before = 3
        self.before_after(data_before)
        return self.data

    def data_after_treatment(self):
        """
        打印筛选处理后，num_images（图片数量）、num_labelme（json文件数量）、num_background（有图片但没有标注的数量）
        """
        data_after = 4
        self.before_after(data_after)
        return self.data
