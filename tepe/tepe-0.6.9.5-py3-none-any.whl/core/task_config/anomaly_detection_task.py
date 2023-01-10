import os
from loguru import logger
from tabulate import tabulate
import numpy as np
import torch

from tepe.core import BaseTask


class BaseADTask(BaseTask):
    def __init__(self):
        super(BaseADTask, self).__init__()
        self.task_name = 'rd'
        self.data_root = './mvtec/'
        self.is_mvtec = False
        self.scene = 'bsofa'
        self.feature_extractor = 'wres50'
        self.max_epoch = 20
        self.basic_lr_per_img = 0.005 / 16
        self.batch_size = 16
        self.workers = 4

        self.input_size = 256
        self.keep_ratio = False
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.threshold = 0.5

    def get_train_loader(self):
        from tepe.data.datasets import AnomalyDataset

        data_transform, target_transform = self.get_transform()

        train_data = AnomalyDataset(self.data_root, class_name=self.scene,
                                    transform=data_transform, target_transform=target_transform,
                                    resize=self.input_size, is_train=True, is_mvtec=False)

        thr_data = AnomalyDataset(self.data_root, class_name=self.scene,
                                  transform=data_transform, target_transform=target_transform,
                                  paste=True, is_train=True, is_mvtec=False)

        train_dataloader = torch.utils.data.DataLoader(
            train_data, batch_size=self.batch_size, shuffle=True, num_workers=self.workers
        )
        thr_dataloader = torch.utils.data.DataLoader(
            thr_data, batch_size=self.batch_size, shuffle=True, num_workers=self.workers
        )

        return train_dataloader, thr_dataloader

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

    def get_model(self, train=True):
        from tepe.tasks.rd.model import Model

        model = Model()
        if not train:
            ckpt = torch.load(self.weights, map_location=self.device)
            model.load_state_dict(ckpt['model'])
            model.eval().to(self.device)
            logger.info('Model load done.')

        return model

    def train(self):
        from tepe.utils.general import (
            init_seeds,
            save_task_attr_to_yaml,
            save_task_config_py,
            setup_logger
        )

        init_seeds(self.seed)

        model = self.get_model().to(self.device).train()
        model.encoder.eval()
        optimizer = torch.optim.Adam(
            list(model.decoder.parameters()) + list(model.bn.parameters()),
            lr=self.learning_rate, betas=(0.5,0.999)
        )

        train_dataloader, thr_dataloader = self.get_train_loader()

        save_dir = self.output_dir + f'/{self.scene}'
        os.makedirs(save_dir, exist_ok=True)

        # save args
        save_task_attr_to_yaml(self, save_dir)
        save_task_config_py(self, save_dir)

        # save log text
        logger.add(os.path.join(save_dir, 'train_log.txt'))
        setup_logger(save_file=os.path.join(save_dir, 'train_log.txt'))  # logger

        logger.info('Training start...')
        for epoch in range(1, self.max_epoch + 1):
            loss_list = []
            for img, _, _ in train_dataloader:
                img = img.to(self.device)
                loss = model(img)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                loss_list.append(loss.item())
            logger.info('epoch [{}/{}], loss:{:.4f}'.format(epoch, self.max_epoch, np.mean(loss_list)))

            # save model
            if epoch % 5 == 0 or epoch == self.max_epoch:
                self.weights = os.path.join(save_dir, f'{self.feature_extractor}_rd_{self.scene}.pth')
                torch.save({'model': model.state_dict(),
                            'epoch': epoch}, self.weights)
                logger.info(f"model save in {self.weights}")

        from tepe.tasks.rd.find_thr import find
        self.threshold = find(model, train_dataloader, thr_dataloader, self.device)
        logger.info(f"find a appropriate threshold: {self.threshold}")

        self.set_post_info(scene=self.scene, thr=self.threshold)

    def eval(self):
        from tepe.data.infer_datasets import LoadImages1
        from tepe.tasks.rd.evalutor import read_xml, cal_true_positive

        predictor = self.get_predictor()
        eval_data_root = os.path.join(self.data_root, self.scene, 'test')

        all_precision = {}
        all_recall = {}

        for bad_name in os.listdir(eval_data_root):
            dataset = LoadImages1(os.path.join(eval_data_root, bad_name))
            gt_dir = os.path.join(self.data_root, self.scene, 'ground_truth', bad_name)

            total_pred, total_gt, total_tp = 0, 0, 0
            for data in dataset:
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

                tp = cal_true_positive(gt, pred)

                total_pred += len(pred)
                total_gt += len(gt)
                total_tp += tp

            all_precision[bad_name] = total_tp / total_pred
            all_recall[bad_name] = total_tp / total_gt
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


    def get_predictor(self):
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
            onnx_inf=onnx_inf
        )

        return predictor