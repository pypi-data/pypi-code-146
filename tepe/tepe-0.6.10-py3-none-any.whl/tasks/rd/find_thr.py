from loguru import logger
import numpy as np
import torch
from scipy.ndimage import gaussian_filter
from torch.nn import functional as F
from tqdm import tqdm


def find(model, good_loader, bad_loader, device):
    '''
    找个阈值, thr计算方式: (mean(正常样本的分数)+mean(异常样本分数))/2
    model:
    good_loader, bad_loader:训练样本的loader, 训练样本贴图后的loader
    return: thr <float>
    '''
    model.eval()
    gt_list_sp = []
    pr_list_sp = []
    #
    most = 40
    i = 0

    with torch.no_grad():
        for data in tqdm(good_loader):
            i = i + 1
            if i > most:
                break
            img = data['img'].to(device)
            anomaly_map = model(img)
            anomaly_map = anomaly_map.cpu().detach().numpy()
            anomaly_map = gaussian_filter(anomaly_map, sigma=4)  # [256,256]

            gt_list_sp.append(0)  # 一个值
            pr_list_sp.append(np.max(anomaly_map))
        i = 0
        for data in tqdm(bad_loader):
            i = i + 1
            if i > most:
                break
            img = data['img'].to(device)
            anomaly_map = model(img)
            anomaly_map = anomaly_map.cpu().detach().numpy()
            anomaly_map = gaussian_filter(anomaly_map, sigma=4)  # [256,256]

            gt_list_sp.append(1)  # 一个值
            pr_list_sp.append(np.max(anomaly_map))

        gt_list_sp = np.array(gt_list_sp)
        pr_list_sp = np.array(pr_list_sp)

        # thr=compare(gt_list_sp=gt_list_sp, pr_list_sp=pr_list_sp)
        thr = (np.mean(pr_list_sp[np.where(gt_list_sp == 0)]) + np.mean(pr_list_sp[np.where(gt_list_sp == 1)])) / 2
    return thr


def find_hard_samples(model, dataloader, device, mining_thr=0.3):
    model.eval()

    select_paths = []
    for data in dataloader:
        img = data['img'].to(device)
        
        with torch.no_grad():
            anomaly_map = model(img)
            anomaly_values = anomaly_map.view(anomaly_map.shape[0], -1)

            # hard_pixels = (anomaly_values > mining_thr).sum(dim=1)  # 每个样本中大于mining_thr的像素数量
            # select_indices = torch.where(hard_pixels > 16)  # 寻找大于4x4 pixel的样本索引
            
            max_values = anomaly_values.max(dim=1)  # max value and loc index of per sample
            select_indices = torch.where(max_values[0] > mining_thr)[0].cpu().detach().numpy()
            
        paths = np.array(data['path'])

        select_path = paths[select_indices]
        select_paths.append(select_path)

    select_paths = np.concatenate(select_paths)

    return list(select_paths)