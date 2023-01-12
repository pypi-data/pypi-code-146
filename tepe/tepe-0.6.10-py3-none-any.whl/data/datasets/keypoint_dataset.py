import copy
import json
import math
import os
import random
from loguru import logger

import numpy as np
import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2
import torch
import matplotlib
from matplotlib import pyplot as plt
from torch.utils.data import Dataset
try:
    matplotlib.use('TkAgg')
except:
    pass

class NormalizeImage(object):
    def __init__(self, mean=[103.53,116.28,123.675], 
                 std=[57.375,57.12,58.395]):
        self.mean = np.array(mean).astype(np.float32)
        self.std = np.array(std).astype(np.float32)
        pass

    def __call__(self, image, labels=None):
        image = image - self.mean
        image = image / self.std
        return image, labels


class KPRandomPadCrop(object):
    def __init__(self, ratio=0.25, pad_value=[128, 128, 128]):
        assert (ratio > 0 and ratio <= 1)
        self.ratio = ratio
        self.pad_value = pad_value

    def __call__(self, image, labels=None):
        if random.randint(0,1):
            h, w = image.shape[:2]
            top_offset = int(h * random.uniform(0, self.ratio))
            bottom_offset = int(h * random.uniform(0, self.ratio))
            left_offset = int(w * random.uniform(0, self.ratio))
            right_offset = int(w * random.uniform(0, self.ratio))
            # pad
            if random.randint(0,1):
                image = cv2.copyMakeBorder(image, top_offset, bottom_offset, left_offset, right_offset, cv2.BORDER_CONSTANT, value=self.pad_value)
                if labels is not None and len(labels) > 0:
                    labels[:, 0] = (labels[:, 0] * w + left_offset) / (w + left_offset + right_offset)
                    labels[:, 1] = (labels[:, 1] * h + top_offset) / (h + top_offset + bottom_offset)
            # crop
            else:
                image = image[top_offset:h - bottom_offset, left_offset:w-right_offset]
                if labels is not None and len(labels) > 0:
                    labels[:, 0] = (labels[:, 0] * w - left_offset) / (w - left_offset - right_offset)
                    labels[:, 1] = (labels[:, 1] * h - top_offset) / (h - top_offset - bottom_offset)

        return image, labels


class KPRandomHorizontalFlip(object):
    def __init__(self):
        pass

    def __call__(self, image, labels=None):
        if random.randint(0, 1):
            image = cv2.flip(image, 1)
            h, w = image.shape[:2]
            if labels is not None and len(labels) > 0:
                labels[:, 0] = 1.0 - labels[:, 0]
        return image, labels


class KPResizeImage(object):
    def __init__(self, size):
        self.size = size

    def __call__(self, image, labels=None, resize=None):
        h, w = image.shape[:2]
        if resize is None:
            image = cv2.resize(image, tuple(self.size))
        else:
            image = cv2.resize(image, tuple(resize))
        return image, labels


class KPRandomSwapChannels(object):
    def __init__(self):
        self.swaps = ((0, 1, 2), (0, 2, 1),
                      (1, 0, 2), (1, 2, 0),
                      (2, 0, 1), (2, 1, 0))

    def __call__(self, image, labels=None):
        if random.randint(0, 1):
            index = random.randint(0, len(self.swaps) - 1)
            image = image[:, :, self.swaps[index]]
        return image, labels


class KPRandomContrast(object):
    def __init__(self, lower=0.8, upper=1.2):
        self.lower = lower
        self.upper = upper
        assert self.upper >= self.lower, "contrast upper must be >= lower."
        assert self.lower >= 0, "contrast lower must be non-negative."

    # expects float image
    def __call__(self, image, labels=None):
        if random.randint(0, 1):
            alpha = random.uniform(self.lower, self.upper)
            image = image.astype(np.float32) * alpha
        return image, labels


class KPRandomHSV(object):
    def __init__(self, hue=0.1, saturation=1.2, value=1.2):
        self.hue = hue
        self.saturation = saturation
        self.value = value

    def __call__(self, image, labels=None):
        if random.randint(0, 1):
            dh = random.uniform(-self.hue, self.hue)
            ds = random.uniform(1, self.saturation)
            if random.random() < 0.5:
                ds = 1 / ds
            dv = random.uniform(1, self.value)
            if random.random() < 0.5:
                dv = 1 / dv

            image = image.astype(np.float32) / 255.0
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            def wrap_hue(x):
                x[x >= 360.0] -= 360.0
                x[x < 0.0] += 360.0
                return x

            image[:, :, 0] = wrap_hue(image[:, :, 0] + (360.0 * dh))
            image[:, :, 1] = np.clip(ds * image[:, :, 1], 0.0, 1.0)
            image[:, :, 2] = np.clip(dv * image[:, :, 2], 0.0, 1.0)

            image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
            image = (image * 255.0)
        return image, labels


class Albumentations:
    # Albumentations class (optional, only used if package is installed)
    # pip install albumentations
    def __init__(self, transform):
        self.transform = transform

        logger.info('albumentations:\n' + '\n'.join(f'{x}' for x in self.transform.transforms if x.p))

    def __call__(self, im, labels, p=1.0):
        if self.transform and random.random() < p:
            # decode
            kp = labels[:, :2]
            kp[:, 0] *= im.shape[1]
            kp[:, 1] *= im.shape[0]

            new = self.transform(image=im, keypoints=kp, class_labels=labels[:, 2])  # transformed
            im, labels = new['image'], np.array([[*k, c] for k, c in zip(new['keypoints'], new['class_labels'])])
            labels[:, 0] /= im.shape[1]
            labels[:, 1] /= im.shape[0]

        return im, labels


class KeyPointsDataset(Dataset):
    def __init__(self, root, transform=None, class_name=None, image_sets=None,
                 is_train=False, imgsz=224, stride=8,
                 gauss_ratio=1, gauss_sigma=0.5):
        self.root = root
        self.class_name = {cls: idx for idx, cls in enumerate(class_name)}
        self.kp_num = len(class_name)
        self.transform = transform
        if isinstance(transform, A.Compose):
            self.transform = Albumentations(transform)
        self.data = []

        imgsz = [imgsz, imgsz] if isinstance(imgsz, int) else imgsz
        input_h, input_w = imgsz
        self.heatmap_h, self.heatmap_w = input_h, input_w
        self.gauss_ratio = gauss_ratio * stride
        self.gauss_sigma = gauss_sigma * stride

        is_dir = True if image_sets is None else False
        if is_dir:
            for name in os.listdir(root):
                if name.split('.')[-1] not in ['jpg', 'png']:
                    continue
                path, label = self.get_data(name)
                if label is None:
                    continue
                self.data.append((path, np.stack(label, axis=0)))
        else:
            if not isinstance(image_sets, list):
                image_sets = [image_sets]
            is_txt = True
            txt_paths = []
            for set in image_sets:
                txt = os.path.join(root, set + '.txt')
                txt_paths.append(txt)
                is_txt &= os.path.exists(txt)
            # split dataset
            if not is_txt:
                logger.info(f'Not found {image_sets}.txt, generate it.')
                self.split_train_val(root)
                txt_name = 'train' if is_train else 'val'
                txt_paths = [os.path.join(root, txt_name + '.txt')]
            for txt in txt_paths:
                with open(txt, 'r') as f:
                    for line in f:
                        name = line.strip()
                        path, label = self.get_data(name)
                        if label is None:
                            continue
                        self.data.append((path, np.stack(label, axis=0)))

        logger.info(f'class name: {self.class_name}')

        desc = 'train' if is_train else 'val' if not is_dir else 'IMG'
        desc += f': found {len(self.data)} images'
        logger.info(desc)

    def get_data(self, img_name):
        img_path = os.path.join(self.root, 'images', img_name)
        if not os.path.exists(img_path):
            logger.info(f"{img_path} is not exists")
            return None, None
        suffix = img_name.split('.')[-1]
        json_path = os.path.join(self.root, 'json', img_name.replace(suffix, 'json'))
        if not os.path.exists(json_path):
            logger.info(f"{img_path}'s label is not exists")
            return None, None
        return img_path, self.read_label(json_path)

    def read_label(self, json_path):
        with open(json_path, 'r') as f:
            json_dict = json.load(f)
        img_width, img_height = json_dict["imageWidth"], json_dict["imageHeight"]
        # sort shapes from classes 0
        shapes = [shape for shape in json_dict['shapes'] if shape["shape_type"] == "point"]
        # shapes.sort(key=lambda x: float(x['points'][0][0]) + float(x['points'][0][1]))
        # for shape in shapes:
        #     x, y = shape["points"][0]
        labels = []
        for shape in shapes:
            x, y = shape["points"][0]
            idx = self.class_name[shape["label"]]
            # normalize
            x /= img_width
            y /= img_height
            label = np.array([x, y, idx], dtype=np.float32)
            labels.append(label)
        return labels

    def __getitem__(self, idx):
        img_path, label_ori = self.data[idx]
        labels = copy.deepcopy(label_ori)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if self.transform is not None:
            img, labels = self.transform(img, labels)

        img = img.transpose(2, 0, 1)

        heatmap = self.generate_target(labels)

        return img, heatmap

    def __len__(self):
        return len(self.data)

    def generate_target(self, labels):
        """

        :param labels:  [num_joints, 3]
        :param joints_vis: [num_joints, 3]
        :return: target, target_weight(1: visible, 0: invisible)
        """

        target = np.zeros((
            self.heatmap_h,
            self.heatmap_w,
            self.kp_num
            ), dtype=np.float32)

        tmp_size = self.gauss_ratio

        for kp_id in range(labels.shape[0]):
            label = labels[kp_id]
            kp_cls = int(label[2])
            heatmap = target[...,kp_cls]
            mu_x = int(label[0] * self.heatmap_w + 0.5)
            mu_y = int(label[1] * self.heatmap_h + 0.5)

            # Check that any part of the gaussian is in-bounds
            ul = [int(mu_x - tmp_size), int(mu_y - tmp_size)]
            br = [int(mu_x + tmp_size + 1), int(mu_y + tmp_size + 1)]
            if ul[0] >= self.heatmap_w or ul[1] >= self.heatmap_h \
                    or br[0] < 0 or br[1] < 0:
                continue

            # Generate gaussian
            size = 2 * tmp_size + 1
            x = np.arange(0, size, 1, np.float32)
            y = x[:, np.newaxis]
            x0 = y0 = size // 2
            # The gaussian is not normalized, we want the center value to equal 1
            g = np.exp(- ((x - x0) ** 2 + (y - y0) ** 2) / (2 * self.gauss_sigma ** 2))

            # Usable gaussian range
            g_x = max(0, -ul[0]), min(br[0], self.heatmap_w) - ul[0]
            g_y = max(0, -ul[1]), min(br[1], self.heatmap_h) - ul[1]
            # Image range
            img_x = max(0, ul[0]), min(br[0], self.heatmap_w)
            img_y = max(0, ul[1]), min(br[1], self.heatmap_h)

            heatmap[img_y[0]:img_y[1], img_x[0]:img_x[1]] = g[g_y[0]:g_y[1], g_x[0]:g_x[1]]

        target = cv2.resize(target, (28, 28)).reshape(28, 28, -1).transpose(2, 0, 1)
        return target

    @staticmethod
    def split_train_val(root):
        image_list = []
        folder_path = os.path.join(root, 'images')
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            image_list += [name + '\n' for name in os.listdir(folder_path)
                           if name.split('.')[-1] in ['jpg', 'png']]

        random.shuffle(image_list)
        num_images = len(image_list)
        num_train = int(0.75 * num_images)
        train_images = image_list[:num_train]
        val_images = image_list[num_train:]

        random.shuffle(train_images)
        random.shuffle(val_images)

        ftrain = open(os.path.join(root, 'train.txt'), 'w')
        ftrain.writelines(train_images)
        ftrain.close()
        fval = open(os.path.join(root, 'val.txt'), 'w')
        fval.writelines(val_images)
        fval.close()

        logger.info(f'train.txt and val.txt are generated in {root}')

    @staticmethod
    def collate_fn(batch):
        imgs, labels = list(zip(*batch))
        imgs = torch.from_numpy(np.stack(imgs, 0))
        labels = torch.from_numpy(np.stack(labels, 0))
        return [imgs, labels]

    @staticmethod
    def visual_add_image_with_heatmap(images, labels):
        """
        Args:
            images: (np.ndarray)
            labels:

        Returns:

        """
        fig = plt.figure(figsize=(10, 10), dpi=100)
        plt.clf()

        label0 = labels
        images = images.transpose(1, 2, 0)
        images *= np.array([57.12, 58.395, 57.375])
        images += np.array([123.675, 103.53, 116.28])
        image0 = images.astype(np.uint8)
        h, w = image0.shape[0:2]

        kp_num = label0.shape[0]
        for kp_c in range(kp_num):
            plt.subplot(2, kp_num, kp_c + 1)
            plt.imshow(image0)

        for kp_c in range(kp_num):
            plt.subplot(2, kp_num, kp_num + kp_c + 1)
            plt.imshow(image0)
            plt.imshow(cv2.resize(label0[kp_c], (w, h)), alpha=0.5)

        # plt.savefig('./tran_%d.jpg' % epoch)
        plt.show()


if __name__ == '__main__':

    RESIZE = (224, 224)

    transform = A.Compose([
        A.Resize(RESIZE[0], RESIZE[1], p=1),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.4),
        A.Rotate(limit=15, border_mode=cv2.BORDER_REPLICATE, p=0.3),
        A.OneOf([
            A.HueSaturationValue(p=0.4),
            A.ChannelShuffle(p=0.5)
        ], p=1),
        A.Normalize(),
        # ToTensorV2()
    ], keypoint_params=A.KeypointParams(format='xy', label_fields=['class_labels']))

    data_path = '/home/zepei/DATA/meter/dataset/special_meter'
    dataset_train = KeyPointsDataset(data_path, transform=transform,
                                     class_name=('pointer', 'marker'),
                                     image_sets='train', is_train=True)


    for idx in range(10):
        images, labels = dataset_train[idx]
        print(images.shape)
        print(labels.shape)
        # dataset_train.visual_add_image_with_heatmap(images, labels)
        if idx == 0:
            break

