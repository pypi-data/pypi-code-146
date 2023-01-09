"""Algorithm to evaluate a model on remote data."""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, cast

import numpy as np

from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmFactory,
    _BaseModellerModelAlgorithm,
    _BaseWorkerModelAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.hub.api import BitfountHub
from bitfount.utils import delegates

logger = _get_federated_logger(__name__)


class _ModellerSide(_BaseModellerModelAlgorithm):
    """Modeller side of the ModelInference algorithm."""

    def run(
        self, predictions: Mapping[str, List[np.ndarray]]
    ) -> Dict[str, List[np.ndarray]]:
        """Simply returns predictions."""
        return dict(predictions)


class _WorkerSide(_BaseWorkerModelAlgorithm):
    """Worker side of the ModelInference algorithm."""

    def run(self, data: BaseSource) -> List[np.ndarray]:
        """Runs evaluation and returns metrics."""
        return cast(List[np.ndarray], self.model.predict(data))


@delegates()
class ModelInference(_BaseModelAlgorithmFactory):
    """Algorithm for running inference on a model and returning the predictions.

    :::danger

    This algorithm could potentially return the data unfiltered so should only be used
    when the other party is trusted.

    :::

    Args:
        model: The model to infer on remote data.

    Attributes:
        model: The model to infer on remote data.
    """

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the ModelInference algorithm."""
        model = self._get_model_from_reference()
        return _ModellerSide(model=model, **kwargs)

    def worker(self, hub: BitfountHub, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the ModelInference algorithm.

        Args:
            hub: `BitfountHub` object to use for communication with the hub.
        """
        model = self._get_model_from_reference(hub=hub)
        return _WorkerSide(model=model, **kwargs)
