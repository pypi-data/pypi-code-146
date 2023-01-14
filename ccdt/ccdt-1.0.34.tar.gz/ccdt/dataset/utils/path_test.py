# -*- coding: utf-8 -*-
# @Time : 2022/4/2 20:11
# @Author : Zhan Yong
import os
from pathlib import Path


class PathTest(object):
    def __init__(self, *args, **kwargs):
        """
        初始化方法
        :param args: 元组类型取值顺序，跟传参顺序有关
        :param kwargs:
        """
        self.dir_name = args[0]
        self.object_type = args[1]
        self.file_formats = args[2]
        self.coco_file = args[3]
        self.function = args[4]
        self.output_format = args[5]
        if self.function == 'merge':
            self.dir_paths = self.get_dir_paths()
        elif self.function == 'convert' and self.output_format == 'labelme':
            self.dir_paths = self.get_coco_to_labelme_paths()
        elif self.output_format == 'coco':
            self.dir_paths = self.get_dir_currency()
        else:
            self.dir_paths = self.get_dir_currency()

    def get_dir_paths(self):
        """
        递归组合，合并功能目录
        只循环一次，取第一层dirs目录
        :return:
        """
        path_name = list()  # 文件夹路径
        for root, dirs, files in os.walk(self.dir_name, topdown=True):
            dirs.sort()
            files.sort()
            if self.object_type == 'BaseLabelme':
                for dir_name in dirs:
                    input_data_format = dict(
                        type='',
                        images_dir='',
                        labelme_dir='',
                        file_formats='',
                        coco_file='',
                        input_dir=''
                    )
                    input_data_format['file_formats'] = self.file_formats
                    input_data_format['coco_file'] = self.coco_file
                    input_data_format['input_dir'] = self.dir_name
                    input_data_format['type'] = self.object_type
                    input_data_format['labelme_dir'] = dir_name
                    input_data_format['images_dir'] = dir_name
                    path_name.append(input_data_format)
                # 第一次循环结束就必须return
                return path_name

    @classmethod
    def get_merge_paths(cls, dir_name, file_formats, input_dir, output_dir, data_type, only_annotation):
        """
        递归组合，类别合并功能图片路径，把每一个类别的所有图片路径封装为一个对象。
        以图片为基准组合json文件索引目录
        :param dir_name:
        :param file_formats:
        :param input_dir:
        :param output_dir:
        :param data_type:
        :param only_annotation:
        :return:
        """
        data_paths = list()
        for root, dirs, files in os.walk(os.path.join(input_dir, dir_name), topdown=True):
            # 对目录和文件进行升序排序
            dirs.sort()
            files.sort()
            # 遍历文件名称列表
            if '01.labelme' in root:
                continue
            for file in files:
                obj_file = PathTest.initialize(file)
                if obj_file.suffix in file_formats:
                    make_image_dir = root.replace(os.path.join(input_dir, dir_name), '').strip('\\/')
                    make_labelme_dir = str(PathTest.initialize(make_image_dir).parent.joinpath('01.labelme'))
                    data_path = dict(image_dir=make_image_dir,
                                     image_file=file,
                                     labelme_dir=make_labelme_dir,
                                     labelme_file=obj_file.stem + '.json',
                                     input_dir=os.path.join(input_dir, dir_name),
                                     output_dir=output_dir,
                                     data_type=data_type,
                                     labelme_info=None,
                                     background=False,
                                     only_annotation=only_annotation, )
                    data_paths.append(data_path)
        return data_paths

    @classmethod
    def initialize(cls, images_dir):
        """
        路径实列对象初始化
        :param images_dir:
        :return:
        """
        obj_dir = Path(images_dir)
        return obj_dir

    def get_dir_currency(self):
        """
        通用递归路径组合，包含筛选功能、重命名功能、抠图功能、转换功能
        :return:
        """
        path_name = list()  # 文件夹路径
        for root, dirs, files in os.walk(self.dir_name, topdown=True):
            dirs.sort()
            files.sort()
            input_data_format = dict(
                type='',
                images_dir='',
                labelme_dir='',
                file_formats='',
                coco_file='',
                input_dir=''
            )
            for dir_name in dirs:
                # 存在的问题：如果约定目录（00.images与01.labelme）有变动，会导致数据加载不完整
                if dir_name == '00.images' or dir_name == '01.labelme':
                    replace_path = root.replace(self.dir_name, '').strip('\\/')
                    input_data_format['file_formats'] = self.file_formats
                    input_data_format['coco_file'] = self.coco_file
                    input_data_format['input_dir'] = self.dir_name
                    input_data_format['type'] = self.object_type
                    input_data_format['labelme_dir'] = os.path.join(replace_path, '01.labelme')
                    input_data_format['images_dir'] = os.path.join(replace_path, '00.images')
            if input_data_format.get('labelme_dir') != '' and input_data_format.get('images_dir') != '':
                # print(input_data_format.get('labelme_dir'))
                # print(input_data_format.get('images_dir'))
                # if input_data_format.get('labelme_dir') not in dirs:
                #     assert False, '{} 约定目录不为01.labelme'.format(root)
                # if input_data_format.get('images_dir') not in dirs:
                #     assert False, '{} 约定目录不为00.images'.format(root)
                path_name.append(input_data_format)
        return path_name

    @classmethod
    def get_filter_paths(cls, images_dir, file_formats, input_dir, output_dir, data_type, only_annotation, labelme_dir):
        """
        递归组合，筛选功能、重命名功能、抠图功能、的图片路径
        以图片为基准组合json文件索引路径
        :param images_dir:
        :param file_formats:
        :param input_dir:
        :param output_dir:
        :param data_type:
        :param only_annotation:
        :param labelme_dir:
        :return:
        """
        data_paths = list()
        for root, dirs, files in os.walk(os.path.join(input_dir, images_dir), topdown=True):
            # 对目录和文件进行升序排序
            dirs.sort()
            files.sort()
            # 遍历文件名称列表
            if '01.labelme' in root:
                continue
            for file in files:
                obj_file = PathTest.initialize(file)
                if obj_file.suffix in file_formats:
                    data_path = dict(image_dir=images_dir,  #
                                     image_file=file,
                                     labelme_dir=labelme_dir,
                                     labelme_file=obj_file.stem + '.json',
                                     input_dir=input_dir,  #
                                     output_dir=output_dir,
                                     data_type=data_type,
                                     labelme_info=None,
                                     background=False,
                                     only_annotation=only_annotation, )
                    data_paths.append(data_path)
        return data_paths

    @classmethod
    def get_videos_path(cls, root_dir, file_formats):
        """
        视频帧提取组合路径
        :param root_dir:
        :param file_formats:
        :return:
        """
        # dir_name_list = list()  # 文件夹名称
        # files_name = list()  # 文件名称
        # path_name = list()  # 文件夹路径
        file_path_name = list()  # 文件路径
        for root, dirs, files in os.walk(root_dir, topdown=True):
            dirs.sort()
            files.sort()
            # for dir_name in dirs:
            # if dir_name != '00.images' and dir_name != '01.labelme':
            # dir_name_list.append(dir_name)
            # 遍历文件名称列表
            for file in files:
                # 获取文件后缀
                file_suffix = os.path.splitext(file)[-1]
                # 如果读取的文件后缀，在指定的后缀列表中，则返回真继续往下执行
                if file_suffix in file_formats:
                    # 如果文件在文件列表中，则返回真继续往下执行
                    # files_name.append(file)
                    # path_name.append(root)
                    file_path_name.append(os.path.join(root, file))
        return file_path_name

    def get_coco_to_labelme_paths(self):
        """
        组合coco转labelme路径
        :return:
        """
        path_name = list()  # 文件夹路径
        for root, dirs, files in os.walk(self.dir_name, topdown=True):
            obj_path = Path(root)
            image_path = '00.images'
            labelme_path = '01.labelme'
            dirs.sort()
            files.sort()
            if self.object_type == 'Coco':
                input_data_format = dict(
                    type='',
                    images_dir='',
                    labelme_dir='',
                    file_formats='',
                    coco_file='',
                    input_dir=''
                )
                input_data_format['type'] = self.object_type
                input_data_format['input_dir'] = obj_path.parent.parent
                two_levels_path = os.path.join(root.split('/')[-2], root.split('/')[-1])
                input_data_format['images_dir'] = os.path.join(two_levels_path, image_path)
                input_data_format['labelme_dir'] = os.path.join(two_levels_path, labelme_path)
                input_data_format['coco_file'] = self.coco_file
                input_data_format['file_formats'] = self.file_formats
                path_name.append(input_data_format)
                # 第一次循环结束就必须return
                return path_name
