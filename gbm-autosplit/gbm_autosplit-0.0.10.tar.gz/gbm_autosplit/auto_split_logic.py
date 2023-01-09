import logging
import copy

import numpy
from numpy import random

from gbm_autosplit import utils


logger = logging.getLogger(__name__)


def tune_n_estimator(learner, x, y, **kwargs):
    learner_clone = copy.deepcopy(learner)
    xtr, ytr, xva, yva = split_xy(x, y, learner.ratio_training, learner.random_state)
    learner_clone.call_parent_fit(
        xtr, ytr, eval_set=[(xva, yva)], **kwargs
    )
    n_estimators = utils.get_n_estimators(learner_clone)
    if kwargs.get("init_model") is not None:
        # only for lightgbm
        n_estimators -= kwargs["init_model"].booster_.num_trees()
    learner.set_params(n_estimators=n_estimators)
    learner.set_params(early_stopping_rounds=None)
    logger.debug(f"set n_estimators={learner.n_estimators}")
    if learner.n_estimators == learner.max_n_estimators:
        logger.warning(f"n_estimators reached max_n_estimators: {learner.n_estimators}")


def split_xy(x, y, training_ratio, seed):
    sample_size = len(y)
    size_training = int(training_ratio * sample_size)
    indices_list = numpy.arange(x.shape[0])
    gen = random.default_rng(seed)
    gen.shuffle(indices_list)
    indices_training = indices_list[:size_training]
    indices_validation = indices_list[size_training:]
    return x[indices_training, :], y[indices_training], x[indices_validation, :], y[indices_validation]
