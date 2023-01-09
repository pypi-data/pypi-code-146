"""@Author Rayane AMROUCHE

Utils for ModelManager.
"""

import os
import datetime
import itertools

from concurrent.futures import FIRST_COMPLETED
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from typing import Any, Set

import optuna

from sklearn.model_selection import cross_val_score  # type: ignore

from dsmanager.controller.logger import make_logger
from dsmanager.controller.utils import fill_kwargs


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
    def generic_scorer(
        model: Any, X: Any, y: Any = None, **kwargs  # pylint: disable=invalid-name
    ) -> float:
        """Generate a generic scorer and return score.

        Args:
            model (Any): Model class or instance used for the cross val scorer.
            X (Any): The data matrix.
            y (Any, optional): The labels for X. Defaults to None.

        Returns:
            Any: Score of cross_val_score of X wrt. y.
        """
        cv_kwargs = fill_kwargs(cross_val_score, **kwargs)
        if callable(model):
            model = model(**kwargs)
        model.set_params(**kwargs)
        cv_kwargs["estimator"] = model
        return cross_val_score(X=X, y=y, **cv_kwargs).mean()

    @staticmethod
    def _one_study(  # pylint: disable=too-many-arguments
        study: Any,
        scorer: Any,
        n_trials: Any,
        timeout: Any,
        distributions_params: dict,
        fixed_params: dict,
    ):
        i_trial = 0
        time_start = datetime.datetime.now()
        while True:
            if n_trials is not None:
                if i_trial >= n_trials:
                    break
                i_trial += 1

            if timeout is not None:
                elapsed_seconds = (datetime.datetime.now() - time_start).total_seconds()
                if elapsed_seconds >= timeout:
                    break

            trial = study.ask(distributions_params)
            fixed_params.update(trial.params)
            score = scorer(**fixed_params)
            if "model" in fixed_params:
                trial.set_user_attr(key="model", value=fixed_params["model"])
            study.tell(trial, score)

        return study

    @staticmethod
    def _many_study(  # pylint: disable=too-many-arguments
        study: Any,
        scorer: Any,
        n_jobs: int,
        n_trials: Any,
        timeout: Any,
        distributions_params: dict,
        fixed_params: dict,
    ):
        time_start = datetime.datetime.now()

        def to_exec(study_, scorer_, distributions_params_, fixed_params_):
            trial = study_.ask(distributions_params_)
            fixed_params_.update(trial.params)
            score = scorer_(**fixed_params_)
            if "model" in fixed_params_:
                trial.set_user_attr(key="model", value=fixed_params_["model"])
            study_.tell(trial, score)

        futures: Set[Future] = set()
        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            for i_trial in itertools.count():
                if n_trials is not None and i_trial >= n_trials:
                    break

                if timeout is not None:
                    elapsed = (datetime.datetime.now() - time_start).total_seconds()
                    if elapsed >= timeout:
                        break

                if len(futures) >= n_jobs:
                    completed, futures = wait(futures, return_when=FIRST_COMPLETED)
                    for _f in completed:
                        _f.result()

                futures.add(
                    executor.submit(
                        to_exec, study, scorer, distributions_params, fixed_params
                    )
                )

    @staticmethod
    def launch_study(  # pylint: disable=too-many-arguments
        study: Any,
        scorer: Any,
        distributions_params: dict,
        n_jobs: int = 1,
        n_trials: Any = None,
        timeout: Any = None,
        **fixed_params: Any,
    ) -> Any:
        """Generate a study and launch a certain number of optimization trials.

        Args:
            study (Any): Optuna study.
            scorer (Any): Function that returns a score and take both distributions
                parameters and fixed parameters.
            distributions_params (dict): Dict of params as optuna distributions.
            n_trials (int): Number of trials to run. Defaults to 5.

        Returns:
            Any: Study trained.
        """
        if study is None:
            study = optuna.create_study()

        # if not study._optimize_lock.acquire(False):  # pylint: disable=protected-access
        #     raise RuntimeError("Nested invocation of launch_study isn't allowed.")

        try:
            if n_jobs == 1:
                Utils._one_study(
                    study, scorer, n_trials, timeout, distributions_params, fixed_params
                )
            else:
                if n_jobs == -1:
                    n_jobs = os.cpu_count() or 1
                Utils._many_study(
                    study,
                    scorer,
                    n_jobs,
                    n_trials,
                    timeout,
                    distributions_params,
                    fixed_params,
                )
        finally:  # pylint: disable=broad-except
            # study._optimize_lock.release()  # pylint: disable=protected-access
            ...

        return study

    @staticmethod
    def to_distribution(*args: Any) -> Any:
        """Transform argument to distribution.

        Returns:
            Any: Arguments as an optuna distribution.
        """
        res: optuna.distributions.BaseDistribution | None = None
        if len(args) == 1:
            _l = args[0]
            if isinstance(_l, optuna.distributions.BaseDistribution):
                return _l
            if isinstance(_l, range):
                res = optuna.distributions.IntDistribution(
                    _l.start, _l.stop, step=_l.step
                )
            elif isinstance(_l, (list, tuple)):
                if all(isinstance(x, int) for x in _l):
                    res = optuna.distributions.IntDistribution(min(_l), max(_l))
                elif all(isinstance(x, (float, int)) for x in _l):
                    res = optuna.distributions.FloatDistribution(min(_l), max(_l))
                else:
                    res = optuna.distributions.CategoricalDistribution(_l)
        elif len(args) == 2 and all(isinstance(x, (int, float)) for x in args):
            if any(isinstance(x, float) for x in args):
                res = optuna.distributions.FloatDistribution(*args)
            elif all(isinstance(x, int) for x in args):
                res = optuna.distributions.IntDistribution(*args)
        if res is None:
            res = optuna.distributions.CategoricalDistribution(args)
        if res.single():
            return args[0]
        return res
