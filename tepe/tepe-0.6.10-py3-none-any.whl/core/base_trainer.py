import os
import sys
import shutil
import time
import datetime
import yaml
from typing import Dict, Iterable

import torch
from loguru import logger
from torch.utils.tensorboard import SummaryWriter

from ..modules.utils.model_utils import get_model_info
from ..utils.dist import get_local_rank, get_rank, get_world_size
from ..utils.general import get_bar, setup_logger, save_task_attr_to_yaml
from ..utils.meter import MeterBuffer
from ..utils.torch_utils import select_device, load_ckpt, ModelEMA, EarlyStopping, is_parallel


class Trainer:
    def __init__(self, task):
        # init function only defines some basic attr, other attrs like model,
        # optimizer are built in before_train methods.
        self.task = task
        
        # training related attr
        self.epoch = 0
        self.amp_training = task.fp16
        self.scaler = torch.cuda.amp.GradScaler(enabled=task.fp16)
        self.is_distributed = get_world_size() > 1
        self.rank = get_rank()
        self.local_rank = get_local_rank()
        self.device = select_device(task.device)
        self.use_model_ema = task.ema if hasattr(task, 'ema') else False
        self.max_epoch = self.task.max_epoch

        # data/dataloader related attr
        self.data_type = torch.float16 if task.fp16 else torch.float32
        self.input_size = task.input_size
        self.best_eval_value = ['', 0]

        # ealy stop
        self.stopper = EarlyStopping(patience=30, early_stop=task.early_stop)

        # metric record
        self.meter = MeterBuffer(window_size=task.print_interval)

        self.resume = task.resume
        if self.resume:
            self.train_result_path = os.path.dirname(task.resume_ckpt)
        else:
            self.train_result_path = task.output_dir

        if self.rank == 0:
            os.makedirs(self.train_result_path, exist_ok=True)

        # logger
        setup_logger(os.path.join(self.train_result_path, 'train_log.txt'), mode='o')
        # Tensorboard logger
        self.tblogger = SummaryWriter(self.train_result_path)

        # save args
        save_task_attr_to_yaml(task, self.train_result_path)

        logger.info("task value:\n{}".format(self.task))

    def train(self):
        self.before_train()
        try:
            for self.epoch in range(self.start_epoch, self.max_epoch):
                logger.info("---> Epoch{}/{}".format(self.epoch + 1, self.max_epoch))
                self.before_epoch()

                self.train_one_epoch()

                stop = self.after_epoch()
                # early stop
                if stop < 0:
                    break
        except Exception:
            raise
        finally:
            self.after_train()

    def before_train(self):

        # 1. model related init
        torch.cuda.set_device(self.device)
        model = self.task.get_model(train=True)
        model.to(self.device)
        get_model_info(model, verbose=True, img_size=self.input_size)

        # 2. data related init
        self.train_loader = self.task.get_train_loader()
        # self.prefetcher = DataPrefetcher(self.train_loader)

        # max_iter means iters per epoch
        self.max_iter = len(self.train_loader)

        # 3. evaluator init
        self.evaluator = self.task.get_evaluator(train=True)

        # 4. loss
        self.loss_fn = self.task.get_loss()

        # 5. solver related init
        self.optimizer = self.task.get_optimizer()
        self.init_lr = self.task.learning_rate
        self.lr_scheduler = self.task.get_lr_scheduler()
        # value of epoch will be set in `resume_train`
        model = self.resume_train(model)

        # EMA
        if self.use_model_ema:
            logger.info('Use ema model')
            self.ema_model = ModelEMA(model, 0.9998)
            self.ema_model.updates = self.max_iter * self.start_epoch

        self.model = model
        self.model.train()

        self.t0 = time.time()
        logger.info("Training start...")
        # logger.info("\n{}".format(model))

    def before_epoch(self):
        pass

    def train_one_epoch(self):
        self.pbar = get_bar(self.train_loader, 'train')
        for self.iter, data in enumerate(self.pbar):
            self.before_iter()
            outputs = self.train_one_iter(data)
            self.after_iter(outputs)

    def before_iter(self):
        self.iter_start_time = time.time()

    def train_one_iter(self, data) -> Dict:
        inps, targets = data
        inps = inps.to(self.data_type)
        targets = targets.to(self.data_type)
        targets.requires_grad = False

        with torch.cuda.amp.autocast(enabled=self.amp_training):
            outputs = self.model(inps, targets)

        loss = outputs['loss']

        self.optimizer.zero_grad()
        self.scaler.scale(loss).backward()
        self.scaler.step(self.optimizer)
        self.scaler.update()

        # update per iter or per epoch?
        if self.lr_scheduler:
            lr = self.lr_scheduler.update_lr(self.progress_in_iter + 1)
            for param_group in self.optimizer.param_groups:
                param_group["lr"] = lr
        else:
            lr = self.init_lr

        outputs['lr'] = lr
        return outputs

    def after_iter(self, outputs):
        self.iter_end_time = time.time()

        # update ema model
        if self.use_model_ema:
            self.ema_model.update(self.model)

        self.meter.update(
            iter_time=self.iter_end_time - self.iter_start_time,
            **outputs
        )

        # log needed information
        if (self.iter + 1) % self.task.print_interval == 0:
            # self.pbar.set_description(('%10s' * 2 + '%10.4g' * 5) % (
            #     f'{self.iter + 1}/{self.max_iter}', mem, *mloss, targets.shape[0], imgs.shape[-1]))

            loss_meter = self.meter.get_filtered_meter("loss")
            loss_str = ", ".join(
                ["{}: {:.5f}".format(k, v.latest) for k, v in loss_meter.items()]
            )
            for k, v in loss_meter.items():
                self.tblogger.add_scalar(tag=k, scalar_value=v.latest, global_step=self.progress_in_iter)

            time_meter = self.meter.get_filtered_meter("time")
            time_str = ", ".join(
                ["{}: {:.3f}s".format(k, v.avg) for k, v in time_meter.items()]
            )

            postfix_str = "mem: {:.0f}MB, {}".format(
                torch.cuda.max_memory_allocated() / (1024 * 1024),
                loss_str,
            )

            if self.meter["lr"].latest is not None:
                lr_value = self.meter["lr"].latest
                postfix_str += ", lr: {:.5f}".format(lr_value)
                self.tblogger.add_scalar(
                    tag='lr', scalar_value=lr_value, global_step=self.progress_in_iter)

            self.pbar.set_postfix_str(postfix_str)
            self.meter.clear_meters()

    def after_epoch(self):
        self.save_ckpt(ckpt_name="latest")

        if (self.epoch + 1) % self.task.eval_interval == 0:
            if self.evaluator is not None:
                update_ckpt, current_eval_value = self.validate()
            else:
                # TODO: =========
                update_ckpt, current_eval_value = 1, 0
            if update_ckpt:
                # save a best ckpt file
                filename = os.path.join(self.train_result_path, "latest_ckpt.pth")
                best_filename = os.path.join(self.train_result_path, "best_ckpt.pth")
                shutil.copyfile(filename, best_filename)

            if self.stopper(epoch=self.epoch, fitness=current_eval_value):
                return -1
        return 0

    def after_train(self):
        # set best trained model path to task.weights
        setattr(self.task, 'weights', os.path.join(self.train_result_path, 'best_ckpt.pth'))
        
        logger.info(
            "Training task is done in {:.3f} hours and the best {} is {:.2f}".format(
                (time.time() - self.t0) / 3600, self.best_eval_value[0], self.best_eval_value[1])
        )
        logger.info("Save weights to {}".format(self.train_result_path))

    @property
    def progress_in_iter(self):
        return self.epoch * self.max_iter + self.iter

    def resume_train(self, model):
        if self.task.resume:
            logger.info("resume training")
            if self.task.resume_ckpt is None:
                ckpt_file = os.path.join(self.train_result_path, "latest" + "_ckpt.pth")
            else:
                ckpt_file = self.task.resume_ckpt

            ckpt = torch.load(ckpt_file, map_location=self.device)
            # resume the model/optimizer state dict
            model.load_state_dict(ckpt["model"])
            self.optimizer.load_state_dict(ckpt["optimizer"])
            # resume the training states variables
            start_epoch = ckpt['epoch'] + 1
            self.start_epoch = start_epoch
            logger.info( f"loaded checkpoint '{ckpt_file}' (epoch {self.start_epoch})")
            if self.max_epoch < self.start_epoch:
                logger.info(
                    f"{ckpt_file} has been trained for {ckpt['epoch']} epochs. "
                    f"Training for {self.max_epoch} more epochs.")
                self.max_epoch += ckpt['epoch']  # finetune additional epochs
            # save last ckpt
            last_ckpt_file = os.path.join(self.train_result_path, f'epoch-{start_epoch}.pth')
            shutil.copyfile(ckpt_file, last_ckpt_file)
        else:
            if self.task.weights is not None and self.task.pretrained:
                logger.info("loading checkpoint for fine tuning")
                weights_file = self.task.weights
                load_ckpt(model, weights_file,
                          device=self.device,
                          is_state_dict=True,
                          load_keys='model')

                # Freeze
                freeze = [f'model.{x}.' for x in range(self.task.freeze_layer)]  # layers to freeze
                for k, v in model.named_parameters():
                    v.requires_grad = True  # train all layers
                    if any(x in k for x in freeze):
                        logger.info(f'freezing {k}')
                        v.requires_grad = False

            self.start_epoch = 0

        return model

    def validate(self):
        if self.use_model_ema:
            eval_model = self.ema_model.ema
        else:
            eval_model = self.model
            if is_parallel(eval_model):
                eval_model = eval_model.module

        eval_model.eval()

        eval_result = self.evaluator.evaluate(model=eval_model)
        self.model.train()

        eval_res_list = [[k, v] for k, v in eval_result.items() if not isinstance(v, Iterable)]
        eval_key_value = eval_res_list[0]  # first eval value
        self.best_eval_value[0] = eval_key_value[0]
        if 'loss' in eval_key_value[0]:
            if self.epoch == 0:
                self.best_eval_value[1] = 1000  # adjust initial eval_value
                self.stopper.best_fitness = 1000
            self.stopper.up_down = False
            update_ckpt = eval_key_value[1] < self.best_eval_value[1]
            self.best_eval_value[1] = min(self.best_eval_value[1], eval_key_value[1])
        else:
            update_ckpt = eval_key_value[1] > self.best_eval_value[1]
            self.best_eval_value[1] = max(self.best_eval_value[1], eval_key_value[1])

        for k, v in eval_res_list:
            if isinstance(v, str): continue
            self.tblogger.add_scalar(f"val/{k}", v, self.epoch + 1)

        current_eval_value = eval_key_value[1]

        return update_ckpt, current_eval_value

    def save_ckpt(self, ckpt_name):
        if self.rank == 0:
            save_model = self.ema_model.ema if self.use_model_ema else self.model
            ckpt_state = {
                "epochs": self.epoch + 1,
                "model": save_model.state_dict(),
                "optimizer": self.optimizer.state_dict(),
                'date': datetime.datetime.now().isoformat()
            }

            filename = os.path.join(self.train_result_path, ckpt_name + "_ckpt.pth")
            torch.save(ckpt_state, filename)