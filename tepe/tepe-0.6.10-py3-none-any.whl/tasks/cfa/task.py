import os
import yaml
import numpy as np
import torch
from loguru import logger
from torch import nn
from torch.optim import AdamW

from tepe.core import BaseTask, register_config
from tepe.utils.general import check_requirements


@register_config()
class CFAConfig(BaseTask):
    def __init__(self):
        super(CFAConfig, self).__init__()

        check_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'))
        self.input_size = 224  # [h, w]
        self.keep_ratio = True
        self.max_epoch = 30
        self.batch_size = 8
        self.workers = 4

        self.data_root = ''
        self.scene = ''
        self.is_mvtec = False

        self.encoder_name = 'wrn50_2'  # ['res18', 'wrn50_2']
        self.ae_cfg = dict(
            use_ae=False,
            weights=''
        )

        self.gamma_c = 1
        self.gamma_d = 1

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.threshold = 0.5
        self.autobatch = True

    def get_model(self, train=True):
        if not train:
            model = torch.load(self.weights)
            model.eval()
            return model

        from tepe.tasks.cfa.build_encoder import build_feature_extractor
        from tepe.tasks.cfa.module import DSVDD

        feature_extractor = build_feature_extractor(self.encoder_name, self.ae_cfg)
        feature_extractor = feature_extractor.to(self.device)
        feature_extractor.eval()

        loss_fn = DSVDD(self.encoder_name,
                        self.gamma_c, self.gamma_d,
                        self.device,
                        feature_act=True)
        loss_fn = loss_fn.to(self.device)
        loss_fn.train()

        return feature_extractor, loss_fn

    def get_train_loader(self):
        from torch.utils.data import DataLoader
        from tepe.data.datasets import AnomalyDataset

        transform, transform_mask = self.get_transform()
        dataset = AnomalyDataset(dataset_path=self.data_root,
                                 class_name=self.scene,
                                 transform=transform,
                                 target_transform=transform_mask,
                                 resize=self.input_size,
                                 is_train=True,
                                 is_mvtec=self.is_mvtec)

        train_loader = DataLoader(
            dataset, self.batch_size, shuffle=True, pin_memory=True,
            num_workers=self.workers, drop_last=True
        )

        return train_loader

    def get_transform(self, mode='train'):
        assert mode in ['train', 'val', 'test']
        from functools import partial
        from PIL import Image
        from torchvision import transforms as T
        from tepe.data import letterbox

        new_shape = [self.input_size, self.input_size] \
            if isinstance(self.input_size, int) else self.input_size
        resize_fn = partial(letterbox, new_shape=new_shape, pad_color=(114, 114, 114),
                            auto=False, stride=None, keep_ratio=self.keep_ratio,
                            scaleup=True, rgb=True, interpolation=3)

        if mode == 'train':
            transform = T.Compose([T.Lambda(lambda x: resize_fn(im=x)[0]),
                                   T.ToTensor(),
                                   T.RandomRotation(10),
                                   T.Normalize(mean=[0.485, 0.456, 0.406],
                                               std=[0.229, 0.224, 0.225])])
            transform_mask = T.Compose([T.Resize(self.input_size, Image.NEAREST),
                                        T.RandomRotation(10),
                                        T.ToTensor()]) if self.is_mvtec else None
            return transform, transform_mask
        elif mode == 'val':
            transform = T.Compose([T.Lambda(lambda x: resize_fn(im=x)[0]),
                                   T.ToTensor(),
                                   T.Normalize(mean=[0.485, 0.456, 0.406],
                                               std=[0.229, 0.224, 0.225])])

            transform_mask = T.Compose([T.Resize(self.input_size, Image.NEAREST),
                                        T.ToTensor()]) if self.is_mvtec else None
            return transform, transform_mask
        else:
            transform = T.Compose([T.ToTensor(),
                                   T.Normalize(mean=[0.485, 0.456, 0.406],
                                               std=[0.229, 0.224, 0.225])])

            return transform, resize_fn

    def train(self):
        from tepe.utils.general import (
            init_seeds,
            save_task_attr_to_yaml,
            save_task_config_py,
            setup_logger
        )

        init_seeds(seed=self.seed, auto_batch=self.autobatch)
        save_dir = self.output_dir + f'/{self.scene}'
        os.makedirs(save_dir, exist_ok=True)

        # save args
        save_task_attr_to_yaml(self, save_dir)
        save_task_config_py(self, save_dir)

        # save log text
        logger.add(os.path.join(save_dir, 'train_log.txt'))
        setup_logger(save_file=os.path.join(save_dir, 'train_log.txt'))  # logger

        # train ae
        if self.ae_cfg['use_ae']:
            from .auto_encoder import train as train_ae
            self.ae_cfg['weights'] = os.path.join(save_dir, self.ae_cfg['weights'])
            train_ae(self, encoder_name=self.encoder_name, wights_path=self.ae_cfg['weights'])

        logger.info('get cfa model')
        feature_extractor, loss_fn = self.get_model(train=True)

        # init centroid
        logger.info('init centroid')
        bz = self.batch_size
        self.batch_size = 2
        train_loader = self.get_train_loader()
        loss_fn.init_centroid(feature_extractor, train_loader)
        model = nn.Sequential(feature_extractor, loss_fn)
        self.batch_size = bz

        # find a batch-size according to CUDA memery
        if self.autobatch:
            from tepe.utils.autobatch import check_train_batch_size
            self.batch_size = check_train_batch_size(
                model, self.input_size, amp=False, fraction=0.9
            )
        logger.info(f'batch size: {self.batch_size}, num worker: {self.workers}')
        train_loader = self.get_train_loader()

        # optimizer
        for param in model[0].parameters():
            param.requires_grad = False
        params = [{'params': model[-1].parameters()}, ]
        optimizer = AdamW(params=params,
                          lr=1e-3,
                          weight_decay=5e-4,
                          amsgrad=True)

        # train loop
        logger.info(f'class: {self.scene}')
        self.weights = f'{save_dir}/{self.encoder_name}_cfa_{self.scene}.pth'

        for epoch in range(1, self.max_epoch + 1):
            loss_list = []
            for data in train_loader:
                x = data['img'].to(self.device)
                optimizer.zero_grad()
                loss, _ = model(x)

                loss.backward()
                optimizer.step()
                loss_list.append(loss.item())
            logger.info('epoch [{}/{}], loss:{:.4f}'.format(epoch, self.max_epoch, np.mean(loss_list)))
            # save model
            if epoch % 5 == 0 or epoch == self.max_epoch:
                torch.save(model, self.weights)
                logger.info(f"model save in {self.weights}")

        # set post http info
        self.set_post_info(model_path=self.weights)

    def get_predictor(self):
        from .predictor import Predictor

        onnx_inf = False
        if os.path.splitext(self.weights)[-1] == '.onnx':
            logger.info('use onnxruntime for inference')
            import onnxruntime as ort
            model = ort.InferenceSession(self.weights)
            onnx_inf = True
        else:
            model = self.get_model(train=False)

        transform, resize_fn = self.get_transform(mode='test')
        predictor = Predictor(
            model=model,
            resize_fn=resize_fn,
            input_size=self.input_size,
            transform=transform,
            threshold=self.threshold,
            save_path=self.output_dir,
            onnx_inf=onnx_inf
        )
        return predictor

    def export(self):
        self.model = self.get_model(train=False)
        self.model[-1].export = True
        super().export()
        delattr(self, 'model')