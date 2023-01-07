import cv2
import torch
import numpy as np
import os.path as osp
from PIL import Image
from sklearn import metrics

try:
    from mmseg.datasets.vsp import VSPDataset
    CLASSES = VSPDataset.CLASSES
except Exception as e:
    CLASSES = ('background', 'island', 'nick', 'open', 'protrusion', \
        'short', 'copper', 'pinhole')
    Warning('VSPDataset not found, use default CLASSES:{}'.format(CLASSES)) 

def post_process(name, mask, cfg):
    post_process_cfg = cfg.get('post_process_cfg', None)
    if post_process_cfg == None:
        return mask
    else:
        k = post_process_cfg.get('MORPH_OPEN_KERNEL', 3)
        img = np.asarray(mask).astype(np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k,k))
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = Image.fromarray(img.astype(bool))
    return mask

def get_OK_NG(seg_map_pre, cfg = {}):
    classes = np.array(CLASSES)
    class_mask = []
    if type(seg_map_pre) is str:
        seg_map_pre = Image.open(seg_map_pre).convert('L')
    if type(seg_map_pre) is torch.tensor:
        seg_map_pre = seg_map_pre.cpu().numpy()
    if type(seg_map_pre) is np.ndarray:
        seg_map_pre = Image.fromarray(np.squeeze(seg_map_pre.astype('uint8')), mode='L')
    assert isinstance(seg_map_pre, Image.Image)
    for label, name in enumerate(classes):
        if label != 0 and name != '':
            table = [0]*256
            table[label] = 1
            mask = seg_map_pre.point(table, '1')
            mask_post = post_process(name, mask, cfg)
            if mask_post.getextrema() != (0, 0):
                # print('[{}]: {}'.format(label, name))
                class_mask.append(dict(name=name, mask=mask, mask_post=mask_post))
    return 'OK' if len(class_mask) == 0 else 'NG'

def evaluateOK_NGLists(pre_results, gts, post_cfg={}, logger=None):
    try:
        from mmcv.utils import print_log
    except Exception as e:
        def print_log(msg, logger=None):
            print(msg)
    target_names = {'OK':0, 'NG':1}
    pre_list, gt_list = [], []
    for pre, gt in zip(pre_results, gts):
        # post_cfg = {'post_process_cfg':{'MORPH_OPEN_KERNEL':3}}
        pre_list.append(target_names.get(get_OK_NG(pre, post_cfg)))
        gt_list.append(target_names.get(gt))
    assert len(pre_list) == len(gt_list)
    # acc_rate = metrics.accuracy_score(gt_list, pre_list, normalize=True, sample_weight=None)
    print_msg = metrics.classification_report(gt_list, pre_list, target_names = list(target_names.keys()))
    if logger is None:
        print(print_msg)
    else:
        print_log(print_msg, logger=logger)
    return metrics.classification_report(gt_list, pre_list, target_names = list(target_names.keys()), output_dict=True)

def evaluateOK_NG_segmap(results, post_cfg={}, logger=None):
    try:
        from mmcv.utils import print_log
    except Exception as e:
        def print_log(msg, logger=None):
            print(msg)
    target_names = {'OK':0, 'NG':1}
    pre_list, gt_list = [], []
    for pre, gt, _ in results:
        # post_cfg = {'post_process_cfg':{'MORPH_OPEN_KERNEL':3}}
        pre_list.append(target_names.get(get_OK_NG(pre, post_cfg)))
        gt_list.append(target_names.get(gt))
    assert len(pre_list) == len(gt_list)
    # acc_rate = metrics.accuracy_score(gt_list, pre_list, normalize=True, sample_weight=None)
    print_msg = metrics.classification_report(gt_list, pre_list, target_names = list(target_names.keys()))
    if logger is None:
        print(print_msg)
    else:
        print_log(print_msg, logger=logger)
    return metrics.classification_report(gt_list, pre_list, target_names = list(target_names.keys()), output_dict=True)

def evaluateOK_NG(results, output=None, logger=None):
    try:
        from mmcv.utils import print_log
    except Exception as e:
        def print_log(msg, logger=None):
            print(msg)
    target_names = {'OK':0, 'NG':1}
    pre_list, gt_list = [], []
    if output != None:
        with open(osp.join(output, 'pre_gt_filename.txt'), 'w') as f:
            for pre, gt, filename in results:
                f.writelines(f"{pre} {gt} {filename}\n")
                pre_list.append(target_names.get(pre))
                gt_list.append(target_names.get(gt))
    else:
        for pre, gt, _ in results:
            pre_list.append(target_names.get(pre))
            gt_list.append(target_names.get(gt))
    assert len(pre_list) == len(gt_list)
    # acc_rate = metrics.accuracy_score(gt_list, pre_list, normalize=True, sample_weight=None)
    print_msg = metrics.classification_report(gt_list, pre_list, target_names = list(target_names.keys()))
    if logger is None:
        print(print_msg)
    else:
        print_log(print_msg, logger=logger)
    return metrics.classification_report(gt_list, pre_list, target_names = list(target_names.keys()), output_dict=True)
