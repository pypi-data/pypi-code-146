import torch
from tepe.core.base_trainer import Trainer


class SegTrainer(Trainer):
    def __init__(self, task):
        super().__init__(task)

    def train_one_iter(self, data):
        
        x, y = data
        x = x.to(self.data_type).cuda(non_blocking=True)
        y = y.to(torch.long).cuda(non_blocking=True)

        y_pred = self.model(x)

        loss = self.loss_fn(y_pred, y)

        self.optimizer.zero_grad()
        if self.scaler is not None:
            self.scaler.scale(loss).backward()
            self.scaler.step(self.optimizer)
            self.scaler.update()
        else:
            loss.backward()
            self.optimizer.step()

        self.lr_scheduler.step()
        
        return {'loss': loss}
