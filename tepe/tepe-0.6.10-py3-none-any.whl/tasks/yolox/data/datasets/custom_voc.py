# Code are based on
# https://github.com/fmassa/vision/blob/voc_dataset/torchvision/datasets/voc.py
import glob
import os
import os.path
import xml.etree.ElementTree as ET
from tabulate import tabulate

import cv2
import numpy as np
from loguru import logger

from tepe.core.evaluator.metrics.voc_metrics import voc_eval
from .datasets_wrapper import Dataset


class CustomVOC(Dataset):

    """
    VOC Detection Dataset Object

    input is image, target is annotation

    Args:
        root (string): filepath to VOCdevkit folder.
        image_set (string): imageset to use (eg. 'train', 'val', 'test')
        transform (callable, optional): transformation to perform on the
            input image
        target_transform (callable, optional): transformation to perform on the
            target `annotation`
            (eg: take in caption string, return tensor of word indices)
        dataset_name (string, optional): which dataset to load
            (default: 'VOC2007')
    """

    def __init__(
        self,
        data_dir,
        cls_name,
        image_sets=["trainval"],
        img_size=(416, 416),
        preproc=None,
        dataset_name="VOC0712",
        cache=False,
        desc=''
    ):
        super().__init__(img_size)
        self.root = data_dir
        self.image_set = image_sets if isinstance(image_sets, list) else [image_sets]
        self.img_size = img_size
        self.preproc = preproc
        self.class_to_ind = dict(zip(cls_name, range(len(cls_name))))
        # self.target_transform = AnnotationTransform(cls_name=cls_name)
        self.name = dataset_name
        self._annopath = os.path.join(self.root, "Annotations")
        self._imgpath = os.path.join(self.root, "JPEGImages")
        self._setpath = os.path.join(self.root, "ImageSets", "Main")
        if not os.path.exists(self._setpath) or len(os.listdir(self._setpath)) == 0:
            self._gen_voc_train_val_sets()
        self.classes = cls_name

        self.ids = list()
        for name in self.image_set:
            txt_file = os.path.join(self._setpath, name + ".txt")
            if not os.path.exists(txt_file):
                logger.info("%s is not exists, please check your 'image_sets' input." % txt_file)
            for line in open(txt_file):
                self.ids.append(line.strip())

        logger.info(f'{desc}: found {len(self.ids)} images')
        self.annotations = self._load_voc_annotations()
        self.imgs = None
        if cache:
            self._cache_images()

    def __len__(self):
        return len(self.ids)

    def _load_voc_annotations(self):
        return [self.load_anno_from_ids(_ids) for _ids in range(len(self.ids))]

    def _cache_images(self):
        logger.warning(
            "\n********************************************************************************\n"
            "You are using cached images in RAM to accelerate training.\n"
            "This requires large system RAM.\n"
            "Make sure you have 60G+ RAM and 19G available disk space for training VOC.\n"
            "********************************************************************************\n"
        )
        max_h = self.img_size[0]
        max_w = self.img_size[1]
        cache_file = self.root + "/img_resized_cache_" + self.name + ".array"
        if not os.path.exists(cache_file):
            logger.info(
                "Caching images for the first time. This might take about 3 minutes for VOC"
            )
            self.imgs = np.memmap(
                cache_file,
                shape=(len(self.ids), max_h, max_w, 3),
                dtype=np.uint8,
                mode="w+",
            )
            from tqdm import tqdm
            from multiprocessing.pool import ThreadPool

            NUM_THREADs = min(8, os.cpu_count())
            loaded_images = ThreadPool(NUM_THREADs).imap(
                lambda x: self.load_resized_img(x),
                range(len(self.annotations)),
            )
            pbar = tqdm(enumerate(loaded_images), total=len(self.annotations))
            for k, out in pbar:
                self.imgs[k][: out.shape[0], : out.shape[1], :] = out.copy()
            self.imgs.flush()
            pbar.close()
        else:
            logger.warning(
                "You are using cached imgs! Make sure your dataset is not changed!!\n"
                "Everytime the self.input_size is changed in your exp file, you need to delete\n"
                "the cached data and re-generate them.\n"
            )

        logger.info("Loading cached imgs...")
        self.imgs = np.memmap(
            cache_file,
            shape=(len(self.ids), max_h, max_w, 3),
            dtype=np.uint8,
            mode="r+",
        )

    def load_anno_from_ids(self, index):
        img_id = self.ids[index]
        xml = ET.parse(os.path.join(self._annopath, img_id + '.xml')).getroot()

        res, img_info = self._read_annotation(xml)
        height, width = img_info

        r = min(self.img_size[0] / height, self.img_size[1] / width)
        res[:, :4] *= r  # [xmin, ymin, xmax, ymax, label_ind]
        resized_info = (int(height * r), int(width * r))

        return (res, img_info, resized_info)

    def _read_annotation(self, xml):
        """
        Arguments:
            xml (annotation) : the target annotation to be made usable
                will be an ET.Element
        Returns:
            a list containing lists of bounding boxes  [bbox coords, class name]
        """
        res = np.empty((0, 5))
        for obj in xml.iter("object"):
            difficult = obj.find("difficult")
            if difficult is not None:
                difficult = int(difficult.text) == 1
            else:
                difficult = False
            keep_difficult = True
            if not keep_difficult and difficult:
                continue
            name = obj.find("name").text.strip()
            bbox = obj.find("bndbox")

            pts = ["xmin", "ymin", "xmax", "ymax"]
            bndbox = []
            for i, pt in enumerate(pts):
                cur_pt = round(float(bbox.find(pt).text)) - 1
                # scale height or width
                # cur_pt = cur_pt / width if i % 2 == 0 else cur_pt / height
                bndbox.append(cur_pt)
            label_idx = self.class_to_ind[name]
            bndbox.append(label_idx)
            res = np.vstack((res, bndbox))  # [xmin, ymin, xmax, ymax, label_ind]
            # img_id = target.find('filename').text[:-4]

        width = int(xml.find("size").find("width").text)
        height = int(xml.find("size").find("height").text)
        img_info = (height, width)

        return res, img_info

    def load_anno(self, index):
        return self.annotations[index][0]

    def load_resized_img(self, index):
        img = self.load_image(index)
        r = min(self.img_size[0] / img.shape[0], self.img_size[1] / img.shape[1])
        resized_img = cv2.resize(
            img,
            (int(img.shape[1] * r), int(img.shape[0] * r)),
            interpolation=cv2.INTER_LINEAR,
        ).astype(np.uint8)

        return resized_img

    def load_image(self, index):
        img_id = self.ids[index]
        img = cv2.imread(os.path.join(self._imgpath, img_id + '.jpg'), cv2.IMREAD_COLOR)
        assert img is not None

        return img

    def pull_item(self, index):
        """Returns the original image and target at an index for mixup

        Note: not using self.__getitem__(), as any transformations passed in
        could mess up this functionality.

        Argument:
            index (int): index of img to show
        Return:
            img, target
        """
        if self.imgs is not None:
            target, img_info, resized_info = self.annotations[index]
            pad_img = self.imgs[index]
            img = pad_img[: resized_info[0], : resized_info[1], :].copy()
        else:
            img = self.load_resized_img(index)
            target, img_info, _ = self.annotations[index]

        return img, target, img_info, index

    @Dataset.mosaic_getitem
    def __getitem__(self, index):
        img, target, img_info, img_id = self.pull_item(index)

        if self.preproc is not None:
            img, target = self.preproc(img, target, self.input_dim)

        return img, target, img_info, img_id

    def evaluate_detections(self, all_boxes, write_result=False, output_dir=None):
        """
        all_boxes is a list of length number-of-classes.
        Each list element is a list of length number-of-images.
        Each of those list elements is either an empty list []
        or a numpy array of detection.

        all_boxes[class][image] = [] or np.array of shape #dets x 5
        """
        all_detection = self._write_voc_results_file(all_boxes, write_result, output_dir)
        IouTh = np.linspace(
            0.5, 0.95, int(np.round((0.95 - 0.5) / 0.05)) + 1, endpoint=True
        )
        mAPs = []
        table_header = ["class", "mAP50"]
        result_log = "\n"
        for i, iou in enumerate(IouTh):
            aps = self._do_python_eval(all_detection, iou)

            # show AP50 per class in a table
            if i == 0:
                ap50_table = []
                for i, cls in enumerate(self.classes):
                    if cls == "__background__":
                        continue
                    ap50_table.append((cls, aps[i]))
                result_log += tabulate(ap50_table, headers=table_header, tablefmt="fancy_grid")

            mAP = np.mean(aps)
            mAPs.append(mAP)

        logger.info(result_log + 
                f"\n---------------------------\n"
                f"map_5095: {np.mean(mAPs)}\n"
                f"map_50: {mAPs[0]}\n"
                f"---------------------------"
            )
        return np.mean(mAPs), mAPs[0]

    def _write_voc_results_file(self, all_boxes, write_result=False, output_dir=None):
        all_detection = {}
        for cls_ind, cls in enumerate(self.classes):
            if cls == "__background__":
                continue

            detection = []
            for im_ind, index in enumerate(self.ids):
                # index = index[1]
                dets = all_boxes[cls_ind][im_ind]
                if dets == []:
                    continue
                for k in range(dets.shape[0]):
                    detection.append([index,
                                      dets[k, -1],
                                      dets[k, 0] + 1,
                                      dets[k, 1] + 1,
                                      dets[k, 2] + 1,
                                      dets[k, 3] + 1, ])

            if write_result and output_dir is not None:
                filename = os.path.join(output_dir, "det_result_{:s}.txt").format(cls)
                logger.info("Writing {} VOC results in {}".format(cls, filename))
                f = open(filename, "wt")
                for im_ind, index in enumerate(self.ids):
                    # index = index[1]
                    dets = all_boxes[cls_ind][im_ind]
                    if dets == []:
                        continue
                    for k in range(dets.shape[0]):
                        f.write(
                            "{:s} {:.3f} {:.1f} {:.1f} {:.1f} {:.1f}\n".format(
                                index,
                                dets[k, -1],
                                dets[k, 0] + 1,
                                dets[k, 1] + 1,
                                dets[k, 2] + 1,
                                dets[k, 3] + 1,
                            )
                        )
                f.close()


            all_detection[cls] = detection
        return all_detection

    def _do_python_eval(self, all_detection, iou=0.5):
        rootpath = self.root
        name = self.image_set[0]
        annopath = os.path.join(rootpath, "Annotations", "{:s}.xml")
        imagesetfile = os.path.join(rootpath, "ImageSets", "Main", name + ".txt")
        cachedir = os.path.join(
            self.root, "annotations_cache", name
        )
        if not os.path.exists(cachedir):
            os.makedirs(cachedir)
        aps = []
        # The PASCAL VOC metric changed in 2010
        use_07_metric = False

        for i, cls in enumerate(self.classes):
            if cls == "__background__":
                continue

            detecion = all_detection[cls]
            rec, prec, ap = voc_eval(
                detecion,
                annopath,
                imagesetfile,
                cls,
                cachedir,
                ovthresh=iou,
                use_07_metric=use_07_metric,
            )
            aps.append(ap)

        return aps

    def _gen_voc_train_val_sets(self, trainval_ratio=1, train_ratio=0.7):
        import random
        set_dir = os.path.join(self.root, "ImageSets", "Main")
        if not os.path.exists(set_dir):
            os.makedirs(set_dir, exist_ok=True)

        annos = glob.glob(os.path.join(self._annopath, '*.xml'))

        num = len(annos)
        l = range(num)

        tv = int(num * trainval_ratio)
        tr = int(tv * train_ratio)

        trainval = random.sample(l, tv)
        train = random.sample(range(tv), tr)

        ftrainval = open(os.path.join(self._setpath, 'trainval.txt'), 'w')
        ftest = open(os.path.join(self._setpath, 'test.txt'), 'w')
        ftrain = open(os.path.join(self._setpath, 'train.txt'), 'w')
        fval = open(os.path.join(self._setpath, 'val.txt'), 'w')

        for i in l:
            name = os.path.basename(annos[i]).replace('.xml', '\n')
            if i in trainval:
                ftrainval.write(name)
                if i in train:
                    ftrain.write(name)
                else:
                    fval.write(name)
            else:
                ftest.write(name)

        ftrainval.close()
        ftrain.close()
        fval.close()
        ftest.close()

        logger.info('OUTPUT: trainval.txt, test.txt, train.txt, val.txt\n')