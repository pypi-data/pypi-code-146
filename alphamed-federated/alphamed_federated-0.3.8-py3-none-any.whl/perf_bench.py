"""Take a simple performance benchmark."""

import cProfile
import os
import pstats
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from time import sleep
from typing import Tuple

import requests
import torch
import torch.nn as nn
import torch.nn.functional as F


class SimplePerfBench:

    TIMEOUT = 30

    def __init__(self) -> None:
        self.name = 'perf_bench'
        self.batch_size = 256
        self.learning_rate = 0.01
        self.momentum = 0.5

        self.data_dir = os.path.join(self.name, 'data')

        self.random_seed = 42
        torch.manual_seed(self.random_seed)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def _build_model(self) -> nn.Module:
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

        return ConvNet()

    def _run_network_benchmark(self) -> float:
        """Perform some download operations and return the time cost."""
        url = 'https://dev-sapce-1309103037.cos.ap-nanjing.myqcloud.com/ones'
        repeat = 5
        with cProfile.Profile() as pr:
            for _ in range(repeat):
                requests.get(url)
        ps = pstats.Stats(pr)
        return ps.total_tt

    def _run_calculation_benchmark(self) -> float:
        """Perform some inferring operations and return the time cost."""
        model = self._build_model()
        model.train()
        optimizer = torch.optim.SGD(model.parameters(),
                                    lr=self.learning_rate,
                                    momentum=self.momentum)
        repeat = 10
        with cProfile.Profile() as pr:
            for _ in range(repeat):
                data = torch.rand((1024, 1, 28, 28))
                data = data * 2 - 1
                labels = torch.randint(0, 10, (1024,))
                data, labels = data.to(self.device), labels.to(self.device)
                optimizer.zero_grad()
                output = model(data)
                loss = F.nll_loss(output, labels)
                loss.backward()
                optimizer.step()
        ps = pstats.Stats(pr)
        return ps.total_tt

    def _run_benchmark(self, results: list) -> None:
        """Run performence benchmark and return results in background.

        :args
            results:
                A reference to a list container for saving benchmark results.
        """
        net_time = self._run_network_benchmark()
        print(f'{net_time=}')
        calc_time = self._run_calculation_benchmark()
        print(f'{calc_time=}')
        results.extend((net_time, calc_time))

    def run(self) -> Tuple[float, float]:
        """Run performence benchmark and return results.

        Return actual results if benchmark task finish in time, otherwize worst results.

        :return
            (net_time, calc_time)
        """
        results = []
        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(self._run_benchmark, results)
        for _ in range(self.TIMEOUT):
            sleep(0.1)
            if results and len(results) == 2:
                net_time, calc_time = results
                return net_time, calc_time
        return self.TIMEOUT, self.TIMEOUT


@dataclass
class SimplePerfBenchResult:

    runner_id: str
    net_time: float
    calc_time: float

    @classmethod
    def from_json(cls, data: dict) -> 'SimplePerfBenchResult':
        """Instantiate a SimplePerfBenchResult object from json data."""
        assert isinstance(data, dict), f'invalid json data: {data}'
        runner_id = data.get('runner_id')
        assert runner_id and isinstance(runner_id, str), f'invalid runner_id: {runner_id}'
        net_time = data.get('net_time')
        assert (
            net_time and isinstance(runner_id, float) and net_time > 0
        ), f'invalid net_time: {net_time}'
        calc_time = data.get('calc_time')
        assert (
            calc_time and isinstance(calc_time, float) and calc_time > 0
        ), f'invalid calc_time: {calc_time}'
        return SimplePerfBenchResult(runner_id=runner_id,
                                     net_time=net_time,
                                     calc_time=calc_time)
