import os
import json
import math
import shutil
import datetime
import argparse
import numpy as np
from tkinter import _flatten
from shapely.geometry import Polygon

PRE_DEFINE_CATEGORIES = None # {'short', 'open'}

info = {
    "year": int,
    "version": str,
    "description": str,
    "contributor": str,
    "url": str,
    "date_created": str,
}
license = {
    "id": int,
    "name": str,
    "url": str,
}
image = {
    "id": int,
    "version": str,
    "width": int,
    "height": int,
    "file_name": str,
    "license": int,
    "flickr_url": str,
    "coco_url": str,
    "date_captured": str,
}
annotation = {
    "id": int,
    "image_id": int,
    "category_id": int,
    "segmentation": [], #RLE or [polygon]
    "area": float,
    "bbox": [int, int, int, int], #[x,y,width,height]
    "iscrowd": bool,
}
category = {
    "id": int,
    "name": str,
    "supercategory": str,
}
json_dict = {"info": info, "licenses": [], "images": [], "annotations": [], "categories": []}

def parse_args():
    parser = argparse.ArgumentParser('parser for converting dataset format')
    parser.add_argument("--data_path", type=str, default='')
    parser.add_argument("--output_dir", type=str, default='../outputs_coco')
    parser.add_argument("--train", '-t', action='store_true')
    parser.add_argument("--val", '-v', action='store_true')
    # parser.add_argument("--display", '-d', action='store_true')
    # parser.add_argument("--save", '-s', action='store_true')

    return parser.parse_args()

def findAllFile(base, format=None):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if format:
                if f.endswith(format):
                    fullname = os.path.join(root, f)
                    yield fullname
            else:
                fullname = os.path.join(root, f)
                yield fullname

def eucliDist(A,B):
    return math.sqrt(sum([(a - b)**2 for (a,b) in zip(A,B)]))

def polygon_area(points):
    """
 
    """
    area = 0
    q = points[-1]
    for p in points:
        area += p[0] * q[1] - p[1] * q[0]
        q = p
    return area / 2

def polygon2bbox(points, img_height, img_width):
    points_array = np.array(points, dtype=np.float32)
    [xmax, ymax] = np.max(points_array, axis=0)
    [xmin, ymin] = np.min(points_array, axis=0)
    if xmax > img_width and xmax - img_width < 1:
        xmax = img_width
    if ymax > img_height and ymax - img_height < 1:
        ymax = img_height
    assert xmax >= xmin and xmax <= img_width and xmin >= 0
    assert ymax >= ymin and ymax <= img_height and ymin >= 0
    width = xmax - xmin
    height = ymax - ymin
    bbox = [int(xmin), int(ymin), int(width), int(height)]
    assert bbox[0] + bbox[2] <= img_width and bbox[1] + bbox[3] <= img_height
    return bbox

def get_categories(ann_files):
    """Generate category name to id mapping from a list of xml files.
    
    Arguments:
        xml_files {list} -- A list of xml file paths.
    
    Returns:
        dict -- category name to id mapping.
    """
    classes_names = []
    for ann_file in ann_files:
        with open(ann_file,"r") as f:
            load_dict = json.load(f)
            shapes = load_dict['shapes']
            for shape in shapes:
                if shape['label'] != 'offset':
                    classes_names.append(shape['label'])
    classes_names = list(set(classes_names))
    classes_names.sort()
    return classes_names

def init_json(json_dict, base, ann_format):
    cur = datetime.datetime.now()
    json_dict["info"]["year"] = cur.year
    json_dict["info"]["date_created"] = str(cur)
    json_dict["info"]["version"] = '1.0'
    json_dict["info"]["description"] = 'converting AI-VS dataset format'
    json_dict["info"]["contributor"] = 'Jack'
    json_dict["info"]["url"] = None

    json_dict["licenses"].append({"id": 1, "name": 'optima', 'url': None})

    if PRE_DEFINE_CATEGORIES is not None:
        categories = PRE_DEFINE_CATEGORIES
    else:
        ann_files = findAllFile(base, ann_format)
        categories = get_categories(ann_files)
    for index, cat_name in enumerate(categories):
        json_dict["categories"].append({"id": index, "name": cat_name, "supercategory": None})
    return categories

def format2coco(json_dict, ann_file_path, ann_id, img_id, categories):
    with open(ann_file_path,"r") as f:
        load_dict = json.load(f)
    version = load_dict['version']
    shapes = load_dict['shapes']
    img_name = load_dict['imagePath']
    img_height = load_dict['imageHeight']
    img_width = load_dict['imageWidth']

    json_dict["images"].append({"id": img_id, "version": version, "width": img_width, \
        "height": img_height, "file_name": img_name, \
            "license": 1, "flickr_url": None, "coco_url": None, "date_captured": None})

    for shape in shapes:
        label = shape['label']
        points = shape['points']
        shape_type = shape['shape_type']
        # area = polygon_area(points)
        if shape_type == "polygon":
            assert len(points) >= 3, print(ann_file_path)
        elif shape_type == "circle":
            print("The annotation of {} is circle.".format(img_name))
            assert len(points) == 2
            [center, point_edg] = points
            radius = eucliDist(center, point_edg)
            points = [[center[0]-radius, center[1]-radius], \
            [center[0]-radius, center[1]+radius],\
            [center[0]+radius, center[1]+radius],\
            [center[0]+radius, center[1]-radius]]
        elif shape_type == "point":
            assert len(points) == 1 and label == 'offset', print(ann_file_path)
            continue
        else:
            raise ValueError("The shape_type must be polygon or circle.")
        area = Polygon(points).area
        polygon = list(_flatten(points))
        try:
            bbox = polygon2bbox(points, img_height, img_width)
        except AssertionError:
            print(ann_file_path)
        json_dict["annotations"].append({"id": ann_id, "image_id": img_id, "category_id": categories.index(label), \
        "segmentation": [polygon], "area": area, "bbox": bbox, "iscrowd": False})
        ann_id = ann_id + 1

    return ann_id

def labelme2coco():
    img_format = '.jpg'
    cam_format = '.png'
    ann_format = '.json'
    args = parse_args()
    if args.train and not args.val:
        trainval = 'train2017'
    elif not args.train and args.val:
        trainval = 'val2017'
    else:
        raise ValueError('Please select train or val set.')
    if not os.path.exists(os.path.join(args.output_dir, 'annotations')):
        os.makedirs(os.path.join(args.output_dir, 'annotations'))
    if not os.path.exists(os.path.join(args.output_dir, trainval)):
        os.makedirs(os.path.join(args.output_dir, trainval))
    if not os.path.exists(os.path.join(args.output_dir, trainval+'_cam')):
        os.makedirs(os.path.join(args.output_dir, trainval+'_cam'))

    output_ann = os.path.join(args.output_dir, 'annotations/instances_{}.json'.format(trainval))
    
    img_id = 0
    ann_id = 0
    categories = init_json(json_dict, args.data_path, ann_format)
    for img in findAllFile(args.data_path, img_format):
        cam = img.replace(img_format, cam_format)
        ann = img.replace(img_format, ann_format)
        if os.path.exists(ann):
            output_img = os.path.join(args.output_dir, trainval, os.path.basename(img))
            output_cam = os.path.join(args.output_dir, trainval+'_cam', os.path.basename(cam))
            shutil.copy(img, output_img)
            shutil.copy(cam, output_cam)
            ann_id = format2coco(json_dict, ann, ann_id, img_id, categories)
            img_id = img_id + 1
        else:
            print('There not exist annotation \'{}\''.format(ann))
            # raise ValueError('There not exist annotation \'{}\''.format(ann))

    fout_ann = open(output_ann, "w")
    json_str = json.dumps(json_dict)
    fout_ann.write(json_str)
    fout_ann.close()

if __name__ == "__main__":
    labelme2coco()
