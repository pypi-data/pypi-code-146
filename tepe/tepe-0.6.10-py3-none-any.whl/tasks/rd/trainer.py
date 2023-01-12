import os
from loguru import logger
import torch
from tepe.core import Trainer as BaseTrainer
from tepe.data.datasets import AnomalyDataset
from tepe.utils.general import (
    init_seeds,
    save_task_attr_to_yaml,
    save_task_config_py,
    setup_logger
)

class Trainer(BaseTrainer):
    def __init__(self, task):
        self.task = task
        self.batch_size = task.batch_size
        self.learning_rate = task.learning_rate
        self.scene = task.scene
        self.save_dir = task.output_dir + f'/{self.scene}'
        os.makedirs(self.save_dir, exist_ok=True)

        # save args
        # save_task_attr_to_yaml(self, save_dir)
        save_task_config_py(self, self.save_dir)

        # save log text
        logger.add(os.path.join(self.save_dir, 'train_log.txt'))
        setup_logger(save_file=os.path.join(self.save_dir, 'train_log.txt'))  # logger

    def before_train(self):
        init_seeds(self.task.seed)

        # data--------------------------
        data_root = self.task.data_root
        data_transform, target_transform = self.task.get_transform()

        self.train_data = AnomalyDataset(data_root, class_name=self.task.scene,
                                         transform=data_transform, target_transform=target_transform,
                                         resize=self.task.input_size, is_train=True, is_mvtec=False,
                                         cache_img=self.task.cache)

        thr_data = AnomalyDataset(data_root, class_name=self.task.scene,
                                  transform=data_transform, target_transform=target_transform,
                                  paste=True, is_train=True, is_mvtec=False)

        train_dataloader = torch.utils.data.DataLoader(
            self.train_data, batch_size=self.batch_size, shuffle=True, num_workers=self.task.workers
        )
        thr_dataloader = torch.utils.data.DataLoader(
            thr_data, batch_size=self.batch_size, shuffle=True, num_workers=self.task.workers
        )

        self.model = self.task.get_model(train=True).to(self.device).train()

        self.model.encoder.eval()
        self.optimizer = torch.optim.Adam(
            list(self.model.decoder.parameters()) + list(self.model.bn.parameters()),
            lr=self.learning_rate, betas=(0.5,0.999)
        )


def train(self):
        pass