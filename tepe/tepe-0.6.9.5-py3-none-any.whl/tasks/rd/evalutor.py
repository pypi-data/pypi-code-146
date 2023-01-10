import glob
import os
from statistics import mean

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from numpy import ndarray
from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter
from skimage import measure
from skimage.measure import label, regionprops
from sklearn.metrics import roc_auc_score, auc, precision_recall_curve, roc_curve
from torch.utils.data import DataLoader
from tqdm import tqdm

from tepe.data.datasets import AnomalyDataset
from tepe.data.voc_xml import PascalVocReader


def roc_auc_img(gt, score):
    img_roc_auc = roc_auc_score(gt, score)

    return img_roc_auc

def roc_auc_pxl(gt, score):
    per_pixel_roc_auc = roc_auc_score(gt.flatten(), score.flatten())

    return per_pixel_roc_auc


def pro_auc_pxl(gt, score):
    gt = np.squeeze(gt, axis=1)

    gt[gt <= 0.5] = 0
    gt[gt > 0.5] = 1
    gt = gt.astype(np.bool)

    max_step = 200
    expect_fpr = 0.3

    max_th = score.max()
    min_th = score.min()
    delta = (max_th - min_th) / max_step

    pros_mean = []
    pros_std = []
    threds = []
    fprs = []

    binary_score_maps = np.zeros_like(score, dtype=np.bool)

    for step in range(max_step):
        thred = max_th - step * delta
        binary_score_maps[score <= thred] = 0
        binary_score_maps[score > thred] = 1

        pro = []
        for i in range(len(binary_score_maps)):
            label_map = label(gt[i], connectivity=2)
            props = regionprops(label_map, binary_score_maps[i])

            for prop in props:
                pro.append(prop.intensity_image.sum() / prop.area)

        pros_mean.append(np.array(pro).mean())
        pros_std.append(np.array(pro).std())

        gt_neg = ~gt
        fpr = np.logical_and(gt_neg, binary_score_maps).sum() / gt_neg.sum()
        fprs.append(fpr)
        threds.append(thred)

    threds = np.array(threds)
    pros_mean = np.array(pros_mean)
    pros_std = np.array(pros_std)
    fprs = np.array(fprs)

    idx = fprs <= expect_fpr
    fprs_selected = fprs[idx]
    fprs_selected = rescale(fprs_selected)
    pros_mean_selected = rescale(pros_mean[idx])
    per_pixel_roc_auc = auc(fprs_selected, pros_mean_selected)

    return per_pixel_roc_auc


def rescale(x):
    return (x - x.min()) / (x.max() - x.min())


def get_threshold(gt, score):
    gt_mask = np.asarray(gt)
    precision, recall, thresholds = precision_recall_curve(gt_mask.flatten(), score.flatten())
    a = 2 * precision * recall
    b = precision + recall
    f1 = np.divide(a, b, out=np.zeros_like(a), where=b != 0)
    threshold = thresholds[np.argmax(f1)]

    return threshold


def cal_img_roc(scores, gt_list):
    img_scores = scores.reshape(scores.shape[0], -1).max(axis=1)
    gt_list = np.asarray(gt_list)

    fpr, tpr, _ = roc_curve(gt_list, img_scores)
    img_roc_auc = roc_auc_img(gt_list, img_scores)

    return fpr, tpr, img_roc_auc


def cal_pxl_roc(gt_mask, scores):
    fpr, tpr, _ = roc_curve(gt_mask.flatten(), scores.flatten())
    per_pixel_rocauc = roc_auc_pxl(gt_mask.flatten(), scores.flatten())

    return fpr, tpr, per_pixel_rocauc


def cal_pxl_pro(gt_mask, scores):
    per_pixel_proauc = pro_auc_pxl(gt_mask, scores)

    return per_pixel_proauc


def mvtec_eval(task):
    data_transform, target_transform = task.get_transform(mode='val')

    dataset = AnomalyDataset(task.data_root, class_name=task.scene,
                             transform=data_transform, target_transform=target_transform,
                             resize=task.input_size, is_train=False, is_mvtec=True,
                             cache_img=task.cache)

    dataloader = DataLoader(
        dataset, batch_size=task.batch_size, shuffle=False, num_workers=task.workers
    )

    model = task.get_model(train=False)

    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    fig_img_rocauc = ax[0]
    fig_pixel_rocauc = ax[1]


    gt_list = []
    gt_mask_list = []
    anomaly_maps = []

    for data in tqdm(dataloader):
        img, gt, label = data['img'], data['mask'], data['target']
        img = img.to(task.device)

        gt_list.extend(label.cpu().detach().numpy())
        gt_mask_list.extend(gt.cpu().detach().numpy())
        with torch.no_grad():
            anomaly_map = model(img)
        anomaly_maps.append(anomaly_map)

    anomaly_maps = torch.cat(anomaly_maps, dim=0).cpu().detach().numpy()
    for i in range(anomaly_maps.shape[0]):
        anomaly_maps[i] = gaussian_filter(anomaly_maps[i], sigma=8)

    gt_mask = np.asarray(gt_mask_list)
    # rescale

    r'Image-level AUROC'
    fpr, tpr, img_roc_auc = cal_img_roc(anomaly_maps, gt_list)
    fig_img_rocauc.plot(fpr, tpr, label='%s img_ROCAUC: %.3f' % (task.scene, img_roc_auc))
    fig_img_rocauc.set_xlabel('fpr')
    fig_img_rocauc.set_ylabel('tpr')
    fig_img_rocauc.title.set_text('image ROCAUC')
    fig_img_rocauc.legend(loc="lower right")

    r'Pixel-level AUROC'
    fpr, tpr, per_pixel_rocauc = cal_pxl_roc(gt_mask, anomaly_maps)
    fig_pixel_rocauc.plot(fpr, tpr, label='%s ROCAUC: %.3f' % (task.scene, per_pixel_rocauc))
    fig_pixel_rocauc.set_xlabel('fpr')
    fig_pixel_rocauc.set_ylabel('tpr')
    fig_pixel_rocauc.title.set_text('pixel ROCAUC')
    fig_pixel_rocauc.legend(loc="lower right")

    r'Pixel-level AUPRO'
    per_pixel_proauc = cal_pxl_pro(gt_mask, anomaly_maps)

    # print('image ROCAUC: %.3f'% (img_roc_auc))
    # print('pixel ROCAUC: %.3f'% (per_pixel_rocauc))
    # print('pixel PROAUC: %.3f'% (per_pixel_proauc))

    fig.tight_layout()
    fig.savefig(os.path.join(task.output_dir, task.scene, 'roc_curve.png'), dpi=100)

    return dict(img_rocauc=img_roc_auc, pixel_rocauc=per_pixel_rocauc, pixel_proauc=per_pixel_proauc)


def compute_pro(masks: ndarray, amaps: ndarray, num_th: int = 200) -> None:

    """Compute the area under the curve of per-region overlaping (PRO) and 0 to 0.3 FPR
    Args:
        category (str): Category of product
        masks (ndarray): All binary masks in test. masks.shape -> (num_test_data, h, w)
        amaps (ndarray): All anomaly maps in test. amaps.shape -> (num_test_data, h, w)
        num_th (int, optional): Number of thresholds
    """

    assert isinstance(amaps, ndarray), "type(amaps) must be ndarray"
    assert isinstance(masks, ndarray), "type(masks) must be ndarray"
    assert amaps.ndim == 3, "amaps.ndim must be 3 (num_test_data, h, w)"
    assert masks.ndim == 3, "masks.ndim must be 3 (num_test_data, h, w)"
    assert amaps.shape == masks.shape, "amaps.shape and masks.shape must be same"
    assert set(masks.flatten()) == {0, 1}, "set(masks.flatten()) must be {0, 1}"
    assert isinstance(num_th, int), "type(num_th) must be int"

    df = pd.DataFrame([], columns=["pro", "fpr", "threshold"])
    binary_amaps = np.zeros_like(amaps, dtype=np.bool)

    min_th = amaps.min()
    max_th = amaps.max()
    delta = (max_th - min_th) / num_th

    for th in np.arange(min_th, max_th, delta):
        binary_amaps[amaps <= th] = 0
        binary_amaps[amaps > th] = 1

        pros = []
        for binary_amap, mask in zip(binary_amaps, masks):
            for region in measure.regionprops(measure.label(mask)):
                axes0_ids = region.coords[:, 0]
                axes1_ids = region.coords[:, 1]
                tp_pixels = binary_amap[axes0_ids, axes1_ids].sum()
                pros.append(tp_pixels / region.area)

        inverse_masks = 1 - masks
        fp_pixels = np.logical_and(inverse_masks, binary_amaps).sum()
        fpr = fp_pixels / inverse_masks.sum()

        df = df.append({"pro": mean(pros), "fpr": fpr, "threshold": th}, ignore_index=True)

    # Normalize FPR from 0 ~ 1 to 0 ~ 0.3
    df = df[df["fpr"] < 0.3]
    df["fpr"] = df["fpr"] / df["fpr"].max()

    pro_auc = auc(df["fpr"], df["pro"])
    return pro_auc


def read_xml(xml_path, limit_label=()):
    reader = PascalVocReader(xml_path)
    anno_bboxes = reader.get_bbox()
    bboxes = []
    for anno in anno_bboxes:
        label, box = anno.get('name'), anno.get('bndbox')
        if limit_label:
            if label in limit_label:
                bboxes.append(box)
        else:
            bboxes.append(box)

    return torch.tensor(bboxes)


def box_iou(box1, box2):
    """
    Return intersection-over-union (Jaccard index) of boxes.
    Both sets of boxes are expected to be in (x1, y1, x2, y2) format.
    Arguments:
        box1 (Tensor[N, 4])
        box2 (Tensor[M, 4])
    Returns:
        iou (Tensor[N, M]): the NxM matrix containing the pairwise
            IoU values for every element in boxes1 and boxes2
    """

    def box_area(box):
        # box = 4xn
        return (box[2] - box[0]) * (box[3] - box[1])

    area1 = box_area(box1.T)
    area2 = box_area(box2.T)

    # inter(N,M) = (rb(N,M,2) - lt(N,M,2)).clamp(0).prod(2)
    inter = (torch.min(box1[:, None, 2:], box2[:, 2:]) - torch.max(box1[:, None, :2], box2[:, :2])).clamp(0).prod(2)
    return inter / (area1[:, None] + area2 - inter)  # iou = inter / (area1 + area2 - inter)


def cal_true_positive(gt, pred, iou_thr=0.001):
    num_pred = len(pred)
    num_gt = len(gt)
    p_tp, r_tp = 0, 0
    if num_gt > 0 and num_pred > 0:
        ious = box_iou(gt, pred)  # h: num_gt, w: num_pred
        for iou in ious:  # 对于每个GT
            r_tp += int((iou > iou_thr).sum() > 0)  # 只要有重叠即为检出

        ious = ious.T
        for iou in ious:  # 对于每个Pred
            p_tp += int((iou > iou_thr).sum() > 0)  # 只要有重叠即为预测正确

    return p_tp, r_tp


if __name__ == '__main__':
    pred_dir = '/home/zepei/workspace/ad-tepe/outputs/rd_bjguo_101_1110/bjguo/xml_predict'
    label_idr = '/home/zepei/DATA/lenovo_anomaly/bjguo/ground_truth/bad'

    total_pred, total_gt, total_rtp, total_ptp = 0, 0, 0, 0
    for pred_xml_path in glob.glob(os.path.join(pred_dir, '*.xml')):
        if '22273' in pred_xml_path: # or '32428' in pred_xml_path:

            xml_name = os.path.basename(pred_xml_path)
            label_xml_path = os.path.join(label_idr, xml_name)

            pred = read_xml(pred_xml_path)
            gt = read_xml(label_xml_path)

            num_pred = len(pred)
            num_gt = len(gt)
            p_tp, r_tp = cal_true_positive(gt, pred, iou_thr=0.00001)

            total_pred += num_pred
            total_gt += num_gt
            total_rtp += r_tp
            total_ptp += p_tp
            print(r_tp, p_tp, num_gt, num_pred)
            print(f'{pred_xml_path}')

    precision = total_ptp / total_pred
    recall = total_rtp / total_gt

    print('精度， 召回：', precision, recall)