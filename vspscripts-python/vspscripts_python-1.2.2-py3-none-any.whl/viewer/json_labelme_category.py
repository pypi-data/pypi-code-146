import os
import json
import tkinter as tk
from tkinter import filedialog
import argparse

from vspscripts.helpers.json_coco_category import json_coco_category
from vspscripts.helpers.labelme2coco import json_dict, findAllFile, format2coco, init_json

def json_labelme_category(ann_dir):
    img_id = 0
    ann_id = 0
    categories = init_json(json_dict, ann_dir, '.json')

    for ann in findAllFile(ann_dir, '.json'):
        if "matched" not in os.path.basename(ann) and \
            "aligned" not in os.path.basename(ann):
            ann_id = format2coco(json_dict, ann, ann_id, img_id, categories)
            img_id = img_id + 1
        else:
            continue

    coco_json = 'tmp/coco.json'
    if not os.path.exists(os.path.dirname(coco_json)):
        os.makedirs(os.path.dirname(coco_json))

    fout_ann = open(coco_json, "w")
    json_str = json.dumps(json_dict)
    fout_ann.write(json_str)
    fout_ann.close()

    json_coco_category(coco_json)

if __name__ == "__main__":

    parser = argparse.ArgumentParser('parser for json-coco-category')
    parser.add_argument("--ann_dir", type=str, default='/data/AIVS_new')
    args = parser.parse_args()

    ann_dir = args.ann_dir

    # root = tk.Tk()
    # root.withdraw()
    # ann_dir = filedialog.askdirectory()
    # root.destroy()

    json_labelme_category(ann_dir)
    