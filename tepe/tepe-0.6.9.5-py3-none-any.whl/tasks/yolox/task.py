#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) 2014-2021 Megvii Inc. All rights reserved.

import os
import random
import warnings

import torch
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.nn as nn
from loguru import logger

from tepe.core import BaseTask, register_config


@register_config('yolox')
class YOLOXConfig(BaseTask):
    def __init__(self):
        super().__init__()
        self.task_name = 'yolox'

        # ---------------- model config ---------------- #
        self.model_type = 'l'
        self.CLASS = ('01', '02', )
        self.num_classes = 80
        self.act = 'silu'

        # ---------------- dataloader config ---------------- #
        self.dataset_type = 'coco'  # or voc
        # set worker to 4 for shorter dataloader init time
        self.data_num_workers = 4
        self.input_size = (640, 640)  # (height, width)
        # Actual multiscale ranges: [640-5*32, 640+5*32].
        # To disable multiscale training, set the
        # self.multiscale_range to 0.
        self.multiscale_range = 5
        # You can uncomment this line to specify a multiscale range
        # self.random_size = (14, 26)
        self.data_root = None
        self.train_ann = "instances_train2017.json"
        self.val_ann = "instances_val2017.json"
        self.batch_size = 64
        self.cache = True

        # --------------- transform config ----------------- #
        self.no_aug = False
        self.mosaic_prob = 1.0
        self.mixup_prob = 1.0
        self.hsv_prob = 1.0
        self.flip_prob = 0.5
        self.degrees = 10.0
        self.translate = 0.1
        self.mosaic_scale = (0.1, 2)
        self.mixup_scale = (0.5, 1.5)
        self.shear = 2.0
        self.enable_mixup = True

        # --------------  training config --------------------- #
        self.device = 0
        self.is_distributed = False
        self.occupy = False  # occupy GPU memory first for training
        self.fp16 = False
        self.warmup_epochs = 5
        self.max_epoch = 300
        self.warmup_lr = 0
        self.basic_lr_per_img = 0.01 / 64.0
        self.scheduler = "yoloxwarmcos"
        self.no_aug_epochs = 15
        self.min_lr_ratio = 0.05
        self.ema = True

        self.weight_decay = 5e-4
        self.momentum = 0.9
        self.print_interval = 10
        self.eval_interval = 10
        self.exp_name = os.path.split(os.path.realpath(__file__))[1].split(".")[0]

        # -----------------  testing config ------------------ #
        self.test_size = (640, 640)
        self.test_conf = 0.01
        self.nmsthre = 0.65

    def get_model(self, train=True):
        from tepe.tasks.yolox.models import YOLOX, YOLOPAFPN, YOLOXHead
        model_dict = {
            'x': [1.33, 1.25],  # depth, width
            'l': [1.0, 1.0],
            'm': [0.67, 0.75],
            's': [0.33, 0.5],
            'tiny': [0.33, 0.375],  # self.input_size = 416
            'nano': [0.33, 0.25]  # self.input_size = 416
        }
        depth, width = model_dict[self.model_type]
        depthwise = True if self.model_type == 'nano' else False
        logger.info(f'model type: yolox-{self.model_type}, '
                    f'depth: {depth}, width: {width}, depthwise: {depthwise}')

        def init_yolo(M):
            for m in M.modules():
                if isinstance(m, nn.BatchNorm2d):
                    m.eps = 1e-3
                    m.momentum = 0.03

        if getattr(self, "model", None) is None:
            in_channels = [256, 512, 1024]
            backbone = YOLOPAFPN(depth, width, in_channels=in_channels, act=self.act, depthwise=depthwise)
            head = YOLOXHead(self.num_classes, width, in_channels=in_channels, act=self.act, depthwise=depthwise)
            self.model = YOLOX(backbone, head)

        self.model.apply(init_yolo)
        self.model.head.initialize_biases(1e-2)
        if not train:
            self.model.eval()
            self.load_ckpt(self.model, self.weights, -1, load_keys='model')
            self.model.to(self.device)

        # weight type
        if self.device != -1:
            self.model.cuda()
            if self.fp16:
                self.model.half()  # to FP16

        return self.model

    def get_train_loader(self):
        from tepe.tasks.yolox.data import (
            CustomVOC,
            COCODataset,
            TrainTransform,
            YoloBatchSampler,
            DataLoader,
            InfiniteSampler,
            MosaicDetection,
            worker_init_reset_seed,
        )
        from .utils import (
            wait_for_the_master,
            get_local_rank,
        )
        # from tepe.data.datasets.yolox_voc import YOLOXVOC

        local_rank = get_local_rank()

        if self.dataset_type == 'coco':
            with wait_for_the_master(local_rank):
                dataset = COCODataset(
                    data_dir=self.data_root,
                    json_file=self.train_ann,
                    img_size=self.input_size,
                    preproc=TrainTransform(
                        max_labels=50,
                        flip_prob=self.flip_prob,
                        hsv_prob=self.hsv_prob),
                    cache=self.cache,
                )
        else:
            with wait_for_the_master(local_rank):
                dataset = CustomVOC(
                    data_dir=self.data_root,
                    cls_name=self.CLASS,
                    image_sets=['train'],
                    img_size=self.input_size,
                    preproc=TrainTransform(
                        max_labels=50,
                        flip_prob=self.flip_prob,
                        hsv_prob=self.hsv_prob),
                    cache=self.cache,
                )

        mosaic_prob = self.mosaic_prob
        mosaic_scale = self.mosaic_scale
        enable_mixup = self.enable_mixup
        if self.model_type in ['tiny', 'nano']:
            if self.model_type == 'nano':
                mosaic_prob = 0.5
            mosaic_scale = (0.5, 1.5)
            enable_mixup = False
        dataset = MosaicDetection(
            dataset,
            mosaic=not self.no_aug,
            img_size=self.input_size,
            preproc=TrainTransform(
                max_labels=120,
                flip_prob=self.flip_prob,
                hsv_prob=self.hsv_prob),
            degrees=self.degrees,
            translate=self.translate,
            mosaic_scale=mosaic_scale,
            mixup_scale=self.mixup_scale,
            shear=self.shear,
            enable_mixup=enable_mixup,
            mosaic_prob=self.mosaic_prob,
            mixup_prob=self.mixup_prob,
        )

        self.dataset = dataset

        batch_size = self.batch_size
        if self.is_distributed:
            batch_size = self.batch_size // dist.get_world_size()

        sampler = InfiniteSampler(len(self.dataset), seed=self.seed if self.seed else 0)

        batch_sampler = YoloBatchSampler(
            sampler=sampler,
            batch_size=batch_size,
            drop_last=False,
            mosaic=not self.no_aug,
        )

        dataloader_kwargs = {"num_workers": self.data_num_workers, "pin_memory": True}
        dataloader_kwargs["batch_sampler"] = batch_sampler

        # Make sure each process has different random seed, especially for 'fork' method.
        # Check https://github.com/pytorch/pytorch/issues/63311 for more details.
        dataloader_kwargs["worker_init_fn"] = worker_init_reset_seed

        self.train_loader = DataLoader(self.dataset, **dataloader_kwargs)

        return self.train_loader

    def random_resize(self, data_loader, epoch, rank, is_distributed):
        tensor = torch.LongTensor(2).cuda()

        if rank == 0:
            size_factor = self.input_size[1] * 1.0 / self.input_size[0]
            if not hasattr(self, 'random_size'):
                min_size = int(self.input_size[0] / 32) - self.multiscale_range
                max_size = int(self.input_size[0] / 32) + self.multiscale_range
                self.random_size = (min_size, max_size)
            size = random.randint(*self.random_size)
            size = (int(32 * size), 32 * int(size * size_factor))
            tensor[0] = size[0]
            tensor[1] = size[1]

        if is_distributed:
            dist.barrier()
            dist.broadcast(tensor, 0)

        input_size = (tensor[0].item(), tensor[1].item())
        return input_size

    def preprocess(self, inputs, targets, tsize):
        scale_y = tsize[0] / self.input_size[0]
        scale_x = tsize[1] / self.input_size[1]
        if scale_x != 1 or scale_y != 1:
            inputs = nn.functional.interpolate(
                inputs, size=tsize, mode="bilinear", align_corners=False
            )
            targets[..., 1::2] = targets[..., 1::2] * scale_x
            targets[..., 2::2] = targets[..., 2::2] * scale_y
        return inputs, targets

    def get_optimizer(self):
        if "optimizer" not in self.__dict__:
            if self.warmup_epochs > 0:
                lr = self.warmup_lr
            else:
                lr = self.learning_rate

            pg0, pg1, pg2 = [], [], []  # optimizer parameter groups

            for k, v in self.model.named_modules():
                if hasattr(v, "bias") and isinstance(v.bias, nn.Parameter):
                    pg2.append(v.bias)  # biases
                if isinstance(v, nn.BatchNorm2d) or "bn" in k:
                    pg0.append(v.weight)  # no decay
                elif hasattr(v, "weight") and isinstance(v.weight, nn.Parameter):
                    pg1.append(v.weight)  # apply decay

            optimizer = torch.optim.SGD(
                pg0, lr=lr, momentum=self.momentum, nesterov=True
            )
            optimizer.add_param_group(
                {"params": pg1, "weight_decay": self.weight_decay}
            )  # add pg1 with weight_decay
            optimizer.add_param_group({"params": pg2})
            self.optimizer = optimizer

        return self.optimizer

    def get_lr_scheduler(self):
        from tepe.tasks.yolox.utils import LRScheduler

        scheduler = LRScheduler(
            self.scheduler,
            self.learning_rate,
            len(self.train_loader),
            self.max_epoch,
            warmup_epochs=self.warmup_epochs,
            warmup_lr_start=self.warmup_lr,
            no_aug_epochs=self.no_aug_epochs,
            min_lr_ratio=self.min_lr_ratio,
        )
        return scheduler

    def get_eval_loader(self):
        from tepe.tasks.yolox.data import COCODataset, CustomVOC, ValTransform

        if self.dataset_type == 'coco':
            testdev = False
            valdataset = COCODataset(
                data_dir=self.data_root,
                json_file=self.val_ann if not testdev else "image_info_test-dev2017.json",
                name="val2017" if not testdev else "test2017",
                img_size=self.input_size,
                preproc=ValTransform(legacy=False),
            )
        else:
            valdataset = CustomVOC(
                data_dir=self.data_root,
                cls_name=self.CLASS,
                image_sets=['val'],
                img_size=self.input_size,
                preproc=ValTransform()
            )

        batch_size = self.batch_size
        if self.is_distributed:
            batch_size = self.batch_size // dist.get_world_size()
            sampler = torch.utils.data.distributed.DistributedSampler(
                valdataset, shuffle=False
            )
        else:
            sampler = torch.utils.data.SequentialSampler(valdataset)

        dataloader_kwargs = {
            "num_workers": self.data_num_workers,
            "pin_memory": True,
            "sampler": sampler,
        }
        dataloader_kwargs["batch_size"] = batch_size
        val_loader = torch.utils.data.DataLoader(valdataset, **dataloader_kwargs)

        return val_loader

    def get_evaluator(self, train=False):
        from tepe.tasks.yolox.evaluators import COCOEvaluator, VOCEvaluator

        model = None if train else self.get_model(train=False)
        val_loader = self.get_eval_loader()
        if self.dataset_type == 'coco':
            testdev = False
            evaluator = COCOEvaluator(
                dataloader=val_loader,
                training=train,
                img_size=self.test_size,
                num_classes=self.num_classes,
                model=model,
                confthre=self.test_conf,
                nmsthre=self.nmsthre,
                distributed=self.is_distributed,
                half=self.fp16,
                testdev=testdev,
                save_dir=self.output_dir,
                save_result=True
            )
        else:
            evaluator = VOCEvaluator(
                dataloader=val_loader,
                training=train,
                img_size=self.test_size,
                model=model,
                conf_thr=self.test_conf,
                nms_thr=self.nmsthre,
                num_classes=self.num_classes,
                distributed=self.is_distributed,
                half=self.fp16,
                save_dir=self.output_dir,
                save_result=True
            )
        return evaluator

    def get_predictor(self):
        from tepe.tasks.yolox.data import ValTransform
        from tepe.tasks.yolox.yolox_detector import YOLOXPredictor

        model = self.get_model(train=False)
        predictor = YOLOXPredictor(
            input_size=self.input_size,
            classes=self.CLASS,
            model=model,
            preprocess=ValTransform(legacy=True),
            conf_thres=self.test_conf,
            iou_thres=self.nmsthre,
            device=self.device,
            save_dir=self.output_dir
        )
        return predictor

    def eval(self):
        evaluator = self.get_evaluator(train=False)
        return evaluator.evaluate()

    def train(self):
        from tepe.tasks.yolox.core.trainer import Trainer

        if self.seed is not None:
            random.seed(self.seed)
            torch.manual_seed(self.seed)
            cudnn.deterministic = True
            warnings.warn(
                "You have chosen to seed training. This will turn on the CUDNN deterministic setting, "
                "which can slow down your training considerably! You may see unexpected behavior "
                "when restarting from checkpoints."
            )
        cudnn.benchmark = True

        trainer = Trainer(self)
        trainer.train()

    def export(self):
        assert self.weights is not None, "model weight path is None"
        from tepe.core.exporter import Exporter

        self.batch_size = 1
        model = self.get_model(train=False)
        model.head.decode_in_inference = False
        exporter = Exporter(self, model=model)
        exporter.export()