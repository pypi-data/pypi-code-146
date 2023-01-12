import os
import cv2
import numpy as np
import random
from loguru import logger
from PIL import Image

import torch
from torch.utils.data.dataset import Dataset


class CustomClsDataset(Dataset):
    """
    自定义的分类数据集，支持两种数据集结构：
    第一种：
        root
        ├── 0
        │   ├── 20211201-11330_5.jpg
        │   ├── 20211201-11340_5.jpg
        │   └── 20211201-11361_5.jpg
        ├── 1
        │   ├── 20211201-11330_5.jpg
        │   ├── 20211201-11340_5.jpg
        │   └── 20211201-11361_5.jpg
        ├── ...
        │   └── ...
        ├── train.txt
        └── val.txt
    第二种：
        root
        ├── train
        │   ├── 0
        │   │   ├── 20211201-11340_5.jpg
        │   │   ├── 20211201-11350_5.jpg
        │   │   └── 20211201-11361_5.jpg
        │   ├── 1
        │   │   ├── 20211201-11340_5.jpg
        │   │   ├── 20211201-11350_5.jpg
        │   │   └── 20211201-11361_5.jpg
        │   └── ...
        │       └── ...
        └── val
            ├── 0
            │   ├── 20211201-11330_5.jpg
            │   ├── 20211201-11360_5.jpg
            │   └── 20211201-11361_5.jpg
            ├── 1
            │   ├── 20211201-11340_5.jpg
            │   ├── 20211201-11360_5.jpg
            │   └── 20211201-11361_5.jpg
            └── ...
                └── ...
    """
    def __init__(self,
                 root,
                 classes,
                 image_sets=None,
                 transform=None,
                 is_train=False):
        self.class_dict = {classes[i]: i for i in range(len(classes))}
        self.imgs = []
        self.transform = transform

        if image_sets is None:
            image_sets = ['train']
        if not isinstance(image_sets, list):
            image_sets = [image_sets]
        is_dir, is_txt = True, True
        image_folders, txt_paths = [], []
        for set in image_sets:
            folder = os.path.join(root, set)
            txt = os.path.join(root, set + '.txt')
            image_folders.append(folder)
            txt_paths.append(txt)
            is_txt &= os.path.exists(txt)
            is_dir &= os.path.exists(folder)

        # generate train.txt and val.txt
        if not (is_txt | is_dir):  
            logger.info(f'Not found {image_sets}.txt, generate it.')
            self.split_train_val_for_cls(root, self.class_dict)

            is_txt = True
            txt_name = 'train' if is_train else 'val'
            txt_paths = [os.path.join(root, txt_name + '.txt')]

        cls_num = {cls: 0 for cls in classes}
        if is_txt:
            for txt in txt_paths:
                with open(txt, 'r') as f:
                    for line in f:
                        _path, label = line.strip().rsplit(maxsplit=1)
                        path = os.path.join(root, _path)
                        if os.path.exists(path) and (label in self.class_dict):
                            self.imgs.append((path, self.class_dict[label]))
                            cls_num[label] += 1
        else:
            for folder in image_folders:
                for label in os.listdir(folder):
                    imgs_label = [(os.path.join(folder, label, name), self.class_dict[label])
                                  for name in os.listdir(os.path.join(folder, label))
                                  if os.path.getsize(os.path.join(folder, label, name))]
                    self.imgs.extend(imgs_label)
                    cls_num[label] += len(imgs_label)

        assert len(self.imgs), 'number of images is 0'
        logger.info(f'class map: {self.class_dict}')
        desc = 'train' if is_train else 'val'
        desc += f': found {len(self.imgs)} images, '
        desc += ' '.join(['{}: {}'.format(k, v) for k, v in cls_num.items()])
        logger.info(desc)

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (img, target, img_info, img_path)
        """
        img_path, label = self.imgs[index]

        # img = cv2.imread(img_path)
        # img = img[:,:,::-1]  # BGR to RGB
        with open(img_path, 'rb') as f:
            img = Image.open(f).convert('RGB')
        img_info = dict(shape=img.size)
        # img_info = img.shape[:2]
        # target = label.to(torch.long)
        target = label

        if self.transform is not None:
            img = self.transform(img)

        return img, target, img_info, img_path

    @staticmethod
    def collate_fn(batch):
        imgs = [img[0] for img in batch]
        targets = torch.tensor([target[1] for target in batch], dtype=torch.int64)
        w = imgs[0].size[0]
        h = imgs[0].size[1]
        tensor = torch.zeros((len(imgs), 3, h, w), dtype=torch.uint8)
        for i, img in enumerate(imgs):
            nump_array = np.asarray(img, dtype=np.uint8)
            tens = torch.from_numpy(nump_array)
            if (nump_array.ndim < 3):
                nump_array = np.expand_dims(nump_array, axis=-1)
            nump_array = np.rollaxis(nump_array, 2)

            tensor[i] += torch.from_numpy(nump_array)

        return tensor, targets

    @staticmethod
    def split_train_val_for_cls(root, class_dict=None):
        ftrain = open(os.path.join(root, 'train.txt'), 'w')
        fval = open(os.path.join(root, 'val.txt'), 'w')
        train_list, val_list = [], []
        for label in os.listdir(root):
            if class_dict:
                if label not in class_dict: continue
            image_list = os.listdir(os.path.join(root, label))
            random.shuffle(image_list)
            num_images = len(image_list)
            num_train = int(0.7 * num_images)
            train_images = image_list[:num_train]
            val_images  = image_list[num_train:]

            train_list += [label + '/' + name + ' ' + label + '\n' for name in train_images]
            val_list += [label + '/' + name + ' ' + label + '\n' for name in val_images]

        random.shuffle(train_list)
        random.shuffle(val_list)
        ftrain.writelines(train_list)
        fval.writelines(val_list)
        ftrain.close()
        fval.close()

        logger.info(f'train.txt and val.txt are generated in {root}')