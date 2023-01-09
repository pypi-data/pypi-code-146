import torch
import torch.nn as nn
from torchdiffeq import odeint
from .model import SimpleVF


class OdeNetEo(nn.Module):
    def __init__(self, n_features: int) -> None:
        super().__init__()

        self.ode = SimpleVF(n_features)

    def forward(self, x) -> torch.tensor:
        x_tensor = torch.cat(
            [x["seasonal"], x["position"], x["promo1"], x["promo2"], x["price_time"], x["classification"]], dim=-1
        )
        t0 = torch.tensor([0.0, 1.0])

        x_tensor = x_tensor.float()

        predy = odeint(self.ode, x_tensor, t0, method="rk4")

        return predy[1, :, -3:-2]
