# -*- coding: utf-8 -*-
# @Time : 2022/3/30 11:35
# @Author : Zhan Yong
import prettytable as pt
from collections import Iterable


class TotalLabelmeInfos(object):
    """
    这里耗时太久，针对标签数量达到365个的时候，打印会很耗时
    """
    def __init__(self, shapes_data):
        self.obj_judge_condition = 0  # 数据集判断条件，单数据集为2，多数据集为1
        self.shapes_data = list()
        self.title = ''
        self.num_labelme = 0
        self.num_images = 0
        self.num_background = 0
        if isinstance(shapes_data, Iterable):  # 判断传入对象是否为可迭代对象
            self.shapes_data = shapes_data
            self.obj_judge_condition = 1
        else:
            self.shapes_data.append(shapes_data)
            self.obj_judge_condition = 2
        self.number = 0
        self.shapes_data_info = dict()

    def __iter__(self):
        return self

    def __next__(self):
        """
        每次迭代出想要的内容，又能抛出异常终止迭代，raise StopIteration
        #  https://www.cnblogs.com/xifengmo/p/11029391.html
        :return:
        """
        # cursor = 0
        # while cursor < len(self.shapes_data):
        #     yield self.shapes_data.items[cursor]
        #     cursor += 1
        # if self.number <= self.number:

        if self.number < self.shapes_data.__len__():
            for shapes_data in self.shapes_data:
                if self.obj_judge_condition == 1:
                    self.title = str(shapes_data.input_dir)
                    self.num(shapes_data.num_labelme, shapes_data.num_images, shapes_data.num_background)
                elif self.obj_judge_condition == 2:
                    # from ccdt.dataset.utils.path_operate import PathOperate
                    from ccdt.dataset import PathTest
                    title_path = PathTest.initialize(shapes_data.input_dir)
                    slash = str(title_path.joinpath(shapes_data.input_dir, shapes_data.images_dir))
                    self.title = slash.replace('\\', '/')  # 对象转字符串时，有转义字符，替换后方便，直接输入路径
                    self.num(shapes_data.num_labelme, shapes_data.num_images, shapes_data.num_background)
                for label_key, label_infos in shapes_data.label2label_info.items():
                    self.label_info(label_key, label_infos)
                self.number += 1
            return self.shapes_data_info
        else:
            raise StopIteration  # 抛出异常停止遍历

    def label_info(self, label_key, label_info):
        """
        封装同一个标签类别对应的相关属性为字典，方便打印输出
        封装后数据结构：{{'person': {'shape_type': ['rectangle'], 'flags': ['狗狗', '活', '安全帽', '工装'], 'group_id': [None]}}
        :param label_key: 标签类别
        :param label_info: 标签类别对应相关属性
        """
        label_shape_flag_group = dict()
        label_shape_flag_group[label_key] = {'shape_type': [], 'flags': [], 'group_id': []}
        shape_type = list()
        group_id = list()
        flags = list()
        for label in label_info:
            shape_type += label[0]
            flags += label[1]
            group_id += label[2]
            label_shape_flag_group[label_key]['shape_type'] = list(set(shape_type))
            label_shape_flag_group[label_key]['group_id'] = list(set(group_id))
        label_shape_flag_group[label_key]['flags'] = list(set(self.flags_info(flags)))
        return self.shapes_data_info.update(label_shape_flag_group)

    def flags_info(self, flags):
        """
        封装类别标签属性flags，把同一个标签类别下flags属性值为True的键封装成列表返回
        封装前数据结构：<class 'list'>: [{'活': False}, {'狗狗': True}, {'工装': False}, {'安全帽': True}]
        封装后数据结构：['狗狗','工装']
        :param flags:
        :return:
        """
        fg = list()
        for flag in flags:
            for key, value in flag.items():
                if flag[key] is True:
                    fg.append(key)
        return fg

    def num(self, num_labelme, num_images, num_background):
        """
        对象图片数量、json文件数量、背景图片数量统计
        :param num_background:
        :param num_images:
        :param num_labelme:
        """
        self.num_labelme += num_labelme
        self.num_images += num_images
        self.num_background += num_background

    def __repr__(self):
        property_tb = pt.PrettyTable(['label_name', 'shape_type_name', 'flags_name'])
        for key, value in self.shapes_data_info.items():
            property_tb.add_row([key, value['shape_type'], value['flags']])
        # print(property_tb.get_string(title=self.title))
        num_tb = pt.PrettyTable(['num_images', 'num_labelme', 'num_background'])
        num_tb.add_row([self.num_images, self.num_labelme, self.num_background])
        print(num_tb.get_string(title=self.title))
        return str(property_tb.get_string(title=self.title))
