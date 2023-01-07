"""@Author Rayane AMROUCHE

Utils for ModelManager.
"""

import os

from typing import Any

from sklearn.model_selection import cross_val_score  # type: ignore

from dsmanager.controller.logger import make_logger


class Utils:
    """Utils class brings utils tools for the model manager."""

    def __init__(
        self, __mm: Any, logger_path: str = "/tmp/logs", verbose: int = 0
    ) -> None:
        """Init class Utils with an empty local storage.

        Args:
            __mm (Any): ModelManager from which these utils are called.
            logger_path (str, optional): Path of the logger for the ModelManager.
                Defaults to "/tmp/logs".
            verbose (int, optional): Verbose level for the logger . Defaults to 0.
        """
        # self.__mm = __mm
        self.logger = make_logger(
            os.path.join(logger_path, "model"), "utils", verbose=verbose
        )

    @staticmethod
    def generate_params(trial: Any, params: dict | None) -> dict:
        """Generate trial features for an optuna study.

        Args:
            trial (Any): Optuna trial object.
            params (dict): Parameters dict. Each key that contains a suggest_type field
                may be added to args variables dict.

        Returns:
            dict: Optuna variables in a dict.
        """
        args = {}  # type: dict
        if params is None:
            return args
        for key_, param in params.items():
            if "suggest_type" in param:
                suggester = getattr(trial, f"suggest_{param['suggest_type']}")
                if "args" not in param:
                    param["args"] = []
                if "kwargs" not in param:
                    param["kwargs"] = {}
                args[key_] = suggester(key_, *param["args"], **param["kwargs"])
        return args

    @staticmethod
    def generate_objective(params: dict | None = None) -> Any:
        """Generate an optuna objective function.

        Args:
            params (dict | None, optional): Optuna dict of parameters. Defaults to None.

        Returns:
            Any: Internal objective function.
        """

        def objective(  # pylint: disable=too-many-arguments
            trial: Any,
            estimator: Any,
            X: Any,  # pylint: disable=invalid-name
            y: Any,  # pylint: disable=invalid-name
            spliting: Any = None,
            scoring: Any = None,
        ):
            args = Utils.generate_params(trial, params)
            model = estimator(**args)
            score = cross_val_score(
                estimator=model, X=X, y=y, cv=spliting, scoring=scoring
            ).mean()
            trial.set_user_attr(key="best_model", value=model)
            trial.set_user_attr(key="best_params", value=args)
            return score

        return objective
