import torch
from ..base_trainer import Trainer


class ClsTrainer(Trainer):
    def __init__(self, task):
        super().__init__(task)

    def train_one_iter(self, data):

        inps, targets, _, _ = data
        inps = inps.to(self.data_type).cuda(non_blocking=True)
        targets = targets.to(torch.long).cuda(non_blocking=True)
        targets.requires_grad = False

        with torch.cuda.amp.autocast(enabled=self.amp_training):
            outputs = self.model(inps, targets)

        loss = outputs['loss']

        self.optimizer.zero_grad()
        self.scaler.scale(loss).backward()
        self.scaler.step(self.optimizer)
        self.scaler.update()

        if self.use_model_ema:
            self.ema_model.update(self.model)

        lr = self.lr_scheduler.update_lr(self.progress_in_iter + 1)
        for param_group in self.optimizer.param_groups:
            param_group["lr"] = lr

        outputs['lr'] = lr

        return outputs