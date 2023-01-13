# -*- coding: utf-8 -*-
# @Time : 2022/3/25 13:54
# @Author : Zhan Yong
import prettytable as pt


class LabelInfo(object):
    """
    创建可迭代对象，操作labelme的json文件中shapes列表中包含的字典对象属性。最节约内存
    """

    def __init__(self, shapes_data):
        self.shapes_data = shapes_data
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

        if self.number < self.shapes_data.__len__():
            for label_key, label_infos in self.shapes_data.items():
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

    def __repr__(self):
        # property_tb = pt.PrettyTable()
        # property_tb.field_names = ['label_name', 'shape_type_name', 'flags_name']
        property_tb = pt.PrettyTable(['label_name', 'shape_type_name', 'flags_name'])
        for key, value in self.shapes_data_info.items():
            property_tb.add_row([key, value['shape_type'], value['flags']])
            # property_tb.add_row([key])
            # property_tb.add_row([value['flags']])
            # property_tb.add_row([value['shape_type']])

        # print(property_tb.get_string(title='title'))
        return str(property_tb.get_string(title='title'))
        # return str(property_tb)
