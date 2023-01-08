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

from typing import Any, List, Optional, Union

import numpy as np

from modalic.api.common.client import Client
from modalic.api.tf.tf_utils import (
    _get_tf_model_dtype,
    _get_tf_model_shape,
    _get_tf_weights,
    _set_tf_weights,
)
from modalic.config import Conf
from modalic.utils import shared


class TfClient(Client):
    r"""
    Tensorflow Keras compatible client object which abstracts all the distributed communication.
    Serves as a simple layer and API that enables participating within a
    Federated Learning process.

    :param trainer: Custom Tensorflow Keras Trainer object implementing all the learning procedure.
        See the example below for the structure, functions & attributes or check out usage in /examples folder.
    :param conf: (Optional) :class:`modalic.Conf` that stores all the parameters concerning the process.
    """

    def __init__(
        self,
        trainer: Any,
        conf: Optional[Union[dict, Conf]] = None,
        client_id: Optional[int] = 0,
        # data: Optional[Any] = None,
    ):
        try:
            self.model = trainer.model
        except AttributeError:
            raise AttributeError(
                f"Custom {trainer} object has no model. Please define the model architecture that should be trained."
            )

        super().__init__(trainer, conf)

    def _set_weights(self, weights: shared.Weights) -> None:
        r"""Sets the model weights from a list of NumPy ndarrays.

        :param weights: Model weights as a list of NumPy ndarrays.
        """
        self.model = _set_tf_weights(self.model, weights)

    def _get_weights(self) -> shared.Weights:
        r"""Returns model weights as a list of NumPy ndarrays."""
        return _get_tf_weights(self.model)

    def _get_model_shape(self) -> List[np.ndarray]:
        r"""Extracts the shape of the tensorflow model.

        :returns: List of np.array representing the model shape.
            (Example: [np.array([1, 4]), np.array([1])])
        """
        return _get_tf_model_shape(self.model)

    def _get_model_dtype(self) -> str:
        r"""Extracts the data type of the tensorflow model."""
        return _get_tf_model_dtype(self.model)

    def run(self, mode: str = "train"):
        r"""Endpoint for running the Machine Learning setup as Modalic client."""
        if mode == "train":
            self._loop_training()
        else:
            raise AttributeError(
                f"The input value of mode: {mode} unknown. Consider choosing either 'train' or 'eval'."
            )
