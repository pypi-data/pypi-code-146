import os
from loguru import logger
from tqdm import tqdm
import cv2
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms as T

from tepe.data.augments.paste_images import paste_images


MVTEC_CLASS_NAMES = ['bottle', 'cable', 'capsule', 'carpet', 'grid',
                     'hazelnut', 'leather', 'metal_nut', 'pill', 'screw',
                     'tile', 'toothbrush', 'transistor', 'wood', 'zipper']

class AnomalyDataset(Dataset):
    def __init__(self, dataset_path, class_name='bottle',
                 transform=None, target_transform=None,
                 resize_fn=None, is_train=True, paste=False,
                 is_mvtec=True, cache_img = False):
        # assert class_name in CLASS_NAMES, 'class_name: {}, should be in {}'.format(class_name, CLASS_NAMES)
        self.dataset_path = dataset_path
        self.class_name = class_name
        self.is_train = is_train
        self.resize_fn = resize_fn
        self.transform = transform
        self.mask_transform = target_transform
        self.is_mvtec = is_mvtec
        self.cache_img = cache_img
        self.imgs, self.img_paths, self.tgt_paths, self.masks = self.load_dataset_folder()
        phase = 'train' if is_train else 'test'
        logger.info(f'{phase}: found {len(self.img_paths)} images in scene {self.class_name}')
        self.paste = paste
        self.paste_img_paths = []

    def __getitem__(self, idx):
        if self.cache_img:
            img, x, y, mask = self.imgs[idx], self.img_paths[idx], self.tgt_paths[idx], self.masks[idx]
        else:
            x, y, mask = self.img_paths[idx], self.tgt_paths[idx], self.masks[idx]
            img = self.load_resized_image(x)  # resized

        if self.paste:
            img = paste_images(img, self.paste_img_paths)

        if self.transform:
            img = self.transform(img)

        if y == 0 or not self.is_mvtec:
            mask = torch.zeros_like(img)
        else:
            mask = Image.open(mask)
            mask = self.mask_transform(mask)
        
        
        return dict(img=img, target=y, mask=mask, path=x)

    def __len__(self):
        return len(self.img_paths)
    
    def load_resized_image(self, path):

        im = cv2.imread(path)  # BGR
        assert im is not None, f'Image Not Found {path}'

        if self.resize_fn is not None:  # if sizes are not equal
            im, ratio, dwh = self.resize_fn(im)

        return im

    def load_dataset_folder(self):
        phase = 'train' if self.is_train else 'test'
        imgs, x, y, mask = [], [], [], []

        img_dir = os.path.join(self.dataset_path, self.class_name, phase)
        gt_dir = os.path.join(self.dataset_path, self.class_name, 'ground_truth')

        img_types = sorted(os.listdir(img_dir))
        for img_type in img_types:

            img_type_dir = os.path.join(img_dir, img_type)
            if not os.path.isdir(img_type_dir):
                continue
            img_fpath_list = sorted([os.path.join(img_type_dir, f)
                                    for f in os.listdir(img_type_dir)
                                    if f.endswith(('.jpg', '.png'))])

            x.extend(img_fpath_list)

            if img_type == 'good':
                y.extend([0] * len(img_fpath_list))
                mask.extend([None] * len(img_fpath_list))
            else:
                y.extend([1] * len(img_fpath_list))
                if self.is_mvtec:
                    gt_type_dir = os.path.join(gt_dir, img_type)
                    img_fname_list = [os.path.splitext(os.path.basename(f))[0] for f in img_fpath_list]
                    gt_fpath_list = [os.path.join(gt_type_dir, img_fname + '_mask.png')
                                    for img_fname in img_fname_list]
                    mask.extend(gt_fpath_list)
                else:
                    mask.extend([None] * len(img_fpath_list))

        assert len(x) == len(y), 'number of x and y should be same'
        if self.cache_img:
            for img_path in tqdm(x, desc='cache images'):
                imgs.append(self.load_resized_image(img_path))

        return list(imgs), list(x), list(y), list(mask)

    def add_hard_samples(self, samples):
        self.img_paths.extend(list(samples))
        if self.cache_img:
            for p in samples:
                self.imgs.append(self.load_resized_image(p))
        self.tgt_paths.extend([0] * len(samples))
        self.masks.extend([None] * len(samples))
        logger.info(f'add {len(samples)} hard samples to dataset, new dataset size: {len(self.img_paths)}')