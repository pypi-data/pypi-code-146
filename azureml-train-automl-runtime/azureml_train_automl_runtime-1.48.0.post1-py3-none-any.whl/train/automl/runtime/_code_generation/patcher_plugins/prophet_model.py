# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator

from azureml.training.tabular.models._timeseries._prophet_model import ProphetModel

from .abstract_code_generator import AbstractCodeGenerator


class ProphetModelCodeGenerator(AbstractCodeGenerator):
    @contextmanager
    def patch(self) -> Any:
        return self._patch_class(ProphetModel)

    @classmethod
    def get_params(cls, obj: Any) -> Dict[str, Any]:
        params = {
            "timeseries_param_dict": obj.timeseries_param_dict,
            "prophet_param_dict": obj.prophet_param_dict
        }
        return params

    @classmethod
    def can_handle(cls, obj: Any) -> bool:
        return "ProphetModel" in [mro.__name__ for mro in obj.__class__.__mro__]
