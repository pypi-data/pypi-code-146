from collections.abc import Callable
import math
import warnings

import lightgbm

from . import auto_split_logic


def suppress_params_warnings(func: Callable) -> Callable:
    def decorated_func(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", message="Found `early_stopping_rounds` in params. Will use it instead of argument")
            return func(*args, **kwargs)
    return decorated_func


class LGBMClassifier(lightgbm.LGBMClassifier):
    """
    Estimator which learns n_estimator by using only training data set
    """
    def __init__(self, max_n_estimators=5000, ratio_training=0.8, eval_metric="auc",
                 ratio_min_child_samples=None, early_stopping_rounds=100,
                 boosting_type=None, num_leaves=None, max_depth=None, learning_rate=None,
                 subsample_for_bin=None, objective=None, class_weight=None, min_split_gain=None,
                 min_child_weight=None, min_child_samples=None, subsample=None, subsample_freq=None,
                 colsample_bytree=None, reg_alpha=None, reg_lambda=None, random_state=None,
                 n_jobs=1, importance_type="gain", **kwargs):
        super(LGBMClassifier, self).__init__(
            boosting_type=boosting_type, num_leaves=num_leaves, max_depth=max_depth, learning_rate=learning_rate,
            n_estimators=max_n_estimators, subsample_for_bin=subsample_for_bin, 
            objective=objective, class_weight=class_weight,
            min_split_gain=min_split_gain, min_child_weight=min_child_weight, min_child_samples=min_child_samples,
            subsample=subsample, subsample_freq=subsample_freq, colsample_bytree=colsample_bytree,
            reg_alpha=reg_alpha, reg_lambda=reg_lambda, random_state=random_state, n_jobs=n_jobs, 
            importance_type=importance_type, early_stopping_rounds=early_stopping_rounds, **kwargs
        )
        self.max_n_estimators = max_n_estimators
        self.ratio_training = ratio_training
        self.ratio_min_child_samples = ratio_min_child_samples
        self.eval_metric = eval_metric

    @suppress_params_warnings
    def call_parent_fit(self, x, y, **kwargs):
        return super(LGBMClassifier, self).fit(x, y, **kwargs)

    def fit(self, x, y, **kwargs):
        if self.early_stopping_rounds > 0:
            self._set_min_child_samples(self.ratio_training * x.shape[0])
            auto_split_logic.tune_n_estimator(self, x, y, eval_metric=self.eval_metric, **kwargs)
        self._set_min_child_samples(x.shape[0])
        self.call_parent_fit(x, y, **kwargs)

    def _set_min_child_samples(self, sample_size: int):
        if self.ratio_min_child_samples is not None:
            self.set_params(min_child_samples=int(math.ceil(sample_size * self.ratio_min_child_samples)))


class LGBMRegressor(lightgbm.LGBMRegressor):
    def __init__(self, max_n_estimators=5000, ratio_training=0.8, eval_metric="rmse", ratio_min_child_samples=None,
                 early_stopping_rounds=100,
                 boosting_type=None, num_leaves=None, max_depth=None, learning_rate=None,
                 subsample_for_bin=None, objective=None, min_split_gain=None,
                 min_child_weight=None, min_child_samples=None, subsample=None, subsample_freq=None,
                 colsample_bytree=None, reg_alpha=None, reg_lambda=None, random_state=None,
                 n_jobs=1, importance_type="gain", **kwargs):
        super(LGBMRegressor, self).__init__(
            boosting_type=boosting_type, num_leaves=num_leaves, max_depth=max_depth, learning_rate=learning_rate,
            n_estimators=max_n_estimators, subsample_for_bin=subsample_for_bin, objective=objective,
            min_split_gain=min_split_gain, min_child_weight=min_child_weight, min_child_samples=min_child_samples,
            subsample=subsample, subsample_freq=subsample_freq, colsample_bytree=colsample_bytree,
            reg_alpha=reg_alpha, reg_lambda=reg_lambda, random_state=random_state, n_jobs=n_jobs,
            importance_type=importance_type, early_stopping_rounds=early_stopping_rounds, **kwargs
        )
        self.max_n_estimators = max_n_estimators
        self.ratio_training = ratio_training
        self.ratio_min_child_samples = ratio_min_child_samples
        self.eval_metric = eval_metric

    @suppress_params_warnings
    def call_parent_fit(self, x, y, **kwargs):
        return super(LGBMRegressor, self).fit(x, y, **kwargs)

    def fit(self, x, y, **kwargs):
        if self.early_stopping_rounds > 0:
            self._set_min_child_samples(self.ratio_training * x.shape[0])
            auto_split_logic.tune_n_estimator(self, x, y, eval_metric=self.eval_metric, **kwargs)
        self._set_min_child_samples(x.shape[0])
        self.call_parent_fit(x, y, **kwargs)

    def _set_min_child_samples(self, sample_size: int):
        if self.ratio_min_child_samples is not None:
            self.set_params(min_child_samples=int(math.ceil(sample_size * self.ratio_min_child_samples)))
