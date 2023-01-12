import os
from typing import Union, Callable

import numpy as np
import torch
from loguru import logger
from tabulate import tabulate
from torch.utils.data import DataLoader
from torch.nn.parallel import DistributedDataParallel as DDP

from tepe.core import BaseTask
from tepe.utils.dist import get_world_size, get_rank, get_local_rank, synchronize
from tepe.utils.general import check_requirements


class RDConfig(BaseTask):
    def __init__(self):
        super(RDConfig, self).__init__()

        check_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'))
        self.task_name = 'rd'
        self.data_root = './mvtec/'
        self.is_mvtec = False
        self.scene = 'bsofa'
        self.feature_extractor = 'wres50'
        self.batch_size = 16
        self.workers = 4
        self.cache = False
        self.input_size = 256
        self.num_slice = []
        self.keep_ratio = False
        
        # train----------------------------------------------------        
        self.max_epoch = 20
        self.basic_lr_per_img = 0.01 / 16
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.weight_decay = 0
        self.sched_type = 'cosine'
        self.warmup_epochs = 0
        self.min_lr = 1e-5  # 下降到的最小学习率
        self.lr_noise = 0.6  # 从0.6*max_epoch时开始添加lr噪声
        self.lr_noise_pct = 0.2  # 噪声抖动大小
        self.is_distributed = get_world_size() > 1

        # predict--------------------------------------------------
        self.threshold = 0.4
        self.save_result = True
        self.save_xml = False
        self.show_heatmap = True

    def get_train_loader(self):
        from tepe.data.datasets import AnomalyDataset
        from tepe.utils.dist import wait_for_the_master, get_local_rank
        
        with wait_for_the_master(get_local_rank()):
            data_transform, target_transform = self.get_transform()
            self.train_data = AnomalyDataset(self.data_root, class_name=self.scene,
                                            transform=data_transform, target_transform=target_transform,
                                            resize=self.input_size, is_train=True, is_mvtec=False,
                                            cache_img=self.cache)

        train_dataloader = DataLoader(
            self.train_data, batch_size=self.batch_size, shuffle=True, num_workers=self.workers
        )

        return train_dataloader

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
                                   T.Normalize(mean=[0.485, 0.456, 0.406],
                                               std=[0.229, 0.224, 0.225])])
            transform_mask = T.Compose([T.Resize(self.input_size, Image.NEAREST),
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

    def get_model(self, train=True):
        from tepe.tasks.rd.model import Model

        model = Model(self.feature_extractor, self.input_size)
        if not train:
            ckpt = torch.load(self.weights, map_location=self.device)
            model.load_state_dict(ckpt['model'])
            model.eval().to(self.device)
            logger.info('Model load done.')

        return model

    def train(self):
        from torch.utils.tensorboard import SummaryWriter
        from tepe.utils.general import (
            init_seeds,
            save_task_config_py,
            setup_logger
        )
        from tepe.modules.scheduler import create_scheduler
        from tepe.tasks.rd.find_thr import find_hard_samples
        
        init_seeds(self.seed)
        
        # dist info
        rank = get_rank()
        local_rank = get_local_rank()
        device = "cuda:{}".format(self.local_rank)

        save_dir = self.output_dir + f'/{self.scene}'
        if rank == 0:
            os.makedirs(save_dir, exist_ok=True)

        # save args
        # save_task_attr_to_yaml(self, save_dir)
        save_task_config_py(self, save_dir)

        # save log text
        setup_logger(save_file=os.path.join(save_dir, 'train_log.txt'))  # logger
        if rank == 0:
            tblogger = SummaryWriter(save_dir)  # tensorboard

        torch.cuda.set_device(local_rank)
        model = self.get_model()  #.to(self.device).train()
        if self.is_distributed:
            model = DDP(model, device_ids=[local_rank], broadcast_buffers=False)
        model.train()
        model.encoder.eval()
        
        optimizer = torch.optim.Adam(
            list(model.decoder.parameters()) + list(model.bn.parameters()),
            lr=self.learning_rate, betas=(0.5,0.999), weight_decay=self.weight_decay
        )
        lr_scheduler, num_epoch = create_scheduler(self, self.sched_type, optimizer)

        self.train_dataloader = self.get_train_loader()

        logger.info('Training start...')
        for epoch in range(1, num_epoch + 1):
            loss_list = []
            for data in self.train_dataloader:
                img = data['img'].to(self.device)
                loss = model(img)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                loss_list.append(loss.item())
            
            # get current lr
            lrl = [param_group['lr'] for param_group in optimizer.param_groups]
            lr = sum(lrl) / len(lrl)
            if lr_scheduler is not None:
                lr_scheduler.step(epoch + 1)  # update lr
            
            # logger
            logger.info('epoch [{}/{}], loss:{:.4f}, lr:{:.5f}'.format(epoch, num_epoch, np.mean(loss_list), lr))
            if rank == 0:
                tblogger.add_scalar(tag=f'{self.scene}/loss', scalar_value=np.mean(loss_list), global_step=epoch)
                tblogger.add_scalar(tag=f'{self.scene}/lr', scalar_value=lr, global_step=epoch)
                
            # save model
            if epoch % 5 == 0 or epoch == num_epoch:
                synchronize()
                self.weights = os.path.join(save_dir, f'{self.feature_extractor}_rd_{self.scene}.pth')
                torch.save({'model': model.state_dict(),
                            'epoch': epoch}, self.weights)
                logger.info(f"model save in {self.weights}")

            # hard sample mining
            if epoch > num_epoch - 30 and epoch % 5 == 0 and epoch != num_epoch:
                select_paths = find_hard_samples(model, self.train_dataloader,
                                                 self.device, mining_thr=self.threshold * 0.75)
                model.train()
                model.encoder.eval()
                if len(select_paths):
                    dataset = self.train_dataloader.dataset
                    dataset.add_hard_samples(select_paths)
                    # update train dataloader
                    self.train_dataloader = DataLoader(
                        self.train_data, batch_size=self.batch_size,
                        shuffle=True, num_workers=self.workers
                    )

        # from tepe.tasks.rd.find_thr import find
        # self.threshold = find(model, self.train_dataloader, thr_dataloader, self.device)
        # logger.info(f"find a appropriate threshold: {self.threshold}")

        self.set_post_info(scene=self.scene, thr=self.threshold)

    def eval(self):
        from tepe.data.infer_datasets import LoadImages1
        from .evalutor import read_xml, cal_true_positive

        predictor = self.get_predictor()
        eval_data_root = os.path.join(self.data_root, self.scene, 'test')

        all_precision = {}
        all_recall = {}

        for bad_name in os.listdir(eval_data_root):
            dataset = LoadImages1(os.path.join(eval_data_root, bad_name))
            gt_dir = os.path.join(self.data_root, self.scene, 'ground_truth', bad_name)

            total_pred, total_gt, total_rtp, total_ptp = 0, 0, 0, 0
            for idx, data in enumerate(dataset):
                img_path = data['path']
                # get prediction
                results = predictor.run(data)
                pred = torch.Tensor(results['anomaly_area'])

                # get ground-truth
                img_name = os.path.basename(data['path'])
                xml_path = os.path.join(
                    gt_dir, img_name.replace(img_name.rsplit('.', maxsplit=1)[-1], 'xml')
                )
                if not os.path.exists(xml_path):
                    logger.warning(f'not found {xml_path}')
                    continue
                gt = read_xml(xml_path)

                p_tp, r_tp = cal_true_positive(gt, pred)

                total_pred += len(pred)
                total_gt += len(gt)
                total_rtp += r_tp
                total_ptp += p_tp
                logger.info(f'[{idx + 1}/{len(dataset)}] {img_path} tp={r_tp}')

            all_precision[bad_name] = total_ptp / total_pred if total_pred > 0 else 1
            all_recall[bad_name] = total_rtp / total_gt if total_gt > 0 else 1

            logger.info(f'{bad_name} precision: {all_precision[bad_name]}, '
                        f'recall: {all_recall[bad_name]}')

        # show eval results
        all_precision['mean'] = sum(list(all_precision.values())) / len(all_precision)
        all_recall['mean'] = sum(list(all_recall.values())) / len(all_recall)
        bad_name = list(all_recall.keys())
        table_header = [" "] + bad_name
        each_p = ["precision"] + [all_precision[k] for k in bad_name]
        each_r = ["recall"] + [all_recall[k] for k in bad_name]
        result_table = [
            each_p,
            each_r
        ]
        logger.info('eval result:\n{}'.format(
            tabulate(result_table, headers=table_header, tablefmt="fancy_grid")
        ))

        return dict(p=all_precision, r=all_recall)

    def get_predictor(self) -> Union[None, Callable]:
        from tepe.tasks.rd.predictor import Predictor

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
            onnx_inf=onnx_inf,
            save_result=self.save_result,
            save_xml=self.save_xml,
            show_heatmap=self.show_heatmap
        )

        return predictor