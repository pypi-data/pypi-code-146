# -*- coding: utf-8 -*-
"""
Created on Tue May 25 21:31:42 2021
@author: lmx
"""

import tkinter as tk
from tkinter import filedialog
from pycocotools.coco import COCO
import numpy as np
import matplotlib.pyplot as plt
import argparse
import pandas as pd 

def json_coco_category(annfile):

    coco = COCO(annfile)

    cats = coco.loadCats(coco.getCatIds())
    cat_nms = [cat['name'] for cat in cats ]
    print('number of categories:', len(cat_nms))
    print('COCO categories: \n',cat_nms)

    number_img = []
    number_bbox = []

    for cat_name in cat_nms:
        catId = coco.getCatIds(catNms=[cat_name])
        imgId = coco.getImgIds(catIds=catId)
        annId = coco.getAnnIds(catIds=catId)
        print("{:<15} {:<6d} {:<10d}".format(cat_name, len(imgId),len(annId)))
        
        number_img.append(len(imgId))
        number_bbox.append(len(annId))
        
    bar_width = 0.4

    img_num = len(coco.dataset['images'])
    ann_num = len(coco.dataset['annotations'])
    y1 = number_img
    y2 = number_bbox

    x = np.arange(len(cat_nms))
    # print(np.array([y1,y2]))
    # df = pd.DataFrame(np.transpose(np.array([y1,y2])), index=cat_nms, columns=["image({})".format(sum(y1)),"defect({})".format(sum(y2))])
    # df.plot(kind='bar', rot=30, width=0.8, figsize=(50,10))
    # # plt.savefig('tmp/柱状统计图')
    # plt.show()

    str1 = cat_nms

    plt.figure(num = 1, figsize=(15,15))
    for a, b in zip(x,y1):
        plt.text(a,b+0.05,'%.0f' %b,ha = 'center',va = 'bottom',fontsize = 12)
        
    for a, b in zip(x,y2):
        plt.text(a+bar_width,b+0.05,'%.0f' %b,ha = 'center',va = 'bottom',fontsize = 12)
        
    #柱状图绘制
    p1 = plt.bar(x, height=y1, width=bar_width,label='image({})'.format(img_num),tick_label=str1)
    p1 = plt.bar(x+bar_width, height=y2, width=bar_width,label='defect({})'.format(ann_num),tick_label=str1)
    plt.xticks(x+bar_width/2, str1, rotation=30, fontsize = 15)

    plt.legend(fontsize = 20)
    plt.title('class_status', fontsize = 20)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('tmp/柱状统计图')

    #饼状图绘制
    plt.figure(num=2,figsize=(15,15))
    plt.axis('equal')
    explode=[0.01]*len(cat_nms)
    patches,l_text,p_text = plt.pie(number_img,explode=explode,labels=str1,autopct='%1.1f%%')
    for t in p_text:
        t.set_size(20)
    for t in l_text:
        t.set_size(20)
    plt.legend(loc='upper left', fontsize = 10)
    plt.title('image numbers ({})'.format(img_num), fontsize = 20)
    plt.savefig('tmp/images统计饼状图')

    plt.figure(num=3,figsize=(15,15))
    plt.axis('equal')
    explode=[0.01]*len(cat_nms)
    patches,l_text,p_text = plt.pie(number_bbox,explode=explode,labels=str1,autopct='%1.1f%%')
    for t in p_text:
        t.set_size(20)
    for t in l_text:
        t.set_size(20)
    plt.legend(loc='upper left', fontsize = 10)
    plt.title('defect numbers ({})'.format(ann_num), fontsize = 20)
    plt.savefig('tmp/defect统计饼状图')

    plt.show()


if __name__ == "__main__":
    # parser = argparse.ArgumentParser('parser for json-coco-category')
    # parser.add_argument("--annfile", type=str, default='../AIVS_coco/annotations/instances_train2017.json')
    # args = parser.parse_args()

    # annfile = args.annfile

    root = tk.Tk()
    root.withdraw()
    annfile = filedialog.askopenfilename()
    root.destroy()

    json_coco_category(annfile)
    