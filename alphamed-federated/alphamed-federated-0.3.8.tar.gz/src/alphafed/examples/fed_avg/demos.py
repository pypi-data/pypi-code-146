"""Process demo."""

import os
from time import time
from typing import Dict

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torch import optim
from torch.utils.data import DataLoader

from ... import logger
from ...fed_avg import FedAvgScheduler, FedSGDScheduler, SecureFedAvgScheduler
from ...fed_avg.dp_fed_avg import DPFedAvgScheduler
from . import DEV_TASK_ID
from .demo_FedIRM import DemoFedIRM

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


VANILLA = 'vanilla'
SGD = 'sgd'
DP = 'dp'
SECURE = 'secure'
FED_IRM = 'fedirm'


class ConvNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=10, kernel_size=5)
        self.conv2 = nn.Conv2d(in_channels=10, out_channels=20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(in_features=320, out_features=50)
        self.fc2 = nn.Linear(in_features=50, out_features=10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=-1)


class DemoAvg(FedAvgScheduler):

    def __init__(self,
                 min_clients: int,
                 max_clients: int,
                 name: str = None,
                 max_rounds: int = 0,
                 merge_epochs: int = 1,
                 calculation_timeout: int = 300,
                 log_rounds: int = 0,
                 is_centralized: bool = True,
                 involve_aggregator: bool = False,
                 batch_size: int = 64,
                 learning_rate: float = 0.01,
                 momentum: float = 0.5) -> None:
        super().__init__(min_clients=min_clients,
                         max_clients=max_clients,
                         name=name,
                         max_rounds=max_rounds,
                         merge_epochs=merge_epochs,
                         calculation_timeout=calculation_timeout,
                         log_rounds=log_rounds,
                         is_centralized=is_centralized,
                         involve_aggregator=involve_aggregator)
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.momentum = momentum

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.seed = 42
        torch.manual_seed(self.seed)

    def build_model(self) -> nn.Module:
        model = ConvNet()
        return model.to(self.device)

    def build_optimizer(self, model: nn.Module) -> optim.Optimizer:
        assert self.model, 'must initialize model first'
        return optim.SGD(self.model.parameters(),
                         lr=self.learning_rate,
                         momentum=self.momentum)

    def build_train_dataloader(self) -> DataLoader:
        return DataLoader(
            torchvision.datasets.MNIST(
                os.path.join(self.name, 'data'),
                train=True,
                download=True,
                transform=torchvision.transforms.Compose([
                    torchvision.transforms.ToTensor(),
                    torchvision.transforms.Normalize((0.1307,), (0.3081,))
                ])
            ),
            batch_size=self.batch_size,
            shuffle=True
        )

    def build_test_dataloader(self) -> DataLoader:
        return DataLoader(
            torchvision.datasets.MNIST(
                os.path.join(self.name, 'data'),
                train=False,
                download=True,
                transform=torchvision.transforms.Compose([
                    torchvision.transforms.ToTensor(),
                    torchvision.transforms.Normalize((0.1307,), (0.3081,))
                ])
            ),
            batch_size=self.batch_size,
            shuffle=False
        )

    def state_dict(self) -> Dict[str, torch.Tensor]:
        return self.model.state_dict()

    def load_state_dict(self, state_dict: Dict[str, torch.Tensor]):
        self.model.load_state_dict(state_dict)

    def validate_context(self):
        super().validate_context()
        assert self.train_loader and len(self.train_loader) > 0, 'failed to load train data'
        logger.info(f'There are {len(self.train_loader.dataset)} samples for training.')
        assert self.test_loader and len(self.test_loader) > 0, 'failed to load test data'
        logger.info(f'There are {len(self.test_loader.dataset)} samples for testing.')

    def train_an_epoch(self) -> None:
        self.model.train()
        for data, labels in self.train_loader:
            data: torch.Tensor
            labels: torch.Tensor
            data, labels = data.to(self.device), labels.to(self.device)
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = F.nll_loss(output, labels)
            loss.backward()
            self.optimizer.step()

    def test(self):
        start = time()
        self.model.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            for data, labels in self.test_loader:
                data: torch.Tensor
                labels: torch.Tensor
                data, labels = data.to(self.device), labels.to(self.device)
                output: torch.Tensor = self.model(data)
                test_loss += F.nll_loss(output, labels, reduction='sum').item()
                pred = output.max(1, keepdim=True)[1]
                correct += pred.eq(labels.view_as(pred)).sum().item()

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


class DemoSGD(FedSGDScheduler):

    def __init__(self,
                 min_clients: int,
                 name: str = None,
                 max_rounds: int = 0,
                 calculation_timeout: int = 300,
                 log_rounds: int = 0,
                 is_centralized: bool = True,
                 learning_rate: float = 0.01,
                 momentum: float = 0.5) -> None:
        super().__init__(min_clients=min_clients,
                         name=name,
                         max_rounds=max_rounds,
                         calculation_timeout=calculation_timeout,
                         log_rounds=log_rounds,
                         is_centralized=is_centralized)
        self.learning_rate = learning_rate
        self.momentum = momentum

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.seed = 42
        torch.manual_seed(self.seed)

    def build_model(self) -> nn.Module:
        model = ConvNet()
        return model.to(self.device)

    def build_optimizer(self, model: nn.Module) -> optim.Optimizer:
        assert self.model, 'must initialize model first'
        return optim.SGD(self.model.parameters(),
                         lr=self.learning_rate,
                         momentum=self.momentum)

    def build_train_dataloader(self) -> DataLoader:
        dataset = torchvision.datasets.MNIST(
            os.path.join(self.name, 'data'),
            train=True,
            download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,))
            ])
        )
        return DataLoader(dataset=dataset, batch_size=len(dataset), shuffle=True)

    def build_test_dataloader(self) -> DataLoader:
        return DataLoader(
            torchvision.datasets.MNIST(
                os.path.join(self.name, 'data'),
                train=False,
                download=True,
                transform=torchvision.transforms.Compose([
                    torchvision.transforms.ToTensor(),
                    torchvision.transforms.Normalize((0.1307,), (0.3081,))
                ])
            ),
            batch_size=64,  # no need be total number in test phrase
            shuffle=False
        )

    def state_dict(self) -> Dict[str, torch.Tensor]:
        return self.model.state_dict()

    def load_state_dict(self, state_dict: Dict[str, torch.Tensor]):
        self.model.load_state_dict(state_dict)

    def validate_context(self):
        super().validate_context()
        assert self.train_loader and len(self.train_loader) > 0, 'failed to load train data'
        self.push_log(f'There are {len(self.train_loader.dataset)} samples for training.')
        assert self.test_loader and len(self.test_loader) > 0, 'failed to load test data'
        self.push_log(f'There are {len(self.test_loader.dataset)} samples for testing.')

    def train_an_epoch(self) -> None:
        self.model.train()
        for data, labels in self.train_loader:
            data: torch.Tensor
            labels: torch.Tensor
            data, labels = data.to(self.device), labels.to(self.device)
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = F.nll_loss(output, labels)
            loss.backward()
            self.optimizer.step()

    def test(self):
        start = time()
        self.model.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            test_loader = self.build_test_dataloader()
            for data, labels in test_loader:
                data: torch.Tensor
                labels: torch.Tensor
                data, labels = data.to(self.device), labels.to(self.device)
                output: torch.Tensor = self.model(data)
                test_loss += F.nll_loss(output, labels, reduction='sum').item()
                pred = output.max(1, keepdim=True)[1]
                correct += pred.eq(labels.view_as(pred)).sum().item()

        test_loss /= len(test_loader.dataset)
        accuracy = correct / len(test_loader.dataset)
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


class DemoSecure(SecureFedAvgScheduler):

    def __init__(self,
                 min_clients: int,
                 max_clients: int,
                 t: int,
                 name: str = None,
                 max_rounds: int = 0,
                 merge_epochs: int = 1,
                 calculation_timeout: int = 300,
                 log_rounds: int = 0,
                 is_centralized: bool = True) -> None:
        super().__init__(min_clients=min_clients,
                         max_clients=max_clients,
                         t=t,
                         name=name,
                         max_rounds=max_rounds,
                         merge_epochs=merge_epochs,
                         calculation_timeout=calculation_timeout,
                         log_rounds=log_rounds,
                         is_centralized=is_centralized)
        self.batch_size = 64
        self.learning_rate = 0.01
        self.momentum = 0.5
        self.random_seed = 42

        torch.manual_seed(self.random_seed)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def build_model(self) -> nn.Module:
        model = ConvNet()
        return model.to(self.device)

    def build_optimizer(self, model: nn.Module) -> optim.Optimizer:
        return optim.SGD(self.model.parameters(),
                         lr=self.learning_rate,
                         momentum=self.momentum)

    def build_train_dataloader(self) -> DataLoader:
        return DataLoader(
            torchvision.datasets.MNIST(
                os.path.join(self.name, 'data'),
                train=True,
                download=True,
                transform=torchvision.transforms.Compose([
                    torchvision.transforms.ToTensor(),
                    torchvision.transforms.Normalize((0.1307,), (0.3081,))
                ])
            ),
            batch_size=self.batch_size,
            shuffle=True
        )

    def build_test_dataloader(self) -> DataLoader:
        return DataLoader(
            torchvision.datasets.MNIST(
                os.path.join(self.name, 'data'),
                train=False,
                download=True,
                transform=torchvision.transforms.Compose([
                    torchvision.transforms.ToTensor(),
                    torchvision.transforms.Normalize((0.1307,), (0.3081,))
                ])
            ),
            batch_size=self.batch_size,
            shuffle=False
        )

    def state_dict(self) -> Dict[str, torch.Tensor]:
        return self.model.state_dict()

    def load_state_dict(self, state_dict: Dict[str, torch.Tensor]):
        self.model.load_state_dict(state_dict)

    def validate_context(self):
        super().validate_context()
        assert self.train_loader and len(self.train_loader) > 0, 'failed to load train data'
        self.push_log(f'There are {len(self.train_loader.dataset)} samples for training.')
        assert self.test_loader and len(self.test_loader) > 0, 'failed to load test data'
        self.push_log(f'There are {len(self.test_loader.dataset)} samples for testing.')

    def train_an_epoch(self) -> None:
        self.model.train()
        for data, labels in self.train_loader:
            data: torch.Tensor
            labels: torch.Tensor
            data, labels = data.to(self.device), labels.to(self.device)
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = F.nll_loss(output, labels)
            loss.backward()
            self.optimizer.step()

    def test(self):
        self.model.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            test_loader = self.build_test_dataloader()
            for data, labels in test_loader:
                data: torch.Tensor
                labels: torch.Tensor
                data, labels = data.to(self.device), labels.to(self.device)
                output: torch.Tensor = self.model(data)
                test_loss += F.nll_loss(output, labels, reduction='sum').item()
                pred = output.max(1, keepdim=True)[1]
                correct += pred.eq(labels.view_as(pred)).sum().item()

        test_loss /= len(test_loader.dataset)
        correct_rate = 100. * correct / len(test_loader.dataset)
        logger.info(f'Test set: Average loss: {test_loss:.4f}')
        logger.info(
            f'Test set: Accuracy: {correct}/{len(test_loader.dataset)} ({correct_rate:.2f}%)'
        )

        self.tb_writer.add_scalar('test_results/average_loss', test_loss, self.current_round)
        self.tb_writer.add_scalar('test_results/correct_rate', correct_rate, self.current_round)


class DemoDP(DPFedAvgScheduler):

    def __init__(self,
                 min_clients: int,
                 w_cap: int,
                 q: float,
                 S: float,
                 z: float,
                 name: str = None,
                 max_rounds: int = 0,
                 merge_epochs: int = 1,
                 calculation_timeout: int = 300,
                 log_rounds: int = 0,
                 is_centralized: bool = True,
                 involve_aggregator: bool = False) -> None:
        super().__init__(min_clients=min_clients,
                         w_cap=w_cap,
                         q=q,
                         S=S,
                         z=z,
                         name=name,
                         max_rounds=max_rounds,
                         merge_epochs=merge_epochs,
                         calculation_timeout=calculation_timeout,
                         log_rounds=log_rounds,
                         is_centralized=is_centralized,
                         involve_aggregator=involve_aggregator)
        self.batch_size = 64
        self.learning_rate = 0.01
        self.momentum = 0.5
        self.random_seed = 42

        torch.manual_seed(self.random_seed)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def build_model(self) -> nn.Module:
        model = ConvNet()
        return model.to(self.device)

    def build_optimizer(self, model: nn.Module) -> optim.Optimizer:
        return optim.SGD(self.model.parameters(),
                         lr=self.learning_rate,
                         momentum=self.momentum)

    def build_train_dataloader(self) -> DataLoader:
        return DataLoader(
            torchvision.datasets.MNIST(
                os.path.join(self.name, 'data'),
                train=True,
                download=True,
                transform=torchvision.transforms.Compose([
                    torchvision.transforms.ToTensor(),
                    torchvision.transforms.Normalize((0.1307,), (0.3081,))
                ])
            ),
            batch_size=self.batch_size,
            shuffle=True
        )

    def build_test_dataloader(self) -> DataLoader:
        return DataLoader(
            torchvision.datasets.MNIST(
                os.path.join(self.name, 'data'),
                train=False,
                download=True,
                transform=torchvision.transforms.Compose([
                    torchvision.transforms.ToTensor(),
                    torchvision.transforms.Normalize((0.1307,), (0.3081,))
                ])
            ),
            batch_size=self.batch_size,
            shuffle=False
        )

    def state_dict(self) -> Dict[str, torch.Tensor]:
        return self.model.state_dict()

    def load_state_dict(self, state_dict: Dict[str, torch.Tensor]):
        self.model.load_state_dict(state_dict)

    def validate_context(self):
        super().validate_context()
        assert self.train_loader and len(self.train_loader) > 0, 'failed to load train data'
        self.push_log(f'There are {len(self.train_loader.dataset)} samples for training.')
        assert self.test_loader and len(self.test_loader) > 0, 'failed to load test data'
        self.push_log(f'There are {len(self.test_loader.dataset)} samples for testing.')

    def train_a_batch(self, *batch_train_data):
        data: torch.Tensor
        labels: torch.Tensor
        data, labels = batch_train_data
        data, labels = data.to(self.device), labels.to(self.device)
        self.optimizer.zero_grad()
        output = self.model(data)
        loss = F.nll_loss(output, labels)
        loss.backward()
        self.optimizer.step()

    def test(self):
        self.model.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            test_loader = self.build_test_dataloader()
            for data, labels in test_loader:
                data: torch.Tensor
                labels: torch.Tensor
                data, labels = data.to(self.device), labels.to(self.device)
                output: torch.Tensor = self.model(data)
                test_loss += F.nll_loss(output, labels, reduction='sum').item()
                pred = output.max(1, keepdim=True)[1]
                correct += pred.eq(labels.view_as(pred)).sum().item()

        test_loss /= len(test_loader.dataset)
        correct_rate = 100. * correct / len(test_loader.dataset)
        logger.info(f'Test set: Average loss: {test_loss:.4f}')
        logger.info(
            f'Test set: Accuracy: {correct}/{len(test_loader.dataset)} ({correct_rate:.2f}%)'
        )

        self.tb_writer.add_scalar('test_results/average_loss', test_loss, self.current_round)
        self.tb_writer.add_scalar('test_results/correct_rate', correct_rate, self.current_round)


def get_task_id() -> str:
    return DEV_TASK_ID


def get_scheduler(mode: str = VANILLA) -> FedAvgScheduler:
    assert mode in (VANILLA, SGD, SECURE, DP, FED_IRM), f'unknown mode: {mode}'

    pickle_file = './scheduler.pickle'
    import cloudpickle as pickle

    if os.path.exists(pickle_file):
        os.remove(pickle_file)

    if mode == VANILLA:
        scheduler = DemoAvg(min_clients=3,
                            max_clients=3,
                            name='demo_fed_avg',
                            max_rounds=5,
                            log_rounds=1,
                            calculation_timeout=60,
                            involve_aggregator=True)

    elif mode == SGD:
        scheduler = DemoSGD(min_clients=3,
                            name='demo_fed_sgd',
                            max_rounds=50,
                            log_rounds=1,
                            calculation_timeout=60)

    elif mode == DP:
        scheduler = DemoDP(min_clients=2,
                           w_cap=20000,
                           q=0.9,
                           S=1,
                           z=0.1,
                           name='demo_dp_fed_avg',
                           max_rounds=5,
                           log_rounds=1,
                           calculation_timeout=60,
                           involve_aggregator=True)

    elif mode == SECURE:
        scheduler = DemoSecure(min_clients=3,
                               max_clients=3,
                               t=2,
                               name='demo_secure_avg',
                               max_rounds=5,
                               log_rounds=1,
                               calculation_timeout=120)

    elif mode == FED_IRM:
        root_dir = '/data/alphamed/alphamed-dataset/tutorials/FedIRM/'
        scheduler = DemoFedIRM(
            min_clients=4,
            max_clients=4,
            root_path=os.path.join(root_dir, 'gtr21/ISIN-2018/train_image_224'),
            csv_file_train=os.path.join(root_dir, 'train.csv'),
            csv_file_test=os.path.join(root_dir, 'test.csv'),
            name='demo_Fed_IRM',
            max_rounds=50,
            log_rounds=5,
            calculation_timeout=3600,
            involve_aggregator=True
        )

    with open(pickle_file, 'w+b') as pf:
        pickle.dump(scheduler, pf)

    with open(pickle_file, 'rb') as f:
        scheduler = pickle.load(f)
        return scheduler
