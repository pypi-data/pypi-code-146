"""@Author Rayane AMROUCHE

ModelManager Class.
"""

import os

from typing import Any, List

import optuna

from sklearn.linear_model import LinearRegression  # type: ignore

from dsmanager.datamanager.datastorage import DataStorage
from dsmanager.model.model import Model
from dsmanager.model.utils import Utils
from dsmanager.controller.logger import make_logger
from dsmanager.controller.utils import to_distribution


class ModelManager:
    """ModelManager class handle all the Model work."""

    def __init__(self, logger_path: str = "/tmp/logs", verbose: int = 0) -> None:
        """Init Modelmanager.

        Args:
            logger_path (str, optional): Path of the logger for the ModelManager.
                Defaults to "/tmp/logs".
            verbose (int, optional): Verbose level for the logger (1 = Log in stdin).
                Defaults to 0.
        """
        self.models = DataStorage()
        self.logger = make_logger(
            os.path.join(logger_path, "model"),
            "modelmanager",
            verbose=verbose,
            logger=optuna.logging._get_library_root_logger(),
        )
        self.utils = Utils(self, logger_path, verbose)
        self.models = DataStorage()

    def add_model(
        self,
        name: str,
        estimator: Any,
        params: dict,
        **kwargs: Any,
    ) -> None:
        """Generate and add a model to the model manager models dict.

        Args:
            name (str): Name of the model to add.
            estimator (Any): Model class.
            params (dict): Dict of params for grid search.
        """
        self.models[name] = Model(name, estimator, params, **kwargs)

    def update_model(
        self,
        name: str,
        **kwargs: Any,
    ) -> None:
        """Generate and add a model to the model manager models dict.

        Args:
            name (str): Name of the model to add.
            estimator (Any): Model class.
        """
        self.models[name].set_params(**kwargs)

    def get_model(self, name: str, **kwargs: Any) -> Any:
        """Get a model from the model manager models dict.

        Args:
            name (str): Name of the model.

        Returns:
            Any: Model instance.
        """
        model = self.models[name]
        model.estimator.set_params(**kwargs)
        return model

    def get_optuna_params(self, names: List[str]) -> dict:
        """Get params for optuna grid search.

        Args:
            names (List[str]): Names of the models to use.

        Returns:
            dict: Params for the optuna grid search.
        """

        all_params = {}
        models = []
        for name in names:
            temp_params = self.models[name].get_optuna_params()
            for param in temp_params:
                all_params[f"{name}__{param}"] = temp_params[param]
            models.append(self.models[name])
        all_params["estimator"] = to_distribution([model.estimator for model in models])
        all_params["name"] = to_distribution(names)
        return all_params

    def get_optuna_cv(self, names: List[str], **kwargs: Any) -> Any:
        """Get Optuna CV model.

        Args:
            names (List[str]): List of name of the models to tune.

        Returns:
            Any: OptunaSearchCV instance.
        """
        params = self.get_optuna_params(names)
        models = Model("empty", LinearRegression, {})
        optuna_cv = optuna.integration.OptunaSearchCV(models, params, **kwargs)
        return optuna_cv
