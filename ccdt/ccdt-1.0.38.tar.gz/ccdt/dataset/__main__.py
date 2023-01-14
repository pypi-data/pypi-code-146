# -*- coding: utf-8 -*-
# @Time : 2022/3/25 13:44
# @Author : Zhan Yong
import argparse
import ast
from ccdt.dataset import *


def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_datasets', type=ast.literal_eval, help="labelme数据集路径、coco数据集路径，列表字典传参")
    parser.add_argument('--output-dir', type=str, help="保存路径")
    # parser.add_argument('--replace-dir', type=str, help="替换路径")
    parser.add_argument('--output-format', type=str, help="输出功能格式，有labelme、coco")
    parser.add_argument('-f', '--function', type=str, required=True,
                        help="功能参数:print,convert,filter,matting,rename,visualize,merge，只能输入单个")
    parser.add_argument('--filter-label', type=ast.literal_eval, help="类别筛选参数，单个与多个都可以输入")
    # 当不输入--only_annotation，默认为False；输入--only_annotation，才会触发True值。False处理labelme和图片，True只处理labelme
    parser.add_argument('--only-annotation', action="store_true", help="默认False，是否只处理注释文件。是为True，否为False")
    parser.add_argument('--filter-shape-type', type=ast.literal_eval, help="形状筛选参数，单个与多个都可以输入")
    parser.add_argument('--input-coco-file', type=str, help="输入形状筛选参数，单个与多个都可以输入")
    parser.add_argument('--rename-attribute', type=ast.literal_eval, help="属性重命名，包含label、flags")
    parser.add_argument('--select-empty', action="store_true", help="默认False，是否保留背景类。是为True，否为False")
    parser.add_argument('--only-select-empty', action="store_true", help="默认False，是否只筛选背景数据。是为True，否为False")
    parser.add_argument('--only-select-shapes', action="store_true", help="默认False，是否只筛选标注有框的数据。是为True，否为False")
    # parser.add_argument('--only-empty', action="store_true", help="默认False，不保留背景类。传参则设置为True，只保留背景类")
    parser.add_argument('--shapes-attribute', type=str, help="筛选属性，包含label（类别）、shape_type（类别形状）、flags（类别属性）")
    parser.add_argument('--filter-flags', type=ast.literal_eval,
                        help="类别属性筛选，输入类别属性字典列表。比如person类下有，手、脚、头")
    parser.add_argument('--file_formats', default=['.jpg', '.jpeg', '.png', '.JPEG', '.JPG', '.PNG'], type=str,
                        help="文件格式")
    parser.add_argument('--filter-combin', action="store_true", help="是否组合筛选，是为True，否为False")
    parser.add_argument('--min-pixel', type=int, default=512, help='最小像素截图设置，默认512像素。即大于512像素的矩形框才进行截图')
    parser.add_argument('--print-more', action="store_true", help="打印详细信息")
    parser.add_argument('--del-label', type=str, help="删除label标签")

    args = parser.parse_args()
    if args.function == 'filter':
        return args
    # 如果需要进行类别过滤，则必须要有操作功能filter参数存在
    if args.filter_label and args.function == 'filter':
        return args
    if args.filter_flags and args.function == 'filter':
        return args
    if args.filter_shape_type and args.function == 'filter':
        return args
    # 重命名
    elif args.rename_attribute and args.function == 'rename':
        return args
    # labelme转coco，coco转labelme
    elif args.function == 'convert':
        return args
    # 抠图，单数据集、多数据集
    elif args.function == 'matting':
        return args
    # 可视化
    elif args.function == 'visualize':
        return args
    # 合并类别筛选数据
    elif args.function == 'merge':
        return args
    elif args.function == 'print':
        return args
    elif args.function == 'delete':
        return args
    else:
        assert not args.function, '传入的操作功能参数不对:{}'.format(args.function)


def deal_with_data_set(datasets, args):
    """
    多项数据集循环处理实现
    :param args:
    :param datasets: 数据集对象参数
    :return:
    """
    show_tool = ShowTool(datasets)
    print('打印输出加载中。。。。。。')
    print(show_tool.total_single_print())
    if args.function == 'merge':  # 合并功能
        BaseLabelme.merge(datasets)
    for dataset in datasets:
        if args.function == 'matting':  # 抠图功能
            print(args.min_pixel)
            dataset.crop_objs(args.min_pixel)
        elif args.function == 'merge':  # 合并功能
            pass
        elif args.function == 'convert':  # 转换功能，包含labelme转coco，coco转labelme
            if args.output_format == 'labelme':  # coco转labelme
                dataset.save_labelme()
            elif args.output_format == 'coco':  # labelme转coco
                # print('什么情况')
                # print(dataset)
                pass
        elif args.function == 'rename':  # 重命名功能
            dataset.rename(args.rename_attribute)
            dataset.save_labelme()
        elif args.function == 'visualize':  # 可视化功能
            dataset.visualization(args.output_dir)
        elif args.function == 'filter':  # 筛选功能
            filter_data = dataset(select_empty=args.select_empty,
                                  filter_combin=args.filter_combin,
                                  filter_label=args.filter_label,
                                  filter_shape_type=args.filter_shape_type,
                                  filter_flags=args.filter_flags,
                                  only_select_empty=args.only_select_empty,
                                  only_select_shapes=args.only_select_shapes,
                                  shapes_attribute=args.shapes_attribute, )
            # 保存筛选后的数据
            filter_data.save_labelme()
        elif args.function == 'print' and args.print_more:  # 打印功能
            show_tool = ShowTool(dataset)
            print(show_tool.total_single_print())
        elif args.function == 'delete':
            dataset.del_label(args.del_label)
            # print(dataset)
            dataset.save_labelme()


def main():
    args = parser_args()
    datasets = list()
    for dataset_info in args.input_datasets:
        # 如果输入路径为空，报错
        # print(dataset_info)
        if dataset_info.get('input_dir', False) == '' or dataset_info['type'] == '':
            assert False, '{}值不能为空，检查路径是否不为/，检查type是否为处理对象名称，BaseLabelme'.format(dataset_info)
        if dataset_info.get('coco_file') is None:
            dataset_info['coco_file'] = None
        # labelme_path_list = PathOperate(dataset_info['input_dir'], dataset_info['type'], args.file_formats,
        # dataset_info['coco_file'])
        # print(dataset_info)
        labelme_path_list = PathTest(dataset_info['input_dir'], dataset_info['type'], args.file_formats,
                                     dataset_info['coco_file'], args.function, args.output_format)
        for path in labelme_path_list.dir_paths:
            # print(path)
            # print(path['images_dir'])
            # 使用类名称调用初始化函数
            dataset = eval(dataset_info['type'])(labelme_dir=path['labelme_dir'],
                                                 images_dir=path['images_dir'],
                                                 file_formats=path['file_formats'],
                                                 coco_file=path['coco_file'],
                                                 data_type=path['type'],
                                                 input_dir=path['input_dir'],
                                                 output_dir=args.output_dir,
                                                 select_empty=args.select_empty,
                                                 function=args.function,
                                                 only_annotation=args.only_annotation)
            datasets.append(dataset)
    # 2.对数据进行处理
    deal_with_data_set(datasets, args)


if __name__ == '__main__':
    main()
