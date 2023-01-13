"""HeteroNN demos."""

import os
from hashlib import md5
from time import time
from typing import Dict, List, Set, Tuple, Union

import cloudpickle as pickle
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
from torch.utils.data import DataLoader, Subset

from ... import logger
from ...hetero_nn import (HeteroNNCollaboratorScheduler, HeteroNNHostScheduler,
                          SecureHeteroNNCollaboratorScheduler,
                          SecureHeteroNNHostScheduler)
from . import DEV_TASK_ID

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

_DATA_DIR = os.path.join(CURRENT_DIR, 'data')

VANILLA = 'vanilla'
SECURE = 'secure'

torch.manual_seed(42)


class ConvNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=10, kernel_size=(5, 3))
        self.conv2 = nn.Conv2d(in_channels=10, out_channels=20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(in_features=80, out_features=50)
        self.fc2 = nn.Linear(in_features=50, out_features=20)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 80)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        return self.fc2(x)


class InferModule(nn.Module):

    def __init__(self) -> None:
        super().__init__()
        self.fc1 = nn.Linear(40, 20)
        self.fc2 = nn.Linear(20, 10)

    def forward(self, input):
        out = F.relu(self.fc1(input))
        out = self.fc2(out)
        return F.log_softmax(out, dim=-1)


class DemoHeteroHost(HeteroNNHostScheduler):

    def __init__(self,
                 feature_key: str,
                 batch_size: int,
                 data_dir: str,
                 name: str = None,
                 max_rounds: int = 0,
                 calculation_timeout: int = 300,
                 schedule_timeout: int = 30,
                 log_rounds: int = 0) -> None:
        super().__init__(feature_key=feature_key,
                         name=name,
                         max_rounds=max_rounds,
                         calculation_timeout=calculation_timeout,
                         schedule_timeout=schedule_timeout,
                         log_rounds=log_rounds)
        self.batch_size = batch_size
        self.data_dir = data_dir

    def load_local_ids(self) -> List[str]:
        train_ids = [str(i) for i in range(0, 20000)]
        test_ids = [str(i) for i in range(100000, 105000)]
        return train_ids + test_ids

    def split_dataset(self, id_intersection: Set[str]) -> Tuple[Set[str], Set[str]]:
        ids = [int(_id) for _id in id_intersection]
        ids.sort()
        train_ids = ids[:10000]
        test_ids = ids[10000:]

        logger.info(f'Got {len(train_ids)} intersecting samples for training.')
        logger.info(f'Got {len(test_ids)} intersecting samples for testing.')

        return set(train_ids), set(test_ids)

    def make_feature_model(self) -> nn.Module:
        return ConvNet()

    def make_feature_optimizer(self, feature_model: nn.Module) -> optim.Optimizer:
        return optim.SGD(feature_model.parameters(), lr=0.01, momentum=0.9)

    def _erase_right(self, _image: torch.Tensor) -> torch.Tensor:
        return _image[:, :, :, :14]

    def iterate_train_feature(self,
                              feature_model: nn.Module,
                              train_ids: Set[str]) -> Tuple[torch.Tensor, torch.Tensor]:
        train_dataset = torchvision.datasets.MNIST(
            self.data_dir,
            train=True,
            download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,))
            ])
        )
        train_ids: List = list(train_ids)
        train_ids.sort(key=lambda x: md5(bytes(x + self.current_round)).digest())

        train_dataset = Subset(train_dataset, train_ids)
        self.train_loader = DataLoader(train_dataset,
                                       batch_size=self.batch_size,
                                       shuffle=False)

        for _data, _labels in self.train_loader:
            _data = self._erase_right(_data)
            yield feature_model(_data), _labels

    def iterate_test_feature(self,
                             feature_model: nn.Module,
                             test_ids: Set[str]) -> Tuple[torch.Tensor, torch.Tensor]:
        test_dataset = torchvision.datasets.MNIST(
            self.data_dir,
            train=False,
            download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,))
            ])
        )
        test_ids = [(i - 100000) for i in test_ids]
        test_dataset = Subset(test_dataset, test_ids)
        self.test_loader = DataLoader(test_dataset,
                                      batch_size=self.batch_size,
                                      shuffle=False)

        for _data, _labels in self.test_loader:
            _data = self._erase_right(_data)
            yield feature_model(_data), _labels

    def make_infer_model(self) -> nn.Module:
        return InferModule()

    def make_infer_optimizer(self, infer_model: nn.Module) -> optim.Optimizer:
        return optim.SGD(infer_model.parameters(), lr=0.01, momentum=0.9)

    def train_a_batch(self, feature_projection: Dict[str, torch.Tensor], labels: torch.Tensor):
        fusion_tensor = torch.concat((feature_projection['demo_host'],
                                      feature_projection['demo_collaborator']), dim=1)
        self.optimizer.zero_grad()
        out = self.infer_model(fusion_tensor)
        loss = F.nll_loss(out, labels)
        loss.backward()
        self.optimizer.step()

    def test(self,
             batched_feature_projections: List[torch.Tensor],
             batched_labels: List[torch.Tensor]):
        start = time()
        test_loss = 0
        correct = 0
        for _feature_projection, _lables in zip(batched_feature_projections, batched_labels):
            fusion_tensor = torch.concat((_feature_projection['demo_host'],
                                          _feature_projection['demo_collaborator']), dim=1)
            out: torch.Tensor = self.infer_model(fusion_tensor)
            test_loss += F.nll_loss(out, _lables)
            pred = out.max(1, keepdim=True)[1]
            correct += pred.eq(_lables.view_as(pred)).sum().item()

        test_loss /= len(self.test_loader.dataset)
        accuracy = correct / len(self.test_loader.dataset)
        correct_rate = 100. * accuracy
        logger.info(f'Test set: Average loss: {test_loss:.4f}')
        logger.info(
            f'Test set: Accuracy: {accuracy} ({correct_rate:.2f}%)'
        )

        end = time()

        self.tb_writer.add_scalar('timer/run_time', end - start, self.current_round)
        self.tb_writer.add_scalar('test_results/average_loss', test_loss, self.current_round)
        self.tb_writer.add_scalar('test_results/accuracy', accuracy, self.current_round)
        self.tb_writer.add_scalar('test_results/correct_rate', correct_rate, self.current_round)


class DemoHeteroCollaborator(HeteroNNCollaboratorScheduler):

    def __init__(self,
                 feature_key: str,
                 batch_size: int,
                 data_dir: str,
                 name: str = None,
                 schedule_timeout: int = 30,
                 is_feature_trainable: bool = True) -> None:
        super().__init__(feature_key=feature_key,
                         name=name,
                         schedule_timeout=schedule_timeout,
                         is_feature_trainable=is_feature_trainable)
        self.batch_size = batch_size
        self.data_dir = data_dir

    def load_local_ids(self) -> List[str]:
        train_ids = [str(i) for i in range(10000, 30000)]
        test_ids = [str(i) for i in range(103000, 107000)]
        return train_ids + test_ids

    def split_dataset(self, id_intersection: Set[str]) -> Tuple[Set[str], Set[str]]:
        ids = [int(_id) for _id in id_intersection]
        ids.sort()
        train_ids = ids[:10000]
        test_ids = ids[10000:]

        logger.info(f'Got {len(train_ids)} intersecting samples for training.')
        logger.info(f'Got {len(test_ids)} intersecting samples for testing.')

        return set(train_ids), set(test_ids)

    def make_feature_model(self) -> nn.Module:
        return ConvNet()

    def make_feature_optimizer(self, feature_model: nn.Module) -> optim.Optimizer:
        return optim.SGD(feature_model.parameters(), lr=0.01, momentum=0.9)

    def _erase_left(self, _image: torch.Tensor) -> torch.Tensor:
        return _image[:, :, :, 14:]

    def iterate_train_feature(self,
                              feature_model: nn.Module,
                              train_ids: Set[str]) -> torch.Tensor:
        train_dataset = torchvision.datasets.MNIST(
            self.data_dir,
            train=True,
            download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,))
            ])
        )
        train_ids: List = list(train_ids)
        train_ids.sort(key=lambda x: md5(bytes(x + self.current_round)).digest())

        train_dataset = Subset(train_dataset, train_ids)
        self.train_loader = DataLoader(train_dataset,
                                       batch_size=self.batch_size,
                                       shuffle=False)

        for _data, _ in self.train_loader:
            _data = self._erase_left(_data)
            yield feature_model(_data)

    def iterate_test_feature(self,
                             feature_model: nn.Module,
                             test_ids: Set[str]) -> torch.Tensor:
        test_dataset = torchvision.datasets.MNIST(
            self.data_dir,
            train=False,
            download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,))
            ])
        )
        test_ids = [(i - 100000) for i in test_ids]
        test_dataset = Subset(test_dataset, test_ids)
        self.test_loader = DataLoader(test_dataset,
                                      batch_size=self.batch_size,
                                      shuffle=False)

        for _data, _ in self.test_loader:
            _data = self._erase_left(_data)
            yield feature_model(_data)


class DemoSecureHeteroHost(SecureHeteroNNHostScheduler):

    def __init__(self,
                 feature_key: str,
                 project_layer_config: List[Tuple[str, int, int]],
                 project_layer_lr: float,
                 batch_size: int,
                 data_dir: str,
                 name: str = None,
                 max_rounds: int = 0,
                 calculation_timeout: int = 300,
                 schedule_timeout: int = 30,
                 log_rounds: int = 0,
                 is_feature_trainable: bool = True) -> None:
        super().__init__(feature_key=feature_key,
                         project_layer_config=project_layer_config,
                         project_layer_lr=project_layer_lr,
                         name=name,
                         max_rounds=max_rounds,
                         calculation_timeout=calculation_timeout,
                         schedule_timeout=schedule_timeout,
                         log_rounds=log_rounds,
                         is_feature_trainable=is_feature_trainable)
        self.batch_size = batch_size
        self.data_dir = data_dir

    def load_local_ids(self) -> List[str]:
        train_ids = [str(i) for i in range(0, 20000)]
        test_ids = [str(i) for i in range(100000, 105000)]
        return train_ids + test_ids

    def split_dataset(self, id_intersection: Set[str]) -> Tuple[Set[str], Set[str]]:
        ids = [int(_id) for _id in id_intersection]
        ids.sort()
        train_ids = ids[:10000]
        test_ids = ids[10000:]

        logger.info(f'Got {len(train_ids)} intersecting samples for training.')
        logger.info(f'Got {len(test_ids)} intersecting samples for testing.')

        return set(train_ids), set(test_ids)

    def make_feature_model(self) -> nn.Module:
        return ConvNet()

    def make_feature_optimizer(self, feature_model: nn.Module) -> optim.Optimizer:
        return optim.SGD(feature_model.parameters(), lr=0.01, momentum=0.9)

    def _erase_right(self, _image: torch.Tensor) -> torch.Tensor:
        return _image[:, :, :, :14]

    def iterate_train_feature(self,
                              feature_model: nn.Module,
                              train_ids: Set[str]) -> Tuple[torch.Tensor, torch.Tensor]:
        train_dataset = torchvision.datasets.MNIST(
            self.data_dir,
            train=True,
            download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,))
            ])
        )
        train_ids: List = list(train_ids)
        train_ids.sort(key=lambda x: md5(bytes(x + self.current_round)).digest())
        train_dataset = Subset(train_dataset, train_ids)
        self.train_loader = DataLoader(train_dataset,
                                       batch_size=self.batch_size,
                                       shuffle=False,
                                       drop_last=True)

        for _data, _labels in self.train_loader:
            _data = self._erase_right(_data)
            yield feature_model(_data), _labels

    def iterate_test_feature(self,
                             feature_model: nn.Module,
                             test_ids: Set[str]) -> Tuple[torch.Tensor, torch.Tensor]:
        test_dataset = torchvision.datasets.MNIST(
            self.data_dir,
            train=False,
            download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,))
            ])
        )
        test_ids = [(i - 100000) for i in test_ids]
        test_dataset = Subset(test_dataset, test_ids)
        self.test_loader = DataLoader(test_dataset,
                                      batch_size=self.batch_size,
                                      shuffle=False,
                                      drop_last=True)

        for _data, _labels in self.test_loader:
            _data = self._erase_right(_data)
            yield feature_model(_data), _labels

    def make_infer_model(self) -> nn.Module:
        return InferModule()

    def make_infer_optimizer(self, infer_model: nn.Module) -> optim.Optimizer:
        return optim.SGD(infer_model.parameters(), lr=0.01, momentum=0.9)

    def train_a_batch(self, feature_projection: Dict[str, torch.Tensor], labels: torch.Tensor):
        fusion_tensor = torch.concat((feature_projection['demo_host'],
                                      feature_projection['demo_collaborator']), dim=1)
        self.optimizer.zero_grad()
        out = self.infer_model(fusion_tensor)
        loss = F.nll_loss(out, labels)
        loss.backward()
        self.optimizer.step()

    def test(self,
             batched_feature_projections: List[torch.Tensor],
             batched_labels: List[torch.Tensor]):
        start = time()
        test_loss = 0
        correct = 0
        for _feature_projection, _lables in zip(batched_feature_projections, batched_labels):
            fusion_tensor = torch.concat((_feature_projection['demo_host'],
                                          _feature_projection['demo_collaborator']), dim=1)
            out: torch.Tensor = self.infer_model(fusion_tensor)
            test_loss += F.nll_loss(out, _lables)
            pred = out.max(1, keepdim=True)[1]
            correct += pred.eq(_lables.view_as(pred)).sum().item()

        test_loss /= len(self.test_loader.dataset)
        accuracy = correct / len(self.test_loader.dataset)
        correct_rate = 100. * accuracy
        logger.info(f'Test set: Average loss: {test_loss:.4f}')
        logger.info(
            f'Test set: Accuracy: {accuracy} ({correct_rate:.2f}%)'
        )

        end = time()

        self.tb_writer.add_scalar('timer/run_time', end - start, self.current_round)
        self.tb_writer.add_scalar('test_results/average_loss', test_loss, self.current_round)
        self.tb_writer.add_scalar('test_results/accuracy', accuracy, self.current_round)
        self.tb_writer.add_scalar('test_results/correct_rate', correct_rate, self.current_round)


class DemoSecureHeteroCollaborator(SecureHeteroNNCollaboratorScheduler):

    def __init__(self,
                 feature_key: str,
                 project_layer_lr: int,
                 batch_size: int,
                 data_dir: str,
                 name: str = None,
                 schedule_timeout: int = 30,
                 is_feature_trainable: bool = True) -> None:
        super().__init__(feature_key=feature_key,
                         project_layer_lr=project_layer_lr,
                         name=name,
                         schedule_timeout=schedule_timeout,
                         is_feature_trainable=is_feature_trainable)
        self.batch_size = batch_size
        self.data_dir = data_dir

    def load_local_ids(self) -> List[str]:
        train_ids = [str(i) for i in range(10000, 30000)]
        test_ids = [str(i) for i in range(103000, 107000)]
        return train_ids + test_ids

    def split_dataset(self, id_intersection: Set[str]) -> Tuple[Set[str], Set[str]]:
        ids = [int(_id) for _id in id_intersection]
        ids.sort()
        train_ids = ids[:10000]
        test_ids = ids[10000:]

        logger.info(f'Got {len(train_ids)} intersecting samples for training.')
        logger.info(f'Got {len(test_ids)} intersecting samples for testing.')

        return set(train_ids), set(test_ids)

    def make_feature_model(self) -> nn.Module:
        return ConvNet()

    def make_feature_optimizer(self, feature_model: nn.Module) -> optim.Optimizer:
        return optim.SGD(feature_model.parameters(), lr=0.01, momentum=0.9)

    def _erase_left(self, _image: torch.Tensor) -> torch.Tensor:
        return _image[:, :, :, 14:]

    def iterate_train_feature(self,
                              feature_model: nn.Module,
                              train_ids: Set[str]) -> torch.Tensor:
        train_dataset = torchvision.datasets.MNIST(
            self.data_dir,
            train=True,
            download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,))
            ])
        )
        train_ids: List = list(train_ids)
        train_ids.sort(key=lambda x: md5(bytes(x + self.current_round)).digest())
        train_dataset = Subset(train_dataset, train_ids)
        self.train_loader = DataLoader(train_dataset,
                                       batch_size=self.batch_size,
                                       shuffle=False,
                                       drop_last=True)

        for _data, _ in self.train_loader:
            _data = self._erase_left(_data)
            yield feature_model(_data)

    def iterate_test_feature(self,
                             feature_model: nn.Module,
                             test_ids: Set[str]) -> torch.Tensor:
        test_dataset = torchvision.datasets.MNIST(
            self.data_dir,
            train=False,
            download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,))
            ])
        )
        test_ids = [(i - 100000) for i in test_ids]
        test_dataset = Subset(test_dataset, test_ids)
        self.test_loader = DataLoader(test_dataset,
                                      batch_size=self.batch_size,
                                      shuffle=False,
                                      drop_last=True)

        for _data, _ in self.test_loader:
            _data = self._erase_left(_data)
            yield feature_model(_data)


def get_task_id() -> str:
    return DEV_TASK_ID


def get_host(mode: str = VANILLA) -> Union[DemoHeteroHost, DemoSecureHeteroHost]:
    assert mode in (VANILLA, SECURE), f'unknown mode: {mode}'

    pickle_file = './scheduler_host.pickle'

    if os.path.exists(pickle_file):
        os.remove(pickle_file)

    if mode == VANILLA:
        scheduler = DemoHeteroHost(feature_key='demo_host',
                                   batch_size=128,
                                   data_dir=_DATA_DIR,
                                   name='demo_hetero_host',
                                   max_rounds=5,
                                   calculation_timeout=60,
                                   log_rounds=1)
    else:
        project_layer_config = [
            ('demo_host', 20, 20),
            ('demo_collaborator', 20, 20)
        ]
        # Too big batch size could kill the server
        scheduler = DemoSecureHeteroHost(feature_key='demo_host',
                                         project_layer_config=project_layer_config,
                                         project_layer_lr=0.01,
                                         batch_size=128,
                                         data_dir=_DATA_DIR,
                                         name='demo_hetero_host',
                                         max_rounds=5,
                                         calculation_timeout=60,
                                         log_rounds=1)

    with open(pickle_file, 'w+b') as pf:
        pickle.dump(scheduler, pf)

    with open(pickle_file, 'rb') as f:
        scheduler = pickle.load(f)
        return scheduler


def get_collaborator(mode: str = VANILLA) -> Union[DemoHeteroCollaborator,
                                                   DemoSecureHeteroCollaborator]:
    assert mode in (VANILLA, SECURE), f'unknown mode: {mode}'

    pickle_file = './scheduler_collaborator.pickle'

    if os.path.exists(pickle_file):
        os.remove(pickle_file)

    if mode == VANILLA:
        scheduler = DemoHeteroCollaborator(feature_key='demo_collaborator',
                                           batch_size=128,
                                           data_dir=_DATA_DIR,
                                           name='demo_hetero_collaborator')

    else:
        # Too big batch size could kill the server
        scheduler = DemoSecureHeteroCollaborator(feature_key='demo_collaborator',
                                                 project_layer_lr=0.01,
                                                 batch_size=128,
                                                 data_dir=_DATA_DIR,
                                                 name='demo_hetero_collaborator')

    with open(pickle_file, 'w+b') as pf:
        pickle.dump(scheduler, pf)

    with open(pickle_file, 'rb') as f:
        scheduler = pickle.load(f)
        return scheduler
