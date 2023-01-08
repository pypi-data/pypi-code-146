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

from __future__ import annotations

from typing import Any, List, Optional, Union

import numpy as np

from modalic.api.common.client import Client
from modalic.api.torch.torch_utils import (
    _get_torch_model_dtype,
    _get_torch_model_shape,
    _get_torch_weights,
    _set_torch_weights,
)
from modalic.config import Conf
from modalic.utils import shared


class PytorchClient(Client):
    r"""
    Pytorch compatible client object which abstracts all the distributed communication.
    Serves as a simple layer and API that enables participating within a
    Federated Learning process.

    :param trainer: Custom Pytorch Trainer object implementing all the learning procedure.
        See the example below for the structure, functions & attributes or check out usage in /examples folder.
    :param conf: (Optional) Configuration object that stores all the parameters concerning the process.
        Although conf is optional, should be set as important parameters are stored there that
        will influence the sucess of the process. Union type as it can be either :class:`modalic.Conf` directly or
        a dict type that gets converted to :class:`modalic.Conf`. See below for an example.
    :param client_id: (Optional) Client ID. This parameter is optional as it can also be set in the conf param directly.
        Will overwrite the client_id in conf anyway.
    :param data: Dataset object that can be set for the Pytorch Trainer object.

    :Example:
        >>> # Custom Trainer object
        >>> class Trainer():
        >>>     def __init__(self):
        >>>         self.model = CustomModel()
        >>>         self.dataset = CustomDataloader()
        >>>         self.trainloader = torch.utils.data.DataLoader(
        >>>             self.dataset, batch_size=32, shuffle=True
        >>>         )
        >>>         ...
        >>>     def train(self):
        >>>         # Implements training logic.
        >>>         ...
        >>>
        >>> # Configuration object provided by modalic.
        >>> client_id = 1
        >>> conf = modalic.Conf.create_conf(conf, client_id)
        >>> # Instantiate the Modalic PytorchClient
        >>> client = modalic.PytorchClient(Trainer(), conf)
        >>> # Run the Federated Learning via
        >>> client.run()

    :raises AttributeError: Input object trainer has to contain a model & train() function.
    """

    def __init__(
        self,
        trainer: Any,
        conf: Optional[Union[dict, Conf]] = None,
        client_id: Optional[int] = 0,
        # dataloaders: Optional[Any] = None
    ):
        try:
            self.model = trainer.model
        except AttributeError:
            raise AttributeError(
                f"Custom {trainer} object has no model. Please define the model architecture that should be trained."
            )
        super().__init__(trainer, conf)

    def __repr__(self) -> str:
        r"""Returns string representative of object."""
        return f"Modalic Pytorch Client Object with ID {self._client_id}"

    def _set_weights(self, weights: shared.Weights) -> None:
        r"""Sets the model weights from a list of NumPy ndarrays.

        :param weights: Model weights as a list of NumPy ndarrays.
        """
        self.model = _set_torch_weights(self.model, weights)

    def _get_weights(self) -> shared.Weights:
        r"""Returns model weights as a list of NumPy ndarrays."""
        return _get_torch_weights(self.model)

    def _get_model_shape(self) -> List[np.ndarray]:
        r"""Extracts the shape of the pytorch model.

        :returns: List of np.array representing the model shape.
            (Example: [np.array([1, 4]), np.array([1])])
        """
        return _get_torch_model_shape(self.model)

    def _get_model_dtype(self) -> str:
        r"""Extracts the data type of the pytorch model."""
        return _get_torch_model_dtype(self.model)

    def run(self, mode: str = "train"):
        r"""Endpoint for running the Machine Learning setup as Modalic Pytorch client."""
        if mode == "train":
            self._loop_training()
        else:
            raise AttributeError(
                f"The input value of mode: {mode} unknown. Consider choosing either 'train' or 'eval'."
            )
