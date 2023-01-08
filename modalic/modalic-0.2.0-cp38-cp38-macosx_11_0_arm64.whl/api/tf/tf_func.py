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

"""Tensorflow decorator for training."""
import functools
from logging import INFO

from modalic.api.common.communication import get_global_model, update
from modalic.api.tf.tf_utils import (
    _get_tf_model_dtype,
    _get_tf_model_shape,
    _get_tf_weights,
    _set_tf_weights,
)
from modalic.config import Conf
from modalic.data.misc import get_dataset_length
from modalic.logging.logging import logger
from modalic.utils.serde import parameters_to_weights


def tf_train(conf: Conf = Conf()):
    r"""Training function decorator for Tensorflow. Performs the underlying train() function
    multiply times while participating in a Federated Learning procedure.

    :param conf: :class:`modalic.Conf` that stores all the parameters concerning the process.

    :important: For the design of the custom training function, please make sure that
        a model object is defined as an input and will be returned in order to
        enable the communication with the server to happen.

    Examples:
        >>> # Decorate a custom function where the training logic is defined.
        >>> @modalic.tf_train(conf=conf)
        >>> def train_step(model, x_train, y_train):
        >>>     model.fit(x_train, y_train, batch_size=32, epochs=1)
        >>>     return model
        >>>
        >>> ...
        >>> train_step(model, X_train, y_train)
    """

    def inner_train(func, *args, **kwargs):
        logger.log(
            INFO, f"Training runs with the following hyperparameters: \n\t{conf}"
        )

        @functools.wraps(func)
        def wrapper(model, dataset=None, *args, **kwargs):
            wrapper.model_shape = _get_tf_model_shape(model)
            wrapper.dtype = _get_tf_model_dtype(model)

            if dataset is not None:
                wrapper.data_stack = get_dataset_length(dataset, conf.client_id)
            else:
                wrapper.data_stack = 1

            while wrapper.round_id < conf.training_rounds:
                params = get_global_model(conf.client_id, conf.server_address)

                if params is not None and len(params.tensor) != 0:
                    weights = parameters_to_weights(
                        params, wrapper.model_shape, wrapper.dtype
                    )
                    model = _set_tf_weights(model, weights)
                    logger.log(
                        INFO,
                        f"Client {conf.client_id} received global model from aggregation server.",
                    )
                wrapper.round_id += 1

                model = func(model, dataset, *args, **kwargs)

                logger.log(
                    INFO,
                    f"Client {conf.client_id} | training round: {wrapper.round_id}",
                )
                update(
                    conf.client_id,
                    conf.server_address,
                    _get_tf_weights(model),
                    wrapper.dtype,
                    wrapper.round_id,
                    wrapper.data_stack,
                    wrapper.loss,
                )

        wrapper.round_id = 0
        wrapper.loss = 0.0

        return wrapper

    return inner_train
