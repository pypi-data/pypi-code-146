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

"""Client Object API."""
import threading
from logging import DEBUG, ERROR, INFO, WARNING
from typing import Any, List, Optional, Union

import backoff
import numpy as np

try:
    from modalic.client import mosaic_python_sdk
except ImportError:
    import warnings

    warnings.warn("ImportError: .so bindings mosaic_python_sdk could not be imported.")

from modalic.config import Conf
from modalic.logging.logging import logger

from .client import Client


class InternalClient(threading.Thread):
    r"""Client object implements all the functionality that enables Federated Learning.
    It serves also for a base class for the specific child classes that implement
    specific functions for specific ML frameworks.

    :param client: Custom Client object.
    :param conf: :class:`modalic.Conf` that stores all the parameters concerning
        the Federated Learning process.
    :param state:
    """

    def __init__(
        self,
        client: Client,
        conf: Optional[Union[dict, Conf]] = None,
        state: Optional[List[int]] = None,
    ):
        # Configuration init.
        #
        if conf is None or isinstance(conf, dict):
            self.conf = Conf.create_conf(conf)
        else:
            self.conf = conf
        # Internal client
        #
        # Implements the internal logic that makes the client able to
        # process the Modalic Federated Learning protocol.
        self._mosaic_client = mosaic_python_sdk.Client(
            self.conf.server_address, 1.0, state
        )

        # Client API
        #
        # https://github.com/python/cpython/blob/3.9/Lib/multiprocessing/process.py#L80
        # stores the Client class with its args and kwargs.
        #
        # Based on composition over inheritance.
        self._client = client

        # Setting all the internal necessary attributes.
        #
        self._server_address = self.conf.server_address
        self._training_rounds = self.conf.training_rounds
        self._round_id = 0
        # Instantiate global & local model to None.
        self._global_model = None
        self._local_model = None
        #
        self._model_shape = self._get_model_shape()
        self._dtype = self._get_model_dtype()

        # State instigating that an error occured while fetching a global model
        # from the aggregation server.
        self._error_on_fetch_global_model = False
        # threading internals
        self._exit_event = threading.Event()

        # Primitive lock objects. Once a thread has acquired a lock,
        # subsequent attempts to acquire it block, until it is released;
        # any thread may release it.
        self._step_lock = threading.Lock()
        super().__init__(daemon=True)

    @property
    def server_address(self) -> int:
        r"""Returns the server address the client uses to connect."""
        return self._server_address

    @property
    def backoff_interval(self) -> float:
        r"""Returns the internal backoff interval."""
        return self.conf.backoff_interval

    @property
    def dtype(self) -> str:
        r"""Returns the underlying data type that is set via Conf."""
        return self._dtype

    @property
    def round_id(self) -> int:
        r"""Holds state of the training round the local model is in."""
        return self._round_id

    @property
    def model_shape(self) -> List[np.ndarray]:
        r"""Returns the shape of model architecture the client holds."""
        return self._model_shape

    def _get_model_shape(self) -> List[List[int]]:
        r"""Extracts the shape of the custom implemented model.

        :returns: List of List of ints representing the model shape.
            Each indivdual list is the shape of a tensor storing the values of
            in each model layer.
            (Example: [[1, 4], [1]])
        """
        return self._client.get_model_shape()

    def _get_model_dtype(self) -> str:
        r"""Extracts the data type of the custom implemented model."""
        return self._client.get_model_dtype()

    def _serialize_local_model(self, local_model: Any) -> List[Any]:
        r"""
        Serializes the local model into a `list` data type. The data type of the
        elements must match the data type attached as metadata.
        :returns: The local model (self.model) as a `list`.
        """
        return self._client.serialize_local_model(local_model)

    def _deserialize_global_model(self, global_model: List[Any]) -> Any:
        r"""
        Deserializes the `global_model` from a `list` to a specific model type.
        The data type of the elements matches the data type defined.
        If no global model exists (usually in the first round), the method is
        not called.

        :param global_model: The global model.
        :returns:
        """
        return self._client.deserialize_global_model(global_model)

    def _with_latest_global_model(self, model):
        r"""Handles the cases when the latest global model was fetched.
        This function can be used for e.g. storing the model locally.
        """
        model = model

    def _fetch_global_model(self) -> None:
        r"""Fetches the latest global model exposed by the server.

        :raises GlobalModelUnavailable:
        :raises GlobalModelDataTypeError:
        """
        try:
            global_model = self._mosaic_client.global_model()
        except (
            mosaic_python_sdk.GlobalModelUnavailable,
            mosaic_python_sdk.GlobalModelDataTypeError,
        ) as err:
            self._error_on_fetch_global_model = True
            logger.log(WARNING, f"Failed to fetch global model. {err}.")
        else:
            if global_model is not None:
                self._global_model = self._deserialize_global_model(global_model)
            else:
                self._global_model = None
            self._error_on_fetch_global_model = False

    def _set_local_model(self, local_model: List[Any]) -> None:
        r"""Sets a local model. This method can be called at any time. Internally the
        participant first caches the local model.

        If a local model is already in the cache and `set_local_model` is called
        with a new local model,
        the current cached local model will be replaced by the new one.

        :param local_model: The local model in the form of a list. The data type of the
            elements must match the data type defined in the coordinator configuration.
        :raises LocalModelDataTypeError: If the data type of the local model
            does not match the data type used for the actual model.
        """
        try:
            self._mosaic_client.set_model(local_model)
        except (mosaic_python_sdk.UninitializedClient):
            self._exit_event.set()

    def run(self) -> None:
        r"""."""
        try:
            self._run()
        except Exception as err:
            logger.log(ERROR, f"Exception during client runtime : {err}.")
            self._exit_event.set()

    def _run(self) -> None:
        r"""Internal `run` function which performs looping internal `step` function
        until an exit event is triggered.
        """
        while not self._exit_event.is_set():
            self._step()

    def _step(self) -> None:
        r"""Performs a single `step`. The client calls its internal state engine
        which then requests a new task by the server.

        The engine sets internal states which determine which task will be performed.
        """

        @backoff.on_predicate(
            backoff.constant, jitter=None, interval=self.conf.backoff_interval
        )
        def _step_unwrapped(self) -> None:
            r"""."""
            with self._step_lock:
                # Internal request for determining the latest task.
                #
                # Handled by the modalic python binding object `mosaic_client`.
                self._mosaic_client.step()

                # Get latest global model.
                if (
                    self._mosaic_client.new_global_model()
                    or self._error_on_fetch_global_model
                ):
                    self._fetch_global_model()

                    if not self._error_on_fetch_global_model:
                        self._with_latest_global_model(self._global_model)

                # Training branch as the latest task.
                if (
                    self._mosaic_client.should_set_model()
                    and not self._error_on_fetch_global_model
                ):
                    self._train()

        _step_unwrapped(self)

    def _train(self) -> None:
        r"""Runs a single training step."""
        logger.log(INFO, "Client starts training.")
        # Calling the `train` function of the custom client.
        #
        local_update = self._client.train(self._global_model)
        # Convert the model into serialized data format.
        local_update_ser = self._serialize_local_model(local_update)
        try:
            self._set_local_model(local_update_ser)
        except (mosaic_python_sdk.LocalModelDataTypeError,) as err:
            logger.log(WARNING, f"failed to set local model. {err}.")

    def stop(self) -> None:
        r"""Stopping the client. State will be saved if enabled."""
        self._exit_event.set()

        with self._step_lock:
            if self.conf.save_state:
                state = self._mosaic_client.save()
                logger.log(DEBUG, f"Client state {state} saved.")
            logger.log(WARNING, "Client stopped.")
