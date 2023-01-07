import os
import json
import copy
import errno
import base64
import numpy as np
from PIL import Image

from vspscripts.alignment.utils.utils import Sim_Trans, Crop_Trans

def Modification_ann(ann_path, M_Sim, matching_acc, output_dir=None, img_size=None, method='matched'):
    if os.path.isfile(ann_path):
        with open(ann_path, "r") as f:
            load_dict = json.load(f)
            # print(ann_path)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ann_path)
        # print("There is not exist {}".format(ann_path))
        # return None
    if output_dir == None:
        output_dir = os.path.dirname(ann_path)
        ann_new_path = ann_path.replace('.json', '_{}.json'.format(method))
    else:
        ann_name = os.path.basename(ann_path)
        ann_new_path = os.path.join(output_dir, ann_name.replace('.json', '_{}.json'.format(method)))
    
    ori_shape = (load_dict['imageWidth'], load_dict['imageHeight'])

    load_dict['imagePath'] = load_dict['imagePath'].replace('.jpg', '_{}.jpg'.format(method))
    img_path = os.path.join(output_dir, os.path.basename(ann_new_path).replace(".json", ".jpg"))
    if img_size == None:
        img = Image.open(img_path)
        load_dict['imageHeight'], load_dict['imageWidth'] = img.height, img.width
        if img.height == img.width:
            img_size = img.height
        else:
            raise ValueError("height and width of image must be equal!")
    else:
        load_dict['imageHeight'] = img_size
        load_dict['imageWidth'] = img_size

    load_dict['flags'].update({
        'type': '{} and cropped transformation.'.format(method),
        'matching_acc': matching_acc
    })
    with open(img_path, "rb") as imageFile:
        image2str = base64.b64encode(imageFile.read())
    load_dict['imageData'] = image2str.decode('ascii')
    
    shapes = load_dict['shapes']
    shapes_new = []
    for shape in shapes:
        if shape['label'] == "offset" or shape['label'] == "off set":
            continue
        else:
            shapes_new.append(shape)
    rm_index = []
    for idx, shape in enumerate(shapes_new):
        points = np.array(shape['points'])
        points_sim = Sim_Trans(points, M_Sim)
        # print(points_sim)
        points_new = Crop_Trans(points_sim, ori_shape, img_size)
        shapes_new[idx]['points'] = points_new.tolist()
        if points_new.size == 0:
            rm_index.append(idx)
    for index in reversed(rm_index):
        shapes_new.pop(index)
    load_dict['shapes'] = shapes_new

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # print(load_dict)
    jsonDict = json.dumps(load_dict, sort_keys=True, indent=4, separators=(',', ': '))
    with open(ann_new_path, "w") as f:
        f.write(jsonDict)
