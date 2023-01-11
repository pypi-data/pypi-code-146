import copy
import hashlib
import json
import logging
import pickle
import time
import uuid
from dataclasses import asdict, dataclass
from logging import Logger
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import tqdm
from torch.optim import Adam
from torch.utils.data import DataLoader, Dataset, random_split

from selcol.traintime.dataset import Chunk, Metadata

logger = logging.getLogger(__name__)


@dataclass
class SelfColDataset(Dataset):
    n_dof: int
    X: torch.Tensor
    Y: torch.Tensor
    header: Metadata

    def __len__(self) -> int:
        return len(self.Y)

    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.X[idx], self.Y[idx]

    @classmethod
    def load(cls, base_path: Path) -> "SelfColDataset":
        hash_values = set()

        x_list = []
        y_list = []

        n_dof: Optional[int] = None
        header: Optional[Metadata] = None
        for file_path in base_path.iterdir():
            if not file_path.name.startswith("dataset"):
                continue
            if not file_path.name.endswith(".pkl"):
                continue

            with file_path.open(mode="rb") as f:
                chunk: Chunk = pickle.load(f)
            header = chunk.header
            hash_values.add(hashlib.md5(pickle.dumps(header)).hexdigest())

            for sample in chunk.samples:
                x, y = sample
                x_list.append(torch.from_numpy(x).float())
                y_list.append(torch.tensor(y))

            n_dof = len(chunk.header.joint_names)

        all_hashvalue_same = len(hash_values) == 1
        assert all_hashvalue_same

        X = torch.stack(x_list)
        Y = torch.stack(y_list)
        assert n_dof is not None
        assert header is not None
        return cls(n_dof, X, Y.float(), header)


@dataclass
class SelcolNetConfig:
    n_dof: int
    n_width: int = 200
    n_depth: int = 3


class SelcolNet(nn.Module):
    device: torch.device
    linears: nn.Sequential
    unique_id: str
    config: SelcolNetConfig

    def __init__(self, config: SelcolNetConfig, device: Optional[torch.device] = None):
        super().__init__()
        self._setup_from_config(config)

        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.device = device
        self.unique_id = str(uuid.uuid4())
        self.config = config
        logger.info("model name: {}".format(self.__class__.__name__))
        logger.info("model config: {}".format(config))
        logger.info("model is initialized")

    def put_on_device(self, device: Optional[torch.device] = None):
        if device is not None:
            self.device = device
        self.to(self.device)

    def _setup_from_config(self, config: SelcolNetConfig) -> None:
        layers = []
        layers.append(nn.Linear(config.n_dof, config.n_width))
        layers.append(nn.ReLU())  # type: ignore[arg-type]

        for _ in range(config.n_depth - 1):
            layers.append(nn.Linear(config.n_width, config.n_width))
            layers.append(nn.ReLU())  # type: ignore[arg-type]

        layers.append(nn.Linear(config.n_width, 1))
        layers.append(nn.Sigmoid())  # type: ignore[arg-type]
        self.linears = nn.Sequential(*layers)

    def loss(self, sample: Tuple[torch.Tensor, torch.Tensor]) -> torch.Tensor:
        X, Y = sample
        Y_pred = self.linears(X)
        loss = nn.MSELoss()(Y, torch.squeeze(Y_pred, dim=1))
        return loss

    def forward(self, inp: torch.Tensor) -> torch.Tensor:
        return self.linears(inp)


@dataclass
class TrainConfig:
    batch_size: int = 200
    valid_data_ratio: float = 0.1
    learning_rate: float = 0.001
    n_epoch: int = 100


def split_with_ratio(dataset: Dataset, valid_ratio: float = 0.1):
    """split dataset into train and validation dataset with specified ratio"""

    n_total = len(dataset)  # type: ignore
    n_validate = int(valid_ratio * n_total)
    ds_train, ds_validate = random_split(dataset, [n_total - n_validate, n_validate])
    return ds_train, ds_validate


def save_models(model: SelcolNet, dataset_metadata: Metadata, valid_loss: float, base_path: Path):
    directory_name = "pretrained-{}-{}-{}".format(
        dataset_metadata.robot_name, dataset_metadata.urdf_md5sum, model.unique_id
    )
    directory_path = base_path / directory_name
    directory_path.mkdir(exist_ok=True)

    model_copied = copy.deepcopy(model).cpu()

    for n_batch in [1, 8, 16, 32, 64, 128]:
        # dump onnx model for different batch sizes
        n_dof = len(dataset_metadata.joint_names)
        model_file_path = directory_path / "model-{}.onnx".format(n_batch)
        torch.onnx.export(
            model_copied,
            torch.randn(n_batch, n_dof),
            str(model_file_path),
            input_names=["x"],
            output_names=["y"],
        )

    metadata_file_path = directory_path / "metadata.json"
    json_dict = asdict(dataset_metadata)
    json_dict["valid_loss"] = valid_loss
    json_dict["time_stamp"] = time.time()
    json_dict["model_config"] = asdict(model.config)
    with metadata_file_path.open(mode="w") as f:
        json.dump(json_dict, f, indent=2)

    # convert to numpy dict and dump it
    np_layers = []
    for torch_layer in model_copied.linears:
        if isinstance(torch_layer, nn.Linear):
            w = torch_layer.weight.detach().numpy()
            b = torch_layer.bias.detach().numpy()
            params = {"w": w, "b": b}
            np_layers.append({"type": "linear", "params": params})
        elif isinstance(torch_layer, nn.ReLU):
            np_layers.append({"type": "relu", "params": None})
        elif isinstance(torch_layer, nn.Sigmoid):
            np_layers.append({"type": "sigmoid", "params": None})
        else:
            assert False
    numpy_layers_path = directory_path / "numpy_layers.pkl"
    with numpy_layers_path.open(mode="wb") as f:
        pickle.dump(np_layers, f)


def train(model: SelcolNet, dataset: SelfColDataset, config: TrainConfig, base_path: Path):

    dataset_train, dataset_validate = split_with_ratio(dataset, config.valid_data_ratio)

    train_loader = DataLoader(dataset=dataset_train, batch_size=config.batch_size, shuffle=True)
    validate_loader = DataLoader(
        dataset=dataset_validate, batch_size=config.batch_size, shuffle=True
    )

    optimizer = Adam(model.parameters(), lr=config.learning_rate)

    def move_to_device(sample):
        if isinstance(sample, torch.Tensor):
            return sample.to(model.device)
        elif isinstance(sample, list):  # NOTE datalodaer return list type not tuple
            return tuple([e.to(model.device) for e in sample])
        else:
            raise RuntimeError

    valid_loss_mean_min = +np.inf

    for epoch in tqdm.tqdm(range(config.n_epoch)):
        model.train()
        train_loss_list: List[float] = []
        for samples in tqdm.tqdm(train_loader, leave=False):
            optimizer.zero_grad()
            samples = move_to_device(samples)
            train_loss = model.loss(samples)
            train_loss_list.append(train_loss.item())
            train_loss.backward()
            optimizer.step()
        train_loss_mean = float(np.mean(train_loss_list))

        valid_loss_list: List[float] = []
        model.eval()
        for samples in validate_loader:
            samples = move_to_device(samples)
            valid_loss = model.loss(samples)
            valid_loss_list.append(valid_loss.item())
        valid_loss_mean = float(np.mean(valid_loss_list))

        logger.info("epoch: {}".format(epoch))
        logger.info("train loss: {}".format(train_loss_mean))
        logger.info("valid loss: {}".format(valid_loss_mean))

        if valid_loss_mean < valid_loss_mean_min:
            valid_loss_mean_min = valid_loss_mean
            save_models(model, dataset.header, valid_loss_mean_min, base_path)

    return valid_loss_mean_min


def create_default_logger(project_path: Path, prefix: str) -> Logger:
    timestr = "_" + time.strftime("%Y%m%d%H%M%S")
    log_dir_path = project_path / "log"
    log_dir_path.mkdir(parents=True, exist_ok=True)
    log_file_path = log_dir_path / (prefix + timestr + ".log")

    logger = logging.getLogger("selcol")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter("[%(levelname)s] %(asctime)s %(name)s: %(message)s")

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)

    fh = logging.FileHandler(str(log_file_path))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    logger.addHandler(sh)
    logger.addHandler(fh)

    log_sym_path = log_dir_path / ("latest_" + prefix + ".log")

    logger.info("create log symlink :{0} => {1}".format(log_file_path, log_sym_path))
    if log_sym_path.is_symlink():
        log_sym_path.unlink()
    log_sym_path.symlink_to(log_file_path)

    return logger
