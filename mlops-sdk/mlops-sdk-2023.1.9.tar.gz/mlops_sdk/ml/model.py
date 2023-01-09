import torch
import torch.nn as nn
from torchdiffeq import odeint
import numpy as np

from typing import Any, Callable, Dict, List, Optional


class MlopsModel:
    def __init__(self, name: str, version: str, predict_fn: Callable, models: Optional[List[Any]] = []):
        self.name = name
        self.version = version
        self.predict_fn = predict_fn
        self.models = models
        self.attrs = {}

    def add_attr(self, key: str, value: Any) -> None:
        self.attrs[key] = value

    def remove_attr(self, key: str) -> None:
        self.attrs.pop(key, None)

    def clear_attrs(self) -> None:
        self.attrs = {}

    async def predict(self, id: str, channel_id: str, **kwargs) -> List[Dict[str, Any]]:
        return await self.predict_fn(models=self.models, id=id, channel_id=channel_id, **kwargs)


class SimpleVF(nn.Module):
    def __init__(self, n_features: int) -> None:
        super().__init__()

        self.main = nn.Sequential(
            nn.Linear(n_features, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, n_features),
        )

        for m in self.main.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, mean=0, std=0.1)
                nn.init.constant_(m.bias, val=0)

    def forward(self, t, x) -> torch.tensor:
        return self.main(x)


class _OdeNet(nn.Module):
    def __init__(self, n_features: int) -> None:
        super().__init__()

        self.ode = SimpleVF(n_features + 2)
        self.emb = nn.Embedding(3000, 3)

    def forward(self, x) -> torch.tensor:
        t0 = torch.tensor([0.0, 1.0])
        _emb = x[:, -4].long()
        _emb = self.emb(_emb)

        x = torch.cat([x[:, :-4], _emb, x[:, -3:]], dim=-1)
        predy = odeint(self.ode, x, t0, method="rk4")

        return predy[1, :, -3:-2]


class OdeNet(nn.Module):
    def __init__(self, n_features: int) -> None:
        super().__init__()

        self.ode = SimpleVF(n_features)

    def forward(self, x) -> torch.tensor:
        x_tensor = torch.cat([x["seasonal"], x["position"], x["promo1"], x["promo2"], x["price_time"]], dim=-1)
        t0 = torch.tensor([0.0, 1.0])

        x_tensor = x_tensor.float()

        predy = odeint(self.ode, x_tensor, t0, method="rk4")

        return predy[1, :, -3:-2]


class CustomLoader:
    def __init__(self, dataset, device="cpu", batch_size=32):
        if isinstance(device, str):
            self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        else:
            self.device = device
        self.dataset = dataset

        self.batch_size = batch_size
        self.dataset_len = len(dataset)

        n_batches, remainder = divmod(self.dataset_len, self.batch_size)
        if remainder > 0:
            n_batches += 1

        self.n_batches = n_batches

    def __iter__(self):
        self.i = 0

        return self

    def __next__(self):

        if self.i >= self.dataset_len:
            raise StopIteration

        batch = self.dataset[self.i : self.i + self.batch_size]
        keys = batch[0].keys()

        tensor_batch = {k: list() for k in batch[0].keys()}
        for item in batch:
            for k in keys:
                tensor_batch[k].append(item[k])
        for k in keys:
            if k == "meta":
                continue
            else:
                tensor_batch[k] = torch.from_numpy(np.vstack(tensor_batch[k])).to(self.device)
        self.i += self.batch_size

        return tensor_batch

    def __len__(self):
        return self.n_batches
