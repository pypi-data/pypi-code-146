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

import time
from abc import abstractmethod
from logging import DEBUG, INFO
from typing import Any, List, Optional, Union

import numpy as np

from modalic.api.common.communication import (
    CommunicationLayer,
    sync_model_version,
    update,
)
from modalic.config import Conf
from modalic.data.misc import get_dataset_length
from modalic.logging.logging import logger
from modalic.utils import shared
from modalic.utils.misc import validate_config, validate_kwargs
from modalic.utils.serde import parameters_to_weights


class Client(CommunicationLayer):
    r"""Client object implements all the functionality that enables Federated Learning.
    It serves also for a base class for the specific child classes that implement
    specific functions for specific ML frameworks.

    :param trainer: Custom Trainer object.
    :param conf: :class:`modalic.Conf` that stores all the parameters concerning the process.
    """

    def __init__(
        self,
        trainer: Any,
        conf: Optional[Union[dict, Conf]] = None,
        # client_id: Optional[int] = 0,
        **kwargs,
    ):
        # Ensure argument validity.
        validate_config(conf)
        # These properties should be set by the user via keyword arguments.
        allowed_kwargs = {"client_id", "dataset"}
        validate_kwargs(kwargs, allowed_kwargs)

        self.trainer = trainer
        if conf is None or isinstance(conf, dict):
            self.conf = Conf.create_conf(conf)
        else:
            self.conf = conf

        if "client_id" in kwargs:
            self.conf.client_id = kwargs["client_id"]

        # Setting all the internal necessary attributes.
        self._server_address = self.conf.server_address
        self._client_id = self.conf.client_id
        self._training_rounds = self.conf.training_rounds
        self._model_shape = self._get_model_shape()
        self._dtype = self._get_model_dtype()
        if hasattr(self.trainer, "dataset"):
            self._stake = get_dataset_length(self.trainer.dataset)
        else:
            logger.log(
                DEBUG,
                f"Object {self.trainer} has no attribute dataset.\
                Federation will proceed with default value 1 as the size of the dataset.",
            )
            self._stake = 1

        self._loss = 0.0
        self._round_id = 0

    @property
    def client_id(self) -> int:
        r"""Returns the client identifier."""
        return self._client_id

    @property
    def server_address(self) -> int:
        r"""Returns the server address the client uses to connect."""
        return self._server_address

    @property
    def dtype(self) -> str:
        r"""Returns the underlying data type that is set via Conf."""
        return self._dtype

    @property
    def round_id(self) -> int:
        r"""Holds state of the training round the local model is in."""
        return self._round_id

    @property
    def loss(self) -> float:
        r"""Holds state of the current loss computed by the loss function of the clients model."""
        return self._loss

    @property
    def model_shape(self) -> List[np.ndarray]:
        r"""Returns the shape of model architecture the client holds."""
        return self._model_shape

    @abstractmethod
    def _set_weights(self, weights: shared.Weights) -> None:
        r"""Sets the model weights from a list of NumPy ndarrays.

        :param weights: Model weights as a list of NumPy ndarrays.
        """
        raise NotImplementedError()

    @abstractmethod
    def _get_weights(self) -> shared.Weights:
        r"""Returns model weights as a list of NumPy ndarrays."""
        raise NotImplementedError()

    @abstractmethod
    def _get_model_shape(self) -> List[np.ndarray]:
        r"""Extracts the shape of the model.

        :returns: List of np.array representing the model shape.
        """
        raise NotImplementedError()

    @abstractmethod
    def _get_model_dtype(self) -> str:
        r"""Extracts the data type of the model."""
        raise NotImplementedError()

    def _update(self) -> None:
        r"""Sends an updated model version to the server."""
        update(
            self._client_id,
            self._server_address,
            self._get_weights(),
            self._dtype,
            self._round_id,
            self._stake,
            self._loss,
        )

    def _get_global_model(self, retry: float = 5.0) -> None:
        r"""Client request to get the latest version of the global model from server.

        :param model_shape: Holds the shape of the model architecture for serialization & deserialization.
        :param retry: (Default: ``5.0``) Defines the periode after which a retry is performed.
        """
        params = sync_model_version(
            self._client_id, self._server_address, self._round_id, retry_period=retry
        )
        if params is not None:
            weights = parameters_to_weights(params, self._model_shape, self._dtype)
            self._set_weights(weights)
            logger.log(
                INFO,
                f"Client {self._client_id} received global model from aggregation server.",
            )

    def _train(self) -> None:
        r"""Runs the train method of custom trainer object for single model."""
        try:
            self.model, self._loss = self.trainer.train()
        except AttributeError:
            raise AttributeError(f"{self.trainer} has no train() functionality.")

    def _run_single_round(self) -> None:
        r"""Runs a single trainings round for a single modalic client."""
        self._get_global_model()
        self._round_id += 1
        self._train()
        logger.log(
            INFO,
            f"Client {self._client_id} | training round: {self._round_id} | loss: {self._loss}",
        )
        self._update()
        time.sleep(self.conf.timeout)

    def _loop_training(self) -> None:
        r"""Looping the whole training process for a single modalic client."""
        while self._round_id < self._training_rounds:
            self._run_single_round()

    # def eval(self) -> None:
    #     pass

    # def val_get_global_model(self, params: shared.Parameters) -> bool:
    #     r"""Validates the response from server."""

    # def _obj_sanity_check_(self):
    #     pass
