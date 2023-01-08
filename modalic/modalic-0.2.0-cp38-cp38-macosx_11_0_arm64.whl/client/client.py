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
"""Client API."""
from abc import ABC, abstractmethod
from typing import Any, List


class Client(ABC):
    r"""An abstract API Object for implementing the actual Machine & Deep Learning logic
    and attach it to an internal modalic client which implements the logic
    of Federated Learning.
    """

    @abstractmethod
    def get_model_shape(self) -> List[List[int]]:
        r"""Extracts the shape of the custom implemented model.

        :returns: List of List of ints representing the model shape.
            Each indivdual list is the shape of a tensor storing the values of
            in each model layer.
            (Example: [[1, 4], [1]])
        """
        raise NotImplementedError()

    @abstractmethod
    def get_model_dtype(self) -> str:
        r"""Extracts the data type of the custom implemented model."""
        raise NotImplementedError()

    @abstractmethod
    def serialize_local_model(self, local_model: Any) -> List[Any]:
        r"""
        Serializes the local model into a `list` of values with the constant data type.
        The data type of the elements must match the data type attached as metadata.
        :returns: The local model (self.model) as a `list`.
        """
        raise NotImplementedError()

    @abstractmethod
    def deserialize_global_model(self, global_model: List[Any]) -> Any:
        r"""
        Deserializes the `global_model` from a `list` to a specific model type.
        The data type of the elements matches the data type defined.
        If no global model exists (usually in the first round), the method is
        not called.

        :param global_model: The global model.
        :returns:
        """
        raise NotImplementedError()

    @abstractmethod
    def train(self, global_model: Any) -> Any:
        r"""."""
        raise NotImplementedError()
