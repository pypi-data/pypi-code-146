import random
import xml.etree.ElementTree as ET

#-------------------------------------#
#       对数据集进行训练
#-------------------------------------#
import datetime
import os
import cv2
import time
from tqdm import tqdm

import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from .nets.yolo import YoloBody
from .nets.yolo_training import (ModelEMA, YOLOLoss, get_lr_scheduler,
                                 set_optimizer_lr, weights_init)
from .utils.callbacks import EvalCallback, LossHistory
from .utils.dataloader import YoloDataset, yolo_dataset_collate
from .utils.utils import download_weights, get_classes, show_config
from .utils.utils_fit import fit_one_epoch
from .utils.utils_map import get_coco_map, get_map


from .yolo import YOLO
from PIL import Image
from typing import List
from thop import clever_format, profile



class Yolov7:

    def __init__(self, classes_path: str = 'voc_classes.txt',
                 VOCdevkit_path: str = '.', anchors: List[list] =
                 [[12., 16.], [19., 36.], [40., 28.], [36., 75.],
                  [76., 55.], [72., 146.], [142., 110.], [192., 243.],
                     [459., 401.]], fonts: str = ".", phi: str = "l",
                 input_shape: list = [640, 640], anchors_mask: List[list] =
                 [[6, 7, 8], [3, 4, 5], [0, 1, 2]]) -> None:

        self.classes_path = classes_path
        self.VOCdevkit_path = VOCdevkit_path
        self.anchors = anchors
        self.classes, self.num_classes = get_classes(self.classes_path)
        self.VOCdevkit_sets: list = [('2007', 'train'), ('2007', 'val')]
        self.photo_nums = np.zeros(len(self.VOCdevkit_sets))
        self.nums = np.zeros(len(self.classes))
        self.input_shape = input_shape
        self.phi = phi
        self.anchors_mask = anchors_mask
        self.fonts = fonts

    def _set_annotation_file(self, annotation_mode: int = 0,
                             trainval_percent: float = 0.9,
                             train_percent: float = 0.9) -> tuple:

        return (annotation_mode, trainval_percent, train_percent)

    def _convert_annotation(self, year: int, image_id: int,
                            list_file: list) -> None:

        annotation_mode, trainval_percent, train_percent = \
            self._set_annotation_file()

        in_file = open(os.path.join(self.VOCdevkit_path,
                       'VOC%s/Annotations/%s.xml' % (year, image_id)),
                       encoding='utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()

        for obj in root.iter('object'):
            difficult = 0
            if obj.find('difficult') is not None:
                difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in self.classes or int(difficult) == 1:
                continue
            cls_id = self.classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (int(float(xmlbox.find('xmin').text)),
                 int(float(xmlbox.find('ymin').text)), int(
                float(xmlbox.find('xmax').text)),
                int(float(xmlbox.find('ymax').text)))
            list_file.write(" " + ",".join([str(a)
                            for a in b]) + ',' + str(cls_id))

            self.nums[self.classes.index(
                cls)] = self.nums[self.classes.index(cls)] + 1

    def voc_annotation(self) -> None:
        random.seed(0)

        annotation_mode, trainval_percent, train_percent = \
            self._set_annotation_file()

        if " " in os.path.abspath(self.VOCdevkit_path):
            raise ValueError("数据集存放的文件夹路径与图片名称中不可以存在空格，否则会影响正常的模型训练，请注意修改。\
                              The path of the folder where the dataset is \
                              stored and the name of the images must not \
                              have spaces, otherwise it will affect the \
                              normal model training.")

        if annotation_mode == 0 or annotation_mode == 1:
            print("Generate txt in ImageSets.")
            xmlfilepath = os.path.join(
                self.VOCdevkit_path, 'VOC2007', 'Annotations')
            saveBasePath = os.path.join(
                self.VOCdevkit_path, 'VOC2007', 'ImageSets/Main')
            temp_xml = os.listdir(xmlfilepath)
            total_xml = []
            for xml in temp_xml:
                if xml.endswith(".xml"):
                    total_xml.append(xml)

            num = len(total_xml)
            list = range(num)
            tv = int(num*trainval_percent)
            tr = int(tv*train_percent)
            trainval = random.sample(list, tv)
            train = random.sample(trainval, tr)

            print("train and val size", tv)
            print("train size", tr)
            ftrainval = open(os.path.join(saveBasePath, 'trainval.txt'), 'w')
            ftest = open(os.path.join(saveBasePath, 'test.txt'), 'w')
            ftrain = open(os.path.join(saveBasePath, 'train.txt'), 'w')
            fval = open(os.path.join(saveBasePath, 'val.txt'), 'w')

            for i in list:
                name = total_xml[i][:-4]+'\n'
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
            print("Generate txt in ImageSets done.")

        if annotation_mode == 0 or annotation_mode == 2:
            print("Generate 2007_train.txt and 2007_val.txt for train.")
            type_index = 0
            for year, image_set in self.VOCdevkit_sets:
                image_ids = open(os.path.join(self.VOCdevkit_path,
                                              'VOC%s/ImageSets/Main/%s.txt' %
                                 (year, image_set)),
                                 encoding='utf-8').read().strip().split()
                list_file = open('%s_%s.txt' %
                                 (year, image_set), 'w', encoding='utf-8')
                for image_id in image_ids:
                    list_file.write('%s/VOC%s/JPEGImages/%s.jpg' %
                                    (os.path.abspath(self.VOCdevkit_path),
                                        year, image_id))

                    self._convert_annotation(year, image_id, list_file)
                    list_file.write('\n')
                self.photo_nums[type_index] = len(image_ids)
                type_index += 1
                list_file.close()
            print("Generate 2007_train.txt and 2007_val.txt for train done.")

            def printTable(List1, List2):
                for i in range(len(List1[0])):
                    print("|", end=' ')
                    for j in range(len(List1)):
                        print(List1[j][i].rjust(int(List2[j])), end=' ')
                        print("|", end=' ')
                    print()

            str_nums = [str(int(x)) for x in self.nums]
            tableData = [
                self.classes, str_nums
            ]
            colWidths = [0]*len(tableData)
            # len1 = 0
            for i in range(len(tableData)):
                for j in range(len(tableData[i])):
                    if len(tableData[i][j]) > colWidths[i]:
                        colWidths[i] = len(tableData[i][j])
            printTable(tableData, colWidths)

            if self.photo_nums[0] <= 500:
                print("[INFO] 训练集数量小于500，属于较小的数据量，请注意设置较大的训练世代（Epoch）以满足足够的梯度下降次数（Step）。The size of the training data is less than 500. Consider training your model for longer epochs for better performance on this dataset.")

            if np.sum(self.nums) == 0:
                print("[WARNING] 在数据集中并未获得任何目标，请注意修改classes_path 对应自己的数据集，并且保证标签名字正确，否则训练将会没有任何效果！No targets were found in dataset. Make sure your classes_path is correct and correspond to your own data set, and ensure that the label names are correct. Otherwise the training will have no effect!")

    def train(self, cuda: bool = True, distributed: bool = False,
              sync_bn: bool = False, fp16: bool = False,
              pretrained: bool = False, model_path: str = "",
              save_dir: str = 'logs', save_period: int = 10,
              eval_flag: bool = True, eval_period: int = 10,
              num_workers: int = 4, epoch: int = 300,
              optimizer_type: str = 'sgd', batch_size: int = 4,
              freeze_train: bool = True, label_smoothing: int = 0) -> None:
        
        """
            训练自己的目标检测模型一定需要注意以下几点：
            1、训练前仔细检查自己的格式是否满足要求，该库要求数据集格式为VOC格式，需要准备好的内容有输入图片和标签
            输入图片为.jpg图片，无需固定大小，传入训练前会自动进行resize。
            灰度图会自动转成RGB图片进行训练，无需自己修改。
            输入图片如果后缀非jpg，需要自己批量转成jpg后再开始训练。
            标签为.xml格式，文件中会有需要检测的目标信息，标签文件和输入图片文件相对应。
            2、损失值的大小用于判断是否收敛，比较重要的是有收敛的趋势，即验证集损失不断下降，如果验证集损失基本上不改变的话，模型基本上就收敛了。
            损失值的具体大小并没有什么意义，大和小只在于损失的计算方式，并不是接近于0才好。如果想要让损失好看点，可以直接到对应的损失函数里面除上10000。
            训练过程中的损失值会保存在logs文件夹下的loss_%Y_%m_%d_%H_%M_%S文件夹中
            
            3、训练好的权值文件保存在logs文件夹中，每个训练世代（Epoch）包含若干训练步长（Step），每个训练步长（Step）进行一次梯度下降。
            如果只是训练了几个Step是不会保存的，Epoch和Step的概念要捋清楚一下。
            
        """

        anchors_mask = self.anchors_mask

        mosaic = True
        mosaic_prob = 0.5
        mixup = True
        mixup_prob = 0.5
        special_aug_ratio = 0.7
        #------------------------------------------------------------------#
        #   label_smoothing     标签平滑。一般0.01以下。如0.01、0.005。
        #------------------------------------------------------------------#
        label_smoothing = label_smoothing

        #----------------------------------------------------------------------------------------------------------------------------#
        #   训练分为两个阶段，分别是冻结阶段和解冻阶段。设置冻结阶段是为了满足机器性能不足的同学的训练需求。
        #   冻结训练需要的显存较小，显卡非常差的情况下，可设置Freeze_Epoch等于UnFreeze_Epoch，Freeze_Train = True，此时仅仅进行冻结训练。
        #
        #   在此提供若干参数设置建议，各位训练者根据自己的需求进行灵活调整：
        #   （一）从整个模型的预训练权重开始训练：
        #       Adam：
        #           Init_Epoch = 0，Freeze_Epoch = 50，UnFreeze_Epoch = 100，Freeze_Train = True，optimizer_type = 'adam'，Init_lr = 1e-3，weight_decay = 0。（冻结）
        #           Init_Epoch = 0，UnFreeze_Epoch = 100，Freeze_Train = False，optimizer_type = 'adam'，Init_lr = 1e-3，weight_decay = 0。（不冻结）
        #       SGD：
        #           Init_Epoch = 0，Freeze_Epoch = 50，UnFreeze_Epoch = 300，Freeze_Train = True，optimizer_type = 'sgd'，Init_lr = 1e-2，weight_decay = 5e-4。（冻结）
        #           Init_Epoch = 0，UnFreeze_Epoch = 300，Freeze_Train = False，optimizer_type = 'sgd'，Init_lr = 1e-2，weight_decay = 5e-4。（不冻结）
        #       其中：UnFreeze_Epoch可以在100-300之间调整。
        #   （二）从0开始训练：
        #       Init_Epoch = 0，UnFreeze_Epoch >= 300，Unfreeze_batch_size >= 16，Freeze_Train = False（不冻结训练）
        #       其中：UnFreeze_Epoch尽量不小于300。optimizer_type = 'sgd'，Init_lr = 1e-2，mosaic = True。
        #   （三）batch_size的设置：
        #       在显卡能够接受的范围内，以大为好。显存不足与数据集大小无关，提示显存不足（OOM或者CUDA out of memory）请调小batch_size。
        #       受到BatchNorm层影响，batch_size最小为2，不能为1。
        #       正常情况下Freeze_batch_size建议为Unfreeze_batch_size的1-2倍。不建议设置的差距过大，因为关系到学习率的自动调整。
        #----------------------------------------------------------------------------------------------------------------------------#
        #------------------------------------------------------------------#
        #   冻结阶段训练参数
        #   此时模型的主干被冻结了，特征提取网络不发生改变
        #   占用的显存较小，仅对网络进行微调
        #   Init_Epoch          模型当前开始的训练世代，其值可以大于Freeze_Epoch，如设置：
        #                       Init_Epoch = 60、Freeze_Epoch = 50、UnFreeze_Epoch = 100
        #                       会跳过冻结阶段，直接从60代开始，并调整对应的学习率。
        #                       （断点续练时使用）
        #   Freeze_Epoch        模型冻结训练的Freeze_Epoch
        #                       (当Freeze_Train=False时失效)
        #   Freeze_batch_size   模型冻结训练的batch_size
        #                       (当Freeze_Train=False时失效)
        #------------------------------------------------------------------#
        Init_Epoch = 0
        Freeze_Epoch = epoch
        Freeze_batch_size = batch_size
        #------------------------------------------------------------------#
        #   解冻阶段训练参数
        #   此时模型的主干不被冻结了，特征提取网络会发生改变
        #   占用的显存较大，网络所有的参数都会发生改变
        #   UnFreeze_Epoch          模型总共训练的epoch
        #                           SGD需要更长的时间收敛，因此设置较大的UnFreeze_Epoch
        #                           Adam可以使用相对较小的UnFreeze_Epoch
        #   Unfreeze_batch_size     模型在解冻后的batch_size
        #------------------------------------------------------------------#
        UnFreeze_Epoch = epoch
        Unfreeze_batch_size = batch_size
        #------------------------------------------------------------------#
        #   Freeze_Train    是否进行冻结训练
        #                   默认先冻结主干训练后解冻训练。
        #------------------------------------------------------------------#
        Freeze_Train = freeze_train

        #------------------------------------------------------------------#
        #   其它训练参数：学习率、优化器、学习率下降有关
        #------------------------------------------------------------------#
        #------------------------------------------------------------------#
        #   Init_lr         模型的最大学习率
        #   Min_lr          模型的最小学习率，默认为最大学习率的0.01
        #------------------------------------------------------------------#
        Init_lr = 1e-2
        Min_lr = Init_lr * 0.01
        #------------------------------------------------------------------#
        #   optimizer_type  使用到的优化器种类，可选的有adam、sgd
        #                   当使用Adam优化器时建议设置  Init_lr=1e-3
        #                   当使用SGD优化器时建议设置   Init_lr=1e-2
        #   momentum        优化器内部使用到的momentum参数
        #   weight_decay    权值衰减，可防止过拟合
        #                   adam会导致weight_decay错误，使用adam时建议设置为0。
        #------------------------------------------------------------------#
        optimizer_type = optimizer_type
        momentum = 0.937
        weight_decay = 5e-4
        #------------------------------------------------------------------#
        #   lr_decay_type   使用到的学习率下降方式，可选的有step、cos
        #------------------------------------------------------------------#
        lr_decay_type = "cos"

        train_annotation_path = '2007_train.txt'
        val_annotation_path = '2007_val.txt'

        #------------------------------------------------------#
        #   设置用到的显卡
        #------------------------------------------------------#
        ngpus_per_node = torch.cuda.device_count()
        if distributed:
            dist.init_process_group(backend="nccl")
            local_rank = int(os.environ["LOCAL_RANK"])
            rank = int(os.environ["RANK"])
            device = torch.device("cuda", local_rank)
            if local_rank == 0:
                print(
                    f"[{os.getpid()}] (rank = {rank}, local_rank = {local_rank}) training...")
                print("Gpu Device Count : ", ngpus_per_node)
        else:
            device = torch.device(
                'cuda' if torch.cuda.is_available() else 'cpu')
            local_rank = 0
            rank = 0

        #------------------------------------------------------#
        #   获取classes和anchor
        #------------------------------------------------------#
        class_names, num_classes = get_classes(self.classes_path)
        anchors, num_anchors = np.array(self.anchors), len(self.anchors)

        #----------------------------------------------------#
        #   下载预训练权重
        #----------------------------------------------------#
        if pretrained:
            if distributed:
                if local_rank == 0:
                    download_weights(self.phi)
                dist.barrier()
            else:
                download_weights(self.phi)

        #------------------------------------------------------#
        #   创建yolo模型
        #------------------------------------------------------#
        model = YoloBody(anchors_mask, num_classes,
                         self.phi, pretrained=pretrained)
        if not pretrained:
            weights_init(model)
        if model_path != '':
            #------------------------------------------------------#
            #   权值文件请看README，百度网盘下载
            #------------------------------------------------------#
            if local_rank == 0:
                print('Load weights {}.'.format(model_path))

            #------------------------------------------------------#
            #   根据预训练权重的Key和模型的Key进行加载
            #------------------------------------------------------#
            model_dict = model.state_dict()
            pretrained_dict = torch.load(model_path, map_location=device)
            load_key, no_load_key, temp_dict = [], [], {}
            for k, v in pretrained_dict.items():
                if k in model_dict.keys() and np.shape(model_dict[k]) == np.shape(v):
                    temp_dict[k] = v
                    load_key.append(k)
                else:
                    no_load_key.append(k)
            model_dict.update(temp_dict)
            model.load_state_dict(model_dict)
            #------------------------------------------------------#
            #   显示没有匹配上的Key
            #------------------------------------------------------#
            if local_rank == 0:
                print("\nSuccessful Load Key:", str(load_key)[
                      :500], "……\nSuccessful Load Key Num:", len(load_key))
                print("\nFail To Load Key:", str(no_load_key)[
                      :500], "……\nFail To Load Key num:", len(no_load_key))
                print(
                    "\n\033[1;33;44m温馨提示，head部分没有载入是正常现象，Backbone部分没有载入是错误的。As a reminder, if the head part of the model is not loaded, thats normal given that you probably using a pretrained model that was trained on a dataset with different number of classes. But if the backbone (or some part of it) of your model is not loaded, thats an error and you should make sure you are usinmg the right pretrained model and the right parameter phi (which can either be 'tiny' for tiny yolov7, 'l' for large yolov7, and 'x' for extra large yolov7).\033[0m")

        #----------------------#
        #   获得损失函数
        #----------------------#
        yolo_loss = YOLOLoss(anchors, num_classes,
                             self.input_shape, anchors_mask, label_smoothing)
        #----------------------#
        #   记录Loss
        #----------------------#
        if local_rank == 0:
            time_str = datetime.datetime.strftime(
                datetime.datetime.now(), '%Y_%m_%d_%H_%M_%S')
            log_dir = os.path.join(save_dir, "loss_" + str(time_str))
            loss_history = LossHistory(
                log_dir, model, input_shape=self.input_shape)
        else:
            loss_history = None

        #------------------------------------------------------------------#
        #   torch 1.2不支持amp，建议使用torch 1.7.1及以上正确使用fp16
        #   因此torch1.2这里显示"could not be resolve"
        #------------------------------------------------------------------#
        if fp16:
            from torch.cuda.amp import GradScaler as GradScaler
            scaler = GradScaler()
        else:
            scaler = None

        model_train = model.train()
        #----------------------------#
        #   多卡同步Bn
        #----------------------------#
        if sync_bn and ngpus_per_node > 1 and distributed:
            model_train = torch.nn.SyncBatchNorm.convert_sync_batchnorm(
                model_train)
        elif sync_bn:
            print("Sync_bn is not support in one gpu or not distributed.")

        if cuda:
            if distributed:
                #----------------------------#
                #   多卡平行运行
                #----------------------------#
                model_train = model_train.cuda(local_rank)
                model_train = torch.nn.parallel.DistributedDataParallel(
                    model_train, device_ids=[local_rank], find_unused_parameters=True)
            else:
                model_train = torch.nn.DataParallel(model)
                cudnn.benchmark = True
                model_train = model_train.cuda()

        #----------------------------#
        #   权值平滑
        #----------------------------#
        ema = ModelEMA(model_train)

        #---------------------------#
        #   读取数据集对应的txt
        #---------------------------#
        with open(train_annotation_path, encoding='utf-8') as f:
            train_lines = f.readlines()
        with open(val_annotation_path, encoding='utf-8') as f:
            val_lines = f.readlines()
        num_train = len(train_lines)
        num_val = len(val_lines)

        if local_rank == 0:
            show_config(
                classes_path=self.classes_path, anchors=self.anchors, anchors_mask=anchors_mask, model_path=model_path, input_shape=self.input_shape,
                Init_Epoch=Init_Epoch, Freeze_Epoch=Freeze_Epoch, UnFreeze_Epoch=UnFreeze_Epoch, Freeze_batch_size=Freeze_batch_size, Unfreeze_batch_size=Unfreeze_batch_size, Freeze_Train=Freeze_Train,
                Init_lr=Init_lr, Min_lr=Min_lr, optimizer_type=optimizer_type, momentum=momentum, lr_decay_type=lr_decay_type,
                save_period=save_period, save_dir=save_dir, num_workers=num_workers, num_train=num_train, num_val=num_val
            )
            #---------------------------------------------------------#
            #   总训练世代指的是遍历全部数据的总次数
            #   总训练步长指的是梯度下降的总次数
            #   每个训练世代包含若干训练步长，每个训练步长进行一次梯度下降。
            #   此处仅建议最低训练世代，上不封顶，计算时只考虑了解冻部分
            #----------------------------------------------------------#
            wanted_step = 5e4 if optimizer_type == "sgd" else 1.5e4
            total_step = num_train // Unfreeze_batch_size * UnFreeze_Epoch
            if total_step <= wanted_step:
                if num_train // Unfreeze_batch_size == 0:
                    raise ValueError('数据集过小，无法进行训练，请扩充数据集.\
                                      The size of your dataset is too small \
                                      to proceed with the training.')
                wanted_epoch = wanted_step // (num_train //
                                               Unfreeze_batch_size) + 1
                # print("\n\033[1;33;44m[Warning] 使用%s优化器时，建议将训练总步长设置到%d以上。\033[0m" % (
                #     optimizer_type, wanted_step))
                # print("\033[1;33;44m[Warning] 本次运行的总训练数据量为%d，Unfreeze_batch_size为%d，共训练%d个Epoch，计算出总训练步长为%d。\033[0m" % (
                #     num_train, Unfreeze_batch_size, UnFreeze_Epoch, total_step))
                # print("\033[1;33;44m[Warning] 由于总训练步长为%d，小于建议总步长%d，建议设置总世代为%d。\033[0m" % (
                #     total_step, wanted_step, wanted_epoch))

        #------------------------------------------------------#
        #   主干特征提取网络特征通用，冻结训练可以加快训练速度
        #   也可以在训练初期防止权值被破坏。
        #   Init_Epoch为起始世代
        #   Freeze_Epoch为冻结训练的世代
        #   UnFreeze_Epoch总训练世代
        #   提示OOM或者显存不足请调小Batch_size
        #------------------------------------------------------#
        if True:
            UnFreeze_flag = False
            #------------------------------------#
            #   冻结一定部分训练
            #------------------------------------#
            if Freeze_Train:
                for param in model.backbone.parameters():
                    param.requires_grad = False

            #-------------------------------------------------------------------#
            #   如果不冻结训练的话，直接设置batch_size为Unfreeze_batch_size
            #-------------------------------------------------------------------#
            batch_size = Freeze_batch_size if Freeze_Train else Unfreeze_batch_size

            #-------------------------------------------------------------------#
            #   判断当前batch_size，自适应调整学习率
            #-------------------------------------------------------------------#
            nbs = 64
            lr_limit_max = 1e-3 if optimizer_type == 'adam' else 5e-2
            lr_limit_min = 3e-4 if optimizer_type == 'adam' else 5e-4
            Init_lr_fit = min(max(batch_size / nbs * Init_lr,
                              lr_limit_min), lr_limit_max)
            Min_lr_fit = min(max(batch_size / nbs * Min_lr,
                             lr_limit_min * 1e-2), lr_limit_max * 1e-2)

            #---------------------------------------#
            #   根据optimizer_type选择优化器
            #---------------------------------------#
            pg0, pg1, pg2 = [], [], []
            for k, v in model.named_modules():
                if hasattr(v, "bias") and isinstance(v.bias, nn.Parameter):
                    pg2.append(v.bias)
                if isinstance(v, nn.BatchNorm2d) or "bn" in k:
                    pg0.append(v.weight)
                elif hasattr(v, "weight") and isinstance(v.weight, nn.Parameter):
                    pg1.append(v.weight)
            optimizer = {
                'adam': optim.Adam(pg0, Init_lr_fit, betas=(momentum, 0.999)),
                'sgd': optim.SGD(pg0, Init_lr_fit, momentum=momentum, nesterov=True)
            }[optimizer_type]
            optimizer.add_param_group(
                {"params": pg1, "weight_decay": weight_decay})
            optimizer.add_param_group({"params": pg2})

            #---------------------------------------#
            #   获得学习率下降的公式
            #---------------------------------------#
            lr_scheduler_func = get_lr_scheduler(
                lr_decay_type, Init_lr_fit, Min_lr_fit, UnFreeze_Epoch)

            #---------------------------------------#
            #   判断每一个世代的长度
            #---------------------------------------#
            epoch_step = num_train // batch_size
            epoch_step_val = num_val // batch_size

            if epoch_step == 0 or epoch_step_val == 0:
                raise ValueError("数据集过小，无法继续进行训练，请扩充数据集。\
                                  The size of your dataset is too small \
                                  to proceed with the training.")

            if ema:
                ema.updates = epoch_step * Init_Epoch

            #---------------------------------------#
            #   构建数据集加载器。
            #---------------------------------------#
            train_dataset = YoloDataset(train_lines, self.input_shape, num_classes, anchors, anchors_mask, epoch_length=UnFreeze_Epoch,
                                        mosaic=mosaic, mixup=mixup, mosaic_prob=mosaic_prob, mixup_prob=mixup_prob, train=True, special_aug_ratio=special_aug_ratio)
            val_dataset = YoloDataset(val_lines, self.input_shape, num_classes, anchors, anchors_mask, epoch_length=UnFreeze_Epoch,
                                      mosaic=False, mixup=False, mosaic_prob=0, mixup_prob=0, train=False, special_aug_ratio=0)

            if distributed:
                train_sampler = torch.utils.data.distributed.DistributedSampler(
                    train_dataset, shuffle=True,)
                val_sampler = torch.utils.data.distributed.DistributedSampler(
                    val_dataset, shuffle=False,)
                batch_size = batch_size // ngpus_per_node
                shuffle = False
            else:
                train_sampler = None
                val_sampler = None
                shuffle = True

            gen = DataLoader(train_dataset, shuffle=shuffle, batch_size=batch_size, num_workers=num_workers, pin_memory=True,
                             drop_last=True, collate_fn=yolo_dataset_collate, sampler=train_sampler)
            gen_val = DataLoader(val_dataset, shuffle=shuffle, batch_size=batch_size, num_workers=num_workers, pin_memory=True,
                                 drop_last=True, collate_fn=yolo_dataset_collate, sampler=val_sampler)

            #----------------------#
            #   记录eval的map曲线
            #----------------------#
            if local_rank == 0:
                eval_callback = EvalCallback(model, self.input_shape, anchors, anchors_mask, class_names, num_classes, val_lines, log_dir, cuda,
                                             eval_flag=eval_flag, period=eval_period)
            else:
                eval_callback = None

            #---------------------------------------#
            #   开始模型训练
            #---------------------------------------#
            for epoch in range(Init_Epoch, UnFreeze_Epoch):
                #---------------------------------------#
                #   如果模型有冻结学习部分
                #   则解冻，并设置参数
                #---------------------------------------#
                if epoch >= Freeze_Epoch and not UnFreeze_flag and Freeze_Train:
                    batch_size = Unfreeze_batch_size

                    #-------------------------------------------------------------------#
                    #   判断当前batch_size，自适应调整学习率
                    #-------------------------------------------------------------------#
                    nbs = 64
                    lr_limit_max = 1e-3 if optimizer_type == 'adam' else 5e-2
                    lr_limit_min = 3e-4 if optimizer_type == 'adam' else 5e-4
                    Init_lr_fit = min(
                        max(batch_size / nbs * Init_lr, lr_limit_min), lr_limit_max)
                    Min_lr_fit = min(
                        max(batch_size / nbs * Min_lr, lr_limit_min * 1e-2), lr_limit_max * 1e-2)
                    #---------------------------------------#
                    #   获得学习率下降的公式
                    #---------------------------------------#
                    lr_scheduler_func = get_lr_scheduler(
                        lr_decay_type, Init_lr_fit, Min_lr_fit, UnFreeze_Epoch)

                    for param in model.backbone.parameters():
                        param.requires_grad = True

                    epoch_step = num_train // batch_size
                    epoch_step_val = num_val // batch_size

                    if epoch_step == 0 or epoch_step_val == 0:
                        raise ValueError("数据集过小，无法继续进行训练，请扩充数据集。\
                                      The size of your dataset is too small \
                                      to proceed with the training.")

                    if ema:
                        ema.updates = epoch_step * epoch

                    if distributed:
                        batch_size = batch_size // ngpus_per_node

                    gen = DataLoader(train_dataset, shuffle=shuffle, batch_size=batch_size, num_workers=num_workers, pin_memory=True,
                                     drop_last=True, collate_fn=yolo_dataset_collate, sampler=train_sampler)
                    gen_val = DataLoader(val_dataset, shuffle=shuffle, batch_size=batch_size, num_workers=num_workers, pin_memory=True,
                                         drop_last=True, collate_fn=yolo_dataset_collate, sampler=val_sampler)

                    UnFreeze_flag = True

                gen.dataset.epoch_now = epoch
                gen_val.dataset.epoch_now = epoch

                if distributed:
                    train_sampler.set_epoch(epoch)

                set_optimizer_lr(optimizer, lr_scheduler_func, epoch)

                fit_one_epoch(model_train, model, ema, yolo_loss, loss_history, eval_callback, optimizer, epoch, epoch_step,
                              epoch_step_val, gen, gen_val, UnFreeze_Epoch, cuda, fp16, scaler, save_period, save_dir, local_rank)

                if distributed:
                    dist.barrier()

    def predict(self, cuda: bool = True, model_path: str = "", mode: str = "predict",
                imagefile_path: str = "",
                from_webcam: bool = False, webcam_num: int = 0, video_path: str = "",
                video_save_path: str = ".", video_fps: float = 25.0, dir_origin_path: str = "",
                dir_save_path: str = ".", save_heatmap_output_as: str = "heatmap_out", crop: bool = False,
                count: bool = False,  test_interval: int = 100,
                simplify: bool = True, onnx_save_path: str = "./model.onnx", confidence: float = 0.5,
                nms_iou: float = 0.3, letterbox_image: bool = True):

        
        """ #----------------------------------------------------------------------------------------------------------#
            #   mode用于指定测试的模式：
            #   'predict'           表示单张图片预测，如果想对预测过程进行修改，如保存图片，截取对象等，可以先看下方详细的注释
            #   'video'             表示视频检测，可调用摄像头或者视频进行检测，详情查看下方注释。
            #   'fps'               表示测试fps，使用的图片是img里面的street.jpg，详情查看下方注释。
            #   'dir_predict'       表示遍历文件夹进行检测并保存。默认遍历img文件夹，保存img_out文件夹，详情查看下方注释。
            #   'heatmap'           表示进行预测结果的热力图可视化，详情查看下方注释。
            #   'export_onnx'       表示将模型导出为onnx，需要pytorch1.7.1以上。
            #----------------------------------------------------------------------------------------------------------#
            #-------------------------------------------------------------------------#
            #   crop                指定了是否在单张图片预测后对目标进行截取
            #   count               指定了是否进行目标的计数
            #   crop、count仅在mode='predict'时有效
            #-------------------------------------------------------------------------#
    
            #----------------------------------------------------------------------------------------------------------#
            #   video_path          用于指定视频的路径，当video_path=0时表示检测摄像头
            #                       想要检测视频，则设置如video_path = "xxx.mp4"即可，代表读取出根目录下的xxx.mp4文件。
            #   video_save_path     表示视频保存的路径，当video_save_path=""时表示不保存
            #                       想要保存视频，则设置如video_save_path = "yyy.mp4"即可，代表保存为根目录下的yyy.mp4文件。
            #   video_fps           用于保存的视频的fps
            #
            #   video_path、video_save_path和video_fps仅在mode='video'时有效
            #   保存视频时需要ctrl+c退出或者运行到最后一帧才会完成完整的保存步骤。
            #----------------------------------------------------------------------------------------------------------#
            
            #----------------------------------------------------------------------------------------------------------#
            #   test_interval       用于指定测量fps的时候，图片检测的次数。理论上test_interval越大，fps越准确。
            #   fps_image_path      用于指定测试的fps图片
            #   
            #   test_interval和fps_image_path仅在mode='fps'有效
            #----------------------------------------------------------------------------------------------------------#
            
            #-------------------------------------------------------------------------#
            #   dir_origin_path     指定了用于检测的图片的文件夹路径
            #   dir_save_path       指定了检测完图片的保存路径
            #   
            #   dir_origin_path和dir_save_path仅在mode='dir_predict'时有效
            #-------------------------------------------------------------------------#
            
            #-------------------------------------------------------------------------#
            #   heatmap_save_path   热力图的保存路径，默认保存在model_data下
            #   
            #   heatmap_save_path仅在mode='heatmap'有效
            #-------------------------------------------------------------------------#
            #-------------------------------------------------------------------------#
            #   simplify            使用Simplify onnx
            #   onnx_save_path      指定了onnx的保存路径
            #-------------------------------------------------------------------------#
        """
        
        
        yolo = YOLO(model_path=model_path, classes_path=self.classes_path, anchors=self.anchors,
                        anchors_mask=self.anchors_mask, input_shape=self.input_shape, phi=self.phi,
                        confidence=confidence, nms_iou=nms_iou, fonts=self.fonts, cuda=cuda)

        if mode == "predict":
            '''
            1、如果想要进行检测完的图片的保存，利用r_image.save("img.jpg")即可保存，直接在predict.py里进行修改即可。 
            2、如果想要获得预测框的坐标，可以进入yolo.detect_image函数，在绘图部分读取top，left，bottom，right这四个值。
            3、如果想要利用预测框截取下目标，可以进入yolo.detect_image函数，在绘图部分利用获取到的top，left，bottom，right这四个值
            在原图上利用矩阵的方式进行截取。
            4、如果想要在预测图上写额外的字，比如检测到的特定目标的数量，可以进入yolo.detect_image函数，在绘图部分对predicted_class进行判断，
            比如判断if predicted_class == 'car': 即可判断当前目标是否为车，然后记录数量即可。利用draw.text即可写字。
            '''
            # while True:
            # img = input('Input image filename:')
            try:
                image = Image.open(imagefile_path)
            except:
                print('Error Loading the image file! Check your path or make sure your image is not corrupted!')
                return
            else:
                r_image, detection_result = yolo.detect_image(
                    image, crop=crop, count=count)
                r_image.show()

                return detection_result

        elif mode == "video":
            if from_webcam:
                capture = cv2.VideoCapture(webcam_num)
            else:
                capture = cv2.VideoCapture(video_path)

            if video_save_path != "":
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)

            ref, frame = capture.read()
            if not ref:
                raise ValueError("未能正确读取摄像头（视频），请注意是否正确安装摄像头（是否正确填写视频路径）。\
                    Failed to read the camera (video) correctly, \
                        check your video path or camera.")

            fps = 0.0
            while (True):
                t1 = time.time()
                # 读取某一帧
                ref, frame = capture.read()
                if not ref:
                    break
                # 格式转变，BGRtoRGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # 转变成Image
                frame = Image.fromarray(np.uint8(frame))
                # 进行检测
                frame, detection_result = yolo.detect_image(frame)
                frame = np.array(frame)
                # RGBtoBGR满足opencv显示格式
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                fps = (fps + (1./(time.time()-t1))) / 2
                print("fps= %.2f" % (fps))
                frame = cv2.putText(frame, "fps= %.2f" % (
                    fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.imshow("video", frame)
                c = cv2.waitKey(1) & 0xff
                if video_save_path != "":
                    out.write(frame)

                if c == 27:
                    capture.release()
                    break

            print("Video Detection Done!")
            capture.release()
            if video_save_path != "":
                print("Save processed video to the path :" + video_save_path)
                out.release()
            cv2.destroyAllWindows()

        elif mode == "fps":
            img = Image.open(imagefile_path)
            tact_time = yolo.get_FPS(img, test_interval)
            print(str(tact_time) + ' seconds, ' +
                  str(1/tact_time) + 'FPS, @batch_size 1')

        elif mode == "dir_predict":
            import os

            from tqdm import tqdm

            img_names = os.listdir(dir_origin_path)
            for img_name in tqdm(img_names):
                if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                    image_path = os.path.join(dir_origin_path, img_name)
                    image = Image.open(image_path)
                    r_image, detection_result = yolo.detect_image(image)
                    if not os.path.exists(dir_save_path):
                        os.makedirs(dir_save_path)
                    r_image.save(os.path.join(dir_save_path, img_name.replace(
                        ".jpg", ".png")), quality=95, subsampling=0)

        elif mode == "heatmap":
            try:
                image = Image.open(imagefile_path)
            except:
                print('Error Loading the image file! Check your path or make sure your image is not corrupted!')
                return
            else:
                yolo.detect_heatmap(image, save_heatmap_output_as)

        elif mode == "export_onnx":
            yolo.convert_to_onnx(simplify, onnx_save_path)

        else:
            raise AssertionError(
                "Please specify the correct mode: 'predict', 'video', 'fps', 'heatmap', 'export_onnx', 'dir_predict'.")

    def compute_map(self, model_path: str = '', cuda: bool = True, map_mode: int = 0, min_overlap: float = 0.5, confidence: float = 0.001,
                    nms_iou: float = 0.3, score_threhold: float = 0.5, map_vis: bool = False,
                    map_out_path: str = "map_out") -> None:
        '''
        Recall和Precision不像AP是一个面积的概念，因此在门限值（Confidence）不同时，网络的Recall和Precision值是不同的。
        默认情况下，本代码计算的Recall和Precision代表的是当门限值（Confidence）为0.5时，所对应的Recall和Precision值。

        受到mAP计算原理的限制，网络在计算mAP时需要获得近乎所有的预测框，这样才可以计算不同门限条件下的Recall和Precision值
        因此，本代码获得的map_out/detection-results/里面的txt的框的数量一般会比直接predict多一些，目的是列出所有可能的预测框，
        '''

        image_ids = open(os.path.join(
            self.VOCdevkit_path, "VOC2007/ImageSets/Main/test.txt")).read().strip().split()

        if not os.path.exists(map_out_path):
            os.makedirs(map_out_path)
        if not os.path.exists(os.path.join(map_out_path, 'ground-truth')):
            os.makedirs(os.path.join(map_out_path, 'ground-truth'))
        if not os.path.exists(os.path.join(map_out_path, 'detection-results')):
            os.makedirs(os.path.join(map_out_path, 'detection-results'))
        if not os.path.exists(os.path.join(map_out_path, 'images-optional')):
            os.makedirs(os.path.join(map_out_path, 'images-optional'))

        class_names, _ = get_classes(self.classes_path)

        if map_mode == 0 or map_mode == 1:
            print("Load model.")
            yolo = YOLO(model_path=model_path, classes_path=self.classes_path, anchors=self.anchors,
                        anchors_mask=self.anchors_mask, input_shape=self.input_shape, phi=self.phi,
                        confidence=confidence, nms_iou=nms_iou, cuda=cuda)
            print("Load model done.")

            print("Get predict result.")
            for image_id in tqdm(image_ids):
                image_path = os.path.join(
                    self.VOCdevkit_path, "VOC2007/JPEGImages/"+image_id+".jpg")
                image = Image.open(image_path)
                if map_vis:
                    image.save(os.path.join(
                        map_out_path, "images-optional/" + image_id + ".jpg"))
                yolo.get_map_txt(image_id, image, class_names, map_out_path)
            print("Get predict result done.")

        if map_mode == 0 or map_mode == 2:
            print("Get ground truth result.")
            for image_id in tqdm(image_ids):
                with open(os.path.join(map_out_path, "ground-truth/"+image_id+".txt"), "w") as new_f:
                    root = ET.parse(os.path.join(
                        self.VOCdevkit_path, "VOC2007/Annotations/"+image_id+".xml")).getroot()
                    for obj in root.findall('object'):
                        difficult_flag = False
                        if obj.find('difficult') != None:
                            difficult = obj.find('difficult').text
                            if int(difficult) == 1:
                                difficult_flag = True
                        obj_name = obj.find('name').text
                        if obj_name not in class_names:
                            continue
                        bndbox = obj.find('bndbox')
                        left = bndbox.find('xmin').text
                        top = bndbox.find('ymin').text
                        right = bndbox.find('xmax').text
                        bottom = bndbox.find('ymax').text

                        if difficult_flag:
                            new_f.write("%s %s %s %s %s difficult\n" %
                                        (obj_name, left, top, right, bottom))
                        else:
                            new_f.write("%s %s %s %s %s\n" %
                                        (obj_name, left, top, right, bottom))
            print("Get ground truth result done.")

        if map_mode == 0 or map_mode == 3:
            print("Get map.")
            get_map(min_overlap, True,
                    score_threhold=score_threhold, path=map_out_path)
            print("Get map done.")

        if map_mode == 4:
            print("Get map.")
            get_coco_map(class_names=class_names, path=map_out_path)
            print("Get map done.")
        
    def summary(self) -> None:
        """该部分代码用于看网络结构 - Model Summary (Architecture, FLOPS, PARAMS)"""
        device  = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        m       = YoloBody(self.anchors_mask, self.num_classes, self.phi, False).to(device)
        for i in m.children():
            print(i)
            print('==============================')
        
        dummy_input     = torch.randn(1, 3, self.input_shape[0], self.input_shape[1]).to(device)
        flops, params   = profile(m.to(device), (dummy_input, ), verbose=False)
        #--------------------------------------------------------#
        #   flops * 2是因为profile没有将卷积作为两个operations
        #   有些论文将卷积算乘法、加法两个operations。此时乘2
        #   有些论文只考虑乘法的运算次数，忽略加法。此时不乘2
        #   本代码选择乘2，参考YOLOX。
        #--------------------------------------------------------#
        flops           = flops * 2
        flops, params   = clever_format([flops, params], "%.3f")
        print('Total GFLOPS: %s' % (flops))
        print('Total params: %s' % (params))



def main():
    yolo = Yolov7(classes_path=os.path.join(
        'yolovxx', 'yolov7pytorch', 'model_data', 'voc_classes.txt'))
    yolo.voc_annotation()
    yolo.train()


if __name__ == "__main__":
    main()
