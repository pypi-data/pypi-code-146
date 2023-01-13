# -*- coding: utf-8 -*-
# @Time : 2022/3/25 14:08
# @Author : Zhan Yong
from ccdt.dataset.utils import Encoder, PathTest
import shutil
import json
import os


class AsyncIoTask(object):
    """
    异步协程IO处理实现类
    参考网址：https://zhuanlan.zhihu.com/p/59621713
    """

    @staticmethod
    async def json_dump(data_info):
        """
        异步协程IO：写json数据到磁盘，拷贝图片数据到磁盘
        :param data_info:
        """
        copy_path = ''
        json_path = ''
        # print(f'get test for {data_info} times')
        # print(f'get test for {out_dir} times')
        jpg = PathTest.initialize(data_info['image_file'])
        # 如果图片名称后缀格式重复多次，就进行重写json文件后保存，重命名图片名称
        if data_info['image_file'].count(jpg.suffix) >= 2:
            # print(data_info['input_dir'])
            # print(data_info['image_dir'])
            # print(data_info['labelme_file'])
            # print(data_info['labelme_info'])
            # print('数据存在问题，路径如下')
            image_file = os.path.join(data_info['input_dir'], data_info['image_dir'], data_info['image_file'])
            if data_info['labelme_file']:
                labelme_file = os.path.join(data_info['input_dir'], data_info['image_dir'], data_info['labelme_file'])
                print(labelme_file)
            print(image_file)

            # print(old_image_path)
            # if data_info['labelme_info']:
            #     labelme_info = data_info['labelme_info']['imagePath'].replace(jpg.suffix, '')
            #     image_file = data_info['image_file'].replace(jpg.suffix, '')
            #     rewrite_labelme_info = labelme_info + jpg.suffix
            #     rewrite_image_file = image_file + jpg.suffix
            #     labelme_file = data_info['labelme_file'].replace(jpg.suffix, '')
            #     data_info['image_file'] = rewrite_image_file
            #     data_info['labelme_file'] = labelme_file
            #     data_info['labelme_info']['imagePath'] = rewrite_labelme_info
            #     new_image_path = os.path.join(data_info['input_dir'], data_info['image_dir'], rewrite_image_file)
            #     # 重命名图片名称
            #     os.rename(old_image_path, new_image_path)
            # else:
            #     # 只重命名图片名称
            #     image_file = data_info['image_file'].replace(jpg.suffix, '')
            #     rewrite_image_file = image_file + jpg.suffix
            #     new_image_path = os.path.join(data_info['input_dir'], data_info['image_dir'], rewrite_image_file)
            #     os.rename(old_image_path, new_image_path)
            # print(old_image_path)
        # 组合保存图片的文件夹路径
        save_images_dir = os.path.join(data_info['output_dir'], data_info['image_dir'])
        os.makedirs(save_images_dir, exist_ok=True)
        # 组合保存json的文件夹路径
        save_labelme_dir = os.path.join(data_info['output_dir'], data_info['labelme_dir'])
        os.makedirs(save_labelme_dir, exist_ok=True)
        # 组合输出json文件路径。其中replace("\\", "/")是为了解决OSError: [Errno 22] Invalid argument错误
        if data_info['labelme_file']:
            json_path = os.path.join(save_labelme_dir, data_info['labelme_file']).replace("\\", "/")
        # 组合拷贝被拷贝图片的路径
        if data_info['data_type'] == 'Coco':
            # if jpg.is_file():
            coco_image_dir = PathTest.initialize(data_info['image_dir']).parent
            copy_path = os.path.join(data_info['input_dir'], coco_image_dir, data_info['image_file'])
            # else:
            #     # 针对特殊目录手动修改并组合
            #     coco_image_dir = PathTest.initialize(data_info['image_dir']).parent
            #     copy_path = os.path.join(data_info['input_dir'], coco_image_dir, data_info['image_file'])

        if data_info['data_type'] == 'BaseLabelme':
            copy_path = os.path.join(data_info['input_dir'], data_info['image_dir'], data_info['image_file'])
        if data_info['only_annotation'] is False:
            try:
                shutil.copy(copy_path, save_images_dir)  # shutil.SameFileError,当同一文件夹拷贝相同文件会出错
            except Exception as e:
                print(e)
                print(copy_path)
                print(save_images_dir)
        try:
            with open(json_path, "w", encoding='UTF-8',) as labelme_fp:  # 以写入模式打开这个文件
                    json.dump(data_info['labelme_info'], labelme_fp, indent=2, cls=Encoder)  # 从新写入这个文件，把之前的覆盖掉（保存）
        except Exception as e:
            if 'No such file or directory' in e.args:
                pass
            else:
                print(e)
                print(json_path)
                print(data_info)

