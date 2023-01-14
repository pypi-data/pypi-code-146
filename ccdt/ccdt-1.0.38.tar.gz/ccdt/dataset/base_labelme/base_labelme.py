# -*- coding: utf-8 -*-
# @Time : 2022/3/25 14:05
# @Author : Zhan Yong
from tqdm import tqdm
from copy import deepcopy
import collections
import cv2
import numpy as np

from .label_infos import *
from .async_io_task import *
import time
import asyncio
import os


class BaseLabelme(object):
    """
    labelme数据集处理基类，实现数据打印、标注区域抠图、类别及flags名称重命名、根据labelme属性筛选、标注可视化
    """

    def __init__(self, *args, **kwargs):
        self.shape = None
        self.only_annotation = kwargs.get('only_annotation')
        self.labelme_dir = kwargs.get('labelme_dir')
        self.images_dir = kwargs.get('images_dir')
        self.file_formats = kwargs.get('file_formats')
        self.data_type = kwargs.get('data_type')
        self.input_dir = kwargs.get('input_dir')
        self.output_dir = kwargs.get('output_dir')
        self.function = kwargs.get('function')
        self.select_empty = kwargs.get('select_empty')
        self.num_labelme = 0  # json文件数量
        self.num_images = 0  # 图片文件数量
        self.num_background = 0  # 背景图片文件数量
        self.label2label_info = collections.defaultdict(list)  # 标注属性多项集
        self.data_paths = list()
        self.data_infos = list()
        self.filter_data = dict()
        from ccdt import Coco
        if type(self) == BaseLabelme:
            self.get_data_paths()
            self.load_labelme()
        elif type(self) == Coco:
            self.self2labelme()  # coco转labelme
            self.self2coco()  # labelme转coco
        self.update_property()  # 更新属性，用于信息打印、类别筛选
        # if self.function == 'merge':
        #     # 这里有一个错误，指定文件夹做为类别判断，如果文件夹变动会出错
        #     if self.images_dir not in self.label2label_info.keys():
        #         print(self.label2label_info.keys())
        #         assert False, '{} 类别合并功能发现数据集类别不对，请核对筛选类别'.format(self.images_dir)

    def __repr__(self):
        """
        数据集表格打印实现
        :return:
        """
        num_tb = pt.PrettyTable()
        num_tb.field_names = ['num_images', 'num_labelme', 'num_background']
        num_tb.add_row(
            [self.num_images, self.num_labelme, self.num_background])
        return str(num_tb)

    def __call__(self, *args, **kwargs):
        """
        把该类的实列变为可调用对象
        :param args:
        :param kwargs:其中filter_empty=False保留背景类，为True不保留背景类。
        only_empty=False为不保留背景类，为True只筛选背景类。
        name_classes为标签类别
        filter_flags为标签类别属性
        shape_type为标注形状
        """
        self.filter_label = kwargs.get('filter_label')
        self.filter_flags = kwargs.get('filter_flags')
        self.only_select_shapes = kwargs.get('only_select_shapes')
        self.filter_shape_type = kwargs.get('filter_shape_type')
        self.filter_combin = kwargs.get('filter_combin')
        self.shapes_attribute = kwargs.get('shapes_attribute')
        self.only_select_empty = kwargs.get('only_select_empty')
        self.auto_filter()
        return self

    def get_data_paths(self):
        """
        封装数据路径方法实现，把图片路径、图片名称、json路径、json名称，一一对应并封装成一个字典
        :return:
        """
        from ccdt import PathTest
        # 针对不同的功能实现，需要有不同路径组合，需要不同的判断条件
        if self.function == 'merge':  # 合并功能
            self.data_paths = PathTest.get_merge_paths(self.images_dir, self.file_formats, self.input_dir,
                                                       self.output_dir, self.data_type, self.only_annotation, )
        # 打印功能、筛选功能、重命名功能、抠图功能、labelme转coco功能
        if self.function == 'filter' or self.function == 'print' \
                or self.function == 'rename' or self.function == 'matting' or self.function == 'convert' \
                or self.function == 'delete':
            self.data_paths = PathTest.get_filter_paths(self.images_dir, self.file_formats, self.input_dir,
                                                        self.output_dir, self.data_type, self.only_annotation,
                                                        self.labelme_dir)
        return self.data_paths

    def load_labelme(self):
        """
        封装labelme的json文件数据，把整个json对象封装到labelme_info字典中
        :return:
        """
        print("加载labelme数据进度:")
        # ==============================异步读取数据到内存操作==================================================
        # async_time = time.time()
        # loop = asyncio.get_event_loop()
        # # future = asyncio.ensure_future([AsyncIoTask.json_load(data_path) for data_path in tqdm(self.data_paths)])
        # # loop.run_until_complete(future)
        # # print(future.result())
        # tasks = [AsyncIoTask.json_load(data_path) for data_path in tqdm(self.data_paths)]
        # loop.run_until_complete(asyncio.wait(tasks))
        # loop.close()
        # print('异步耗时')
        # print(time.time() - async_time)
        # ==============================异步读取数据到内存操作===================================================

        # ==============================同步读取数据到内存操作===================================================
        # start_time = time.time()
        for data_path in tqdm(self.data_paths):
            # 组合加载json文件的路径
            labelme_path = os.path.join(data_path['input_dir'], data_path['labelme_dir'], data_path['labelme_file'])
            try:
                with open(labelme_path, 'r', encoding='UTF-8') as labelme_fp:
                    data_path['labelme_info'] = json.load(labelme_fp)
                    if data_path['labelme_info']['imageData'] is not None:
                        data_path['labelme_info']['imageData'] = None
                    if not data_path['labelme_info']['shapes']:
                        data_path['background'] = True
            except Exception as e:
                # 如果没有json文件，读取就跳过，并设置为背景
                if 'No such file or directory' in e.args:
                    data_path['background'] = True
                    data_path['labelme_file'] = None
                else:  # 如果是其它情况错误（内容为空、格式错误），就删除json文件并打印错误信息
                    print(e)
                    print(labelme_path)
                    os.remove(labelme_path)
                data_path['background'] = True
            self.data_infos.append(data_path)
        # print(time.time() - start_time)
        # if async_time < start_time:
        #     print('读取数据到内存操作,异步耗时短')
        # if async_time > start_time:
        #     print('读取数据到内存操作,同步耗时短')
        return self.data_infos
        # ==============================同步读取数据到内存操作===================================================

    def self2labelme(self):
        """
        coco转labelme
        coco子类没有实现,就报错
        """
        raise NotImplementedError

    def self2coco(self):
        """
        labelme转coco
        coco子类没有实现,就报错
        """
        raise NotImplementedError

    @property
    def parser(self):
        """
        封装label、shape_type、flags、group_id属性，即把同一个标签下的全部属性封装列表里
        :return:
        """
        label = list()
        shape_type = list()
        flags = list()
        group_id = list()
        if 'label' in self.shape:
            if self.shape['label'] not in label:
                label.append(self.shape['label'])
        if 'shape_type' in self.shape:
            if self.shape['shape_type'] not in shape_type:
                shape_type.append(self.shape['shape_type'])
        if 'group_id' in self.shape:
            if self.shape['group_id'] not in group_id:
                group_id.append(self.shape['group_id'])
        if 'flags' in self.shape:
            if self.shape['flags'] not in flags:
                flags.append(self.shape['flags'])
        return label, shape_type, flags, group_id

    def update_property(self):
        """
        更新属性实现方法，包含统计背景类、类别标签对应属性合并
        """
        num_shapes = 0  # 计数shape为空
        num_labelme = 0  # 计数labelme_info
        num_images = 0  # 计数image_file
        num_background = 0  # 计数labelme_info为空并且image_file不为空.有图片没有标注的算背景，有json文件就算背景不对
        for data_info in self.data_infos:
            if data_info.get('image_file') and data_info.get('labelme_info') is None:
                num_background += 1
            if data_info.get('image_file'):
                num_images += 1
            if data_info.get('image_file') and data_info.get('labelme_info'):
                num_labelme += 1
                if not data_info.get('labelme_info').get('shapes'):
                    num_shapes += 1
                for shape in data_info.get('labelme_info').get('shapes'):
                    # 为类动态添加属性
                    self.shape = shape
                    label, shape_type, flags, group_id = self.parser
                    self.label2label_info[label[0]].append([shape_type, flags, group_id])
        self.num_images = num_images
        self.num_labelme = num_labelme
        self.num_background = num_background + num_shapes
        return self

    def crop_objs(self, min_pixel=10, ):
        """
        截取图像功能实现，一张图片画框多少，就扣多少，不管是否重叠
        标注形状类型，比如rectangle(长方形)、circle(圆)、polygon(多边形)、line(线)
        :param out_dir: 保存截取图像路径
        :param min_pixel:保存截取图片最小像素设置
        """
        print("截图图片进度:")
        for data_info in tqdm(self.data_infos):
            assert data_info['image_file'], '传入的图片路径为空，不能进行图片截取：{}'.format(data_info['labelme_file'])
            if data_info['labelme_file'] is None or data_info['labelme_info']['shapes'] == []:
                continue
            num_obj = 0
            for shape in data_info['labelme_info']['shapes']:
                # 组合保存抠图类别目录（Z:/4.my_work/9.zy/matting/00/00.images/call）
                save_img_dir = os.path.join(data_info['output_dir'], data_info['image_dir'], shape['label'])
                os.makedirs(save_img_dir, exist_ok=True)
                # 组合图片路径
                image_path = os.path.join(data_info['input_dir'], data_info['image_dir'], data_info['image_file'])
                # 组合抠图图片名称
                from ccdt import PathTest
                obj_img_file = PathTest.initialize(image_path)
                image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), 1)
                num_obj += 1
                crop_file_name = obj_img_file.parent.parent.stem + '_' + obj_img_file.stem + '_{:0>6d}'.format(
                    num_obj) + obj_img_file.suffix
                # 组合抠图图片存储路径
                crop_file_path = os.path.join(save_img_dir, crop_file_name)
                crop_obj = self.crop_rectangle(image, shape)
                if crop_obj.size == 0:
                    print("当前文件标注存在异常，路径如下所示:")
                    print(crop_file_path)
                # 默认像素小于10，就不进行截取，可以自动设置
                if crop_obj.shape[0] * crop_obj.shape[1] > min_pixel:
                    cv2.imencode(obj_img_file.suffix, crop_obj)[1].tofile(crop_file_path)

    @staticmethod
    def crop_rectangle(image, shape):
        """
        长方形截取计算过程
        :param image: 图像
        :param shape: 形状坐标
        :return:
        """
        h = image.shape[0]
        w = image.shape[1]
        # 把从任意角度标注兼容计算
        points = np.array(shape['points'])
        point_min, point_max = points.min(axis=0), points.max(axis=0)
        x1, y1 = int(max(0, min(point_min[0], w))), int(max(0, min(point_min[1], h)))
        x2, y2 = int(max(0, min(point_max[0], w))), int(max(0, min(point_max[1], h)))
        # y1:y2 x1:x2,针对负数框在图片的外面时截取不到,正常标注不会超出图片面积范围。max(0, min(x, img_info['width'])把负数变成0。np.clip(point_min)
        crop_obj = image[y1:y2, x1:x2]
        return crop_obj

    def rename(self, rename):
        """
        重命名功能实现，包含label和flags
        :param rename:
        """
        for data_info in self.data_infos:
            if data_info['labelme_info'] is not None:
                for shape in data_info['labelme_info']['shapes']:
                    if rename.get('label') is None and rename.get('flags') is None:
                        assert False, '输入的（--rename-label）重命名属性值为空'.format(rename)
                    if rename.get('label') and rename.get('flags'):
                        self.label_rename(shape, rename)
                        self.flags_rename(shape, rename)
                    if rename.get('flags'):
                        self.flags_rename(shape, rename)
                    if rename.get('label'):
                        self.label_rename(shape, rename)

    @staticmethod
    def label_rename(shape, rename):
        """
        重命名label
        :param shape:
        :param rename:
        """
        if shape['label'] in rename.get('label'):  # 修改标签类别名称
            shape['label'] = rename.get('label').get(shape['label'])

    @staticmethod
    def flags_rename(shape, rename):
        """
        重命名flags
        :param shape:
        :param rename:
        """
        # 判断一个列表的元素是否在另一个列表中
        if set(rename.get('flags').keys()).issubset(shape['flags'].keys()):
            for rename_key in rename.get('flags').keys():  # 修改标签类别属性名称
                shape['flags'][rename.get('flags')[rename_key]] = shape['flags'].pop(rename_key)

    def save_labelme(self):
        """
        根据类别保存labelme。coco转labelme需要现在内存中与datainfos关联上，然后用该方法存储到磁盘上。
        """
        print('处理数据保存处理进度:')
        # ==============================异步写内存数据到磁盘操作==================================================
        loop = asyncio.get_event_loop()
        async_time = time.time()
        if self.filter_data:
            filter_data_info = []
            for value in self.filter_data.values():
                for data in value:
                    filter_data_info.append(data)
            tasks = [AsyncIoTask.json_dump(value) for value in tqdm(filter_data_info)]
        else:
            tasks = [AsyncIoTask.json_dump(data_info) for data_info in tqdm(self.data_infos)]
        if not tasks:
            print('筛选后的保存数据为空，跳过本次处理')
            return
        loop.run_until_complete(asyncio.wait(tasks))
        print('异步耗时')
        print(time.time() - async_time)
        # ==============================异步写内存数据到磁盘操作===================================================

        # ==============================同步写内存数据到磁盘操作=========================================================
        # start_time = time.time()
        # for data_info in tqdm(self.data_infos):
        #     if data_info['image_file']:
        #         image_path = PathOperate.make_up_path(data_info['image_dir'], data_info['image_file'], out_dir, None,
        #                                               data_info['data_type'])
        #         copy_path = PathOperate.make_up_path(data_info['image_dir'], data_info['image_file'], None, None,
        #                                              data_info['data_type'])
        #         shutil.copy(copy_path, image_path)  # shutil.SameFileError,当同一文件夹拷贝相同文件会出错
        #     if data_info['labelme_file']:
        #         json_path = PathOperate.make_up_path(data_info['labelme_dir'], data_info['labelme_file'], out_dir, None,
        #                                              data_info['data_type'])
        #         # print(json_path)
        #         with open(json_path, "w", encoding='UTF-8') as labelme_fp:  # 以写入模式打开这个文件
        #             json.dump(data_info['labelme_info'], labelme_fp, indent=4, cls=Encoder)  # 从新写入这个文件，把之前的覆盖掉（保存）
        # print('同步耗时')
        # print(time.time() - start_time)
        # ==============================同步写内存数据到磁盘操作============================================================
        # if async_time < start_time:
        #     print('异步写内存数据到磁盘操作,异步耗时短')
        # if async_time > start_time:
        #     print('同步写内存数据到磁盘操作,同步耗时短')

    def visualization(self, out_dir):
        """
        可视化保存图片方法实现（未实现，因为OpenCV调用失败）
        :param out_dir:
        :param replaces:
        """
        global left_top, right_bottom, archive_image_path
        for data_info in self.data_infos:
            image = os.path.join(data_info['image_dir'], data_info['image_file'])

            # image = PathOperate.make_up_path(data_info['image_dir'], data_info['image_file'], None, None)
            # output_image = os.path.join(output_dir, data_info['image_file'])
            img = cv2.imread(str(image))
            # for old, new in replaces.items():
            #     replace_image_path = data_info['image_dir'].replace(old, new)
            #     # replace_json_path = data_info['labelme_dir'].replace(old, new)
            #     # 3. 去掉开头的 斜杠
            #     image_slash = replace_image_path.strip('\\/')
            #     # json_slash = replace_json_path.strip('\\/')
            #     archive_image_path = os.path.join(output_dir, image_slash)
            #     os.makedirs(archive_image_path, exist_ok=True)
            #     # archive_json_path = os.path.join(output_dir, json_slash)
            output_image = image.joinpath(out_dir, image.parent.parent.stem, image.parent.name, data_info['image_file'])
            # output_image = os.path.join(archive_image_path, data_info['image_file'])

            if data_info['labelme_info'] is not None:
                for shape in data_info['labelme_info']['shapes']:
                    # 左上角坐标点
                    left_top = (list(map(int, shape['points'][0])))
                    # 右下角坐标点
                    right_bottom = (list(map(int, shape['points'][1])))
                    # (0, 255, 255) => rgb 颜色,3 => 粗细程度,img => 图片数据,
                    cv2.rectangle(img, left_top, right_bottom, (0, 255, 255), 1)
                    # 保存图片
                    cv2.imwrite(str(output_image), img)

    def __add__(self, other):
        """
        类别筛选合并操作方法
        这合并存在一个问题，就是针对不同合并对象，把固定的第一个对象与传入的其它对象进行比较时，如果传入的对象元素在固定对象中不存在
        则保存输出合并数据时候，针对不在固定对象中的元素会单独创建文件夹保存，导致不为一个整体。如果把筛选的原始对象一起进行合并，可以避免这个问题
        考虑第一个对象有背景的情况，被比较的对象有背景的情况
        :param other:
        :return:
        """
        # 传入第二个对象与第一个对象进行比较
        for index, info in enumerate(other.data_infos):
            # 如果返回的索引不相等，直接把整个元素追加到第一个对象
            if self.find(info['image_file']) is None:
                if info['background']:
                    continue
                self.data_infos.append(info)
            # 如果返回的索引相等，表示为同一张图片，并把第二个对象的shapes元素全部追加到第一个对象
            else:
                other_shapes = list()
                if self.data_infos[self.find(info['image_file'])]['background']:
                    # 当筛选出来的数据，在合并过程中出现了背景，不能够全部跳过。被比较对象如果有值就追加，没有值就跳过
                    if self.data_infos[self.find(info['image_file'])]['labelme_info'] is None:
                        if info.get('labelme_info') is None:
                            continue
                        self.data_infos[self.find(info['image_file'])]['labelme_info'] = info.get('labelme_info')
                        self.data_infos[self.find(info['image_file'])]['background'] = False
                    if not self.data_infos[self.find(info['image_file'])]['labelme_info']['shapes']:
                        try:
                            for shape in info.get('labelme_info').get('shapes'):
                                if shape not in self.data_infos[self.find(info['image_file'])].get('labelme_info').get(
                                        'shapes'):
                                    other_shapes.append(shape)
                            self.data_infos[self.find(info['image_file'])]['background'] = False
                            # 把第二个对象的shapes元素全部追加到第一个对象，并且没有相同的元素
                            self.data_infos[self.find(info['image_file'])].get('labelme_info').get('shapes').extend(
                                other_shapes)
                        except Exception as e:
                            print(e)
                            print(info.get('labelme_info'))
                else:
                    if info.get('labelme_info') is None:
                        continue
                    if not info['labelme_info']['shapes']:
                        continue
                    # 如果俩个对象中的同一张图片下shapes元素全部相同，则跳过追加
                    if self.data_infos[self.find(info['image_file'])].get('labelme_info').get('shapes') \
                            == info.get('labelme_info').get('shapes'):
                        continue
                    # 如果俩个对象中的同一张图片下shapes元素部分相同，则取出第二个对象中不同shape元素
                    for shape in info.get('labelme_info').get('shapes'):
                        if shape not in self.data_infos[self.find(info['image_file'])].get('labelme_info').get(
                                'shapes'):
                            other_shapes.append(shape)
                    # 把第二个对象的shapes元素全部追加到第一个对象，并且没有相同的元素
                    self.data_infos[self.find(info['image_file'])].get('labelme_info').get('shapes').extend(
                        other_shapes)
        return self

    def find(self, image_file):
        """
        查找图片索引，image_file 是否在data_infos里面，如果在就返回下标索引，如果不在返回None用于追加判断
        :param image_file:
        :return:
        """
        for index, info in enumerate(self.data_infos):
            # 返回两个对象相同元素图片的索引
            if info['image_file'] == image_file:
                return index
        return None

    @classmethod
    def merge(cls, datasets):
        merge_dataset = datasets[0]
        # 截取列表元素进行循环
        for dataset in datasets[1:]:
            # 第0个和第一个相加后，赋值给一个变量，然后把这个变量看作一个整体，继续加第三个。
            merge_dataset = merge_dataset + dataset
        merge_dataset.save_labelme()

    def auto_filter(self):
        """
        筛选功能实现,包含label、flags、shape_type
        可自动与自定义
        :return:
        """
        background_element = list()
        self.filter_data['background'] = list()
        self.filter_data['positive'] = list()
        for data_info in self.data_infos:
            if self.only_select_shapes:  # 只筛选标注画框数据（正样本）
                if data_info['labelme_info'] is None:
                    continue
                elif data_info['labelme_info']:
                    if data_info['labelme_info']['shapes']:
                        self.filter_data['positive'].append(data_info)
                        data_info['output_dir'] = os.path.join(data_info['output_dir'], 'positive')
            if self.only_select_empty:  # 只背景筛选（负样本）
                if data_info['labelme_info'] is None:
                    self.filter_data['background'].append(data_info)
                    data_info['output_dir'] = os.path.join(data_info['output_dir'], 'background')
                if data_info['labelme_info']:
                    if not data_info['labelme_info']['shapes']:
                        self.filter_data['background'].append(data_info)
                        data_info['output_dir'] = os.path.join(data_info['output_dir'], 'background')
            if self.shapes_attribute:  # 按shapes的属性筛选，包含label、flags、shape_type
                filter_shapes = list()
                label = list()
                shape_type = list()
                flags = list()
                check_input = ['label', 'flags', 'shape_type']
                if self.shapes_attribute is None or self.shapes_attribute == "''" or \
                        self.shapes_attribute == '' or self.shapes_attribute not in check_input:
                    # 验证是否填写，是否填错
                    assert False, '输入的（--automatic）筛选属性不对'.format(self.shapes_attribute)
                if data_info['labelme_info'] is None:
                    if self.select_empty:
                        background_element.append(data_info)
                    else:
                        continue
                if data_info['labelme_info']:
                    if not data_info['labelme_info']['shapes']:
                        if self.select_empty:
                            background_element.append(data_info)
                        else:
                            continue
                    for shape in reversed(data_info['labelme_info']['shapes']):
                        if self.shapes_attribute == 'label':
                            label.append(shape['label'])
                        if self.shapes_attribute == 'flags':
                            if 'flags' in shape:
                                for key, value in shape['flags'].items():
                                    if shape['flags'][key] is True:
                                        flags.append(key)
                        if self.shapes_attribute == 'shape_type':
                            shape_type.append(shape['shape_type'])
                if self.filter_label is None and self.shapes_attribute == 'label':
                    # 自动筛选时，筛选元素集汇总。每一张图片的类别与整个对象中多个图片的类别取相同的部分
                    filter_shapes = set(label)
                elif self.filter_label and self.shapes_attribute == 'label':
                    # 指定元素筛选时，筛选元素集汇总
                    filter_shapes = set(label) & set(self.filter_label)
                if self.filter_flags is None and self.shapes_attribute == 'flags':
                    filter_shapes = set(flags)
                elif self.filter_flags and self.shapes_attribute == 'flags':
                    filter_shapes = set(flags) & set(self.filter_flags)
                if self.filter_shape_type is None and self.shapes_attribute == 'shape_type':
                    filter_shapes = set(shape_type)
                elif self.filter_shape_type and self.shapes_attribute == 'shape_type':
                    filter_shapes = set(shape_type) & set(self.filter_shape_type)
                for label_key in filter_shapes:
                    label_flags = deepcopy(data_info)
                    # 同一个对象中同一张图片的相同类别筛选
                    if label_key not in self.filter_data:
                        self.filter_data[label_key] = []
                        label_flags['labelme_info']['shapes'] = self.data_info_shapes(data_info, label_key,
                                                                                      self.filter_combin)
                        self.filter_data[label_key].append(label_flags)
                        # if self.only_select_shapes is False:
                        label_flags['output_dir'] = os.path.join(label_flags['output_dir'], label_key)
                    # 同一个对象，不同图片的相同类别筛选
                    if not (self.filter_data[label_key][-1]['image_dir'] == data_info['image_dir']
                            and self.filter_data[label_key][-1]['image_file'] == data_info['image_file']):
                        label_flags['labelme_info']['shapes'] = self.data_info_shapes(data_info, label_key,
                                                                                      self.filter_combin)
                        self.filter_data[label_key].append(label_flags)
                        # if self.only_select_shapes is False:
                        label_flags['output_dir'] = os.path.join(label_flags['output_dir'], label_key)
        if self.select_empty:  # 筛选label时，把背景元素追加到每个类别
            for key in self.filter_data.keys():
                for bk in deepcopy(background_element):  # 同一个对象反复迭代修改值，必须深度拷贝
                    # 根据键修改值，需要深度拷贝一份，否则相同的键为同时一起修改
                    bk['output_dir'] = os.path.join(self.output_dir, key)
                    self.filter_data[key].append(bk)
            del self.filter_data['background']
            del self.filter_data['positive']
        return self

    @staticmethod
    def data_info_shapes(data_info, label_key, filter_combin):
        """
        shapes属性对象处理
        组合筛选预想思路，以label为准，查找是否存在flags为真的，然后追加shape元素
        reversed()逆序遍历方便删除列表元素后继续迭代,并转列表为可迭代对象，减少内存消耗
        :param filter_combin:
        :param data_info:
        :param label_key:
        :return:
        """
        filter_result = list()
        for shape in reversed(data_info['labelme_info']['shapes']):
            # if shape['label'] == label_key and filter_combin:
            #     for key, value in shape['flags'].items():
            #         if shape['flags'][key] is True:
            #             filter_result.append(shape)
            if shape['label'] == label_key:
                filter_result.append(shape)
            if shape['shape_type'] == label_key:
                filter_result.append(shape)
            for key, value in shape['flags'].items():
                if shape['flags'][key] is True:
                    if key == label_key:
                        filter_result.append(shape)
        return filter_result

    def del_label(self, label):
        """
        指定label类别进行删除操作
        :param label:
        """
        for data_info in self.data_infos:
            if data_info['labelme_info'] is None:
                continue
            elif data_info['labelme_info']:
                for shape in reversed(data_info['labelme_info']['shapes']):
                    # print(shape)
                    if shape['label'] in label:
                        data_info.get('labelme_info').get('shapes').remove(shape)
