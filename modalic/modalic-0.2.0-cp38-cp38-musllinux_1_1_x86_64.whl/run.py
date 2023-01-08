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
"""Spawn & run a Client."""
from typing import Optional

from modalic.client import Client, InternalClient, mosaic_python_sdk
from modalic.config import Conf


def run_client(client: Client, conf: Optional[Conf] = None):
    r"""The main endpoint on the client side. This function will intialize an
    internal modalic client and starts it in a separate thread.

    :param client: Custom Client object designed by the developer outside of modalic.
        An example can be seen down below:
        >>> class FLClient(modalic.Client):
        >>>     def __init__(self, dataset):
        >>>         self.model = Net()
                    self.dataset = torch.utils.data.DataLoader(dataset, batch_size=32)
                    ...

        >>>     def train(self):
        >>>         ...
        >>>     get_model_shape(self):
        >>>         ...
        >>>     get_model_dtype(self):
        >>>         ...
        >>>     serialize_local_model(self):
        >>>         ...
        >>>     deserialize_global_model(self):
        >>>         ...
    """
    # Init the internal logger.
    #
    # Logs the underlying logical steps. Particularly helpful for debugging.
    mosaic_python_sdk.init_logging()

    # Internal Client which implements the backend Federated protocol logic.
    #
    modalic_client = InternalClient(client, conf)
    # Spawns the InternalClient in a separate thread by using threading library.
    # `start` calls the `run` method of `InternalClient`.
    #
    # https://docs.python.org/3.8/library/threading.html#threading.Thread.start
    modalic_client.start()

    # Join the main thread.
    #
    # This blocks the calling main thread until the thread whole `join` method
    # is called terminates.
    try:
        modalic_client.join()
    except KeyboardInterrupt:
        modalic_client.stop()
