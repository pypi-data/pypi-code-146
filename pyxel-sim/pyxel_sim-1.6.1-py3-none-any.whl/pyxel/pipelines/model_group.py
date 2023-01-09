#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""TBW."""
import logging
from copy import deepcopy
from typing import TYPE_CHECKING, Iterator, List, Mapping, Optional, Sequence

from pyxel import util
from pyxel.pipelines import ModelFunction

if TYPE_CHECKING:
    from pyxel.detectors import Detector
    from pyxel.pipelines import DetectionPipeline


# TODO: These methods could also be as a `abc.Sequence` with magical methods:
#       __getitem__, __iter__, __len__, __contains__, ...
#       See #181
class ModelGroup:
    """TBW."""

    def __init__(self, models: Sequence[ModelFunction], name: str):
        self._log = logging.getLogger(__name__)
        self._name = name
        self.models: Sequence[ModelFunction] = models

    def __repr__(self):
        cls_name: str = self.__class__.__name__

        all_models: List[str] = [model.name for model in self.models if model.name]

        return f"{cls_name}<name={self._name!r}, models={all_models!r}>"

    def __deepcopy__(self, memo: dict) -> "ModelGroup":
        copied_models = deepcopy(self.models)
        return ModelGroup(models=copied_models, name=self._name)

    def __iter__(self) -> Iterator[ModelFunction]:
        for model in self.models:
            if model.enabled:
                yield model

    def __getstate__(self) -> Mapping:
        return {"models": tuple(self.models), "name": self._name}

    def __setstate__(self, state: Mapping) -> None:
        self.models = list(state["models"])
        self._name = state["name"]

    def __getattr__(self, item: str) -> ModelFunction:
        for model in self.models:
            if model.name == item:
                return model
        else:
            raise AttributeError(f"Cannot find model {item!r}.")

    def __dir__(self):
        return dir(type(self)) + [model.name for model in self.models]

    # TODO: Why is this method returning a `bool` ?
    def run(
        self,
        detector: "Detector",
        pipeline: "DetectionPipeline",
        abort_model: Optional[str] = None,
    ) -> bool:
        """Execute each enabled model in this group.

        Parameters
        ----------
        detector : Detector
        pipeline : DetectionPipeline
        abort_model : str, optional

        Returns
        -------
        bool
            TBW.
        """
        model: ModelFunction
        for model in self.models:
            if model.name == abort_model:
                return True
            if not pipeline.is_running:
                raise util.PipelineAborted("Pipeline has been aborted.")
            else:
                if model.enabled:
                    self._log.info("Model: %r", model.name)
                    model(detector)

        return False
