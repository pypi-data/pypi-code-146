#  Copyright (c) modalic 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

"""Multithreaded Pool of Modalic Clients."""
import multiprocessing
import traceback
from logging import DEBUG, ERROR, INFO
from typing import Any, List

from modalic.logging.logging import logger


class ClientPool:
    r"""Object holds and manages a bunch of individual simulated clients.

    :param clients: List of modalic client object. Options are [`PytorchClient`] or [`TfClient`]
    :param num_clients: Number of clients you want to run the federated learning with.
    """

    def __init__(self, clients: List[Any], num_clients: int = 0):
        self.clients = clients
        self.num_clients = len(clients) if num_clients == 0 else num_clients

        # Health checking
        assert (
            len(self.clients) >= self.num_clients
        ), f"Specfified number of clients: {self.num_clients} exceeds number of instantiated modalic clients: {len(self.clients)}."

        logger.log(INFO, f"Federated Learning with {self.num_clients} clients started.")

    def run(self) -> None:
        r"""Endpoint to execute the whole client pool in parallel."""
        self.spawn_pool(self.num_clients)

    def spawn_pool(self, num_workers: int = 1) -> None:
        r"""Launching a pool of separated clients using concurrent.futures ThreadPoolExecutor.

        :param num_workers: Number of workers.
        """
        with multiprocessing.Pool(processes=num_workers) as pool:
            pool.map(self.exec_single_thread, range(1, num_workers + 1))

    def exec_single_thread(self, name: str) -> None:
        r"""Executes the single thread object which holds the main functionality."""
        logger.log(INFO, f"Thread {name} for simulating client {name} started.")
        try:
            self.clients[int(name) - 1].run()
        except Exception:
            logger.log(ERROR, f"Running thread {name} failed.")
            logger.log(DEBUG, traceback.print_exc())

        logger.log(INFO, f"Thread {name} for simulating client {name} finished.")
