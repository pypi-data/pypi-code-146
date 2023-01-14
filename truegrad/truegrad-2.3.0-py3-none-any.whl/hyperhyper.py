import datetime

import numpy
import torch

from torchvision.models import resnet18


class OptimizerOptimizer(torch.optim.Optimizer):
    def __init__(self, inner_optimizer: torch.optim.Optimizer, learning_rate_learning_rate: float = 1):
        self.learning_rate_learning_rate = learning_rate_learning_rate

        self.inner_optimizer = inner_optimizer
        param_groups = self.inner_optimizer.param_groups
        self.inner_optimizer.param_groups = []
        for group in param_groups:
            for param in group["params"]:
                group = {k: v for k, v in group.items() if k != "params"}
                group["params"] = [param]
                self.inner_optimizer.param_groups.append(group)

        super(OptimizerOptimizer, self).__init__(param_groups, {})

    def step(self, closure=None):
        loss = self.inner_optimizer.step(closure)

        for group in self.inner_optimizer.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                state = self.state[p]
                if "param" in state:
                    neg_update = state["param"] - p
                    dims = ''.join(chr(ord('a') + i) for i in range(neg_update.ndim))
                    lr_grad = torch.einsum(f"{dims},{dims}->", neg_update.double(), p.grad.double()) * self.learning_rate_learning_rate
                    group["lr"] = group["lr"] + lr_grad.item()
                state["param"] = torch.clone(p.detach())

        return loss


model = resnet18().cuda()
optim = torch.optim.Adam(model.parameters(), lr=.000001, weight_decay=0)  # weight_decay currently not supported
optim = OptimizerOptimizer(optim, 0.01)

inp = torch.randn((2, 3, 224, 224)).cuda()
tgt = torch.randint(0, 1000, (2,)).cuda()

i = 0
while True:
    loss = torch.nn.functional.cross_entropy(model(inp), tgt)
    loss.backward()
    optim.step()
    optim.zero_grad()
    i += 1
    if i % 100 == 0:
        lrs = numpy.array([g["lr"] for g in optim.inner_optimizer.param_groups])

        print(datetime.datetime.now(), i, loss.item(), lrs.min(), lrs.max(), lrs.mean(), lrs.std())
