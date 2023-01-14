# -*- coding: utf-8 -*-
# @Time : 2022/3/25 14:11
# @Author : Zhan Yong
from ccdt.dataset.base_labelme.base_labelme import BaseLabelme, PathTest, Encoder, json, collections, np
from pycocotools.coco import COCO
from tqdm import *
import os
from collections import defaultdict


class Coco(BaseLabelme):
    """
    coco实现类，主要实现coco转labelme，labelme转coco，同时继承BaseLabelme
    子类就可以访问到基类（父类）的属性和方法了，它提高了代码的可扩展性和重用行。
    """

    def __init__(self, *args, **kwargs):
        self.coco_dataset = {
            "categories": [],
            "images": [],
            "annotations": [],
            "info": "",
            "licenses": [],
        }  # the complete json
        self.anns = dict()  # anns[annId]={}
        self.cats = dict()  # cats[catId] = {}
        self.imgs = dict()  # imgs[imgId] = {}
        self.imgToAnns = defaultdict(list)  # imgToAnns[imgId] = [ann]
        self.catToImgs = defaultdict(list)  # catToImgs[catId] = [imgId]
        self.imgNameToId = defaultdict(list)  # imgNameToId[name] = imgId
        self.maxAnnId = 0
        self.maxImgId = 0
        self.category_id = 0
        self.result_addImage_id = 0
        # 定义一个目录，每次labelme基类循环某一个目录的时候，追加所有数据
        # self.coco_data_infos = []

        # # 注释ID
        # self.cur_ann_id = 0
        # # 图片ID
        # self.cur_image_id = 0
        # # 图片对象列表
        # self.images = list()
        # # 注释对象列表
        # self.annotations = list()
        # # 类别对象列表
        # self.categories = list()
        # # 所有标注属性对象列表
        self.coco_shapes = list()
        # # 目标检测类别对象列表
        self.categories_name = list()

        # 自定义coco文件名称
        self.coco_file_name = 'coco.json'
        self.coco_file = kwargs.get('coco_file')
        self.coco = None
        if self.coco_file:
            self.coco = COCO(self.coco_file)  # 加载coco文件数据
        super().__init__(*args, **kwargs)

    def has_image(self, image_name):
        """
        图片文件id查询
        :param image_name:
        :return:
        """
        img_id = self.imgNameToId.get(image_name, None)
        return img_id is not None

    def add_image(self, file_name: str, width: int, height: int, id: int = None):
        """
        追加图片描述属性，返回图片image_id
        :param file_name:
        :param width:
        :param height:
        :param id:
        :return:
        """
        if self.has_image(file_name):
            print(f"{file_name}图片已存在")
            return
        if not id:
            self.maxImgId += 1
            id = self.maxImgId
        image = {
            "id": id,
            "width": width,
            "height": height,
            "file_name": file_name
        }
        self.coco_dataset["images"].append(image)
        self.imgs[id] = image
        self.imgNameToId[file_name] = id
        return id

    def get_bbox(self, bbox, image_w_h, file_path):
        """
        实现矩形框转换计算，得到：左上角的坐标点+宽+高，即[x，y，宽，高]
        :param bbox:
        :param image_w_h:
        :return:
        """
        # points = np.array([1,2,3,4])
        # points = np.array([])
        # points[0, 0] = '赋值'
        # print(image_w_h)
        # shape['points'] == bbox，值为：[[453.59124755859375, 81.40898895263672], [654.3768920898438, 279.54791259765625]]
        if len(bbox) == 2:
            x1 = bbox[0][0]
            y1 = bbox[0][1]
            x2 = bbox[1][0]
            y2 = bbox[1][1]
            # 只针对坐标点越界的矩形进行处理
            if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x1 > image_w_h[0] or y1 > image_w_h[1] or x2 > image_w_h[
                0] or y2 > \
                    image_w_h[1]:
                print(f'标注的矩形框的坐标点已经超越图像边界:{file_path}')
                clamp_x1 = np.clip(x1, 0, image_w_h[0])
                clamp_y1 = np.clip(y1, 0, image_w_h[1])
                clamp_x2 = np.clip(x2, 0, image_w_h[0])
                clamp_y2 = np.clip(y2, 0, image_w_h[1])
                # 替换
                bbox[0][0] = clamp_x1
                bbox[0][1] = clamp_y1
                bbox[1][0] = clamp_x2
                bbox[1][1] = clamp_y2
            points = np.array(bbox)
            point_min, point_max = points.min(axis=0), points.max(axis=0)
            w, h = point_max - point_min
            return [point_min[0], point_min[1], w, h]

    def get_area(self, bbox):
        """
        计算矩形框的面积
        :param bbox:
        :return:
        """
        points = np.array(bbox)
        point_min, point_max = points.min(axis=0), points.max(axis=0)
        w, h = point_max - point_min
        return w * h
        # x = bbox[::2]
        # y = bbox[1::2]
        # return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def add_annotation(self, image_id: int, category_id: int, segmentation: list, bbox: list, id: int = None,
                       image_w_h: tuple = (), file_name: str = ''):
        """
        追加coco标注属性
        :param image_id:
        :param category_id:
        :param segmentation:
        :param bbox:
        :param id:
        :param image_w_h:
        :param file_name:
        :return:
        """
        if id is not None and self.anns.get(id, None) is not None:
            print("标签已经存在")
            return
        if not id:
            self.maxAnnId += 1
            id = self.maxAnnId
        ann = {
            "id": id,
            "iscrowd": 0,
            "image_id": image_id,
            "category_id": category_id,
            "segmentation": [segmentation],
            "area": self.get_area(bbox),
            "bbox": self.get_bbox(bbox, image_w_h, file_name),
        }
        self.coco_dataset["annotations"].append(ann)
        self.anns[id] = ann
        self.imgToAnns[image_id].append(ann)
        self.catToImgs[category_id].append(image_id)
        return id

    def add_category(self, id: int, name: str, color: list, supercategory: str = ""):
        """
        追加类别属性
        :param id:
        :param name:
        :param color:
        :param supercategory:
        """
        cat = {
            "id": id,
            "name": name,
            "color": color,
            "supercategory": supercategory,
        }
        self.cats[id] = cat
        self.coco_dataset["categories"].append(cat)

    def self2labelme(self):
        """
        coco转labelme实现
        """
        # 如果self.coco为空，则实现labelme转coco
        if self.coco is None:
            return
        # 获取每一张图片的id
        img_ids = self.coco.getImgIds()
        # 循环遍历每一个id
        i = 0
        for img_id in tqdm(img_ids):
            img_info = self.coco.loadImgs(img_id)[0]
            obj_dir = PathTest.initialize(img_info['file_name'])
            relative_path = os.path.join('..', '00.images', img_info['file_name'])
            # 通过注释id寻找到同一帧图片下的多个注释属性
            labelme_data = self.single_coco2labelme(img_id)
            labelme_data['imageHeight'] = img_info['height']
            labelme_data['imageWidth'] = img_info['width']
            labelme_data['imagePath'] = relative_path
            data_info = dict(image_dir=self.images_dir,
                             image_file=img_info['file_name'],
                             labelme_dir=self.labelme_dir,
                             labelme_file=obj_dir.stem + '.json',
                             labelme_info=labelme_data,
                             data_type=self.data_type,
                             input_dir=self.input_dir,
                             output_dir=self.output_dir,
                             only_annotation=self.only_annotation)
            self.data_infos.append(data_info)
            i += 1
        print("coco转labelme结束,一共%d" % i)

    def single_coco2labelme(self, img_id):
        """
        实现每一个coco注释合成labelme注释
        @param img_id:
        @return:
        """
        ann_ids = self.coco.getAnnIds(imgIds=img_id)
        labelme_data = dict(
            version='4.5.9',
            flags={},
            shapes=[],
            imagePath=None,
            imageData=None,
            imageHeight=None,
            imageWidth=None
        )
        if ann_ids:
            shapes = []
            anns = self.coco.loadAnns(ann_ids)
            for ann in anns:
                # 取到同一张图片的多个注释属性
                category_id = ann['category_id']
                # 获取坐标框
                bbox = ann['bbox']
                # 坐标切割
                bbox = [bbox[0:2], bbox[2:4]]
                # 左上角的坐标(x,y)右上角的坐标(x,y+h)左下角的坐标(x+w,y)右下角的坐标(x+w,y+h)
                points = [bbox[0], [bbox[0][0] + bbox[1][0], bbox[0][1] + bbox[1][1]]]
                # 通过类别id获取类别名称
                cats = self.coco.loadCats(category_id)[0]
                # 取到类别名称
                name = cats['name']
                shape = {"label": name, "points": points, "group_id": None, "shape_type": "rectangle", "flags": {}}
                shapes.append(shape)
            labelme_data['shapes'] = shapes
        return labelme_data

    def self2coco(self):
        """
        labelme转coco实现
        """
        # 如果self.coco不为空，则实现coco转labelme
        if self.coco:
            return
        self.get_data_paths()
        self.load_labelme()
        try:
            self.update_property()
        except Exception as e:
            print(e)
        print('后面不执行')
        if self.data_infos:
            # self.coco_data_infos.extend(self.data_infos)
            # 定义coco数据格式
            # coco_data = dict(
            #     images=self.images,
            #     annotations=self.annotations,
            #     categories=self.categories,
            # )
            # 递归的目录转coco，有多少个文件夹就会被类实列多少次。递归多少次文件夹，这里就会被循环多少次，不管循环多少次，这里需要生成一个coco文件
            for labelme_info in self.data_infos:
                # self.coco_data_infos.append(labelme_info)
                # 针对背景类直接跳过、有json文件没有图片文件直接跳过，不写入图片属性
                if labelme_info['labelme_info'] is None or labelme_info['labelme_info']['shapes'] == [] \
                        or labelme_info['image_file'] is None:
                    continue
                # 1、添加coco类别

                # 2、追加每张图片文件属性
                self.result_addImage_id = self.add_image(labelme_info['image_file'],
                                                    labelme_info['labelme_info']['imageWidth'],
                                                    labelme_info['labelme_info']['imageHeight'], None)
                w = labelme_info.get('labelme_info').get('imageWidth')
                h = labelme_info.get('labelme_info').get('imageHeight')
                size = (w, h)  # 把宽高定义成元组
                file_path = os.path.join(labelme_info.get('input_dir'), labelme_info.get('image_dir'),
                                         labelme_info.get('image_file'))
                # print(type(size))
                # self.cur_image_id += 1
                # images = dict(
                #     file_name=labelme_info['image_file'],
                #     height=labelme_info['labelme_info']['imageHeight'],
                #     width=labelme_info['labelme_info']['imageWidth'],
                #     id=self.cur_image_id,
                # )
                # self.images.append(images)
                # self.coco_shapes = labelme_info['labelme_info']['shapes']
                # 标签属性处理
                one_img_ann_list = self.labelme_shapes2coco_ann(labelme_info)
                for ann in one_img_ann_list:
                    # print(ann)
                    category_id = 0
                    # 如果标注的标签不存在，就category_id加1
                    if ann['label'] not in self.categories_name:
                        self.category_id += 1
                        self.add_category(self.category_id, str(ann['label']), [], '')
                        self.categories_name.append(ann['label'])
                    # 每一个shape元素中动态查询，
                    for category in self.coco_dataset.get('categories'):
                        # print(category)
                        if category.get('name') == ann['label']:
                            category_id = category.get('id')
                            # print(category_id)
                    # 3、追加标注属性,核心是self.category_id要动态追加，必须要在,self.coco_dataset.get('categories')取
                    self.add_annotation(self.result_addImage_id, category_id, ann.get('segmentation'),
                                        ann.get('points'), None, size, file_path)


                # print(self.coco_dataset)
                # self.annotations.extend(one_img_ann_list)
            # for category_id, category_name in enumerate(self.categories_name, 1):
            #     category = dict(
            #         supercategory='object',
            #         id=category_id,
            #         name=category_name,
            #     )
            #     self.categories.append(category)
            # obj_dir = PathTest.initialize(self.images_dir)
            # self.save_labelme()
            # out_put_coco_file = obj_dir.joinpath(self.output_dir, obj_dir.parent, self.coco_file_name)
            # coco文件的名称是写死的

            # 创建输出目录文件夹
            os.makedirs(os.path.join(self.output_dir), exist_ok=True)
            out_put_coco_file = os.path.join(self.output_dir, self.coco_file_name)
            with open(out_put_coco_file, 'w', encoding='utf-8') as coco_fp:
                json.dump(self.coco_dataset, coco_fp, ensure_ascii=False, indent=2, cls=Encoder)
        print('labelme转coco结束，类别打印时间久，可以手动结束程序')
        print('注意：labelme转coco结束，只能是单级目录下的labelme数据集进行转换')
        return
        # except Exception as e:
        #     print(e)

    @staticmethod
    def labelme_shapes2coco_ann(labelme_info):
        """
        把labeme标签转成coco标签
        针对shape元素二次封装，把group_id做为key，矩形框和关键点作为值。{'group_id': [][], 'b': 2, 'b': '3'}
        找出所有shape元素中相同group_id组的shape元素，合并为一个列表，即一个矩形框对应多个关键点标注。使用：structure_shapes = defaultdict(list)
        @return:
        """
        # tinydict = {}
        # shapes_type = collections.defaultdict(list)
        # from collections import defaultdict
        # 封装新的关键点与矩形框组合列表。即group_id的值作为键，shape元素作为值，构成新的字典集合
        structure_shapes = defaultdict(list)
        i = 0
        # 筛选group_id相同的shape元素，为一个列表集合中，参考网址关键词:字典设置默认值，https://blog.csdn.net/qq_45128719/article/details/125392954
        for shape in labelme_info.get('labelme_info').get('shapes'):
            # rectangle(矩形框),point(关键点),polygon(多边形)，line(线)，linestrip(线带，语义分割)
            if shape['shape_type'] == 'rectangle' or shape['shape_type'] == 'point' or \
                    shape['shape_type'] == 'polygon' or shape['shape_type'] == 'line' or \
                    shape['shape_type'] == 'linestrip':
                # ====================================================
                # # # clamp 标注的矩形框，超越图片宽高边界的，需要对矩形框的坐标点做一次，夹紧计算。
                # # 针对，左上角的坐标点与右下角的坐标点的，计算公式：如下
                # # np.clip(x1, 0, 图像宽)，
                # # np.clip(x1, 0, 图像宽)，
                # # np.clip(y1, 0, 图像高)，
                # # np.clip(x2, 0, 图像宽)，
                # # np.clip(y1, 0, 图像高)，
                # # 最后，在夹紧计算出4个坐标点后，labelme转coco时从新计算[x，y，宽，高]
                # w = labelme_info.get('labelme_info').get('imageWidth')
                # h = labelme_info.get('labelme_info').get('imageHeight')
                # size = (w, h)  # 把宽高定义成元组
                # x1 = shape.get('points')[0][0]
                # y1 = shape.get('points')[0][1]
                # x2 = shape.get('points')[1][0]
                # y2 = shape.get('points')[1][1]
                # 逻辑判断坐标点是否超越图像边界
                # if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x1 > size[0] or y1 > size[1] or x2 > size[0] or y2 > size[1]:
                #     file_path = os.path.join(labelme_info.get('input_dir'), labelme_info.get('image_dir'), labelme_info.get('image_file'))
                #     print('标注的矩形框的坐标点已经超越图像边界:' + file_path)
                # clamp_x1 = np.clip(x1, 0, size[0])
                # clamp_y1 = np.clip(y1, 0, size[1])
                # clamp_x2 = np.clip(x2, 0, size[0])
                # clamp_y2 = np.clip(y2, 0, size[1])
                # ====================================================
                # 针对客户标注的错误，导致转coco时，矩形框出错，该程序不做逻辑处理，给使用者自己过滤，保障shape不少即可
                structure_shapes[shape['group_id']].append(shape)
                # # group_id的值为None，表示当前矩形框没有关键点，需要单独一个shape元素
                # if not shape.get('group_id') and shape.get('group_id') != 0:
                #     id_value = shape.get('group_id')
                #     print(f'group_id的值为空={id_value}')
                #     # print('group_id的值为空' +f{shape.get('group_id')} )
                #     # return self.coco_shapes
                # else:
                #     id_value = shape.get('group_id')
                #     print(f'group_id的值,不为空={id_value}')
                #     # 这里的转换存在一个问题，如果某一个shape打了group_id的值，但没有打关键点，同时标签类别名称和其它有关键点的矩形框相同时。
                #     # group_id值相同会被分一组，如果认为标注出错，分组就会出错，如何避免。会导致转coco的矩形框变少，并且标错位置。
                #     # 针对上述错误的矫正逻辑思路，查询每一个shape字典中的group_id，并且和整个shapes元素进行比较，相同值的放一个列表集合。
                #     structure_shapes[shape['group_id']].append(shape)
        # print(structure_shapes)
        # one_img_ann_list = list()
        rebuild_labelme_infos = []  # 重组一张图片多个shape元素的集合
        for structure_shape, value in structure_shapes.items():
            if not structure_shape and structure_shape != 0:
                # print('不是关键点与矩形框的分组数据')
                rebuild_labelme_infos.extend(value)  # 直接列表相加扩展
            else:
                # 处理标注的shape有group_id的元素，只要group_id有值，就追加segmentation
                rebuild_shape = {}  # 重组shape字典，追加关键点属性，把一个组的多个shape元素，合并成一个shape。针对关键点与shape的组合
                segmentation = []  # 关键点列表定义
                for shape in value:
                    # 如果标注shape是关键点，就追加关键点元素列表
                    if shape['shape_type'] == 'point':
                        segmentation.extend(shape['points'][0])
                    else:
                        rebuild_shape.update(shape)
                # 重组shape属性，并追加关键点列表
                rebuild_shape.update({'segmentation': segmentation})
                rebuild_labelme_infos.append(rebuild_shape)
                # print('组合结束')
        return rebuild_labelme_infos
        # # 添加标签类别名称
        # if structure_shape['label'] not in self.categories_name:
        #     self.categories_name.append(structure_shape['label'])
        # # 处理shape属性
        # ann_list = self.rectangle_shapes2coco(structure_shape)
        # one_img_ann_list.extend(ann_list)

        # for index, shape in enumerate(rebuild_labelme_infos):
        #     # if shape['group_id'] == shape['group_id']:
        #     #     print(shape)
        #         # tinydict.fromkeys(shape['group_id'][shape])
        #
        #     # # 添加标签类别名称
        #     if shape['label'] not in self.categories_name:
        #         self.categories_name.append(shape['label'])
        #         # if shape_type == 'rectangle':
        #         ann = self.get_default_ann()
        #         category_id = index + 1
        #         ann['category_id'] = category_id
        #         points = np.array(shape['points'])
        #         point_min, point_max = points.min(axis=0), points.max(axis=0)
        #         w, h = point_max - point_min
        #         ann['bbox'] = [point_min[0], point_min[1], w, h]
        #         ann['area'] = w * h
        #         ann['segmentation'].extend(shape['segmentation'])
        #         self.annotations.append(ann)

        # ann_list = self.rectangle_shapes2coco(shape)

        # # 处理shape属性
        # ann_list = self.rectangle_shapes2coco(shape)
        # one_img_ann_list.extend(ann_list)

        # if shape['shape_type'] == 'rectangle':
        #     if shape['label'] not in self.categories_name:
        #         self.categories_name.append(shape['label'])
        #     shapes_type[shape['shape_type']].append(shape)
        # elif shape['shape_type'] == 'polygon':
        #     continue
        # elif shape['shape_type'] == 'line':
        #     continue
        # elif shape['shape_type'] == 'linestrip':
        #     continue
        # elif shape['shape_type'] == 'circle':
        #     continue
        # elif shape['shape_type'] == 'point':
        #     if shape['label'] not in self.categories_name:
        #         self.categories_name.append(shape['label'])
        #     shapes_type[shape['shape_type']].append(shape)
        # one_img_ann_list = list()
        # 目前来看，68个关键点，每张图片，只有一个矩形框有关键点。不是所有矩形框都有关键点。
        # for shape_type, shapes_type_ann in shapes_type.items():
        #     if shape_type == 'rectangle':
        #         ann_list = self.rectangle_shapes2coco(shapes_type.get(shape_type))
        #         one_img_ann_list.extend(ann_list)
        #     elif shape_type == 'polygon':
        #         continue
        #     elif shape_type == 'line':
        #         continue
        #     elif shape_type == 'linestrip':
        #         continue
        #     elif shape_type == 'circle':
        #         continue
        #     elif shape_type == 'point':
        #         # 关键点转换到coco文件中的segmentation中
        #         ann_list = self.point_shapes2coco(shapes_type.get(shape_type))
        #         one_img_ann_list.extend(ann_list)
        # return one_img_ann_list

    @staticmethod
    def save_coco():
        """
        coco输出，想要把多个文件夹，的文件一次性输出到一个文件，并且有编号顺序，必须是一次遍历多个目录下的所有文件写coco内存数据，而不是每个目录分成一个对象。
        """
        print('coco保存')
    # def rectangle_shapes2coco(self, shapes):
    #     """
    #     实现矩形框转换计算
    #     @param shapes:
    #     @return:
    #     """
    #     ann_list = []
    #     for shape in shapes:
    #         ann = self.get_default_ann()
    #         category_id = shapes.index(shape) + 1
    #         ann['category_id'] = category_id
    #         points = np.array(shape['points'])
    #         point_min, point_max = points.min(axis=0), points.max(axis=0)
    #         w, h = point_max - point_min
    #         ann['bbox'] = [point_min[0], point_min[1], w, h]
    #         ann['area'] = w * h
    #         ann_list.append(ann)
    #     return ann_list

    # def get_default_ann(self):
    #     """
    #     标签属性定义，并id自增
    #     关键点存放格式如下所示
    #     "segmentation": [
    #             [
    #                 491.0,
    #                 637.0,
    #                 252.0,
    #                 617.0,
    #                 234.0,
    #                 480.0,
    #                 473.0,
    #                 500.0
    #             ]
    #         ],
    #     一张图片，只有一个矩形框，多个关键点比较好弄，如果是多个矩形框，有的矩形框有关键点，有的矩形框没有关键点。
    #     也就是说，关键点和矩形框的对应关系，目前无法确认。（通过组group_id的关系来确认，关键点归属于哪一个矩形框）
    #     @return:
    #     """
    #     self.cur_ann_id += 1
    #     annotation = dict(
    #         segmentation=[],
    #         area=0,
    #         iscrowd=0,  # 做为group_id，关联字段
    #         image_id=self.cur_image_id,
    #         bbox=[],
    #         category_id=0,
    #         id=self.cur_ann_id,
    #     )
    #     return annotation

    # def point_shapes2coco(self, shapes):
    #     """
    #     关键点追加，一个shape矩形框下，就是68个关键点
    #     :param shapes:
    #     :return:
    #     """
    #     ann_list = []
    #     ann = self.get_default_ann()
    #     for shape in shapes:
    #         category_id = shapes.index(shape) + 1
    #         ann['category_id'] = category_id
    #         # points = np.array(shape['points'])
    #         # point_min, point_max = points.min(axis=0), points.max(axis=0)
    #         # w, h = point_max - point_min
    #         # ann['bbox'] = [point_min[0], point_min[1], w, h]
    #         # 算的是关键点连接成线的面积
    #         # ann['area'] = w * h
    #         x = shape.get('points')[0][0]
    #         y = shape.get('points')[0][1]
    #         ann['segmentation'].append(x)  # 追加关键点，待完善
    #         ann['segmentation'].append(y)
    #     ann_list.append(ann)
    #     return ann_list
